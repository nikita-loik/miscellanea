import org.apache.spark.sql.SparkSession

val spark = SparkSession.builder().getOrCreate()

val df = spark.read.csv("CitiGroup_2006-2008")

df.head(5)