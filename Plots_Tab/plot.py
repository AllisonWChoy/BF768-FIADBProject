#!/usr/bin/env python3

import cgi
import cgitb
from unicodedata import decimal, numeric
import pymysql
import json
from decimal import Decimal
from datetime import date

class DecimalEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return float(obj)
    return json.JSONEncoder.default(self, obj)

cgitb.enable()                      # return errors to browser
print("Content-type: text/html\n")  # start http return 
form = cgi.FieldStorage()           # retrieve form data, if any


def get_treeabd(): 
    connection = pymysql.connect(db="Group_F",
                                    user="Group_F",
                                    password="Group_F",
                                    host='bioed.bu.edu', 
                                    port=4253)
    cursor = connection.cursor()
    query = """
                select CONCAT('Plot_', PLOT), count(PLOT)
                from Tree
                join Location on Tree.ID = Location.LOCID
                group by PLOT
            """
    # Execute the mySQL query
    try:
        cursor.execute(query)
    except pymysql.Error as e:
        print(e)
    out = (("PLOT", "Count"), *cursor.fetchall())
    print(json.dumps(out))

def get_treeabdtable(): 
    connection = pymysql.connect(db="Group_F",
                                    user="Group_F",
                                    password="Group_F",
                                    host='bioed.bu.edu', 
                                    port=4253)
    cursor = connection.cursor()
    query = """
            select CONCAT('Plot_', PLOT), count(PLOT)
            from Tree
            join Location on Tree.ID = Location.LOCID
            group by PLOT
            """
    # Execute the mySQL query
    try:
        cursor.execute(query)
    except pymysql.Error as e:
        print(e)
    out = cursor.fetchall()
    print(json.dumps(out))

def get_treesize(): 
    connection = pymysql.connect(db="Group_F",
                                    user="Group_F",
                                    password="Group_F",
                                    host='bioed.bu.edu', 
                                    port=4253)
    cursor = connection.cursor()
    query = """
            select CONCAT(' ', DIA), count(*)
            from Tree 
            group by DIA
            """

    # Execute the mySQL query
    try:
        cursor.execute(query)
    except pymysql.Error as e:
        print(e)
    out = (("Diameter", "Count"), *cursor.fetchall())
    print(json.dumps(out))

def get_treesizetable(): 
    connection = pymysql.connect(db="Group_F",
                                    user="Group_F",
                                    password="Group_F",
                                    host='bioed.bu.edu', 
                                    port=4253)
    cursor = connection.cursor()
    query = """
            select DIA, count(*)
            from Tree 
            group by DIA
            """
    # Execute the mySQL query
    try:
        cursor.execute(query)
    except pymysql.Error as e:
        print(e)

    out = cursor.fetchall()
    print(json.dumps(out))

def get_sppabd(): 
    connection = pymysql.connect(db="Group_F",
                                    user="Group_F",
                                    password="Group_F",
                                    host='bioed.bu.edu', 
                                    port=4253)
    cursor = connection.cursor()
    query = """
            select CONCAT(GENUS, ' ', SPECIES) as Species_Name, count(*)
            from Tree 
            join Species using (SPCD)
            group by Species
            having count(*) > 50
            """

    # Execute the mySQL query
    try:
        cursor.execute(query)
    except pymysql.Error as e:
        print(e)
    out = (("Species","count"), *cursor.fetchall())
    print(json.dumps(out))

def get_spptable(): 
    connection = pymysql.connect(db="Group_F",
                                    user="Group_F",
                                    password="Group_F",
                                    host='bioed.bu.edu', 
                                    port=4253)
    cursor = connection.cursor()
    query = """
            select CONCAT(GENUS, ' ', SPECIES) as Species_Name, count(*)
            from Tree 
            join Species using (SPCD)
            group by Species
            order by count(*) DESC
            """

    # Execute the mySQL query
    try:
        cursor.execute(query)
    except pymysql.Error as e:
        print(e)
    out = cursor.fetchall()
    print(json.dumps(out))

def get_biomass():
    connection = pymysql.connect(db="Group_F",
                                    user="Group_F",
                                    password="Group_F",
                                    host='bioed.bu.edu', 
                                    port=4253)
    cursor = connection.cursor()
    query = """
                select sum(CARBON_BG), sum(CARBON_AG), INVYR, count(*) as tree_count
                from Tree 
                join Location on Tree.ID = Location.LOCID
                join Biomass on Tree.ID = Biomass.BIOID 
                group by INVYR 
                """
    # Execute the mySQL query
    try:
        cursor.execute(query)
    except pymysql.Error as e:
        print(e)
    ids = ["Year_IDs"]
    out = [["Total_CarbonBG", "Total_CarbonAG", "Year", "Tree_Population"], *cursor.fetchall()]
    for i in range(1, len(out)):
        ids.append(str(out[i][2]) + '_id')
    new_out = [(a, *b) for a, b in zip(ids, out)]
    print(json.dumps(new_out, cls=DecimalEncoder))

