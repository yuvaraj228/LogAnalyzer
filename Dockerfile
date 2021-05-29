FROM python:3-alpine

# 1. Install Java
RUN apk update \
&& apk upgrade \
&& apk add --no-cache bash \
&& apk add --no-cache --virtual=build-dependencies unzip \
&& apk add --no-cache curl \
&& apk add --no-cache openjdk8-jre

# 2. Install PYTHON and DEPENDENCIES

ENV PYTHON_VERSION 3.8.10-r0
# ENV ALPINE_OLD_VERSION 3.2

# Installing given python3 version
RUN apk update && \
    apk add python3=$PYTHON_VERSION 

# Upgrading pip to the last compatible version
RUN pip install --upgrade pip

# Installing required packages
RUN pip install ipython
RUN pip install requests
RUN pip install pyspark
RUN pip install pytest
RUN pip install pytest-html

# GENERAL DEPENDENCIES

RUN apk update && \
    apk add curl && \
    apk add bash

# 3. Install HADOOP & SPARK. Configure ENVIRONEMNT Variables

ENV JAVA_HOME="/usr/lib/jvm/java-1.8-openjdk"
ENV HADOOP_VERSION 2.7.2
ENV HADOOP_HOME /usr/hadoop-$HADOOP_VERSION
ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
ENV PATH $PATH:$HADOOP_HOME/bin
RUN curl -sL --retry 3 \
    "http://archive.apache.org/dist/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz" \
    | gunzip \
    | tar -x -C /usr/ && \
    rm -rf $HADOOP_HOME/share/doc

# SPARK

ENV SPARK_VERSION 3.1.1
ENV SPARK_PACKAGE spark-$SPARK_VERSION-bin-without-hadoop
ENV SPARK_HOME /usr/spark-$SPARK_VERSION
ENV PYSPARK_PYTHON python3 
ENV PYSPARK_DRIVER_PYTHON ipython
ENV SPARK_DIST_CLASSPATH="$HADOOP_HOME/etc/hadoop/*:$HADOOP_HOME/share/hadoop/common/lib/*:$HADOOP_HOME/share/hadoop/common/*:$HADOOP_HOME/share/hadoop/hdfs/*:$HADOOP_HOME/share/hadoop/hdfs/lib/*:$HADOOP_HOME/share/hadoop/hdfs/*:$HADOOP_HOME/share/hadoop/yarn/lib/*:$HADOOP_HOME/share/hadoop/yarn/*:$HADOOP_HOME/share/hadoop/mapreduce/lib/*:$HADOOP_HOME/share/hadoop/mapreduce/*:$HADOOP_HOME/share/hadoop/tools/lib/*"
ENV PATH $PATH:$SPARK_HOME/bin
RUN curl -sL --retry 3 \
    "http://apache.mirror.anlx.net/spark/spark-${SPARK_VERSION}/$SPARK_PACKAGE.tgz" \
    | gunzip \
    | tar x -C /usr/ && \
    mv /usr/$SPARK_PACKAGE $SPARK_HOME && \
    rm -rf $SPARK_HOME/examples $SPARK_HOME/ec2

# 4. Copy the project/source files from local to Docker

ADD . /app

# 5. working directory

WORKDIR /$SPARK_HOME