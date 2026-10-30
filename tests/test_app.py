import csv
import io
import re
import sqlite3
import tempfile
import unittest
from datetime import date,timedelta
from pathlib import Path
from app import create_app
from analyse import summarize

class AppTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.path=Path(self.tmp.name)/'test.sqlite3'
        self.app=create_app(self.path);self.app.config['TESTING']=True
        self.client=self.app.test_client()
    def tearDown(self):
        try:
            self.tmp.cleanup()
        except Exception:
            pass
    def csrf(self,client=None):
        client=client or self.client
        client.get('/')
        with client.session_transaction() as s:return s['csrf']
    def join(self,client=None):
        client=client or self.client
        r=client.post('/join',data={'csrf':self.csrf(client),'consent':'yes'})
        self.assertEqual(r.status_code,200)
        with client.session_transaction() as s:return s['pid']
    def post(self,url,data,client=None):
        client=client or self.client
        return client.post(url,data={**data,'csrf':self.csrf(client)})
    def move_to_intervention(self,pid):
        with sqlite3.connect(self.path) as con:
            con.execute('UPDATE participants SET baseline_start=? WHERE participant_id=?',
              ((date.today()-timedelta(days=7)).isoformat(),pid))
    def record(self,client=None,**overrides):
        data={'session_date':date.today().isoformat(),'actual_minutes':'30','distraction_count':'2',
              'focus_rating':'4','completed':'1','planned_minutes':'40'}
        data.update(overrides)
        return self.post('/session',data,client)
    def test_access_consent_csrf(self):
        self.assertEqual(self.client.get('/dashboard').status_code,302)
        self.assertEqual(self.client.post('/join',data={'consent':'yes'}).status_code,400)
        self.assertEqual(self.post('/join',{}).status_code,400)
    def test_baseline_and_intervention(self):
        pid=self.join()
        self.assertNotIn(b'Your recorded patterns',self.client.get('/dashboard').data)
        self.assertEqual(self.post('/reflection',{'useful':'test'}).status_code,400)
        self.record()
        with sqlite3.connect(self.path) as con:
            row=con.execute('SELECT phase,planned_minutes FROM sessions').fetchone()
            self.assertEqual(row,('baseline',None))
        self.move_to_intervention(pid)
        self.assertIn(b'Your recorded patterns',self.client.get('/dashboard').data)
        self.record()
        with sqlite3.connect(self.path) as con:
            self.assertEqual(con.execute("SELECT planned_minutes FROM sessions WHERE phase='intervention'").fetchone()[0],40)
    def test_invalid_log_rejected(self):
        self.join()
        for changes in [{'actual_minutes':'0'},{'distraction_count':'-1'},{'focus_rating':'8'},
                        {'session_date':(date.today()+timedelta(days=1)).isoformat()}]:
            self.record(**changes)
        with sqlite3.connect(self.path) as con:
            self.assertEqual(con.execute('SELECT COUNT(*) FROM sessions').fetchone()[0],0)
    def test_isolation_export_and_withdrawal(self):
        pid=self.join();self.record()
        other=self.app.test_client();other_pid=self.join(other)
        self.record(other,distraction_count='9')
        rows=list(csv.DictReader(io.StringIO(self.client.get('/export').data.decode())))
        self.assertEqual(len(rows),1);self.assertEqual(rows[0]['participant_id'],pid)
        self.assertNotIn('key_hash',rows[0])
        self.move_to_intervention(pid)
        self.post('/reflection',{'useful':'Clear layout','difficult':'','suggested_change':''})
        self.assertEqual(self.post('/withdraw',{'confirm':'wrong'}).status_code,400)
        self.assertEqual(self.post('/withdraw',{'confirm':'DELETE'}).status_code,302)
        with sqlite3.connect(self.path) as con:
            for table in ['participants','sessions','reflections']:
                self.assertEqual(con.execute(f'SELECT COUNT(*) FROM {table} WHERE participant_id=?',(pid,)).fetchone()[0],0)
            self.assertEqual(con.execute('SELECT COUNT(*) FROM participants WHERE participant_id=?',(other_pid,)).fetchone()[0],1)
    def test_login_key(self):
        response=self.client.post('/join',data={'csrf':self.csrf(),'consent':'yes'})
        details=re.findall(rb'<strong>(.*?)</strong>',response.data)
        pid,key=[x.decode() for x in details]
        self.post('/logout',{})
        self.post('/',{'pid':pid,'key':'incorrect'})
        self.assertEqual(self.client.get('/dashboard').status_code,302)
        self.post('/',{'pid':pid,'key':key})
        self.assertEqual(self.client.get('/dashboard').status_code,200)

class AnalysisTest(unittest.TestCase):
    def test_rate_uses_total_minutes_and_preserves_missing(self):
        rows=[dict(participant_id='P1',phase='baseline',actual_minutes='30',distraction_count='3',focus_rating='2',session_date='2026-01-01'),
              dict(participant_id='P1',phase='baseline',actual_minutes='90',distraction_count='3',focus_rating='4',session_date='2026-01-02'),
              dict(participant_id='P1',phase='intervention',actual_minutes='60',distraction_count='1',focus_rating='4',session_date='2026-01-09'),
              dict(participant_id='P2',phase='baseline',actual_minutes='30',distraction_count='0',focus_rating='3',session_date='2026-01-01')]
        p1,p2=summarize(rows)
        self.assertEqual(p1['baseline_distractions_per_hour'],3)
        self.assertEqual(p1['rate_change_intervention_minus_baseline'],-2)
        self.assertEqual(p2['intervention_distractions_per_hour'],'')
        self.assertEqual(p2['rate_change_intervention_minus_baseline'],'')

if __name__=='__main__':unittest.main()