def get_biomasstable(): 
    connection = pymysql.connect(db="Group_F",
                                    user="Group_F",
                                    password="Group_F",
                                    host='bioed.bu.edu', 
                                    port=4253)
    cursor = connection.cursor()
    query = """
            select INVYR, sum(DRYBIO_BOLE), sum(DRYBIO_TOP), sum(DRYBIO_STUMP), sum(DRYBIO_SAPLING), sum(DRYBIO_WDLD_SPP), sum(DRYBIO_BG), sum(CARBON_AG), sum(CARBON_BG)
            from Tree
            join Location on Tree.ID = Location.LOCID 
            join Biomass on Tree.ID = Biomass.BIOID 
            group by INVYR
            """
    # Execute the mySQL query
    try:
        cursor.execute(query)
    except pymysql.Error as e:
        print(e)
    out = cursor.fetchall()
    print(json.dumps(out, cls=DecimalEncoder))

def get_growth():
    connection = pymysql.connect(db="Group_F",
                                    user="Group_F",
                                    password="Group_F",
                                    host='bioed.bu.edu', 
                                    port=4253)
    cursor = connection.cursor()
    query = """
            select INVYR, avg(DIA_BEGIN) as db, avg(DIA_MIDPT) as dm, avg(DIA_END) as de, avg(HT_BEGIN) as hb, avg(HT_MIDPT) as hm, avg(HT_END) as he
            from Tree
            join Location on Tree.ID = Location.LOCID 
            join Growth on Tree.ID = Growth.GROWID 
            group by INVYR 
            having db > 0 and dm > 0 and de > 0 and hb >0 and hm >0 and he > 0
            """
    # Execute the mySQL query
    try:
        cursor.execute(query)
    except pymysql.Error as e:
        print(e)
    out = (("Year", "Diameter_Begin", "Diameter_Midpoint", "Diameter_End", "Height_Begin", "Height_Midpoint", "Height_End"), *cursor.fetchall())
    print(json.dumps(out, cls=DecimalEncoder))
    
def get_growthtable():
    connection = pymysql.connect(db="Group_F",
                                    user="Group_F",
                                    password="Group_F",
                                    host='bioed.bu.edu', 
                                    port=4253)
    cursor = connection.cursor()
    query = """
            select INVYR, avg(DIA_BEGIN) as db, avg(DIA_MIDPT) as dm, avg(DIA_END) as de, avg(HT_BEGIN) as hb, avg(HT_MIDPT) as hm, avg(HT_END) as he
            from Tree
            join Location on Tree.ID = Location.LOCID 
            join Growth on Tree.ID = Growth.GROWID 
            group by INVYR 
            having db > 0 and dm > 0 and de > 0 and hb >0 and hm >0 and he > 0
            """
    # Execute the mySQL query
    try:
        cursor.execute(query)
    except pymysql.Error as e:
        print(e)
    out = cursor.fetchall()
    print(json.dumps(out, cls=DecimalEncoder))

def get_mort():
    connection = pymysql.connect(db="Group_F",
                                    user="Group_F",
                                    password="Group_F",
                                    host='bioed.bu.edu', 
                                    port=4253)
    cursor = connection.cursor()
    query = """
            select INVYR, AVG(MORTCFAL), count(case when AGENTCD = 10 then 1 end) as '10',
                                        count(case when AGENTCD = 20 then 1 end) as '20',
                                        count(case when AGENTCD = 30 then 1 end) as '30',
                                        count(case when AGENTCD = 40 then 1 end) as '40',
                                        count(case when AGENTCD = 50 then 1 end) as '50',
                                        count(case when AGENTCD = 60 then 1 end) as '60',
                                        count(case when AGENTCD = 70 then 1 end) as '70',
                                        count(case when AGENTCD = 80 then 1 end) as '80'
            from Tree
            join Location on Tree.ID = Location.LOCID 
            join Mortality on Tree.ID = Mortality.MORID
            join Growth on Tree.ID = Growth.GROWID
            group by INVYR
            having SUM(GROWCFAL) > 0
            """
    # Execute the mySQL query
    try:
        cursor.execute(query)
    except pymysql.Error as e:
        print(e)
    out = (("Year", "Avg_MORTCFAL", "AD_10", "AD_20", "AD_30","AD_40","AD_50","AD_60", "AD_70", "AD_80"), *cursor.fetchall())
    print(json.dumps(out, cls=DecimalEncoder))

