"""Local researcher export. Never exports access hashes or login secrets."""
import argparse
import csv
import sqlite3
from pathlib import Path

def main():
    p=argparse.ArgumentParser();p.add_argument('--db',type=Path,default=Path(__file__).parent/'studyfocus.sqlite3');p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    if not a.db.is_file():raise SystemExit('Database not found. Run the app first.')
    a.out.mkdir(parents=True,exist_ok=True)
    tables={'participants':'participant_id, baseline_start, consent_version',
            'sessions':'session_id, participant_id, session_date, phase, planned_minutes, actual_minutes, distraction_count, focus_rating, completed',
            'reflections':'reflection_id, participant_id, recorded_date, useful, difficult, suggested_change'}
    with sqlite3.connect(a.db) as con:
        for table,columns in tables.items():
            cursor=con.execute(f'SELECT {columns} FROM {table}')
            with (a.out/f'{table}.csv').open('w',newline='') as f:
                writer=csv.writer(f);writer.writerow([c[0] for c in cursor.description]+['is_synthetic'])
                writer.writerows([list(r)+[1] for r in cursor])
    print('Exported local app records. Do not treat demonstration entries as participant research data.')

if __name__=='__main__':main()
