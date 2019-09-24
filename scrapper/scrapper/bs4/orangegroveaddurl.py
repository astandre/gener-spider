from builtins import range

from bs4 import BeautifulSoup as BS
import requests
import mysql.connector
import datetime
import math

from sqlalchemy import false

domain = 'https://florida.theorangegrove.org/'

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="oerintegrationdb"
    )

myac=mydb.cursor()

#------------------- TO get Row from DB ---------------------
'''
myac.execute('select * from triplesOG where predicate = "hasRaw"')
rows = myac.fetchall()

for r in rows:
    metadata_tb = BS(r[3],'html.parser')
    for p in metadata_tb.find_all('p'):
        print(p.get_text())
    exit()
'''

subjRepository = 'Rep1'

#Insert Repository
'''
sql = "INSERT INTO triplesOG(subject, predicate, object, time_date) VALUES(%s,%s,%s,%s)"
values = (subjRepository,'hasName','The Orange Grove',datetime.datetime.now())
myac.execute(sql,values)
mydb.commit()
sql = "INSERT INTO triplesOG(subject, predicate, object, time_date) VALUES(%s,%s,%s,%s)"
values = (subjRepository,'hasUrl','https://florida.theorangegrove.org/og/hierarchy.do?topic=16fd73ce-64e0-6992-b704-d73a2763d9e7&page=1',datetime.datetime.now())
myac.execute(sql,values)
mydb.commit()
'''

#Find list of subjects pages
subjectRow = [
    ['og/hierarchy.do?topic=612a768f-4979-aa54-68ec-09affba54d09','K-12 Open Textbooks',90],
    ['og/hierarchy.do?topic=acedc05e-0d93-f56d-0034-a70d3546f5e0','OGT+ Print on Demand Books',101],
    ['og/hierarchy.do?topic=e17ea474-21cd-d407-9165-bbbc165884b4','WebAssign Supported Textbooks ',4],
    ['og/hierarchy.do?topic=0fd16144-0047-7064-ab78-1169c0cd3683','InTech',4799],
    ['og/hierarchy.do?topic=94c81979-5a4a-0e4c-f678-458e8d4aa9b8','Open Course Library',39],
    ['og/hierarchy.do?topic=b1530c9e-c5d9-cf13-e5f9-2a6391a2b163','Saylor Fundation',4],
]
query = 'select * from triplesOG where predicate = "hasRaw" and process = 0 and subject="category4"'
myac.execute(query)
rawsInTech = myac.fetchall()

def confirmTitle(title):
    for q in rawsInTech:
        soup = BS(q[3],'html.parser')
        div_title = soup.find('div', {'class': 'displayNodeFull'})
        titleFound = div_title.find('p').get_text().strip()
        if titleFound ==title:
            idRow = q[0]
            rawsInTech.remove(q)
            return [True,idRow]
    return [False]

for x in subjectRow:
    #calculando numero de iteraciones
    numIterate = math.ceil(x[2] / 10)
    subjCategory = '{0}{1}'.format('category', list(subjectRow).index(x) + 1)

    query = f'select * from triplesOG where predicate = "hasRaw" and process = 0 and subject="{subjCategory}"'
    myac.execute(query)
    rawsOfCategory = myac.fetchall()
    for i in range(numIterate):
        # download page of TB
        web_og = requests.get('{0}{1}&page={2}'.format(domain, x[0],i+1))
        raw_og = web_og.content
        soup_og = BS(raw_og, 'html.parser')
        box_results = soup_og.find('div',{'id':'searchresults'})
        titles_tb = box_results.find_all('a',{'class':'titlelink'})
        for a in titles_tb:
            url_tb = a.get('href')
            name_tb = a.get_text().strip()
            url_tb = '{0}{1}'.format(domain, url_tb[1:])
            print(f'{name_tb} - {url_tb}')
            if x[1] == 'InTech':
                rta = confirmTitle(name_tb)
                if rta[0]:
                    sql = f"UPDATE triplesOG SET url_native = '{url_tb}'  WHERE id = {rta[1]}"
                    myac.execute(sql)
                    mydb.commit()
                else:
                    # Descargando RAW TB
                    web_tb = requests.get('{0}{1}'.format(domain, url_tb[1:]))
                    raw_tb = web_tb.content
                    soup_tb = BS(raw_tb, 'html.parser')
                    raw_data = soup_tb.find('div', {'class': 'area'})

                    # Savig RAW
                    sql = "INSERT INTO triplesOG(subject, predicate, object, time_date, process) VALUES(%s,%s,%s,%s,%s)"
                    values = (subjCategory, 'hasRaw', str(raw_data), datetime.datetime.now(), False)
                    myac.execute(sql, values)
                    mydb.commit()
            else:
                #Actuaizando rows, add link
                for r in rawsOfCategory:
                    sql = f"UPDATE triplesOG SET url_native = '{url_tb}'  WHERE id = {r[0]}"
                    myac.execute(sql)
                    mydb.commit()
                    rawsOfCategory.remove(r)
                    break
        print('\t\tIterate {0} / {1}'.format(i+1,numIterate))
    break
    print('END CAT')