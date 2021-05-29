import pytest
import logging
from pyspark.sql import SQLContext, SparkSession
from pyspark.sql.types import StructType, IntegerType, DateType
from pyspark import SparkContext

def quiet_py4j():
    """ turn down spark logging for the test context """
    logger = logging.getLogger('py4j')
    logger.setLevel(logging.WARN)

@pytest.fixture(scope='session')
def sql_context():
    quiet_py4j()
    spark_context = SparkContext()
    sql_context = SQLContext(spark_context)
    return sql_context
    spark_context.stop()

@pytest.fixture(scope='session')
def spark():
    print('In spark')
    quiet_py4j()
    return SparkSession.builder \
      .master("local") \
      .appName("test") \
      .getOrCreate()