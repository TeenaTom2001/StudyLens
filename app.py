"""StudyFocus: local formative-evaluation prototype. No automatic surveillance."""
import csv
import io
import os
import secrets
import sqlite3
from datetime import date
from pathlib import Path
from functools import wraps
from flask import Flask, abort, flash, redirect, render_template, request, session, url_for, Response
from werkzeug.security import generate_password_hash, check_password_hash

BASE = Path(__file__).resolve().parent

def create_app(database=None):
    app = Flask(__name__)
    app.config['DATABASE'] = str(database or BASE / 'studyfocus.sqlite3')
    keyfile = BASE / '.session_key'
    if not keyfile.exists():
        keyfile.write_text(secrets.token_hex(32))
        keyfile.chmod(0o600)
    app.secret_key = os.environ.get('STUDYFOCUS_SECRET') or keyfile.read_text().strip()
    app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax', MAX_CONTENT_LENGTH=16384)

    def db():
        con = sqlite3.connect(app.config['DATABASE'])
        con.row_factory = sqlite3.Row
        con.execute('PRAGMA foreign_keys=ON')
        return con

    with db() as con:
        con.executescript('''
        CREATE TABLE IF NOT EXISTS participants (
          participant_id TEXT PRIMARY KEY, key_hash TEXT NOT NULL,
          baseline_start TEXT NOT NULL, consent_version TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS sessions (
          session_id TEXT PRIMARY KEY, participant_id TEXT NOT NULL REFERENCES participants ON DELETE CASCADE,
          session_date TEXT NOT NULL, phase TEXT NOT NULL CHECK(phase IN ('baseline','intervention')),
          planned_minutes INTEGER, actual_minutes INTEGER NOT NULL CHECK(actual_minutes BETWEEN 1 AND 720),
          distraction_count INTEGER NOT NULL CHECK(distraction_count BETWEEN 0 AND 1000),
          focus_rating INTEGER NOT NULL CHECK(focus_rating BETWEEN 1 AND 5),
          completed INTEGER NOT NULL CHECK(completed IN (0,1)));
        CREATE TABLE IF NOT EXISTS reflections (
          reflection_id TEXT PRIMARY KEY, participant_id TEXT NOT NULL REFERENCES participants ON DELETE CASCADE,
          recorded_date TEXT NOT NULL, useful TEXT NOT NULL, difficult TEXT NOT NULL, suggested_change TEXT NOT NULL);
        ''')

    def protected(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            if not session.get('pid'):
                return redirect(url_for('index'))
            return fn(*args, **kwargs)
        return wrapped

    def token():
        if 'csrf' not in session:
            session['csrf'] = secrets.token_hex(32)
        return session['csrf']
    app.jinja_env.globals['csrf_token'] = token

    @app.before_request
    def check_csrf():
        if request.method == 'POST':
            expected = session.get('csrf', '')
            supplied = request.form.get('csrf', '')
            if not expected or not secrets.compare_digest(expected, supplied):
                abort(400, 'Invalid form token. Reload the page and try again.')

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            pid, key = request.form.get('pid','').strip(), request.form.get('key','')
            with db() as con:
                p = con.execute('SELECT * FROM participants WHERE participant_id=?', (pid,)).fetchone()
            if p and check_password_hash(p['key_hash'], key):
                session.clear()
                session['pid'] = pid
                return redirect(url_for('dashboard'))
            flash('Participant code or access key is incorrect.')
        return render_template('index.html')

    @app.post('/join')
    def join():
        if request.form.get('consent') != 'yes':
            abort(400, 'Consent is required.')
        pid = 'P' + secrets.token_hex(5).upper()
        key = secrets.token_urlsafe(18)
        with db() as con:
            con.execute('INSERT INTO participants VALUES (?,?,?,?)',
                        (pid, generate_password_hash(key), date.today().isoformat(), 'prototype-v1'))
        session.clear()
        session['pid'] = pid
        return render_template('credentials.html', pid=pid, key=key)

    @app.get('/dashboard')
    @protected
    def dashboard():
        with db() as con:
            p = con.execute('SELECT * FROM participants WHERE participant_id=?',(session['pid'],)).fetchone()
            rows = con.execute('SELECT * FROM sessions WHERE participant_id=? ORDER BY session_date,session_id',
                               (session['pid'],)).fetchall()
        if not p:
            session.clear()
            return redirect(url_for('index'))
        day = (date.today()-date.fromisoformat(p['baseline_start'])).days
        phase = 'baseline' if day < 7 else 'intervention'
        ended = day >= 28
        stats=[]
        for ph in ['baseline','intervention']:
            subset = [r for r in rows if r['phase']==ph]
            mins = sum(r['actual_minutes'] for r in subset)
            stats.append({'phase':ph,'n':len(subset),'minutes':mins,
                'rate':round(60*sum(r['distraction_count'] for r in subset)/mins,2) if mins else None,
                'focus':round(sum(r['focus_rating'] for r in subset)/len(subset),2) if subset else None})
        return render_template('dashboard.html', pid=session['pid'], phase=phase, day=day+1,
                               ended=ended, stats=stats, rows=rows, today=date.today().isoformat())

    @app.post('/session')
    @protected
    def log_session():
        try:
            d = date.fromisoformat(request.form['session_date'])
            with db() as con:
                p=con.execute('SELECT baseline_start FROM participants WHERE participant_id=?',(session['pid'],)).fetchone()
            day = (d-date.fromisoformat(p['baseline_start'])).days
            if not 0 <= day < 28 or d > date.today():
                raise ValueError('Date must be within your study period and not in the future.')
            phase='baseline' if day<7 else 'intervention'
            actual=int(request.form['actual_minutes']); distractions=int(request.form['distraction_count'])
            focus=int(request.form['focus_rating']); completed=int(request.form['completed'])
            plan=int(request.form['planned_minutes']) if phase=='intervention' else None
            if not (1<=actual<=720 and 0<=distractions<=1000 and 1<=focus<=5 and completed in (0,1)):
                raise ValueError('Check the permitted numeric ranges.')
            if plan is not None and not 1<=plan<=720:
                raise ValueError('Planned minutes must be between 1 and 720.')
            with db() as con:
                con.execute('INSERT INTO sessions VALUES (?,?,?,?,?,?,?,?,?)',
                  (secrets.token_hex(12),session['pid'],d.isoformat(),phase,plan,actual,distractions,focus,completed))
            flash('Session recorded.')
        except (ValueError, KeyError, TypeError) as error:
            flash('Session not saved. '+str(error))
        return redirect(url_for('dashboard'))

    @app.post('/reflection')
    @protected
    def reflection():
        with db() as con:
            p = con.execute('SELECT baseline_start FROM participants WHERE participant_id=?',(session['pid'],)).fetchone()
        if not p or (date.today()-date.fromisoformat(p['baseline_start'])).days < 7:
            abort(400,'Reflection is available after the baseline week.')
        values=[request.form.get(k,'').strip() for k in ['useful','difficult','suggested_change']]
        if any(len(x)>2000 for x in values) or not any(values):
            abort(400,'Enter at least one response; maximum 2,000 characters each.')
        with db() as con:
            con.execute('INSERT INTO reflections VALUES (?,?,?,?,?,?)',
              (secrets.token_hex(12),session['pid'],date.today().isoformat(),*values))
        flash('Reflection saved. Please do not include names or private information.')
        return redirect(url_for('dashboard'))

    @app.get('/export')
    @protected
    def export():
        with db() as con:
            rows=con.execute('SELECT * FROM sessions WHERE participant_id=? ORDER BY session_date',(session['pid'],)).fetchall()
        output=io.StringIO()
        fields=['session_id','participant_id','session_date','phase','planned_minutes','actual_minutes','distraction_count','focus_rating','completed']
        writer=csv.writer(output); writer.writerow(fields); writer.writerows([tuple(r) for r in rows])
        return Response(output.getvalue(),mimetype='text/csv',headers={'Content-Disposition':'attachment; filename=my_sessions.csv'})

    @app.post('/withdraw')
    @protected
    def withdraw():
        if request.form.get('confirm')!='DELETE':
            abort(400,'Type DELETE to confirm withdrawal.')
        with db() as con:
            con.execute('DELETE FROM participants WHERE participant_id=?',(session['pid'],))
        session.clear()
        return redirect(url_for('index'))

    @app.post('/logout')
    def logout():
        session.clear()
        return redirect(url_for('index'))

    @app.after_request
    def headers(response):
        response.headers['Cache-Control']='no-store'
        response.headers['X-Content-Type-Options']='nosniff'
        response.headers['Content-Security-Policy']="default-src 'self'; style-src 'self' 'unsafe-inline'; form-action 'self'; frame-ancestors 'none'"
        return response
    return app

if __name__=='__main__':
    create_app().run(host='127.0.0.1',port=5000,debug=False)
