from bs4 import BeautifulSoup as BS
import requests
import mysql.connector
import datetime

domain = 'https://open.umn.edu/'

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="oerintegrationdb"
    )

myac=mydb.cursor()

#download page
webumn = requests.get('{0}{1}'.format(domain,'opentextbooks'))
rawumn = webumn.content
soupumn = BS(rawumn,'html.parser')

subjRepository = 'Rep1'

#Insert Repository
'''
sql = "INSERT INTO triple(subject, predicate, object, time_date) VALUES(%s,%s,%s,%s)"
values = (subjRepository,'hasName','Open Textbook Library',datetime.datetime.now())
myac.execute(sql,values)
mydb.commit()
sql = "INSERT INTO triple(subject, predicate, object, time_date) VALUES(%s,%s,%s,%s)"
values = (subjRepository,'hasUrl','https://open.umn.edu/opentextbooks',datetime.datetime.now())
myac.execute(sql,values)
mydb.commit()
'''

#Find list of subjects pages
subjectRow = soupumn.find('div',{'id':'Subjects'})
subjectRow = subjectRow.find('ul').select('> li')

for li in subjectRow[13:]:
    nameSubject = li.find('a').get_text()
    linkSubject = li.find('a').get('href')

    subjCategory = '{0}{1}'.format('category',list(subjectRow).index(li)+1)

    sql = "INSERT INTO triple(subject, predicate, object, time_date) VALUES(%s,%s,%s,%s)"
    values = (subjRepository, 'hasSubject', subjCategory, datetime.datetime.now())
    myac.execute(sql, values)
    mydb.commit()
    print('\nSaving Cat: {0}'.format(nameSubject))

    sql = "INSERT INTO triple(subject, predicate, object, time_date) VALUES(%s,%s,%s,%s)"
    values = (subjCategory, 'hasName', nameSubject, datetime.datetime.now())
    myac.execute(sql, values)
    mydb.commit()

    while(1):
        #Dowload page of subject
        websub = requests.get('{0}{1}'.format(domain, linkSubject[1:]))
        rawsub = websub.content
        soupsub = BS(rawsub, 'html.parser')
        #getting titles of texbooks
        domTitles = soupsub.find('div',{'id':'textbook-list'}).find_all('div',{'class':'ShortDescription'})
        for tb in domTitles:
            domTB = tb.find('div',{'class':'twothird'}).find('h2')
            nameTB = domTB.find('a').get_text()
            linkTB = domTB.find('a').get('href')
            #print(nameTB, linkTB)
            #getting row of TextBook
            webtb = requests.get('{0}{1}'.format(domain,linkTB[1:]))
            rawtb = webtb.content

            sql = "INSERT INTO triple(subject, predicate, object, time_date) VALUES(%s,%s,%s,%s)"
            values = (subjCategory, 'hasRaw', rawtb, datetime.datetime.now())
            myac.execute(sql, values)
            mydb.commit()

        #pagination
        pagDom = soupsub.find('div',{'id':'infinite-scrolling'}).find('div',{'class':'pagination'})
        #Check URL to redirect new page, to more TB
        if pagDom != None:
            linkSubject = pagDom.find('a',{'class':'next_page'}).get('href')
            print('NEW URL',linkSubject)
        else:
            break
    print('End Category')