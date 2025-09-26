import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, to_date, lit

def create_spark(app_name="week1_batch_ingest_transform"):
    return (SparkSession.builder
            .appName(app_name)
            .config("spark.sql.shuffle.partitions", "200")
            .getOrCreate())

def transform(df, partition_col):
    # Normalize column names
    for c in df.columns:
        df = df.withColumnRenamed(c, c.strip().replace(" ", "_").lower())

    # Derive a date partition from a timestamp-like column if present
    ts_candidates = ["tpep_pickup_datetime", "pickup_datetime", "ts", "event_time"]
    ts_col = next((c for c in ts_candidates if c in df.columns), None)
    if ts_col is not None:
        df = df.withColumn(ts_col, to_timestamp(col(ts_col)))
        df = df.withColumn(partition_col, to_date(col(ts_col)))
    else:
        # Fallback: static partition date to allow writes
        df = df.withColumn(partition_col, lit("2023-01-01"))
    return df

def main(args):
    spark = create_spark()

    # Read input
    df = (spark.read
          .option("header", True)
          .option("inferSchema", True)
          .csv(args.input))

    # Fail fast if schema or data is empty
    if len(df.columns) == 0:
        raise ValueError(f"Input dataset has no columns. Check --input path or file format: {args.input}")
    if df.limit(1).count() == 0:
        raise ValueError(f"Input dataset has zero rows. Check --input path or file content: {args.input}")

    # Transform and guarantee partition column
    df = transform(df, args.partition_col)

    # Write output
    (df.repartition(args.repartition)
       .write.mode("overwrite")
       .partitionBy(args.partition_col)
       .parquet(args.output))

    spark.stop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Local path or s3:// bucket/prefix")
    parser.add_argument("--output", required=True, help="Local path or s3:// bucket/prefix")
    parser.add_argument("--partition-col", default="pickup_date")
    parser.add_argument("--repartition", type=int, default=4)
    args = parser.parse_args()
    main(args)