def get_morttable():
    connection = pymysql.connect(db="Group_F",
                                    user="Group_F",
                                    password="Group_F",
                                    host='bioed.bu.edu', 
                                    port=4253)
    cursor = connection.cursor()
    query = """
            select INVYR, AVG(MORTCFAL), count(case when AGENTCD = 10 then 1 end) as '10',
                                        count(case when AGENTCD = 20 then 1 end) as '20',
                                        count(case when AGENTCD = 30 then 1 end) as '30',
                                        count(case when AGENTCD = 40 then 1 end) as '40',
                                        count(case when AGENTCD = 50 then 1 end) as '50',
                                        count(case when AGENTCD = 60 then 1 end) as '60',
                                        count(case when AGENTCD = 70 then 1 end) as '70',
                                        count(case when AGENTCD = 80 then 1 end) as '80'
            from Tree
            join Location on Tree.ID = Location.LOCID 
            join Mortality on Tree.ID = Mortality.MORID
            join Growth on Tree.ID = Growth.GROWID
            group by INVYR
            having SUM(GROWCFAL) > 0
            """
    # Execute the mySQL query
    try:
        cursor.execute(query)
    except pymysql.Error as e:
        print(e)
    out = cursor.fetchall()
    print(json.dumps(out, cls=DecimalEncoder))

def get_mortgrowth():
    connection = pymysql.connect(db="Group_F",
                                    user="Group_F",
                                    password="Group_F",
                                    host='bioed.bu.edu', 
                                    port=4253)
    cursor = connection.cursor()
    query = """
            select SUM(GROWCFAL), SUM(MORTCFAL), INVYR, COUNT(PLOT)
            from Tree
            join Location on Tree.ID = Location.LOCID 
            join Mortality on Tree.ID = Mortality.MORID
            join Growth on Tree.ID = Growth.GROWID
            group by INVYR
            having SUM(GROWCFAL) > 0
            """
    # Execute the mySQL query
    try:
        cursor.execute(query)
    except pymysql.Error as e:
        print(e)
    ids = []
    out =  cursor.fetchall()
    for i in range(len(out)):
        ids.append(str(out[i][2]) + '_id')
    new_out = [(a, *b) for a, b in zip(ids, out)]
    print(json.dumps(new_out, cls=DecimalEncoder))

def get_mortgrowthtable():
    connection = pymysql.connect(db="Group_F",
                                    user="Group_F",
                                    password="Group_F",
                                    host='bioed.bu.edu', 
                                    port=4253)
    cursor = connection.cursor()
    query = """
            select SUM(GROWCFAL), SUM(MORTCFAL), INVYR, COUNT(PLOT), count(case when AGENTCD = 10 then 1 end) as '10',
																	 count(case when AGENTCD = 20 then 1 end) as '20',
																	 count(case when AGENTCD = 30 then 1 end) as '30',
																	 count(case when AGENTCD = 40 then 1 end) as '40',
																	 count(case when AGENTCD = 50 then 1 end) as '50',
																	 count(case when AGENTCD = 60 then 1 end) as '60',
																	 count(case when AGENTCD = 70 then 1 end) as '70',
																	 count(case when AGENTCD = 80 then 1 end) as '80'
            from Tree
            join Location on Tree.ID = Location.LOCID 
            join Mortality on Tree.ID = Mortality.MORID
            join Growth on Tree.ID = Growth.GROWID
            group by INVYR
            having SUM(GROWCFAL) > 0
            """
    # Execute the mySQL query
    try:
        cursor.execute(query)
    except pymysql.Error as e:
        print(e)
    out = cursor.fetchall()
    print(json.dumps(out, cls=DecimalEncoder))


def main(): 
    #check if form data is returned
    if form:
        selector = form.getvalue("selector")
        if selector == "TreeAbundance": 
            get_treeabd()
        if selector == "TreeAbd_Table": 
            get_treeabdtable()
        if selector == "TreeSize": 
            get_treesize()
        if selector == "TreeSize_Table":
            get_treesizetable()
        if selector == "SpeciesAbundance":
            get_sppabd()
        if selector == "SPP_Table": 
            get_spptable()
        if selector == "Biomass":
            get_biomass()
        if selector == "Biomass_Table":
            get_biomasstable()
        if selector == "Growth":
            get_growth()
        if selector == "Growth_Table":
            get_growthtable()
        if selector == "Mort": 
            get_mort() 
        if selector == "Mort_Table": 
            get_morttable()
        if selector == "Mort_vs_Growth":
            get_mortgrowth()
        if selector == "Mort_vs_Growth_Table":
            get_mortgrowthtable()
    else: 
        print("Content-type: text/html\n")  # start http return 

main()
