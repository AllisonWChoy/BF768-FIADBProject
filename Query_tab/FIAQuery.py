#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
import pymysql
import json

# Allows us to see errors on browser
cgitb.enable()

# Required as first part of html output
print("Content-type: text/html\n")

form = cgi.FieldStorage(keep_blank_values=True)

if form:
    selector = form.getvalue("selector", '')
    year1 = form.getvalue("year1", '') 
    year2 = form.getvalue("year2", '') 
    plot = form.getvalue("plot", '')
    plotyear = form.getvalue("plotyear", '')
    category = form.getvalue("category", '')
    subcategory = form.getvalue("subcategory", '')
    
    #Connect to the database.
    connection = pymysql.connect(db='Group_F',
                                user='Group_F',
                                password='Group_F',
                                host='bioed.bu.edu', 
                                port=4253)

    cursor = connection.cursor()
    
    if (selector == 'year1'):
        query = """SELECT DISTINCT INVYR 
        FROM Location;"""
        
        #execute the query
        cursor.execute(query)
        results=cursor.fetchall() 
        print(json.dumps(results))
        
    elif (selector == 'year2'):
        if (year1 != '- All -'):
            query = """SELECT DISTINCT INVYR FROM Location
            WHERE INVYR > %s;"""
            
            #execute the query
            cursor.execute(query, (year1))
            results=cursor.fetchall() 
            print(json.dumps(results))

        else:
            query = """SELECT DISTINCT INVYR FROM Location;"""
            
            #execute the query
            cursor.execute(query)
            results=cursor.fetchall() 
            print(json.dumps(results))

    elif (selector == 'plot'):
        # if year1 == '':
        query = """SELECT DISTINCT PLOT FROM Location ORDER BY PLOT;"""

        #execute the query
        cursor.execute(query)
        results=cursor.fetchall() 
        print(json.dumps(results))

    elif (selector == 'query_table'):
        if plotyear == 'plot':
            if category == 'Biomass':
                if subcategory == 'Carbon AG/BG':
                    query = """SELECT INVYR, COUNTYCD, PLOT, SUM(CARBON_AG) as AG, SUM(CARBON_BG) as BG
                            from Location l join Biomass b on LOCID = BIOID
                            WHERE PLOT = %s
                            group by INVYR, COUNTYCD, PLOT
                            ORDER BY INVYR, COUNTYCD, PLOT;"""

                    try:
                        cursor.execute(query, [plot])
                    except pymysql.Error as e:
                        print(e)

                    results = cursor.fetchall()
                    rDim = [["Year", "County", "Plot", "AG in pounds", "BG in pounds"]]

                    for result in results:
                        row = []
                        for col in result:
                            row.append(str(col))
                        rDim.append(row)

                    print(json.dumps(rDim))

                elif subcategory == 'Dry Biomass':
                    query = """SELECT INVYR, PLOT, SUM(DRYBIO_BOLE) as BOLE, SUM(DRYBIO_TOP) as TOP, 
                            SUM(DRYBIO_STUMP) AS STUMP, SUM(DRYBIO_SAPLING) as SAPLING, 
                            SUM(DRYBIO_WDLD_SPP) AS Wdld_Spp, SUM(DRYBIO_BG) as BG
                            from Location l JOIN Biomass b on b.BIOID = l.LOCID 
                            WHERE PLOT = %s
                            GROUP BY INVYR, PLOT 
                            ORDER BY INVYR, PLOT;"""

                    try:
                        cursor.execute(query, [plot])
                    except pymysql.Error as e:
                        print(e)

                    results = cursor.fetchall()
                    rDim = [["Year", "Plot", "Bole in pounds", "Top in pounds", "Stump in pounds", "Sapling in pounds", "Woodland Species in pounds", "BG in pounds"]]

                    for result in results:
                        row = []
                        for col in result:
                            row.append(str(col))
                        rDim.append(row)

                    print(json.dumps(rDim))

            elif category == 'Growth':
                if subcategory == 'Average Growth':
                    query = """SELECT DISTINCT INVYR, PLOT, AVG(GROWCFAL) as CF_Growth, AVG(DIA_BEGIN) as DIA_start, 
                            AVG(DIA_MIDPT) as DIA_mid, AVG(DIA_END) as DIA_end, AVG(ANN_DIA_GROWTH) as Ann_DIA_Grwth, 
                            AVG(HT_BEGIN) as HT_start, AVG(HT_MIDPT) as HT_mid, AVG(HT_END) as HT_end, AVG(ANN_HT_GROWTH) as Ann_HT_Grwth
                            from Location l JOIN Growth g on GROWID = LOCID 
                            WHERE PLOT = %s
                            GROUP BY INVYR, PLOT;"""

                    try:
                        cursor.execute(query, [plot])
                    except pymysql.Error as e:
                        print(e)

                    results = cursor.fetchall()
                    rDim = [["Year", "Plot", "Growth (Cubic Feet)", "Diameter (begin) (Inch)", "Diameter (mid) (Inch)", "Diameter (end) (Inch)", "Annual Diameter Growth (Inch/Year)", 
                    "Height (begin) (Foot)", "Height (mid) (Foot)", "Height (end) (Foot)", "Annual Height Growth (Feet/Year)"]]

                    for result in results:
                        row = []
                        for col in result:
                            row.append(str(col))
                        rDim.append(row)

                    print(json.dumps(rDim))

            elif category == 'Species':
                query = """SELECT INVYR, PLOT, SPCD, COMMON_NAME, COUNT(SPCD) as Species_Sum
                        from Location l2 join Tree t2 on t2.ID = l2.LOCID join Species s using (SPCD)
                        WHERE PLOT = %s
                        group by INVYR, PLOT, SPCD
                        ORDER BY INVYR, PLOT, SPCD;"""

                try:
                    cursor.execute(query, [plot])
                except pymysql.Error as e:
                    print(e)

                results = cursor.fetchall()
                rDim = [["Year", "Plot", "Species Code", "Species Name", "Species Count"]]

                for result in results:
                    row = []
                    for col in result:
                        row.append(str(col))
                    rDim.append(row)

                print(json.dumps(rDim))

            elif category == 'Tree Dimension':
                query = """SELECT INVYR, COUNTYCD, PLOT, AVG(DIA) as mean_DBH
                        FROM Location l  JOIN Tree t on t.ID = l.LOCID 
                        WHERE PLOT = %s
                        GROUP BY INVYR, COUNTYCD, PLOT;"""

                try:
                    cursor.execute(query, [plot])
                except pymysql.Error as e:
                    print(e)

                results = cursor.fetchall()
                rDim = [["Year", "County", "Plot", "mean DBH in Inches"]]

                for result in results:
                    row = []
                    for col in result:
                        row.append(str(col))
                    rDim.append(row)

                print(json.dumps(rDim))

            elif category == 'Trees per Acre':
                if subcategory == 'Total TPA':
                    query = """SELECT INVYR, PLOT, AVG(NULLIF (TPA_UNADJ,0)) as TPA, AVG(NULLIF (TPAMORT_UNADJ, 0)) as TPA_MORT, AVG(NULLIF (TPAREMV_UNADJ, 0)) as TPA_REMV, AVG(NULLIF (TPAGROW_UNADJ, 0)) as TPA_GROW
                            from Tree t join Location l on t.ID = l.LOCID 
                            WHERE PLOT = %s
                            GROUP BY INVYR, PLOT
                            ORDER BY INVYR, PLOT;"""
                    
                    try:
                        cursor.execute(query, [plot])
                    except pymysql.Error as e:
                        print(e)

                    results = cursor.fetchall()
                    rDim = [["Year", "Plot", "TPA Unadjusted", "TPA Mortality", "TPA Removed", "TPA Growth"]]

                    for result in results:
                        row = []
                        for col in result:
                            row.append(str(col))
                        rDim.append(row)

                    print(json.dumps(rDim))
                    
                elif subcategory == 'TPA by Species':
                    query = """SELECT INVYR, PLOT, AVG(NULLIF (TPA_UNADJ,0)) as TPA, AVG(NULLIF (TPAMORT_UNADJ, 0)) as TPA_MORT, AVG(NULLIF (TPAREMV_UNADJ,0)) as TPA_REMV, AVG(NULLIF (TPAGROW_UNADJ, 0)) as TPA_GROW, COMMON_NAME
                            from Tree t join Location l on t.ID = l.LOCID JOIN Species s using (SPCD)
                            WHERE PLOT = %s
                            GROUP BY INVYR, PLOT, SPCD
                            HAVING TPA > 0 
                            ORDER BY INVYR, PLOT;"""

                    try:
                        cursor.execute(query, [plot])
                    except pymysql.Error as e:
                        print(e)

                    results = cursor.fetchall()
                    rDim = [["Year", "Plot", "TPA Unadjusted", "TPA Mortality", "TPA Removed", "TPA Growth", "Species Name"]]

                    for result in results:
                        row = []
                        for col in result:
                            row.append(str(col))
                        rDim.append(row)

                    print(json.dumps(rDim))

            elif category == "Trees Per Plot":
                query = """SELECT INVYR, COUNTYCD, PLOT, COUNT(TREEID) as count
                        FROM Location L  
                        WHERE PLOT = %s
                        GROUP BY INVYR, COUNTYCD, PLOT;"""

                try:
                    cursor.execute(query, [plot])
                except pymysql.Error as e:
                    print(e)

                results = cursor.fetchall()
                rDim = [["Year", "County", "Plot", "Tree Counts"]]

                for result in results:
                    row = []
                    for col in result:
                        row.append(str(col))
                    rDim.append(row)

                print(json.dumps(rDim))

        if plotyear == 'year':
            if category == 'Biomass':
                if subcategory == 'Carbon AG/BG':
                    query = """SELECT INVYR, COUNTYCD, PLOT, SUM(CARBON_AG) as AG, SUM(CARBON_BG) as BG
                            from Location l join Biomass b on LOCID = BIOID
                            WHERE INVYR = %s
                            group by INVYR, COUNTYCD, PLOT
                            ORDER BY INVYR, COUNTYCD, PLOT;"""

                    try:
                        cursor.execute(query, [year1])
                    except pymysql.Error as e:
                        print(e)

                    results = cursor.fetchall()
                    rDim = [["Year", "County", "Plot", "AG in pounds", "BG in pounds"]]

                    for result in results:
                        row = []
                        for col in result:
                            row.append(str(col))
                        rDim.append(row)

                    print(json.dumps(rDim))

                elif subcategory == 'Dry Biomass':
                    query = """SELECT INVYR, PLOT, SUM(DRYBIO_BOLE) as BOLE, SUM(DRYBIO_TOP) as TOP, 
                            SUM(DRYBIO_STUMP) AS STUMP, SUM(DRYBIO_SAPLING) as SAPLING, 
                            SUM(DRYBIO_WDLD_SPP) AS Wdld_Spp, SUM(DRYBIO_BG) as BG
                            from Location l JOIN Biomass b on b.BIOID = l.LOCID 
                            WHERE INVYR = %s
                            GROUP BY INVYR, PLOT 
                            ORDER BY INVYR, PLOT;"""

                    try:
                        cursor.execute(query, [year1])
                    except pymysql.Error as e:
                        print(e)

                    results = cursor.fetchall()
                    rDim = [["Year", "Plot", "Bole in pounds", "Top in pounds", "Stump in pounds", "Sapling in pounds", "Woodland Species in pounds", "BG in pounds"]]

                    for result in results:
                        row = []
                        for col in result:
                            row.append(str(col))
                        rDim.append(row)

                    print(json.dumps(rDim))

            elif category == 'Growth':
                if subcategory == 'Average Growth':
                    query = """SELECT DISTINCT INVYR, PLOT, AVG(GROWCFAL) as CF_Growth, AVG(DIA_BEGIN) as DIA_start, 
                            AVG(DIA_MIDPT) as DIA_mid, AVG(DIA_END) as DIA_end, AVG(ANN_DIA_GROWTH) as Ann_DIA_Grwth, 
                            AVG(HT_BEGIN) as HT_start, AVG(HT_MIDPT) as HT_mid, AVG(HT_END) as HT_end, AVG(ANN_HT_GROWTH) as Ann_HT_Grwth
                            from Location l JOIN Growth g on GROWID = LOCID 
                            WHERE INVYR = %s
                            GROUP BY INVYR, PLOT;"""

                    try:
                        cursor.execute(query, [year1])
                    except pymysql.Error as e:
                        print(e)

                    results = cursor.fetchall()
                    rDim = [["Year", "Plot", "Growth (Cubic Feet)", "Diameter (begin) (Inch)", "Diameter (mid) (Inch)", "Diameter (end) (Inch)", "Annual Diameter Growth (Inch/Year)", 
                    "Height (begin) (Foot)", "Height (mid) (Foot)", "Height (end) (Foot)", "Annual Height Growth (Feet/Year)"]]

                    for result in results:
                        row = []
                        for col in result:
                            row.append(str(col))
                        rDim.append(row)

                    print(json.dumps(rDim))

            elif category == 'Species':
                query = """SELECT INVYR, PLOT, SPCD, COMMON_NAME, COUNT(SPCD) as Species_Sum
                        from Location l2 join Tree t2 on t2.ID = l2.LOCID join Species s using (SPCD)
                        WHERE INVYR = %s
                        group by INVYR, PLOT, SPCD
                        ORDER BY INVYR, PLOT, SPCD;"""

                try:
                    cursor.execute(query, [year1])
                except pymysql.Error as e:
                    print(e)

                results = cursor.fetchall()
                rDim = [["Year", "Plot", "Species Code", "Species Name", "Species Count"]]

                for result in results:
                    row = []
                    for col in result:
                        row.append(str(col))
                    rDim.append(row)

                print(json.dumps(rDim))

            elif category == 'Tree Dimension':
                query = """SELECT INVYR, COUNTYCD, PLOT, AVG(DIA) as mean_DBH
                        FROM Location l  JOIN Tree t on t.ID = l.LOCID 
                        WHERE INVYR = %s
                        GROUP BY INVYR, COUNTYCD, PLOT;"""

                try:
                    cursor.execute(query, [year1])
                except pymysql.Error as e:
                    print(e)

                results = cursor.fetchall()
                rDim = [["Year", "County", "Plot", "mean DBH in Inches"]]

                for result in results:
                    row = []
                    for col in result:
                        row.append(str(col))
                    rDim.append(row)

                print(json.dumps(rDim))

            elif category == 'Trees per Acre':
                if subcategory == 'Total TPA':
                    query = """SELECT INVYR, PLOT, AVG(NULLIF (TPA_UNADJ,0)) as TPA, AVG(NULLIF (TPAMORT_UNADJ, 0)) as TPA_MORT, AVG(NULLIF (TPAREMV_UNADJ, 0)) as TPA_REMV, AVG(NULLIF (TPAGROW_UNADJ, 0)) as TPA_GROW
                            from Tree t join Location l on t.ID = l.LOCID 
                            WHERE INVYR = %s
                            GROUP BY INVYR, PLOT
                            ORDER BY INVYR, PLOT;"""
                    
                    try:
                        cursor.execute(query, [year1])
                    except pymysql.Error as e:
                        print(e)

                    results = cursor.fetchall()
                    rDim = [["Year", "Plot", "TPA Unadjusted", "TPA Mortality", "TPA Removed", "TPA Growth"]]

                    for result in results:
                        row = []
                        for col in result:
                            row.append(str(col))
                        rDim.append(row)

                    print(json.dumps(rDim))
                    
                elif subcategory == 'TPA by Species':
                    query = """SELECT INVYR, PLOT, AVG(NULLIF (TPA_UNADJ,0)) as TPA, AVG(NULLIF (TPAMORT_UNADJ, 0)) as TPA_MORT, AVG(NULLIF (TPAREMV_UNADJ,0)) as TPA_REMV, AVG(NULLIF (TPAGROW_UNADJ, 0)) as TPA_GROW, COMMON_NAME
                            from Tree t join Location l on t.ID = l.LOCID JOIN Species s using (SPCD)
                            WHERE INVYR = %s
                            GROUP BY INVYR, PLOT, SPCD
                            HAVING TPA > 0 
                            ORDER BY INVYR, PLOT;"""

                    try:
                        cursor.execute(query, [year1])
                    except pymysql.Error as e:
                        print(e)

                    results = cursor.fetchall()
                    rDim = [["Year", "Plot", "TPA Unadjusted", "TPA Mortality", "TPA Removed", "TPA Growth", "Species Name"]]

                    for result in results:
                        row = []
                        for col in result:
                            row.append(str(col))
                        rDim.append(row)

                    print(json.dumps(rDim))

            elif category == "Trees Per Plot":
                query = """SELECT INVYR, COUNTYCD, PLOT, COUNT(TREEID) as count
                        FROM Location L  
                        WHERE INVYR = %s
                        GROUP BY INVYR, COUNTYCD, PLOT;"""

                try:
                    cursor.execute(query, [year1])
                except pymysql.Error as e:
                    print(e)

                results = cursor.fetchall()
                rDim = [["Year", "County", "Plot", "Tree Counts"]]

                for result in results:
                    row = []
                    for col in result:
                        row.append(str(col))
                    rDim.append(row)

                print(json.dumps(rDim))

        elif plotyear == 'year range':
            if category == 'Biomass':
                if subcategory == 'Carbon AG/BG':
                    query = """SELECT INVYR, COUNTYCD, PLOT, SUM(CARBON_AG) as AG, SUM(CARBON_BG) as BG
                            from Location l join Biomass b on LOCID = BIOID
                            WHERE INVYR BETWEEN %s AND %s
                            group by INVYR, COUNTYCD, PLOT
                            ORDER BY INVYR, COUNTYCD, PLOT;"""

                    try:
                        cursor.execute(query, [year1, year2])
                    except pymysql.Error as e:
                        print(e)

                    results = cursor.fetchall()
                    rDim = [["Year", "County", "Plot", "AG in pounds", "BG in pounds"]]

                    for result in results:
                        row = []
                        for col in result:
                            row.append(str(col))
                        rDim.append(row)

                    print(json.dumps(rDim))

                elif subcategory == 'Dry Biomass':
                    query = """SELECT INVYR, PLOT, SUM(DRYBIO_BOLE) as BOLE, SUM(DRYBIO_TOP) as TOP, 
                            SUM(DRYBIO_STUMP) AS STUMP, SUM(DRYBIO_SAPLING) as SAPLING, 
                            SUM(DRYBIO_WDLD_SPP) AS Wdld_Spp, SUM(DRYBIO_BG) as BG
                            from Location l JOIN Biomass b on b.BIOID = l.LOCID 
                            WHERE INVYR BETWEEN %s AND %s
                            GROUP BY INVYR, PLOT 
                            ORDER BY INVYR, PLOT;"""

                    try:
                        cursor.execute(query, [year1, year2])
                    except pymysql.Error as e:
                        print(e)

                    results = cursor.fetchall()
                    rDim = [["Year", "Plot", "Bole in pounds", "Top in pounds", "Stump in pounds", "Sapling in pounds", "Woodland Species in pounds", "BG in pounds"]]

                    for result in results:
                        row = []
                        for col in result:
                            row.append(str(col))
                        rDim.append(row)

                    print(json.dumps(rDim))

            elif category == 'Growth':
                if subcategory == 'Average Growth':
                    query = """SELECT DISTINCT INVYR, PLOT, AVG(GROWCFAL) as CF_Growth, AVG(DIA_BEGIN) as DIA_start, 
                            AVG(DIA_MIDPT) as DIA_mid, AVG(DIA_END) as DIA_end, AVG(ANN_DIA_GROWTH) as Ann_DIA_Grwth, 
                            AVG(HT_BEGIN) as HT_start, AVG(HT_MIDPT) as HT_mid, AVG(HT_END) as HT_end, AVG(ANN_HT_GROWTH) as Ann_HT_Grwth
                            from Location l JOIN Growth g on GROWID = LOCID 
                            WHERE INVYR BETWEEN %s AND %s
                            GROUP BY INVYR, PLOT;"""

                    try:
                        cursor.execute(query, [year1, year2])
                    except pymysql.Error as e:
                        print(e)

                    results = cursor.fetchall()
                    rDim = [["Year", "Plot", "Growth (Cubic Feet)", "Diameter (begin) (Inch)", "Diameter (mid) (Inch)", "Diameter (end) (Inch)", "Annual Diameter Growth (Inch/Year)", 
                    "Height (begin) (Foot)", "Height (mid) (Foot)", "Height (end) (Foot)", "Annual Height Growth (Feet/Year)"]]

                    for result in results:
                        row = []
                        for col in result:
                            row.append(str(col))
                        rDim.append(row)

                    print(json.dumps(rDim))

            elif category == 'Species':
                query = """SELECT INVYR, PLOT, SPCD, COMMON_NAME, COUNT(SPCD) as Species_Sum
                        from Location l2 join Tree t2 on t2.ID = l2.LOCID join Species s using (SPCD)
                        WHERE INVYR BETWEEN %s AND %s
                        group by INVYR, PLOT, SPCD
                        ORDER BY INVYR, PLOT, SPCD;"""

                try:
                    cursor.execute(query, [year1, year2])
                except pymysql.Error as e:
                    print(e)

                results = cursor.fetchall()
                rDim = [["Year", "Plot", "Species Code", "Species Name", "Species Count"]]

                for result in results:
                    row = []
                    for col in result:
                        row.append(str(col))
                    rDim.append(row)

                print(json.dumps(rDim))

            elif category == 'Tree Dimension':
                query = """SELECT INVYR, COUNTYCD, PLOT, AVG(DIA) as mean_DBH
                        FROM Location l  JOIN Tree t on t.ID = l.LOCID 
                        WHERE INVYR BETWEEN %s AND %s
                        GROUP BY INVYR, COUNTYCD, PLOT;"""

                try:
                    cursor.execute(query, [year1, year2])
                except pymysql.Error as e:
                    print(e)

                results = cursor.fetchall()
                rDim = [["Year", "County", "Plot", "mean DBH in Inches"]]

                for result in results:
                    row = []
                    for col in result:
                        row.append(str(col))
                    rDim.append(row)

                print(json.dumps(rDim))

            elif category == 'Trees per Acre':
                if subcategory == 'Total TPA':
                    query = """SELECT INVYR, PLOT, AVG(NULLIF (TPA_UNADJ,0)) as TPA, AVG(NULLIF (TPAMORT_UNADJ, 0)) as TPA_MORT, AVG(NULLIF (TPAREMV_UNADJ, 0)) as TPA_REMV, AVG(NULLIF (TPAGROW_UNADJ, 0)) as TPA_GROW
                            from Tree t join Location l on t.ID = l.LOCID 
                            WHERE INVYR BETWEEN %s AND %s
                            GROUP BY INVYR, PLOT
                            ORDER BY INVYR, PLOT;"""
                    
                    try:
                        cursor.execute(query, [year1, year2])
                    except pymysql.Error as e:
                        print(e)

                    results = cursor.fetchall()
                    rDim = [["Year", "Plot", "TPA Unadjusted", "TPA Mortality", "TPA Removed", "TPA Growth"]]

                    for result in results:
                        row = []
                        for col in result:
                            row.append(str(col))
                        rDim.append(row)

                    print(json.dumps(rDim))
                    
                elif subcategory == 'TPA by Species':
                    query = """SELECT INVYR, PLOT, AVG(NULLIF (TPA_UNADJ,0)) as TPA, AVG(NULLIF (TPAMORT_UNADJ, 0)) as TPA_MORT, AVG(NULLIF (TPAREMV_UNADJ,0)) as TPA_REMV, AVG(NULLIF (TPAGROW_UNADJ, 0)) as TPA_GROW, COMMON_NAME
                            from Tree t join Location l on t.ID = l.LOCID JOIN Species s using (SPCD)
                            WHERE INVYR BETWEEN %s AND %s
                            GROUP BY INVYR, PLOT, SPCD
                            HAVING TPA > 0 
                            ORDER BY INVYR, PLOT;"""

                    try:
                        cursor.execute(query, [year1, year2])
                    except pymysql.Error as e:
                        print(e)

                    results = cursor.fetchall()
                    rDim = [["Year", "Plot", "TPA Unadjusted", "TPA Mortality", "TPA Removed", "TPA Growth", "Species Name"]]

                    for result in results:
                        row = []
                        for col in result:
                            row.append(str(col))
                        rDim.append(row)

                    print(json.dumps(rDim))

            elif category == "Trees Per Plot":
                query = """SELECT INVYR, COUNTYCD, PLOT, COUNT(TREEID) as count
                        FROM Location L  
                        WHERE INVYR BETWEEN %s AND %s
                        GROUP BY INVYR, COUNTYCD, PLOT;"""

                try:
                    cursor.execute(query, [year1, year2])
                except pymysql.Error as e:
                    print(e)

                results = cursor.fetchall()
                rDim = [["Year", "County", "Plot", "Tree Counts"]]

                for result in results:
                    row = []
                    for col in result:
                        row.append(str(col))
                    rDim.append(row)

                print(json.dumps(rDim))
        else:
            if category == 'Growth':
                if subcategory == 'Annual Growth':
                    query = """SELECT INVYR, SUM(GROWCFAL) as CF_Growth, SUM(ANN_DIA_GROWTH) as Ann_DIA_Grwth, SUM(ANN_HT_GROWTH) as Ann_HT_Grwth
                            from Location l JOIN Growth g on g.GROWID = l.LOCID
                            GROUP BY INVYR;"""

                    try:
                        cursor.execute(query)
                    except pymysql.Error as e:
                        print(e)

                    results = cursor.fetchall()
                    rDim = [["Year", "Growth (Cubic Feet)", "Annual Diameter Growth (Inch/Year)", "Annual Height Growth (Feet/Year)"]]

                    for result in results:
                        row = []
                        for col in result:
                            row.append(str(col))
                        rDim.append(row)

                    print(json.dumps(rDim))

            elif category == 'Mortality':
                if subcategory == 'Mortality Code Counts':
                    query = """SELECT INVYR, AGENTCD, COUNT(*) as Mort_Code_count
                            from Location l join Mortality m on m.MORID = l.LOCID 
                            GROUP BY INVYR, AGENTCD
                            HAVING AGENTCD > 0
                            ORDER BY INVYR;"""

                    try:
                        cursor.execute(query)
                    except pymysql.Error as e:
                        print(e)

                    results = cursor.fetchall()
                    rDim = [["Year", "Agent Code", "Mortality Code Counts"]]

                    for result in results:
                        row = []
                        for col in result:
                            row.append(str(col))
                        rDim.append(row)

                    print(json.dumps(rDim))
                
                elif subcategory == 'Damage Code Counts':
                    query = """SELECT INVYR, DECAYCD, COUNT(*) as Dam_Code_count
                            from Location l join Damage d on d.DAMID = l.LOCID 
                            GROUP BY INVYR, DECAYCD
                            HAVING DECAYCD > 0 
                            ORDER BY INVYR;"""

                    try:
                        cursor.execute(query)
                    except pymysql.Error as e:
                        print(e)

                    results = cursor.fetchall()
                    rDim = [["Year", "Decay Code", "Decay Code Counts"]]

                    for result in results:
                        row = []
                        for col in result:
                            row.append(str(col))
                        rDim.append(row)

                    print(json.dumps(rDim))

    cursor.close()
    connection.close()
else:
    print('Please complete the form.')