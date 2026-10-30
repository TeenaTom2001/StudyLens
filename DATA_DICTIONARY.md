# Dataset dictionary

## Provenance and missing data

Files ending SYNTHETIC contain fictional software test data. `is_synthetic=1` denotes synthetic or demonstration data; `0` is reserved for verified real research records. Do not mix them. The app's consent text is for a demonstration, so its exports are marked 1. Never change that flag simply to make demonstration entries look real. Set up a separately approved research collection before producing real records.

An empty cell means not collected, unavailable or not applicable; it never means zero. Zero distraction events is a valid observed self-report. A day with no session rows is an unobserved day, not a zero-distraction day. Store dates as YYYY-MM-DD using one agreed local study timezone. The local app uses the host's calendar date, which must be configured consistently before use.

## participants

| Field | Type / rule | Meaning |
|---|---|---|
| participant_id | Unique text | Random/pseudonymous code; synthetic codes begin SYN |
| baseline_start | ISO date | First day of the 7-day baseline; intervention begins 7 days later |
| consent_version | Text | Approved information/consent version; demo values are not evidence of real informed consent |
| is_synthetic | 0 or 1 | Provenance flag |

The private app database additionally stores `key_hash` for authentication. It is never exported. No names or contact details are required in this table.

## sessions

| Field | Type / rule | Meaning |
|---|---|---|
| session_id | Unique text | One study-session record |
| participant_id | Foreign key | Link to participant |
| session_date | ISO date | Date of self-reported session |
| phase | baseline / intervention | Derived from participant baseline_start: offsets 0–6 / 7–27 |
| planned_minutes | Integer 1–720 or blank | Intended duration in intervention; blank in baseline; not timestamp verified |
| actual_minutes | Integer 1–720 | Self-reported actual study minutes excluding breaks |
| distraction_count | Integer 0–1000 | Self-noticed social-media switching events; upper bound is validation, not a plausible norm |
| focus_rating | Integer 1–5 | Very low, low, moderate, high, very high; purpose-written non-validated item |
| completed | 0 / 1 | Intended task not completed / completed |
| is_synthetic | 0 / 1 | Provenance flag |

Multiple sessions on the same date are valid. Never delete such rows solely because their dates match. Query suspected duplicates using participant, date, durations and counts and retain an audit trail. If richer date/time analysis is required, add start/end timestamps prospectively.

## questionnaire_responses (empty collection template)

One row per participant × timepoint × instrument/version × item. Keep the original responses; derive scores separately.

| Field | Rule |
|---|---|
| participant_id | Must match participants |
| timepoint | baseline or end; SUS=end, BSMAS=baseline in this plan |
| collection_date | Actual ISO collection date |
| instrument | TMBS, BSMAS, UWES_STUDENT, SUS; chosen version must be explicit |
| instrument_version | Exact edition, language and any adaptation identifier |
| item_id | Published version's item identifier, e.g. SUS01 |
| response | Original numeric response; blank for missing |
| is_synthetic | Provenance flag |

Expected response ranges: BSMAS 1–5; SUS 1–5; UWES typically 0–6 but verify the selected student form. TMBS range/item count/subscales must follow the exact agreed version. Never infer reverse-scoring from a column name. No instrument questions are reproduced in this package.

## questionnaire_scores (empty derived-data template)

| Field | Rule |
|---|---|
| participant_id, timepoint, instrument, instrument_version | Link to response set |
| subscale | Exact published subscale, or total only if supported by that instrument |
| score | Derived numeric score; blank if not scoreable |
| items_answered / items_expected | Completeness counts for this score |
| scoring_rule_version | Identifier linking to a documented scoring recipe |
| is_synthetic | Provenance flag |

SUS: sum odd-item (response−1) and even-item (5−response) contributions, multiply by 2.5; 0–100, not percent. BSMAS: six items summed gives 6–30 when all six are answered; keep as contextual baseline, not a diagnosis. Do not supply TMBS scores until item mapping and version are established. For the selected UWES student version, verify subscale membership and mean-score rules in its manual before scoring. No automatic questionnaire scorer is supplied because the final versions are not yet selected.

## reflections

| Field | Rule |
|---|---|
| reflection_id | Unique record ID |
| participant_id | Foreign key |
| recorded_date | ISO date |
| useful | Optional response to what was useful, max 2,000 characters |
| difficult | Optional response to difficulties, max 2,000 characters |
| suggested_change | Optional suggested improvements, max 2,000 characters |
| is_synthetic | Provenance flag |

At least one text field is required for an app reflection. Remove accidental identifiers before sharing; preserve an access-restricted original where permitted. Missing text is not a negative response.

## Derived participant summaries

The analysis script outputs sessions, unique logged days, coverage, study minutes, distractions/hour and mean self-rated focus per phase, plus rate change (intervention minus baseline). A negative change means fewer *logged* events per recorded study hour. It is not an estimated treatment effect. Full scheduled-phase denominators are 7 and 21 days; interpret coverage for withdrawn participants alongside their withdrawal date rather than as simple non-adherence. The script is intended for completed four-week records, not an interim dashboard.
