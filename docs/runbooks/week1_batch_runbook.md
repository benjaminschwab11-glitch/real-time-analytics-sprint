# Week 1 Batch Runbook
Goal: Ingest CSV -> Spark (clean/partition) -> Parquet output

Commands
- bash scripts/nyc_taxi_sample_download.sh
- python spark-jobs/batch_ingest_transform/main.py --input data/raw/nyc_taxi/yellow_2023-01.csv --output data/curated/nyc_taxi_parquet --partition-col pickup_date --repartition 8

Validation
- Parquet files present under data/curated/nyc_taxi_parquet/
- Partition folder structure includes pickup_date=YYYY-MM-DD
- Row count > 0

Troubleshooting
- Memory/local mode: reduce --repartition to 1–4
- Schema issues: add/remove inferSchema and sample fewer rows
- Missing date: adjust transform() to set partition column
