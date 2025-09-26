import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date

def create_spark(app_name="week1_batch_ingest_transform"):
    return (SparkSession.builder
            .appName(app_name)
            .config("spark.sql.shuffle.partitions", "200")
            .getOrCreate())

def transform(df, partition_col):
    # Derive a date partition if missing
    if partition_col not in df.columns:
        for c in ["tpep_pickup_datetime", "pickup_datetime", "ts", "event_time"]:
            if c in df.columns:
                df = df.withColumn(partition_col, to_date(col(c)))
                break
    # Basic cleanup: normalize column names
    for c in df.columns:
        df = df.withColumnRenamed(c, c.strip().replace(" ", "_").lower())
    return df

def main(args):
    spark = create_spark()
    df = (spark.read
          .option("header", True)
          .option("inferSchema", True)
          .csv(args.input))
    df = transform(df, args.partition_col)
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
    parser.add_argument("--repartition", type=int, default=8)
    args = parser.parse_args()
    main(args)
