# StudyFocus: project structure and formative evaluation plan

Prepared for Teena from the supplied teacher feedback. This is a proposed structure, not an approved protocol or a report of completed research. No original proposal was supplied, so the project scope below assumes university students and social-media distraction during independent study.

## 1. Proposed title

**Design and Formative Evaluation of a Web-Based Study Planning and Distraction Reflection Tool for University Students**

## 2. Revised project summary

This project will design, implement and formatively evaluate StudyFocus, a Python web application intended to support students in planning study sessions and reflecting on self-reported social-media distraction. The artefact uses a Flask backend, SQLite database and browser dashboard. A Design Science Research (DSR) approach will connect identified student needs to design requirements, implementation, demonstration, evaluation and subsequent refinement. A convenience sample of approximately 20–30 adult university students will complete a seven-day baseline logging period followed by a three-week period with planning and dashboard feedback. Evaluation will combine usability ratings, questionnaire responses, session logs and qualitative feedback. Analysis will describe observed patterns and participant perceptions; the design will not establish that the application causes changes in time management, academic engagement or distraction.

## 3. Problem, aim and objectives

**Problem:** Students may find it difficult to plan independent study and recognise patterns of social-media distraction. The project explores whether a small, usable planning and reflection tool addresses these needs in a practical student setting. Support the final problem statement with literature and a short needs assessment; do not assume every student has problematic social-media use.

**Aim:** To design and formatively evaluate a usable web application that supports study planning and reflection on self-reported distraction and time-management behaviour.

**Objectives:**

1. Identify student needs and translate them into explicit design requirements.
2. Implement planning, session logging, personalised summaries and reflection features using Flask and SQLite.
3. Examine usability and perceived usefulness through SUS and qualitative feedback.
4. Describe patterns in logged distraction rates, perceived focus and questionnaire scores across the evaluation period.
5. Triangulate findings and revise the artefact, documenting design decisions and limitations.

**Research questions:**

| Question | Evidence | Intended conclusion |
|---|---|---|
| RQ1: What design features meet students' needs for study planning and distraction reflection? | Needs assessment, requirements, observed usability problems | Justified requirements and design lessons |
| RQ2: How usable and useful do participants perceive StudyFocus to be? | SUS, task walkthrough, reflections/interviews | Formative usability and usefulness findings |
| RQ3: What patterns are observed in logged distraction and perceived focus during the evaluation? | Session logs, exposure-normalised distraction rates, missingness | Descriptive within-participant patterns |
| RQ4: What changes do participants report in time-management behaviour and academic engagement? | TMBS and an agreed student engagement scale, qualitative feedback | Exploratory perceived changes, without attribution to the app |

Drop the causal hypothesis and claims about validating effectiveness with a single group. Baseline/end comparisons remain useful descriptive evidence; dropping the hypothesis does not require dropping these measurements.

## 4. Research methodology: DSR

Use the six activities described by Peffers et al. (2007), allowing iteration [R1].

| DSR activity | Work | Output |
|---|---|---|
| Problem identification | Literature and brief student needs assessment | Problem statement, contextual needs |
| Objectives | Specify usability, privacy, planning and reflection requirements | Requirements and evaluation criteria |
| Design and development | Build Flask routes, SQLite tables, forms and dashboard | Working prototype, schema, design rationale |
| Demonstration | Walk through enrolment, logging, feedback and export | Demonstration script and technical checks |
| Evaluation | 20–30 students; logs, scales, SUS and feedback | Formative findings and limitations |
| Communication | Explain results, revisions and provisional design lessons | Dissertation and artefact documentation |

DSR does not remove threats to validity. No control group, non-random recruitment, logging reactivity, exams/workload, attrition and short duration constrain the interpretation. The contribution is an evaluated artefact plus context-specific design learning, not proof of behavioural effectiveness.

## 5. Simple artefact specification

