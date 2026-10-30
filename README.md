# StudyFocus — start here

A small working Flask + SQLite artefact, a revised DSR project plan and a reproducible synthetic dataset, prepared from the teacher feedback supplied by Teena.

## Contents

- PROJECT_PLAN.md: proposed title, aim, objectives, questions, DSR structure, measures, evaluation, analysis, ethics and chapter structure.
- DATA_DICTIONARY.md: dataset fields, scoring boundaries and missing-value rules.
- app.py and templates/: working local web application.
- data/synthetic/: fictional records for 25 participants; **not research findings**.
- data/templates/: empty participant, session, questionnaire-response, score and reflection CSV templates.
- make_dataset.py: reproducible test-data generator, random seed 20261030.
- analyse.py: descriptive participant-level baseline/intervention summaries.
- export_research.py: researcher CSV export from a local database, excluding access hashes.
- tests/: functional checks and analysis verification.

## Run the app

Use Python 3.10 or newer in a terminal opened inside this folder:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

On Windows, activate with `.venv\Scripts\activate` instead. Open http://127.0.0.1:5000 in your browser. Create a demonstration account and save its participant code and access key. SQLite tables and a private session-signing key are created automatically on first run. Do not share the database, access keys or `.session_key`.

New accounts begin with seven baseline days; planning and summaries unlock on day 8. The app derives each log's phase from its date and the participant's baseline start. It does not need a database server. Synthetic CSVs remain separate and are not automatically imported into the app.

## View an intervention demonstration immediately

To test phase transitions without waiting, run the tests below. For a manual demonstration, use a **disposable demonstration account/database** and change that account's baseline_start to seven days before today using a SQLite browser; then log in again. Do not change dates in real research records. Study dates are based on the computer hosting the app.

## Generate and analyse the synthetic dataset

```bash
python make_dataset.py
python analyse.py data/synthetic/sessions_SYNTHETIC.csv --output data/synthetic/summary_SYNTHETIC.csv
```

Generation overwrites only the named synthetic files and EMPTY templates; do not put real records into those templates and rerun generation. Copy empty templates into a separate real-data directory first. Mixed directions and missing logging days are deliberate, not evidence of real participant outcomes. Survey and reflection templates contain no fabricated human responses.

## Export local application data

```bash
python export_research.py --out exports
python analyse.py exports/sessions.csv --output exports/summary.csv
```

Current app exports are marked `is_synthetic=1` because enrolment is explicitly for demonstration. Do not use this demo consent screen for an actual participant study. Real research requires the approved protocol/consent, provenance configuration, appropriate hosting and instrument selection described in PROJECT_PLAN.md. A local single-computer prototype is the delivered scope, not a deployed research service.

Questionnaires are a separate approved survey workflow. Link them by participant code using the empty response template; score using verified version-specific rules. The app does not administer TMBS, BSMAS, UWES or SUS, and no real survey results have been generated.

## Verify

```bash
python -m unittest discover -s tests -v
```

Checks cover protected pages, consent gate, CSRF, baseline/intervention logic, input validation, record isolation, CSV export, withdrawal deletion, and a hand-calculated distraction-rate example. There is no causal inference test.

## Teacher feedback → revision

| Teacher concern | Revision |
|---|---|
| A single-group pre/post design cannot validate the causal hypothesis | Remove causal hypothesis; use descriptive formative research questions |
| Use TMBS, keep BSMAS, consider engagement | TMBS and candidate UWES student version baseline/end; BSMAS baseline context; versions to confirm |
| Notebook is not a web app | Actual Flask backend, SQLite storage and personalised dashboard |
| Avoid causal claims | Report observed patterns, associations only when explored, and user perceptions |
| 20–30 participants/no control group | Justify formative scope; report missingness and triangulate SUS, feedback and logs |

The project plan includes sources and distinguishes implemented features from later research setup. Read it before adapting the prototype or collecting real data.
