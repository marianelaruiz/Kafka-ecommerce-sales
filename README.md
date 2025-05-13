# Kafka: E-commerce Sales(Simulation)
This project involves the development of a message consumer in PySpark to process data received in real-time from Kafka. The main goal is to read sales data, apply transformations to the products sold, and calculate the total sales value per product, displaying the results on the console continuously.

## Objectives
1. Consume data from Kafka: Read sales event data from the ventas-events Kafka topic.

2. Transform the data: Perform aggregations of sales by product, calculating the total sales value for each.

3. Visualize results in real-time: Display the results of transformations on the console using the complete output mode in Spark Streaming, allowing the results to be continuously updated as new batches of data are received.

## Data Structure:
Sales data is received in JSON format, where each entry contains information about an order, the customer, the products purchased, and the sale date. An example of the data is as follows:

```

{
    "order_id": "b253f149-3f22-413c-9427-a79c38d65a2c",
    "customer_document": "431-61-5633",
    "products": [
        {"name": "Smartwatch", "cantidad": 3, "price": 1401},
        {"name": "Laptop", "cantidad": 1, "price": 2000}
    ],
    "sale_date": "12/05/2025 15:33:35"
}

```

Each product has a name, quantity, and price, which allows the total sales value per product to be calculated through the transformations applied in PySpark.

## Technologies Used:
- Apache Kafka: Used as the messaging system to receive real-time data. Kafka handles the ingestion of messages into the ventas-events topic.

- Apache Spark (PySpark): Used to process the data in real-time through Structured Streaming. PySpark reads the messages from Kafka and applies transformations such as aggregations and calculations on the data.

- Python: The programming language used to develop the message consumer, utilizing libraries such as pyspark to handle the data and perform the necessary transformations.

## **Setup and Execution**

### **1️⃣ Pull the Kafka Docker Image:**

Download the latest Kafka image from Docker Hub.

```bash
docker pull apache/kafka:4.0.0
```

### **2️⃣ Start the Kafka Docker Container:**

Run the Kafka container, exposing it on port `9092`.

```bash
docker run --name kafka-server -p 9092:9092 -d apache/kafka:4.0.0
```

### **3️⃣ Create a Kafka Topic:**

Create the topic `ventas-events` inside the Kafka container.

```bash
docker exec -it kafka-server /opt/kafka/bin/kafka-topics.sh --create     --topic ventas-events     --bootstrap-server localhost:9092
```

### **4️⃣ List Available Topics:**

Verify that the topic has been created successfully.

```bash
docker exec -it kafka-server /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
```

### **5️⃣ Run the Producer:**

Activate the virtual environment and start the producer to send data to the topic.

```bash
# Activate the virtual environment
source kafka_venv/bin/activate

# Run the producer
python3 producer.py
```

### **6️⃣ Run the Consumer:**

Execute the PySpark consumer to read and process the data from the Kafka topic.

```bash
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 consumer.py
```

---

## 📊 **Data Transformation:**

The consumer reads messages from Kafka, extracts the product information, and calculates the total sales for each product in real-time. The output is displayed in the console as follows:

```
+------------------+------------------+
|      Product    |   Total Sales   |
+------------------+------------------+
| Bluetooth Speaker |       4300      |
| Smartwatch        |       5500      |
| Laptop            |       2000      |
| Washing Machine   |       5500      |
+------------------+------------------+
```

## Conclusion:
This project provides a real-time processing solution for sales analysis using Kafka and Spark Streaming. Real-time data processing allows businesses to make quick decisions based on up-to-date sales data, which is essential in dynamic business environments.


