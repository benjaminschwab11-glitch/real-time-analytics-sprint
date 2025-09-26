#!/usr/bin/env bash
set -euo pipefail
mkdir -p data/raw/nyc_taxi
curl -L https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2023-01.csv.gz -o data/raw/nyc_taxi/yellow_2023-01.csv.gz
gunzip -f data/raw/nyc_taxi/yellow_2023-01.csv.gz
echo "Downloaded to data/raw/nyc_taxi"
