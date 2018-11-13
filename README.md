#Log Analysis Project

#Task 
My task is to create a reporting tool that prints out reports (in plain text) based on the data in the database. 
This reporting tool is a Python program using the psycopg2 module to connect to the database.

The reporting tool should answer the 3 following questions:

 1. What are the most popular three articles of all time?
 2. Who are the most popular article authors of all time?
 3. On which days did more than 1% of requests lead to errors?

#Installation Procedure 

1. Start by installing VirtualBox,Vagrant,VM config,
Reason for VirtualBox: Virtualbox is the software used specifically for running the virtual machine. Vagrant, in the next step, will run VirtualBox after installing. 
Reason for Vagrant: The software that configures the virtual machine(VM) and enables you to share files between your host computer and VM's filesystem.
Reason for VM configuration : This directory contains the VM files. After downloading it, change to this directory using your terminal with the **```cd```** command. Then change to the vagrant directory inside FSND-Virtual-Machine.


2. Start the virtual machine by running **```vagrant up```**. Vagrant downloads and installs the Linux operating system.
Give it a few minutes for this to complete. After **```vagrant up```** is finished, you can run **```vagrant ssh```** to
log in to the newly installed Linux VM.
   
3. Once inside the VM, change the directory to **```vagrant```** and use **```ls```** to look around.

4. **NOTE - THIS COMMAND ONLY NEEDS TO BE RUN ONCE!** Load the data from newsdata.sql by using **```psql -d news -f newsdata.sql```**. 
This is what each component of the command does:
* psql — the PostgreSQL command line program
* -d news — connect to the database named news which has been set up for you
* -f newsdata.sql — run the SQL statements in the file newsdata.sql ```

5. Type **```psql -d news```** to explore the database.

#View Code : (Run the following commands to create the respective views)
Create the following views before running logsanalysis.py:

```
CREATE VIEW most_viewed_articles as
SELECT articles.title, count(log.path) as views
    FROM articles, log
    WHERE log.path LIKE '%' || articles.slug
    GROUP BY articles.title
    ORDER BY views desc;
        
CREATE VIEW most_popular_author as
SELECT authors.name, count(log.path) as author_views
    FROM authors, articles, log
    WHERE status != '404 NOT FOUND'
    AND articles.author = authors.id
    AND log.path LIKE '%' || articles.slug || '%'
    GROUP BY authors.name
    ORDER BY author_views desc;
        
CREATE VIEW errors_per_day as
SELECT to_char(log.time, 'FMMonth DD, YYYY') "day", count(log.status) as errors
    FROM log
    WHERE status = '404 NOT FOUND'
    GROUP BY 1
ORDER BY 1;
        
CREATE VIEW requests_per_day as
SELECT to_char(log.time, 'FMMonth DD, YYYY') "day", count(log.status) as requests
    FROM log
    GROUP BY 1
    ORDER BY 1;
        
CREATE VIEW day_with_most_errors as
SELECT errors_per_day.day, concat(ROUND((100.0 * errors_per_day.errors / requests_per_day.requests), 2), '%')as percent_errors
    FROM errors_per_day, requests_per_day
    WHERE errors_per_day.day = requests_per_day.day
    AND (((100.0 * errors_per_day.errors / requests_per_day.requests)) > 1)
    ORDER BY percent_errors desc;
```


6. After creating the above views in psql, you may exit PSQL by typing **```\q```**. 
Reason : This returns you to the vagrant directory inside the VM.
 
7. Typing **```python logsanalysis.py```** executes the logsanalysis.py file.
Result : Logsanalysis.py executes SQL queries using the database file (newsdata.sql). 
