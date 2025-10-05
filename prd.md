# LazyMail - a phishing email detection system
### Product summary

A self-hosted, containerized email security platform that ingests mail from Gmail/IMAP or an optional MX gateway, analyzes content and context using a layered pipeline (auth/rules, stylometry, ML), and provides a web dashboard for triage, hunting, and automated policy actions with auditable explanations.

### Goals and non-goals

- Goals: High-precision detection of modern phish and BEC, Gmail/IMAP ingestion, explainable scoring, automated alerts/actions, feedback-driven continuous learning, and full portability.
- Non-goals: Paid SaaS integrations, proprietary feeds, or requiring third‑party security assessments for public distribution; keep scopes minimal and deployment self-hosted.

### Personas and users

- SOC analyst: Needs high-confidence alerts, explainable verdicts, and one-click labeling to reduce MTTR.[^2]
- Security engineer: Needs reliable ingestion, policy automation, and extensible rules/ML hooks under version control.[^2]
- IT admin: Needs low-friction OAuth/IMAP setup, token hygiene, and Dockerized operations.


### Key use cases

- Detect and quarantine high-confidence phishing and BEC, even without links/attachments, via stylometry and behavior anomalies.
- Backfill and re-score historical mailboxes for incident review and posture assessment.
- Auto-label in Gmail and send real-time alerts to channels/webhooks; enable analyst-reviewed promotions/dismissals.


### Scope and features (v1)

- Ingestion
    - Gmail worker with least-privilege scopes: gmail.readonly, gmail.metadata, gmail.modify for labeling; device/loopback auth with token rotation; respect verification guidance to avoid restricted scopes where possible.[^4][^5][^3]
    - IMAP worker for non-Gmail providers with IDLE or scheduled fetch; normalized MIME parsing.[^1]
- Detection pipeline
    - Deterministic layer: SPF/DKIM/DMARC verification, header anomalies, and Rspamd rule scoring as primary gating.[^2]
    - Content/URL analysis: Extract URLs/domains, lexical features, homograph detection, and HTML sanitization.[^2]
    - Stylometry/ML: Lightweight classifier over structured features and text stylometrics to capture BEC and AI-generated phish; model output is a feature in a calibrated ensemble.[^2]
- Intelligence and actions
    - Policy engine with thresholds for auto-quarantine, auto-label, or route-to-review; webhook alerts.[^2]
    - IOC management with export/import hooks for community feeds (future MISP connector in v1.1).[^2]
- Dashboard
    - Inbox view with risk scores, contributors (rules, auth, stylometry), header/auth status, URL intel hits, and explanation trace.[^2]
    - One‑click label: phish/benign/suspicious to feed learning and adjust thresholds.[^2]
- Ops
    - Docker Compose stack: api, workers, rspamd, redis, postgres, web-ui; Mailcow/Mailu optional as MX edge.[^1][^2]


### Out of scope (v1)

- Proprietary threat-intel feeds or paid sandbox integrations.[^4]
- Organization-wide phishing simulation and training (may integrate with GoPhish later).[^6][^7]


### Success metrics

- Precision at 95% recall for link-bearing phish; precision at 80% recall for payloadless BEC.[^8]
- Mean time to alert under 60 seconds for new inbound messages.[^2]
- Analyst actionability: ≥90% of alerts include at least three concrete contributing signals and a clear recommended action.[^2]


### Functional requirements

- Must ingest ≥50 messages/second sustained with horizontal worker scaling; backfill 1M emails within 24 hours on commodity hardware.[^2]
- Must verify SPF/DKIM/DMARC and expose results per message.[^2]
- Must expose an explainable risk score combining Rspamd symbols, auth checks, URL/lexical features, and stylometric classifier output.[^2]
- Must support Gmail label write-back and quarantine folder moves where permitted.[^3]
- Must provide search and filters by sender, domain, score range, and symbol hits.[^2]


### Non-functional requirements

- Security: Principle of least privilege for OAuth scopes; encrypted token storage; RBAC for dashboard; audit logs for all actions.[^5][^3]
- Reliability: Exactly-once processing semantics per message id; idempotent workers; retry with DLQ; health probes.[^2]
- Performance: P95 end-to-end analysis latency under 500 ms without URL fetch; under 5 s with URL metadata.[^2]
- Portability: Single-node Docker Compose; optional K8s manifests later; no paid dependencies.[^1]
- Updatability: Hot-reload rules and feature extractors; model versioning with rollback.[^2]


### Data model (high level)

- Message: message_id, account_id, headers, auth_results, normalized text/html, attachments metadata, timestamps.[^2]
- Features: symbols (Rspamd), lexical/url metrics, stylometry vectors, model version tags.[^2]
- Verdict: score, class, explanation list, action taken, label history, analyst feedback.[^2]


### Integrations

- Gmail API with published scope list and verification paths; document user-consent flows to minimize restricted scopes and avoid third‑party assessment for internal deployments.[^4][^3]
- Optional Mailcow/Mailu as edge for organizations needing MX control; leverage built-in Rspamd/ClamAV.[^9][^1]


### Risks and mitigations

- Gmail scope verification delays or assessment requirements: operate as an internal app with limited user pool; prefer non-restricted scopes; publish documentation of data handling.[^4][^3]
- Rspamd false positives or config drift: version-control rules; gated promotions; beware recent Mailcow/Rspamd regressions and test upgrades before rollout.[^10][^9]
- Dataset drift: periodic calibration on recent mail; time-split validation; feature importance monitoring.[^8]


### Privacy and compliance

- Minimize PII exposure; field-level encryption for bodies/attachments at rest; configurable retention and right-to-erasure workflows.[^3]
- Strict separation of training corpora and live mailbox content unless explicitly consented via settings.[^3]


### Rollout plan

- Alpha: IMAP + Gmail read-only, rules + auth checks + basic stylometry, dashboard with explanations and manual actions.
- Beta: Gmail modify (labels/quarantine), webhook alerts, policy automation, performance tuning and backfill jobs.[^3]
- GA: MISP connector, model A/B with calibration, K8s manifests, RBAC and audit hardening.[^2]


### Acceptance criteria (v1)

- End-to-end ingest-to-alert flow for Gmail and IMAP with Docker Compose deployment.
- ≥90% of alerts have clear explanation artifacts and a reproducible decision trace.
- Achieve target precision/recall on a held-out 90‑day time-split dataset sourced from recent phishing trends.

If desired, the next step will be a technical spec: service boundaries, API contracts, database schema, and a Docker Compose file to spin up the alpha stack.
