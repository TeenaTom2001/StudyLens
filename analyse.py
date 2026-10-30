"""Descriptive within-participant summaries; no causal estimates or hypothesis tests."""
import argparse
import csv
import statistics
from pathlib import Path

def summarize(rows):
    output=[]
    for pid in sorted({r['participant_id'] for r in rows}):
        result={'participant_id':pid}
        for phase,days in [('baseline',7),('intervention',21)]:
            subset=[r for r in rows if r['participant_id']==pid and r['phase']==phase]
            minutes=sum(int(r['actual_minutes']) for r in subset)
            result[phase+'_sessions']=len(subset)
            result[phase+'_logged_days']=len({r['session_date'] for r in subset})
            result[phase+'_coverage']=round(result[phase+'_logged_days']/days,3)
            result[phase+'_minutes']=minutes
            result[phase+'_distractions_per_hour']=round(60*sum(int(r['distraction_count']) for r in subset)/minutes,3) if minutes else ''
            result[phase+'_focus_mean']=round(statistics.mean(int(r['focus_rating']) for r in subset),3) if subset else ''
        a=result['baseline_distractions_per_hour']; b=result['intervention_distractions_per_hour']
        result['rate_change_intervention_minus_baseline']=round(b-a,3) if a!='' and b!='' else ''
        output.append(result)
    return output

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('sessions',type=Path); parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    with args.sessions.open(newline='') as f: rows=list(csv.DictReader(f))
    summary=summarize(rows)
    if not summary:raise SystemExit('No sessions: nothing to summarize.')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(summary[0])); writer.writeheader();writer.writerows(summary)
    print('Descriptive output only. Missing days are not zero-use days. Synthetic input is not research evidence.')
    print(f'Summarized {len(summary)} participants. No causal inference performed.')

if __name__=='__main__':main()