**Stack:** HTML/CSS templates → Flask application → SQLite database. SQLite keeps installation manageable. A notebook may support later analysis but is not the main artefact. PostgreSQL and Django are unnecessary for this first prototype.

| Requirement | Implemented feature | Evaluation evidence |
|---|---|---|
| R1: Keep records separate | Random participant code, private access key, per-user queries | Account-isolation test |
| R2: Record usual study | Baseline session logger without feedback summaries | Baseline records and logging coverage |
| R3: Support planning | Intervention form includes intended study duration | User task and qualitative feedback |
| R4: Record distraction and focus | Actual minutes, event counts, focus rating, task completion | Session dataset |
| R5: Support reflection | Baseline/intervention summary table and open reflections | SUS and interview evidence |
| R6: Support research analysis | Participant CSV and local researcher export | Export checks and analysis script |
| R7: Respect withdrawal | In-app account and record deletion | Cascade-deletion test |

**Implemented screens:** entry/login; one-time access details; phase-aware dashboard; session form; reflection form; export and withdrawal.

**Database:** participants 1→many sessions; participants 1→many reflections. Questionnaire responses are collected separately using approved survey forms and joined by participant code. The package includes the response and score templates; it does not invent or embed unverified scale questions.

**Prototype limits:** Planning is entered in the same form as the final log, so advance planning is a self-report, not a verified timestamped action. There is no website blocking, automatic social-media tracking or background timer. Session minutes and distractions are self-reported. The dashboard is a summary table rather than a chart. No claim should describe logs as objective attention measurement.

For a later iteration, separate plan creation from session completion if verified planning adherence is important. Do not add features merely to make the project look larger; justify features through needs and evaluation.

## 6. Evaluation protocol

**Participants:** Recruit approximately 20–30 university students aged 18 or older who undertake independent study and use social media. Describe convenience recruitment and the actual context. The target supports formative feedback in the supervisor's proposed scope; it is not a statistical power calculation. Report recruited, enrolled, active, withdrawn and analysed numbers separately. Do not claim the sample represents all students.

**Schedule per participant:**

| Time | Activity | Data |
|---|---|---|
| Before day 1 | Approved consent, orientation and baseline questionnaires | TMBS, BSMAS, selected student engagement scale |
| Days 1–7 | Record usual study using the baseline logger; withhold planning and summaries | Session logs and coverage |
| Days 8–28 | Use planning form, record sessions and review summaries | Session logs; optional weekly reflections |
| End of day 28 | Repeat TMBS and engagement measure; complete SUS | End questionnaire responses |
| Within a few days | Short interview or open-ended survey | Benefits, difficulties, workload/context, proposed changes |
| After evaluation | Compare evidence, identify design revisions | Evaluation matrix and revision log |

The whole observation period is four weeks: one baseline week plus three intervention weeks. Use identical distraction definitions and logging fields across phases. Baseline logging itself may change awareness; record this limitation. No logged session does not mean no studying or no distraction. Record optional reasons for low participation separately rather than inventing zero values.

### Measures and operational definitions

| Construct | Measure | Timing and handling |
|---|---|---|
| Time-management behaviour | TMBS, exact version agreed with supervisor | Baseline/end; retain published item wording, subscale mapping and reverse scoring. Document version and missing-item rule. Do not invent a single total across different versions [R2]. |
| Social-media-related difficulties | BSMAS | Baseline context. It has six items and a past-year recall period [R3]. Do not reinterpret its score as a three-week treatment outcome or a diagnosis. |
| Academic engagement | Candidate: UWES student version, preferably an appropriate approved short version | Baseline/end if suitable for population, language and timeframe. Check exact student version and permitted use; do not substitute a workplace version. Engagement is broader than momentary focus [R4]. |
| Session focus | Single purpose-written 1–5 rating | Each session. Label as a non-validated self-report item; not a substitute for an engagement scale. |
| Distraction | Self-noticed switches from studying to checking/using social media | Each session: event count and actual study minutes. Apply the same definition in both phases. |
| Usability | Standard 10-item SUS | End only; responses 1–5. Odd item contribution = response−1; even = 5−response. Sum ×2.5 gives 0–100, not a percentage [R5]. No score if required responses are missing unless a justified rule is specified beforehand. |
| Perceived usefulness | Reflection/interview prompts | What helped? What was difficult? What changed in your routine? What else affected studying? What would you change? Include neutral and negative accounts. |

