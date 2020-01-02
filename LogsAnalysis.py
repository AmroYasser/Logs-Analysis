#!/usr/bin/env python3

import psycopg2


# SQL queries

# 1. What are the most popular three articles of all time?
articles = """select row_number() over (order by count(log.path) desc) as sn,
                    articles.title, count(log.path) as num
                    from log, articles
                    where log.status = '200 OK'
                    and log.path like concat('%', articles.slug)
                    group by articles.title
                    order by num desc limit 3;"""

# 2. Who are the most popular article authors of all time?
authors = """select row_number() over (order by count(log.path) desc) as sn,
             authors.name, count(log.path) as num
             from log, articles, authors
             where log.status = '200 OK'
             and log.path like concat('%', articles.slug)
             and authors.id = articles.author
             group by authors.name
             order by num desc;"""

# 3. On which days did more than 1% of requests lead to errors?
errors = """select errors.date,
    round(errors.errors::decimal/total_requests.total * 100, 2) as percent
            from total_requests
            join errors
            on total_requests.date = errors.date
            and errors.errors::decimal/total_requests.total * 100 > 1;"""


# Connect to the database, execute the query, then close.
def execute(query):
    try:
        conn = psycopg2.connect(database="news")
    except psycopg2.Error as e:
        print('Unable to connect to the database')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Printing the report in plain text
def print_report():
    print('\t \t Report based on analysis of the news site data.\n')

    print('The most popular three articles of all time:')
    best = execute(articles)
    for sn, title, count in best:
        print('{}. {} - {} views.'.format(sn, title, count))

    print('\nThe most popular authors of all time:')
    most = execute(authors)
    for sn, name, count in most:
        print('{}. {} - {} views.'.format(sn, name, count))

    print('\nDays with errors of more than 1% of requests:')
    days = execute(errors)
    for day, percent in days:
        print('{} - {}% errors.'.format(day, percent))


print_report()
