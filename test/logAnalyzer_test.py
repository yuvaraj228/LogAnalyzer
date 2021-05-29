import pytest
from pyspark.sql.types import *
from datetime import datetime,date
import sys

# Local src file path. This needs to be changed to directory where you place project files
sys.path.append("C:/Users/susmi/Sunny/Projects/app/src")
from logAnalyzer import *

def test_data_cleanse(sql_context):
    # Input data. Case - 1 to check if the Empty/Null records get dropped. Checks dataCleanse() logic
    schema = StructType([
        StructField("host_nm", StringType()),
        StructField("dt_ts", TimestampType()),
        StructField("endpoint", StringType()),
        StructField("dt", DateType())
    ])
    data = [
        ("199.72.81.55", datetime.now(), "/history/apollo/3",date.today()),
        ("199.72.81.55", datetime.now(), "/history/apollo/2",date.today()),
        ("199.72.81.55", datetime.now(), "/history/apollo/1",date.today()),
        ("dell.secure.works.com", datetime.now(), "/history/test/1",date.today()),
        ("dell.secure.works.com", datetime.now(), "/history/test/1",date.today()),
        ("dell.secure.works.com", datetime.now(), "/history/test/1",date.today()),
        ("191.192.5.10", datetime.now(), "/history/NASA/1",date.today()),
        (None, None, None, None)
    ]  
    df = sql_context.createDataFrame(data,schema)
    print("Count before performing the data cleanse : ", df.count())
    resDf = dataCleanse(inp_data=df)
    actual = resDf.count()
    expected = df.na.drop().count()
    print("Count after performing the data cleanse : {0}".format(actual))

    assert(actual==expected)
    assert(df.count() >= actual)

def test_transformLogData(sql_context):
    # Case - 2 Check if the column values are getting correctly populated. See if the pattern matching is working as expected
    schema = StructType([
        StructField("Value", StringType())
    ])
    data = [
        ('199.72.81.55 -- [01/Jul/1995:00:00:01 -0400] "GET /history/apollo/ HTTP/1.0\"')
    ]
    df = sql_context.createDataFrame([data],schema)
    print("Schema of input/raw dataframe is : ",df.dtypes)
    resDf = transformLogData(df)
    host_nm = resDf.select("host_nm")
    print("Schema of resulting/transformed dataframe is : {0}".format(resDf.dtypes))

    assert resDf.dtypes == [("host_nm","string"),("dt_ts","timestamp"),("endpoint","string"),("dt","date")]

def test_topNsql(sql_context):
    # Case - 3 Pick the top most visited urls and endpoints
    res = topNsql(sql_context,3)
    
    assert res == True