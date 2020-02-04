from bs4 import BeautifulSoup as BS
import requests
import mysql.connector
import datetime

domain = 'https://www.skillscommons.org/'


mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="oerintegrationdb"
    )

myac=mydb.cursor()




subjRepository = 'Rep1'

#Insert Repository
'''
sql = "INSERT INTO triplesSC(subject, predicate, object, time_date) VALUES(%s,%s,%s,%s)"
values = (subjRepository,'hasName','Open Textbook Library',datetime.datetime.now())
myac.execute(sql,values)
mydb.commit()
sql = "INSERT INTO triplesSC(subject, predicate, object, time_date) VALUES(%s,%s,%s,%s)"
values = (subjRepository,'hasUrl','https://www.skillscommons.org/discover?filtertype=type&filter_relational_operator=equals&filter=Open+Textbook',datetime.datetime.now())
myac.execute(sql,values)
mydb.commit()

sql = "INSERT INTO triplesSC(subject, predicate, object, time_date) VALUES(%s,%s,%s,%s)"
values = (subjRepository,'hasSubject','OC',datetime.datetime.now())
myac.execute(sql,values)
mydb.commit()
sql = "INSERT INTO triplesSC(subject, predicate, object, time_date) VALUES(%s,%s,%s,%s)"
values = ('OC','hasName','Online Course',datetime.datetime.now())
myac.execute(sql,values)
mydb.commit()
'''
query = f"select * from oerintegrationdb.triplesSC where subject='TB' and predicate = 'hasRaw';"
myac.execute(query)
rawsOfCategory = myac.fetchall()

url_of_tb = "discover?filtertype=type&filter_relational_operator=equals&filter=Open+Textbook"
while(1):
    # download page
    websc = requests.get('{0}{1}'.format(domain, url_of_tb))
    rawsc = websc.content
    soupsc = BS(rawsc, 'html.parser')

    #getting titles of texbooks
    domTitles = soupsc.find('ul',{'class':'medium-results'}).find_all('li')
    for tb in domTitles:
        nameTB = tb.find('a').get_text()
        linkTB = tb.find('a').get('href')
        linkTB = '{0}{1}'.format(domain,linkTB[1:])
        print(nameTB)
        #print(nameTB, linkTB)

        #getting Raw of TextBook
        '''webtb = requests.get('{0}{1}'.format(domain,linkTB[1:]))
        rawtb = webtb.content
        soup_tb = BS(rawtb,'html.parser')
        dataRaw = soup_tb.find('div',{'class':'item-view'}).find('div',{'class':'col-sm-8'})
        '''
        #Save Raw
        '''
        sql = "INSERT INTO triplesSC(subject, predicate, object, time_date, process) VALUES(%s,%s,%s,%s,%s)"
        values = ('OC', 'hasRaw', str(dataRaw), datetime.datetime.now(),False)
        myac.execute(sql, values)
        mydb.commit()
        '''
        #Actuaizando rows, add link
        for r in rawsOfCategory:
            sql = f"UPDATE triplesSC SET url_native = '{linkTB}'  WHERE id = {r[0]}"
            myac.execute(sql)
            mydb.commit()
            rawsOfCategory.remove(r)
            break

    #pagination
    pagDom = soupsc.find('div',{'class':'paging'}).find('ul',{'class':'pagination'}).find_all('li')
    last_li = pagDom[len(pagDom)-1]
    last_li = last_li.find('a')
    #Check URL to redirect new page, to more TB
    print(last_li.get_text())
    if last_li.get_text() == 'Next Page':
        url_of_tb = last_li.get('href')
        print('NEW URL',url_of_tb)
    else:
        break