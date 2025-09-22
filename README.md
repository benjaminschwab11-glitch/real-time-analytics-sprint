# Real-Time Analytics Sprint (AWS + Spark)

Production-minded demos focused on reliable, observable data pipelines on AWS. Starting simple (Spark Core + SQL) and progressing to streaming with Kinesis, Glue/MWAA orchestration, and a small end-to-end capstone.

## Goals
- Build durable batch + streaming patterns on AWS
- Show clear SLAs/SLOs, data quality checks, and operability
- Keep costs low and code simple; prefer clarity over cleverness

## Architecture (Current Phase)
- Phase 1 (Week 1): S3 (raw) -> Spark (Core/SQL) -> S3 (curated Parquet, partitioned) -> Athena/Redshift Spectrum (optional)
- Phase 2 (Week 2): Kinesis (ingest) -> Spark Structured Streaming -> S3 curated -> Athena/Spectrum
- Orchestration (Week 3+): Airflow (local/MWAA) to manage batch jobs and health checks

## Repo Structure
.
├── data/                         # small sample data (or S3 pointers)
├── notebooks/                    # quick EDA + query experiments
├── spark-jobs/
│   ├── batch_ingest_transform/   # Week 1 Spark Core + SQL
│   └── streaming_kinesis/        # Week 2 Structured Streaming
├── airflow/                      # DAGs + operators (Week 3)
├── glue/                         # Glue jobs + crawlers (Week 4)
├── infra/                        # optional IaC snippets (minimal)
├── dashboards/                   # CloudWatch/Athena/QuickSight exports
├── scripts/                      # producers, utilities, data quality checks
├── tests/                        # unit + data tests
└── docs/
    ├── architecture-diagrams/
    ├── runbooks/
    └── decisions/                # ADRs (architecture decision records)

## Prerequisites
- Python 3.10+
- Java 8+ (for local Spark)
- Apache Spark 3.x (local) or AWS EMR
- AWS account with access to S3, Kinesis (for Week 2), Glue, IAM
- AWS CLI configured (aws configure)
- Optional: Docker (for local Airflow), Make

## Quick Start (Local Spark)
1) Create and activate a virtual environment
   - macOS/Linux: python3 -m venv .venv && source .venv/bin/activate
   - Windows: py -3 -m venv .venv && .venv\Scripts\activate
2) Install dependencies
   - pip install -r requirements.txt
3) Set environment variables
   - export AWS_REGION=us-west-2
   - export S3_BUCKET=<your-bucket-name>
   - export APP_ENV=dev
4) Run Week 1 batch job
   - python spark-jobs/batch_ingest_transform/main.py --input s3://<raw-bucket>/nyc_taxi/ --output s3://<curated-bucket>/nyc_taxi_parquet/ --partition-col pickup_date
5) Query with Athena (optional)
   - docs/athena-ddl.sql contains external table DDL for Parquet

## Quick Start (EMR)
- Submit job via EMR Steps (example CLI in scripts/emr_submit.sh)
- Configure instance profiles and S3 paths in infra/emr_config.md

## Data Quality & Observability
- Row counts + null checks + schema validation (scripts/dq_checks.py)
- Basic metrics: throughput, latency, error rate (CloudWatch)
- Failure handling: dead-letter S3 path and retry policy
- Runbook: docs/runbooks/week1_batch_runbook.md

## Benchmarks (Week 1)
- Dataset sizes: small (100MB), medium (1–5GB)
- Record runtime, cost notes (Athena/EMR), and partitioning impact
- Results recorded in docs/benchmarks/week1_results.md

## Testing
- Unit tests (Pytest): transformations and utility functions
- Data tests: schema expectations and row-count checks
- Run: pytest -q

## Security & Cost Notes
- Least-privilege IAM (docs/decisions/adr-iam-least-privilege.md)
- S3 encryption at rest (SSE-S3/SSE-KMS), TLS in transit
- Cost controls: small EMR clusters or local Spark; clean up resources with scripts/cleanup.sh

## Roadmap (6 Weeks)
- Week 1: Spark Core + SQL on S3; Parquet partitioning; Athena queries; basic DQ + metrics
- Week 2: Spark Structured Streaming + Kinesis; producer script; CloudWatch dashboards
- Week 3: Airflow orchestration (local or MWAA); backfills; SLA tracking; DQ operators
- Week 4: Glue ETL + Catalog; Redshift Spectrum; performance vs cost comparison
- Week 5: Observability deep dive: metrics, alarms, DLQs, replay strategy; SLA/SLO doc
- Week 6: Capstone: end-to-end pipeline (producer -> Kinesis -> Spark streaming -> S3 curated -> Athena/Redshift -> dashboard)

## Deliverables
- Demo video per milestone (5–7 mins) in docs/
- Architecture diagram (draw.io/mermaid) per phase
- Short blog-style write-ups in docs/ (what/why/how + results)

## Notes
- Spark + Airflow experience: currently ramping via this project; production claims intentionally avoided.
- Open to feedback and PRs. This repo is designed for clarity and learning, not for production reuse.

## Contact
- Ben Schwab — Senior Data Engineer (AWS)
- Email: benjamin.schwab11@gmail.com
- LinkedIn: linkedin.com/in/bschwab03
- 