BSMAS's past-year window overlaps almost entirely if repeated after three weeks. Preserve that wording if it is used; shortening the timeframe creates an adaptation that needs justification and must not be presented as the unchanged validated scale. TMBS and engagement scales may also be insensitive over this short period, so treat their changes as exploratory. Final instrument selection, access and scoring must be checked before real collection. The original TMBS study reports multiple factors [R2]; avoid selecting an arbitrary item count from an online copy.

### Evaluation criteria

Agree these before collection: participants can complete core tasks; records remain separated; users understand the logging fields; summaries are comprehensible; recurring usability barriers can be identified and addressed. Report SUS distribution and actual task success rather than declaring success from one arbitrary cutoff. Document incomplete or contradictory evidence. A revision log should link issue → evidence → design change → follow-up check.

## 7. Dataset and data management

The supplied package contains **25 fictional participants and reproducibly generated synthetic session records**, deliberately mixing increasing, stable and decreasing distraction patterns. These files test the software and analysis pipeline only. They do not represent collected responses or demonstrate that the artefact works.

Real data should be collected prospectively after the relevant university approvals. Start with the EMPTY templates; keep synthetic and real directories separate. No invented TMBS, BSMAS, UWES or SUS results are supplied. Questionnaire templates are intentionally empty.

See DATA_DICTIONARY.md for every field and missing-value rule. Use participant codes to join tables. Store contact details, if needed for recruitment, separately from the analytical dataset. Do not collect social-media passwords, private content or browsing histories. Restrict database/export access, use institution-approved encrypted storage, and set the retention period and withdrawal deadline in the approved information sheet. Open-text feedback may identify someone; review it before sharing.

The bundled app permits demonstration enrolment only. Before a real study, replace the demonstration consent text with the approved process, specify research contacts/retention/withdrawal details, configure study provenance correctly and complete institutional hosting/security review. It runs locally by default; internet deployment needs suitable hosting, TLS, authentication hardening, rate limiting, backups and an agreed multi-participant setup. Prototype tests do not constitute a production security audit.

## 8. Analysis plan

1. Validate codes, phase dates, plausible durations, duplicate records and questionnaire completeness. Report missingness and withdrawals. Preserve raw files and a cleaning log.
2. Summarise each participant separately within each phase. Do not treat multiple sessions from the same person as independent participants.
3. Compute **distraction events/hour = 60 × total events / total actual study minutes** within each participant/phase. Leave it missing when no minutes are recorded. Avoid comparing total event counts from a seven-day baseline against a 21-day intervention.
4. Summarise focus ratings, completion proportions and logging coverage (unique logged days / phase days). Focus ratings are ordinal; report distributions or median/IQR in the dissertation. The supplied app/script also shows means as simple descriptive summaries.
5. For participants with both phases, describe intervention-minus-baseline distraction rates and show individual trajectories. Summarise paired differences using median/IQR. Report who lacked a pair and why. Treat low logging coverage as an interpretation issue; any coverage threshold or sensitivity analysis should be defined before viewing outcomes.
6. Score the agreed TMBS subscales and engagement version using their verified rules. Describe paired baseline/end patterns and complete-pair counts. Keep BSMAS as baseline context. Report SUS descriptively with sample size and variability.
7. Code qualitative feedback: read all responses, develop and refine codes, document themes and exceptions, and use anonymised excerpts with consent. Do not generate participant quotations.
8. Triangulate using a table: log pattern; questionnaire pattern; relevant theme; agreement/disagreement; design implication. For example, low log coverage plus complaints about manual entry may suggest logging burden rather than improved distraction.

