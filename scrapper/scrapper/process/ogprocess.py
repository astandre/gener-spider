from bs4 import BeautifulSoup as BS
import mysql.connector

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="oerintegrationdb"
    )

myac=mydb.cursor()

domain = 'https://florida.theorangegrove.org/'


#------------------- TO get Row from DB ---------------------

myac.execute('select * from triplesOG where predicate = "hasRaw" and process = 0')
rows = myac.fetchall()

for r in rows:
    metadata_tb = BS(r[3],'html.parser')

    #Get metadata
    div_nodes = []
    div_nodes.append(metadata_tb.find_all('div',{'class':'displayNodeFull'}))
    div_nodes.append(metadata_tb.find_all('div', {'class': 'displayNodeHalf'}))
    subjectOer = 'oer'
    for node in div_nodes:
        for n in node:
            '''
            CREATE TABLE clearTriplesOrangeGroove(
               id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
               subject VARCHAR (200) NOT NULL,
               predicate VARCHAR (200) NOT NULL,
               object LONGTEXT NOT NULL
            );
            '''
            try:
                h3_tag = n.find('h3').get_text()
                p_tag = n.find('p').get_text()

                if h3_tag == 'Title':
                    subjectOer = '{}{}'.format(subjectOer,p_tag.replace(" ",""))
                    sql = "INSERT INTO cleantriple(subject, predicate, object) VALUES(%s,%s,%s)"
                    values = (subjectOer, 'has{}'.format(h3_tag.replace(" ","")), p_tag,)
                    myac.execute(sql, values)
                    mydb.commit()
                else:
                    sql = "INSERT INTO cleantriple(subject, predicate, object) VALUES(%s,%s,%s)"
                    values = (subjectOer, 'has{}'.format(h3_tag.replace(" ", "")), p_tag,)
                    myac.execute(sql, values)
                    mydb.commit()
                '''
                if h3_tag == 'Description' or h3_tag == 'Brief Description':
                    sql = "INSERT INTO clearTriplesOrangeGroove(subject, predicate, object) VALUES(%s,%s,%s)"
                    values = (subjectOer, 'has{}'.format(h3_tag.replace(" ", "")), p_tag,)
                    myac.execute(sql, values)
                    mydb.commit()
                    
                if h3_tag == 'Keywords':
                    print('Keywords: {}'.format(p_tag))

                if h3_tag == 'Creator':
                    print('Creator: {}'.format(p_tag))

                if h3_tag == 'Author':
                    print('Author: {}'.format(p_tag))

                if h3_tag == 'Language':
                    print('Language: {}'.format(p_tag))

                if h3_tag == 'Date Published' or h3_tag == 'Publication/Creation date':
                    print('Date Published: {}'.format(p_tag))

                if h3_tag == 'Date Harvested':
                    print('Date Harvested: {}'.format(p_tag))

                if h3_tag == 'ISBN':
                    print('ISBN: {}'.format(p_tag))

                if h3_tag == 'Publisher':
                    print('Published: {}'.format(p_tag))

                if h3_tag == 'Source':
                    print('Source: {}'.format(p_tag))

                if h3_tag == 'Learning resource type':
                    print('Learning resource type: {}'.format(p_tag))

                if h3_tag == 'Discipline':
                    print('Discipline: {}'.format(p_tag))

                if h3_tag == 'Educational context':
                    print('EducationalContext: {}'.format(p_tag))

                if h3_tag == 'Interactivity type':
                    print('Interactivity type: {}'.format(p_tag))

                if h3_tag == 'Rights statement':
                    print('Rights statement {}'.format(p_tag))
                '''
            except Exception as e:
                print('\nException: {}'.format(e))
                print(n)
    #Rights
    try:
        domRights = metadata_tb.find('div',{'class':'content'}).find('table').find_all('tr')
        for tr in domRights:

            tagNameLicense = tr.find('span',{'class':'pagesubheading'}).get_text().strip()
            valueLicense = tr.find('span',{'class':'pagetext'}).get_text().strip()
            sql = "INSERT INTO cleantriple(subject, predicate, object) VALUES(%s,%s,%s)"
            values = (subjectOer, 'has{}'.format(tagNameLicense.replace(" ", "")), valueLicense,)
            myac.execute(sql, values)
            mydb.commit()
            if tagNameLicense == 'Conditions of Use':
                nameLicense = tr.find('a').get_text()
                linkLicense = tr.find('a').get('href')
                sql = "INSERT INTO cleantriple(subject, predicate, object) VALUES(%s,%s,%s)"
                values = (subjectOer, 'hasLicenseName', nameLicense,)
                myac.execute(sql, values)
                mydb.commit()
                sql = "INSERT INTO cleantriple(subject, predicate, object) VALUES(%s,%s,%s)"
                values = (subjectOer, 'hasLicenseUrl', linkLicense,)
                myac.execute(sql, values)
                mydb.commit()
    except Exception as e:
        print('Error at licence: {} \n{}'.format(e, metadata_tb.find('h3').get_text()))

    # get Url of Resources
    linksSrc = metadata_tb.find('ul',{'id':'sc_attachments_browse'}).find_all('li')
    for li in linksSrc:
        try:
            div_a = li.find('div',{'class':'link-div'})
            url_of_resource = div_a.find('a').attrs['href']
            if url_of_resource[:3] == '/og':
                url_of_resource = '{}{}'.format(domain,url_of_resource[1:])

            sql = "INSERT INTO cleantriple(subject, predicate, object) VALUES(%s,%s,%s)"
            values = (subjectOer, 'hasUrlDownload', url_of_resource,)
            myac.execute(sql, values)
            mydb.commit()
        except Exception as e:
            pass
    #update Row
    idRow = r[0]
    sql = "UPDATE triplesOG SET process = 1 WHERE id = {}".format(idRow)
    myac.execute(sql)
    mydb.commit()
    print('\n\nEND')
#Se completo hasta el id 53228