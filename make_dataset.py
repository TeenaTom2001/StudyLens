"""Reproducible SOFTWARE TEST DATA ONLY: no real participants or findings."""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

ROOT=Path(__file__).resolve().parent/'data'
SEED=20261030

def write(path, fields, rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=fields); writer.writeheader(); writer.writerows(rows)

def main():
    rng=random.Random(SEED)
    start=date(2026,1,5)
    participants=[]; sessions=[]
    pfields=['participant_id','baseline_start','consent_version','is_synthetic']
    sfields=['session_id','participant_id','session_date','phase','planned_minutes','actual_minutes','distraction_count','focus_rating','completed','is_synthetic']
    for i in range(1,26):
        pid=f'SYN{i:03}'
        participants.append(dict(zip(pfields,[pid,start.isoformat(),'DEMO-NOT-CONSENT',1])))
        # Mixed directions deliberately: improvement, stability and worsening.
        tendency=[-1,0,1][i%3]
        for day in range(28):
            if rng.random()<(.16 if day<7 else .23):
                continue # Missing logging days are not zero-distraction days.
            for j in range(rng.choice([1,1,2])):
                phase='baseline' if day<7 else 'intervention'
                minutes=rng.randint(20,95)
                shift=tendency if phase=='intervention' else 0
                distractions=max(0,rng.randint(0,7)+shift)
                focus=max(1,min(5,rng.randint(1,5)-shift))
                sessions.append(dict(zip(sfields,[f'SYN-{i:03}-{day:02}-{j}',pid,(start+timedelta(days=day)).isoformat(),phase,
                   rng.choice([25,40,60,90]) if phase=='intervention' else '',minutes,distractions,focus,rng.randint(0,1),1])))
    write(ROOT/'synthetic/participants_SYNTHETIC.csv',pfields,participants)
    write(ROOT/'synthetic/sessions_SYNTHETIC.csv',sfields,sessions)
    write(ROOT/'templates/participants_EMPTY.csv',pfields,[])
    write(ROOT/'templates/sessions_EMPTY.csv',sfields,[])
    write(ROOT/'templates/questionnaire_responses_EMPTY.csv',
      ['participant_id','timepoint','collection_date','instrument','instrument_version','item_id','response','is_synthetic'],[])
    write(ROOT/'templates/questionnaire_scores_EMPTY.csv',
      ['participant_id','timepoint','instrument','instrument_version','subscale','score','items_answered','items_expected','scoring_rule_version','is_synthetic'],[])
    write(ROOT/'templates/reflections_EMPTY.csv',
      ['reflection_id','participant_id','recorded_date','useful','difficult','suggested_change','is_synthetic'],[])
    print(f'Created 25 synthetic participant records and {len(sessions)} synthetic session records (seed {SEED}).')

if __name__=='__main__':main()