Formal significance testing is optional and secondary, to be agreed with the supervisor. A paired test still cannot demonstrate causality in this design. The supplied analysis script deliberately performs descriptive analysis only. Any correlation is exploratory, based on participant-level summaries, and potentially confounded. Avoid adding many correlations to a small sample.

**Acceptable result template:** “Among [n] participants with records in both phases, the median within-participant change in logged distractions per hour was [value]. Participants described [verified theme]. These patterns cannot be attributed to the application because there was no control group and logging was self-reported.”

**Avoid:** “The app proved effective”, “caused better time management”, “reduced addiction”, “produced measurable academic improvement”. Actual results must replace placeholders only after real data collection and analysis.

## 9. Dissertation/chapter structure

| Chapter | Main content |
|---|---|
| 1. Introduction | Context, problem, aim, objectives, research questions, scope, contribution |
| 2. Literature review | Time management, distraction, engagement, existing tools, measures, research gap |
| 3. Methodology | DSR rationale, requirements gathering, sample, protocol, measures, ethics, analysis, validity limits |
| 4. Artefact design and development | Requirements traceability, architecture, database, UI, implementation decisions, technical checks |
| 5. Formative evaluation | Participant flow, usage/missingness, usability, questionnaire patterns, qualitative themes, triangulation |
| 6. Discussion | Answers to RQs, design implications, comparison with literature, revisions, limitations |
| 7. Conclusion | What was built and learned, contribution within scope, future evaluation |
| Appendices | Approved materials, instrument versions/scoring references, data dictionary, test evidence, user guide |

## 10. Work plan and supervisor discussion

Suggested sequence: week 1 refine scope/requirements and submit ethics materials; weeks 2–3 build and technically check the artefact; pilot with a few users after required approval; run the four-week evaluation only after approval; then analyse, revise and write. Ethics review may take longer and should not be assumed complete within week 1.

Confirm the exact TMBS and student engagement versions, whether baseline-only BSMAS is acceptable, the four-week schedule, and the scope of descriptive analysis. The teacher offered Wednesday or Friday at 17:15 online; a date, timezone and your availability are still needed before arranging a meeting. No meeting or message has been sent.

## References and implementation sources

[R1] Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A Design Science Research Methodology for Information Systems Research. Journal of Management Information Systems, 24(3), 45–77. https://doi.org/10.2753/MIS0742-1222240302

[R2] Macan, T. H., Shahani, C., Dipboye, R. L., & Phillips, A. P. (1990). College students' time management: Correlations with academic performance and stress. Journal of Educational Psychology, 82(4), 760–768. https://doi.org/10.1037/0022-0663.82.4.760 ; accessible original paper: https://sdlab.fas.harvard.edu/resource/hoffmacan1990timemanagementperceivedstressandperformancepdf

[R3] Brailovskaia et al. (2022). Addictive social media use during Covid-19 outbreak: Validation of the Bergen Social Media Addiction Scale (BSMAS) and investigation of protective factors in nine countries. Current Psychology. https://pmc.ncbi.nlm.nih.gov/articles/PMC9122809/ . Consult the original Andreassen et al. (2016) instrument source when finalising the survey.

[R4] Schaufeli, W. B., & Bakker, A. B. (2004). Utrecht Work Engagement Scale: Preliminary Manual, version 1.1. Student-version guidance and engagement dimensions. https://www.wilmarschaufeli.nl/publications/Schaufeli/Test%20Manuals/Test_manual_UWES_English.pdf

[R5] GitLab's documented implementation of standard SUS scoring: https://handbook.gitlab.com/handbook/product/ux/performance-indicators/system-usability-scale/ . Use the standard Brooke SUS instrument and verify source/wording before collection.

[R6] Flask official installation guide: https://flask.palletsprojects.com/en/stable/installation/ . Requirements were exercised with Flask 3.1.3 in this preparation environment.
