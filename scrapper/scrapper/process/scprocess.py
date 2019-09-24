from bs4 import BeautifulSoup as BS
import mysql.connector

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="oerintegrationdb"
    )

myac=mydb.cursor()

domain = 'https://www.skillscommons.org'

#------------------- TO get Row from DB ---------------------

myac.execute('select * from triplesSC where predicate = "hasRaw" and process = 0')
rows = myac.fetchall()

for r in rows:
    subjectOer = 'oer'
    metadata_tb = BS(r[3],'html.parser')

    #title
    titleTB = metadata_tb.find('h1').get_text()
    subjectOer = '{}{}'.format(subjectOer, titleTB.replace(" ", ""))
    sql = "INSERT INTO cleantriple(subject, predicate, object) VALUES(%s,%s,%s)"
    values = (subjectOer, 'hasTitle', titleTB)
    myac.execute(sql, values)
    mydb.commit()

    #authors
    try:
        domAuthors = metadata_tb.find('ul',{'class':'authors'}).find_all('li')
        for li in domAuthors:
            author = li.get_text()
            sql = "INSERT INTO cleantriple(subject, predicate, object) VALUES(%s,%s,%s)"
            values = (subjectOer, 'hasAuthor', author)
            myac.execute(sql, values)
            mydb.commit()
    except Exception as e:
        print('get Authors: {0}'.format(e))

    #Description
    abstractTB = metadata_tb.find('div',{'class':'abstract'}).get_text()
    sql = "INSERT INTO cleantriple(subject, predicate, object) VALUES(%s,%s,%s)"
    values = (subjectOer, 'hasAbstract', abstractTB)
    myac.execute(sql, values)
    mydb.commit()


    #Metadatas
    domDl = metadata_tb.find_all('dl')
    lenDomDl = len(domDl)
    for dl in domDl[:lenDomDl-1]:
        divDl = dl.find_all('div')
        for div in divDl:
            name_Tag_dt = div.find('dt').get_text()
            value_Tag_dd = div.find('dd').get_text().strip()
            #To metadata with list Items
            if name_Tag_dt == 'Credit Type:' or name_Tag_dt == 'Credential Type:' or name_Tag_dt == 'Educational Level of Materials:' \
                    or name_Tag_dt == 'Quality of Subject Matter was assured by:' or name_Tag_dt == 'Accessibility Features:':
                try:
                    domTagDd = div.find('dd').find('ul').find_all('li')
                    for li in domTagDd:
                        value_Tag_dd = li.get_text().strip()
                        sql = "INSERT INTO cleantriple(subject, predicate, object) VALUES(%s,%s,%s)"
                        values = (subjectOer, 'has{}'.format(name_Tag_dt.replace(" ","")), value_Tag_dd)
                        myac.execute(sql, values)
                        mydb.commit()
                except Exception as e:
                    print('Error at atribute list {} | {}'.format(e,value_Tag_dd))

            else:
                sql = "INSERT INTO cleantriple(subject, predicate, object) VALUES(%s,%s,%s)"
                values = (subjectOer, 'has{}'.format(name_Tag_dt.replace(" ", "")), value_Tag_dd)
                myac.execute(sql, values)
                mydb.commit()

    # Files
    try:
        domFiles = metadata_tb.find('div', {'class': 'files'}).find_all('td', {'class': 'file-information'})
        for td in domFiles:
            a = td.find('a')
            fileName = a.get_text()
            fileUrlDownload = '{}{}'.format(domain, a.get('href'))
            sql = "INSERT INTO cleantriple(subject, predicate, object) VALUES(%s,%s,%s)"
            values = (subjectOer, 'hasDownloadFileName', fileName)
            myac.execute(sql, values)
            mydb.commit()
            sql = "INSERT INTO cleantriple(subject, predicate, object) VALUES(%s,%s,%s)"
            values = (subjectOer, 'hasDownloadFileUrl', fileUrlDownload)
            myac.execute(sql, values)
            mydb.commit()

    except Exception as e:
        print('get Files: {}'.format(e))

    #Licences
    divDl = domDl[lenDomDl - 1].find_all('div')
    for div in divDl:
        try:
            name_Tag_dt = div.find('dt').get_text()
            sql = "INSERT INTO cleantriple(subject, predicate, object) VALUES(%s,%s,%s)"
            values = (subjectOer, 'hasLicenseType', name_Tag_dt)
            myac.execute(sql, values)

            tag_dd = div.find('dd')
            licenseName = tag_dd.find('a').get_text().strip()
            licenseUrl = tag_dd.find('a').get('href')
            licenseImg = tag_dd.find('img').get('src')
            sql = "INSERT INTO cleantriple(subject, predicate, object) VALUES(%s,%s,%s)"
            values = (subjectOer, 'hasLicenseName', licenseName)
            myac.execute(sql, values)
            sql = "INSERT INTO cleantriple(subject, predicate, object) VALUES(%s,%s,%s)"
            values = (subjectOer, 'hasLicenseUrl', licenseUrl)
            myac.execute(sql, values)
            sql = "INSERT INTO cleantriple(subject, predicate, object) VALUES(%s,%s,%s)"
            values = (subjectOer, 'hasLicenseImg', licenseImg)
            myac.execute(sql, values)

        except Exception as e:
            print('get License: {0}'.format(e))

    # update Row
    idRow = r[0]
    sql = "UPDATE triplesSC SET process = 1 WHERE id = {}".format(idRow)
    myac.execute(sql)
    mydb.commit()
    print('End')