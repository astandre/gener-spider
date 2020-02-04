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

def saveTriple(s, sa, p, o, repository):
    if o == 'None' or o == '' or o == None:
        pass
    else:
        sql = "INSERT INTO scrapydb.cleantriple(subject, subject_alternative, predicate, object,repository) VALUES(%s,%s,%s,%s,%s)"
        values = (s, sa, p, o, repository)
        myac.execute(sql, values)
        mydb.commit()

#------------------- TO get Row from DB ---------------------
source = 'Skill Commons'

myac.execute('select * from triplesSC where predicate = "hasRaw" and process = 0;')
rows = myac.fetchall()
nRows = len(rows)
for r in rows:
    subjectOer = 'oer'
    metadata_tb = BS(r[3],'html.parser')

    #title
    titleTB = metadata_tb.find('h1').get_text()
    subjectOer = r[6]
    saveTriple(subjectOer,'','title',titleTB,source)

    #authors
    try:
        domAuthors = metadata_tb.find('ul',{'class':'authors'}).find_all('li')
        for li in domAuthors:
            author = li.get_text()
            saveTriple(subjectOer,'','author',author,source)
    except Exception as e:
        print('get Authors: {0}'.format(e))

    #Description
    abstractTB = metadata_tb.find('div',{'class':'abstract'}).get_text()
    saveTriple(subjectOer,'','abstract',abstractTB,source)


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
                        saveTriple(subjectOer,'','{}'.format(name_Tag_dt.replace(" ","")),value_Tag_dd,source)
                        
                except Exception as e:
                    print('Error at atribute list {} | {}'.format(e,value_Tag_dd))

            else:
                saveTriple(subjectOer,'','{}'.format(name_Tag_dt.replace(" ","")),value_Tag_dd,source)

    # Files
    try:
        domFiles = metadata_tb.find('div', {'class': 'files'}).find_all('td', {'class': 'file-information'})
        for td in domFiles:
            a = td.find('a')
            fileName = a.get_text()
            fileUrlDownload = '{}{}'.format(domain, a.get('href'))
            obj_subj = f'download-{list(domFiles).index(td)}'
            saveTriple(subjectOer,'','hasDownload',obj_subj,source)
            saveTriple(obj_subj,'','downloadFileName',fileName,source)
            saveTriple(obj_subj,'','downloadFileUrl',fileUrlDownload,source)
        

    except Exception as e:
        print('get Files: {}'.format(e))

    #Licences
    divDl = domDl[lenDomDl - 1].find_all('div')
    for div in divDl:
        try:
            name_Tag_dt = div.find('dt').get_text()
            obj_subj = name_Tag_dt
            saveTriple(subjectOer,'','hasLicenseType',obj_subj,source)
            saveTriple(obj_subj,'','licenseTypeName',name_Tag_dt,source)

            value_Tag_dd = div.find('dd').get_text().strip()
            saveTriple(obj_subj,'','licenseTypeValue',value_Tag_dd,source)

            tag_dd = div.find('dd')
            licenseName = tag_dd.find('a').get_text().strip()
            licenseUrl = tag_dd.find('a').get('href')
            licenseImg = tag_dd.find('img').get('src')
            saveTriple(obj_subj,'','licenseName',licenseName,source)
            saveTriple(obj_subj,'','licenseUrl',licenseUrl,source)
            saveTriple(obj_subj,'','licenseImg',licenseImg,source)

        except Exception as e:
            print('get License: {0}'.format(e))

    print(f'{rows.index(r)} / {nRows}')

    # update Row
    idRow = r[0]
    sql = "UPDATE triplesSC SET process = 1 WHERE id = {}".format(idRow)
    myac.execute(sql)
    mydb.commit()
    print('End')