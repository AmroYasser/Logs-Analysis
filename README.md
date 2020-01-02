##Logs Analysis
This is one of the projects of the [Full Stack Nanodegree on Udacity](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

A reporting tool that prints out reports (in plain text) based on **analysis of data in the database of a fictional news website.**

This reporting tool is a Python program using the `psycopg2` module to connect to the database.

##What is this tool reporting?
Here are the information the tool gives:
1. The most popular three articles on the website of all time.
2. The most popular authors of all time.
3. days on which more than 1% of requests led to errors.

##Install
1. Make sure you have the latest version of **Python 3** installed on your machine, or [download it here.](https://www.python.org/downloads/)
2. You will need [Vagrant](https://www.vagrantup.com/downloads.html) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads) software installed on your machine.
3. Next, [download the website data here.](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) After downloading it, unzip the file then put the file named `newsdata.sql` into `vagrant` directory. 

##Run
On your terminal, run this commands in order:
1. `vagrant up` to start up the VM.
2. `vagrant ssh` to log into the VM.
3. `cd /vagrant` to change to your vagrant directory.
4. `psql -d news -f newsdata.sql` to load the data and create the tables.
5. `python3 newsdata.py` to run the reporting tool.

##Views used
#####total_requests
```
CREATE VIEW total_requests AS
SELECT date(log."time") AS date,
   count(log.id) AS total
  FROM log
 GROUP BY (date(log."time"));
```
#####errors
```
CREATE VIEW errors AS
SELECT date(log."time") AS date,
   count(log.id) AS errors
  FROM log
 WHERE (log.status <> '200 OK'::text)
 GROUP BY (date(log."time"));
```