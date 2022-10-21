# BF768 - FIADB Database

This database and website aims to help professors at BU by providing an updated forest inventory database to help centennial scale projections of forest response to environmental change over time and better estimate terrestrial ecosystem models.This database was implemented as a project for the Boston University BF768 course, Spring 2022.

**The link:**

https://bioed.bu.edu/students_22/Group_F/FIADB.html

# Contributors

**Allison Choy** - Query_tab

**Kyra Griffin** - Database Creator

**Merai Dandouch** - Plots_Tab 

**Raghad Yamani** - Home, contact, and help tabs

# Repository Contents

- **Plots_Tab**: This file contains two files which are called plots.py and plots.html
  - **plots.py**: This file is the CGI component which handles connection between the database and client requests. For each dropdown menu page, there are two different tables being generated, one for the plot and another for the table plot. 
  - **plots.html**: The UI interface for this page 
  - **How to run**: Just open the html file in a web browser and explore the page!

- **Query_tab**: This directory contains two files, FIAQuery.html and FIAQuery.py
  - **FIAQuery.html**: This file creates the UI interface with AJAX, JQuery, and Javascript for all queries from the database. All query selections have a description and allows user to choose between plot number, year, or year range with warnings for improper selections. Also allows user to download the queried data into a csv file for further use.
  - **FIAQuery.py**: This is the CGI file using pymysql that relays user selection and database accession for user request retrieval.
  - **How to run**: The .py file runs in the background. The .html file can be opened on a web browser for exploration. 
