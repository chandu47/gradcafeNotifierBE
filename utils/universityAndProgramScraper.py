from bs4 import BeautifulSoup as bsoup
import re
import requests
import csv
from os  import path
universities = {}
programs = []
BASE_PROGRAM_TO_FETCH_UNIVERSITIES = 'Computer+Science'

def fetchDataPages(rawData):
    pageNo = 1
    totalPages = 1
    totalData = 1
    soup = bsoup(rawData, "html.parser")
    paginationElement = soup.find_all("div", {"class": "admission-search pagination"})
    paginationData = paginationElement[0].contents
    for count, ele in enumerate(paginationData):
        print(ele)
        if("strong"==ele.name):
            totalDataRE = re.search("^(.*)results$", ele.string)
            totalData = totalDataRE.group(1).lstrip().rstrip()
            totalPagesRE = re.search("^ over(.*)pages.*$", paginationData[count+1])
            totalPages = totalPagesRE.group(1).rstrip().lstrip()
            break

    return totalPages, totalData


def populateUniversitiesList(totalPages, totalData):
    for pageNo in range(int(totalPages)):
        print("Reading pageNo: "+str(pageNo))
        subseq_request = requests.get(
            "https://www.thegradcafe.com/survey/index.php?q={collegeProgram}&pp=250&p={pageNo}".format(
                collegeProgram=BASE_PROGRAM_TO_FETCH_UNIVERSITIES, pageNo= pageNo+1)
        )
        if (subseq_request.status_code == 200):
            soup = bsoup(subseq_request.text, "html.parser")
            submissionsTable = soup.find_all("table", {"class": "submission-table"})
            admissionsRows = (submissionsTable[0].find_all("tr", {"class": ["row0", "row1"]}))
            for adm in admissionsRows:
                for con in adm.contents:
                    if("instcol" in con['class']):
                        if con.string not in universities.keys():
                            universities[con.string] = 0
                        else:
                            universities[con.string] += 1
                        break

        writeToCSVFile('../resources/universities_list.csv', universities)

def writeToCSVFile(filename, diction):
    """
        Write to file
    """
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        write_index=0
        for uni, count in diction.items():
            writer.writerow([write_index, uni, count])
            write_index+=1


def writeProgramsToCSVFile(filename, diction, readIndex):
    """
        Write to file
    """
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([str(readIndex)])
        for index, uni in enumerate(diction):
            writer.writerow([index, uni])

def sortUniversitiesAndSave():
    with open('../resources/universities_list.csv') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            universities.append(row[0])

    universities.sort()
    with open('../resources/universities_list.csv', 'w', newline='') as file:
        csv_writer = csv.writer(file)
        for index, uni in enumerate(universities):
            csv_writer.writerow([index, uni])


def populateProgramsList(totalPages, totalData, uni):
    for pageNo in range(int(totalPages)):
        print("Reading pageNo: "+str(pageNo))
        subseq_request = requests.get(
            "https://www.thegradcafe.com/survey/index.php?q={collegeProgram}&pp=250&p={pageNo}".format(
                collegeProgram=uni, pageNo= pageNo+1)
        )
        if (subseq_request.status_code == 200):
            soup = bsoup(subseq_request.text, "html.parser")
            submissionsTable = soup.find_all("table", {"class": "submission-table"})
            admissionsRows = (submissionsTable[0].find_all("tr", {"class": ["row0", "row1"]}))
            for adm in admissionsRows:
                for con in adm.contents:
                    if("tcol2" in con['class']) and _getProgramAndDegree(con.string)[0] not in programs:
                        programs.append(_getProgramAndDegree(con.string)[0])
                        break

def  fetchAllPrograms():
    with open('../resources/universities_list.csv') as file:
        read_index = 0
        if(path.exists('../resources/programs_list.csv')):
            with open('../resources/programs_list.csv') as progFile:
                csv_prog_reader = csv.reader(progFile)
                read_index = int(csv_prog_reader[0][0])
                line_count=0
                for prog_row in csv_prog_reader:
                    if(line_count==0):
                        line_count += 1
                    else:
                        programs.append(prog_row[1])

        csv_reader = csv.reader(file)
        for row in csv_reader:
            if(int(row[0]) < int(read_index)):
                continue
            print("Reading programs for " + row[0]+' '+row[1])
            request = requests.get(
                "https://www.thegradcafe.com/survey/index.php?q={college}&pp=250".format(
                    college=row[1])
            )

            if (request.status_code == 200):
                totalPages, totalData = fetchDataPages(request.text)
                populateProgramsList(totalPages, totalData, row[1])
            if not int(row[0])%5:
                writeProgramsToCSVFile('../resources/programs_list.csv', programs, int(row[0]) + 1)


def getUniversityStats():
    with open('../resources/universities_list.csv') as file:
        csv_reader = csv.reader(file)
        max_stat=0
        avg_stat=0
        total_count =0
        total_uni=0
        count_list=[]
        for row in csv_reader:
            if int(row[2]) > 50:
                universities[row[1]]=int(row[2])
                total_uni+=1
                count_list.append(int(row[2])+1)
                total_count += int(row[2])+1
                if(int(row[2])>max_stat):
                    max_stat=int(row[2])+1

        count_list.sort()
        print("Max count is "+ str(max_stat))
        print("Avg count is "+ str(float(total_count)/total_uni))
        print("Median is - "+ str(count_list[int(len(count_list)/10)]))
    with open('../resources/universities_list.csv','w',newline='') as file:
        csv_writer = csv.writer(file)
        write_count = 0
        for ind in sorted(universities):
            write_count += 1
            csv_writer.writerow([write_count, ind, universities[ind]])

def fetchUniversityInfo():
    initial_request = requests.get(
        "https://www.thegradcafe.com/survey/index.php?q={collegeProgram}&pp=250".format(
            collegeProgram=BASE_PROGRAM_TO_FETCH_UNIVERSITIES)
    )

    if(initial_request.status_code==200):
        totalPages, totalData = fetchDataPages(initial_request.text)
        populateUniversitiesList(totalPages, totalData)


def _getProgramAndDegree(proString):
    program = re.search("^(.*),(.*)\((.*)\)$", proString)
    return program.group(1), program.group(2), program.group(3)


#fetchUniversityInfo()
#fetchAllPrograms()

getUniversityStats()