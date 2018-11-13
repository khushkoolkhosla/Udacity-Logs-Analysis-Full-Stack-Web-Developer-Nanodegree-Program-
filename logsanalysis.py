#!/usr/bin/env python
import psycopg2
import sys

#Connect to database named 'news'

DB_NAME = "news"

def connect(database_name):
    #Connects to the database :  "news"
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        #Cursor executes queries and fetches results
        c = db.cursor()
        #Execute input query from cursor
        return db, c
    except psycopg2.Error as e:
        print "Unable to connect to database"
        #Then exit the program
        sys.exit(1)     
        raise e


def fetch_results(query):
    db, c = connect(DB_NAME)
    c.execute(query)
    #fetch results from cursor
    results = c.fetchall()
    c.close()
    return results


def most_viewed():
    print "What are the most popular three articles of all time?" + '\n'
    query1 = "SELECT * FROM most_viewed_articles limit 3;"
    most_viewed_results = fetch_results(query1)
    for line in most_viewed_results:
        print('"' + str(line[0]) + '"' + ' - ' + str(line[1]) + ' views')
    print '\n'


def most_popular_author():
    print "Who are the most popular article authors of all time?" + '\n'
    query2 = "SELECT * FROM most_popular_author;"
    most_popular_results = fetch_results(query2)
    for line in most_popular_results:
        print('"' + str(line[0]) + '"' + ' - ' + str(line[1]) + ' views')
    print '\n'


def most_error_day():
    """On which days did more than 1% of requests lead to errors?"""
    print "On which days did more than 1% of requests lead to errors?" + '\n'
    query3 = "SELECT * FROM day_with_most_errors;"
    error_results = fetch_results(query3)
    print(str(error_results[0][0]) + ' -- ' + str(error_results[0][1]) +
          ' errors')
    print '\n'


if __name__ == '__main__':
    most_viewed()
    most_popular_author()
    most_error_day()
