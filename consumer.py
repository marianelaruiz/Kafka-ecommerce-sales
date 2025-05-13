from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, explode, expr
from pyspark.sql.types import StructType, StructField, StringType, ArrayType, DoubleType

# Initialize Spark session
spark = SparkSession.builder \
    .appName("KafkaEcommerceConsumer") \
    .getOrCreate()
spark.sparkContext.setLogLevel("WARN")


# Define the schema of the incoming JSON messages
schema = StructType([
    StructField("order_id", StringType(), True),
    StructField("customer_document", StringType(), True),
    StructField("products", ArrayType(StructType([
        StructField("name", StringType(), True),
        StructField("quantity", StringType(), True),
        StructField("price", DoubleType(), True)
    ]))),
    StructField("total_value", DoubleType(), True),
    StructField("sale_date", StringType(), True)
])

# Connect to Kafka and read the stream
ventas_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "sales-events") \
    .option("startingOffsets", "latest") \
    .load()

# Transform the Kafka message from binary to JSON format
ventas_df = ventas_df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

# Explode the array of products into individual rows
# Each row represents one product of the sale
products_df = ventas_df.select(
    explode("products").alias("product")
)


# Select necessary columns and cast them correctly
# Calculate the total value for each product (quantity * price)
products_df = products_df.select(
    col("product.name").alias("product_name"),
    col("product.quantity").cast("int").alias("quantity"),
    col("product.price").alias("price")
).withColumn("total_value", expr("quantity * price"))

# Group by product name and sum the total value for each product
total_sales_df = products_df.groupBy("product_name") \
    .sum("total_value") \
    .withColumnRenamed("sum(total_value)", "total_sold_value")


# products_df.show(10)
query = total_sales_df.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", "false") \
    .start()



query.awaitTermination()
