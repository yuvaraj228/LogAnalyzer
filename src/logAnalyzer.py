from pyspark.sql import SparkSession,SQLContext
from pyspark.sql.functions import *
from logDownload import *

def topNsql(sqlContext, n):

    print("processing top {0} records".format(n))
    # Top N visitors/URLs per day. Generates rank based on maximum number/count of hosts(visitors) & URLs
    topNhost = sqlContext.sql("select * from (select dt,host_nm, count, Rank() over (partition by dt Order by count desc) as rank from (select dt,host_nm,count(host_nm) count from logTable group by 1,2 order by 1)) where rank <="+ str(n))
    topNurl = sqlContext.sql("select * from (select dt,endpoint, count, Rank() over (partition by dt Order by count desc) as rank from (select dt,endpoint,count(endpoint) count from logTable group by 1,2 order by 1)) where rank <="+ str(n))

    topNhost.show(n,False)
    topNurl.show(n,False)
    # Assumption : Write the extracts to file system. First case writes files that are partitioned by date and later will write a single file to file system
    topNhost.write.partitionBy("dt").format("csv").mode("overwrite").option("header","true").save("/app/target/topNhost")
    topNurl.coalesce(1).write.format("csv").mode("overwrite").option("header","true").save("/app/target/topNurl")

    return True

def transformLogData(df):
    # Regex patters to identify visitors/hosts, timestamp & http call/URL in the raw string
    host_nm_regex = "(^\\S+\\.[\\S+\\.]+\\S+)\\s"
    dt_ts_regex = "\\[(\\d{2}/\\w{3}/\\d{4}:\\d{2}:\\d{2}:\\d{2} -\\d{4})]"
    http_method_regex = "\"(\\S+)\\s(\\S+)\\s*(\\S*)\""
    # Creating new dataframe from raw string. This new DF will have data in multiple columns
    extract_colDf = df.select(regexp_extract(col('Value'),host_nm_regex,1).alias("host_nm"),
            regexp_extract(col('Value'),dt_ts_regex,1).alias("dt_ts"),
            regexp_extract(col('Value'),http_method_regex,2).alias("endpoint"))
    # Converting the raw timestamp to a valid timestamp. If not, spark will treat this a string. When we try to cast it to timestamp, it'll return null 
    dt_format = "dd/MMM/yyyy:HH:mm:ss X"
    # Creating a date column from timestamp. This date will be helpful when we roll up/aggregate the data
    stage = extract_colDf.withColumn("dt_ts", to_timestamp(col("dt_ts"),dt_format)).withColumn("dt",to_date("dt_ts"))
    stage.show(5,False)
    return stage

def dataCleanse(inp_data):
    # Cleanse the input data and apply DQ checks to flag/fix or drop unwanted data and continue loading meaningful records
    # Assumption : For now, Let's drop any records that have all nulls/empty strings. This method can be enhanced to perform any data quality checks
    # On the cleansed data, register a temporary table from which we can extract the necessary data
    cleansedDf = inp_data.na.drop()
    # Caching the cleansed dataframe for faster data processing
    cleansedDf.cache()
    cleansedDf.registerTempTable("logTable")
    print("returning cleansedDf")
    cleansedDf.show(5,False)
    return cleansedDf

def main(df, topN):

    print("Transforming the raw log file data.")
    try:
        # function that parses raw data
        stage = transformLogData(df)			
        # Calling data cleanse function by passing the stage dataframe and returning the cleansed dataframe
        transformedDf = dataCleanse(stage)
        print('Final TopN metrics')
        # generating the extracts of top N most visited urls & hosts
        topNsql(sqlContext, topN)

    except RuntimeError as e:
        # This block of code should be improved to handle specific exceptions instead of raising a high level run time error - ToDo 
        print("Needs to handle exception : " + str(e))

    finally:
        # Terminate the spark context
        sc.stop()
		
#  Execution starts here. Guard
if __name__ == '__main__':

    # These values have to go into config file
    ftp_site = "ftp://ita.ee.lbl.gov/traces/NASA_access_log_Jul95.gz"
    topN = 3
    appNm = "NASA_LogAnalyzer"
    inp_file = "/app/input/NASA_access_log_Jul95.gz"

    # Downloading log from the ftp site. Calling another python script (logDownloader.py) from main
    print("Connecting to FTP site : " +ftp_site)
    # makes a call to logDownloader and downloads the file in input path
    logDownloader(ftp_site)
    print("File download successful. Analyzing the log data now")

    # Initializing Spark Session and Spark Context
    spark = SparkSession.builder.master("local[1]").appName(appNm).getOrCreate()
    sc = spark.sparkContext
    sqlContext = SQLContext(sc)
    # Creating dataframe on raw input data. This is a single column value
    df = spark.read.text(inp_file)
    main(df, topN)



