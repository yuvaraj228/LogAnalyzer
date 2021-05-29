#!/bin/bash
echo "Running spark submit to trigger python script..."
# Set Path of Python, Spark, Java & Hadoop, if this wasn't done earlier

# export PYSPARK_HOME=C:\Users\susmi\AppData\Local\Programs\Python\Python39\python.exe
# Directory where spark-submit is defined
# export SPARK_HOME=C:\spark\spark-3.1.1-bin-hadoop2.7
# export JAVA_HOME=C:\Java\jre1.8.0_291

# Run it locally
# ${SPARK_HOME}/bin/spark-submit --class main --master local logAnalyzer.py
# CD PWD # to src files directory where the sprak driver program is placed or give the fully qualified path of logAnalyzer.py file

${SPARK_HOME}/bin/spark-submit --master local logAnalyzer.py


