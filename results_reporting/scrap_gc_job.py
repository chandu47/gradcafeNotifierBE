from utils.manchow import Manchow
from database.model.program import Program
from database.model.university import University
from bs4 import BeautifulSoup as bsoup
from database.model.result import ProgramResult, UniResult
from model.institutionAdmissionRow import InstitutionAdmissionRow
import datetime
import re


from main import app
import requests

class ScrapGCJob:

    @staticmethod
    def loadDataFromGCJob():
        try:
            programsToScrap = Program.get_programs_for_scraping()
            print("Programs present are: --")
            ScrapGCJob.getProgramUpdatesAndSaveCommits(programsToScrap)
        except Exception as ex:
            app.logger.error("Come on... nothing in world is perfect. Some issue while running program updates job"+ex)

    @staticmethod
    def getProgramUpdatesAndSaveCommits(programs):
        for program in programs:
            totalPages = ScrapGCJob.fetchNoOfPagesInfo(program)
            programUpdatesList = ScrapGCJob.getProgramUpdates(totalPages, program)
            if(len(programUpdatesList)>0):
                programResultEntity = ScrapGCJob.createProgramResultEntity(programUpdatesList, program)
                if len(programResultEntity.universities) > 0:
                    try:
                        programResultEntity.save()
                        app.logger.info("Saved programResults entity")

                        program.save()
                        app.logger.info("Saved program with last commit updates")
                    except:
                        app.logger.error("Error while saving program results entity - {}", program.program)

    @staticmethod
    def getProgramUpdates(totalPages, program):
        programManchow = Manchow()
        programUpdatesList = []
        try:
            for pageNo in range(int(totalPages)):
                app.logger.info("Fetching program info for {} page no - {}".format(program, pageNo+1))
                initial_request = requests.get(
                    "https://www.thegradcafe.com/survey/index.php?q={collegeProgram}&t=n&pp=250&p={pageNo}".format(
                        collegeProgram=program.program, pageNo= pageNo+1)
                )
                if (initial_request.status_code == 200):
                    programUpdatesList.extend(programManchow.processData(initial_request.text))

            for programUpdate in programUpdatesList:
                print(programUpdate.resultId, programUpdate.program.program, programUpdate.inst.instName)
        except:
            app.logger.error("Something went wrong while fetching program info")
        return  programUpdatesList

    @staticmethod
    def createProgramResultEntity(updatesList, program):
        programResultsEntity = ProgramResult()
        programResultsEntity.program = program.program
        currentCommit = program.last_commit
        latest_commit = -1
        uniUpdates = []
        for update in updatesList:
            if update.resultId > currentCommit:
                uni = UniResult()

                #Update the resultId
                uni.commit_id = update.resultId
                latest_commit = max(latest_commit, update.resultId)

                if update.inst:
                    uni.university = update.inst.instName

                if update.program:
                    uni.season = update.program.season
                    uni.degree = update.program.degree

                if update.resultInfo:
                    uni.notes = update.resultInfo.notes
                    uni.decision = update.resultInfo.infoType
                    uni.decision_date = update.resultInfo.decisionDate
                    uni.date_added = update.resultInfo.infoDate
                    uni.status = update.resultInfo.nationality
                    uni.decision_medium = update.resultInfo.notifMethod
                uniUpdates.append(uni)

        programResultsEntity.latest_commit = latest_commit
        programResultsEntity.universities = uniUpdates
        program.last_commit = latest_commit
        program.last_commit_at = datetime.datetime.utcnow()
        return programResultsEntity


    @staticmethod
    def fetchNoOfPagesInfo(program):
        initial_request = requests.get(
            "https://www.thegradcafe.com/survey/index.php?q={collegeProgram}&t=n&pp=250".format(
                collegeProgram=program)
        )

        if (initial_request.status_code == 200):
            totalPages, totalData = ScrapGCJob.fetchDataPages(initial_request.text)
            return totalPages
        else:
            app.logger.error("Network call to gc failed.")

    @staticmethod
    def fetchDataPages(rawData):
        pageNo = 1
        totalPages = 1
        totalData = 1
        soup = bsoup(rawData, "html.parser")
        paginationElement = soup.find_all("div", {"class": "admission-search pagination"})
        paginationData = paginationElement[0].contents
        for count, ele in enumerate(paginationData):
            if ("strong" == ele.name):
                totalDataRE = re.search("^(.*)results$", ele.string)
                totalData = totalDataRE.group(1).lstrip().rstrip()
                totalPagesRE = re.search("^ over(.*)pages.*$", paginationData[count + 1])
                totalPages = totalPagesRE.group(1).rstrip().lstrip()
                break

        return totalPages, totalData