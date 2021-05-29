The objective of this project is to analyze the logs of HTTP requests made to NASA Space Center server

#Application Description
1. Data from the HTTP logs of NASA Space Center is downloaded and read into a spark dataframe for consumption
2. Parse the dataframe for host, endpoint and timestamp details. Standarsize the data attributes to a format that spark understands. If not, spark treats them as Null.
3. In this case, timestamp has to be formatted to spark understandable form.
4. Cleanse the dataframe. Any standardization  and data quality logic goes along with this block.
5. Get the top n most frequently visited hosts per day
6. Get the top n most frequently searched url per day

# Data Download the dataset for July:
ftp://ita.ee.lbl.gov/traces/NASA_access_log_Jul95.gz


**Description of the dataset:** The logs are in files with one line per request with the following columns:

* Host making the request. A hostname when possible, otherwise the internet address if the name cannot be identified;
* Timestamp in the format "DAY / MONTH / YEAR: HH: MM: SS TIMEZONE";
* HTTP Request (in quotes);
* HTTP return code;
* Total bytes returned.

# Assumptions :
- For this use case, I'm only dropping those records where the entire row is null. Since they carry no value. Even such records can be investigated further by writing them to an error log file
- This function can be further improvized by adding logic to standardize null validations. 
- There are certain records with url and endpoint values as null. We can have checks in place to handle such records.


## Running the project

Pre requisite local setup
- Python 3 and required dependencies
- Spark - 3.1.1 with hadoop 2.7

Set SPARK_HOME path in spark-log-analyzer.sh and run the script

## Running the project on docker

- Build the docker image with Python and spark env
```docker-compose build pyspark-env```
- Spin up the spark env container and run the job.	
```docker-compose up -d```
- NASA_LogAnalyzer - Spark Jobs.html is the Spark UI page of Docker instance. It's in the main directory of git hub.

***Information extracted from the dataset***
   
####1. top 3 hosts per day
    +----------+--------------------+----+
    |	dt	   |    host            |rank|
    +----------+--------------------+----+
    |1995-07-01|piweba3y.prodigy.com|  1 |
    |1995-07-01|piweba4y.prodigy.com|  2 |
    |1995-07-01|alyssa.prodigy.com	|  3 |
    |1995-07-02|piweba3y.prodigy.com|  1 |
    |1995-07-02|alyssa.prodigy.com	|  2 |
    |1995-07-02|piweba1y.prodigy.com|  3 |
	+----------+--------------------+----+
####2. top 3 urls per day
    +----------+----------------------------+----+
    |	dt	   |    		host            |rank|
    +----------+----------------------------+----+
    |1995-07-01|/images/NASA-logosmall.gif  |  1 |
    |1995-07-01|/images/KSC-logosmall.gif   |  2 |
    |1995-07-01|/shuttle/countdown/count.gif|  3 |
    |1995-07-02|/images/NASA-logosmall.gif	|  1 |
    |1995-07-02|/images/KSC-logosmall.gif	|  2 |
    |1995-07-02|/shuttle/countdown/count.gif|  3 |
    +----------+----------------------------+----+
	
## Running Unit test cases on the Pyspark application

- app/test/ folder has the unit test code.
- conftest.py file will make external modules available for our test cases.
- Create spark context and session and make them available for logAnalayzer_test.py script
- Feed sample input/test data to the actual spark driver code, to see if the code is working as expected
- Run the pytest-html in verbose mode. This will generate a detailed report on succeeded, failed and skipped test cases.
- Attached a pytest-html report output, in the test folder.