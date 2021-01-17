from bs4 import BeautifulSoup as bsoup
import re

from model.institution import Institution
from model.institutionAdmissionRow import InstitutionAdmissionRow
from model.program import Program
from model.resultInfo import ResultInfo
import logging


class Manchow:
    def __init__(self, rawData):
        self.rawData = rawData
        self.instAdmissionList = []

    def processData(self):
        self._startProcessing()

    def getInstAdmissionList(self):
        return self.instAdmissionList

    def _startProcessing(self):
        soup = bsoup(self.rawData, "html.parser")
        submissionsTable = soup.find_all("table", {"class": "submission-table"})
        admissionsRows = (submissionsTable[0].find_all("tr", {"class": ["row0","row1"]}))
        self.instAdmissionList = self._extractInstAdmissionList(admissionsRows)

    def _extractInstAdmissionList(self, admissionsRow):
        admResultRows = []
        for adm in admissionsRow:
            instAdmRow = InstitutionAdmissionRow()
            inst = Institution()
            program = Program()
            resultInfo = ResultInfo()
            try:
                id = self._scrapId(adm['onmouseover']).group(1)
            except:
                logging.error("Something went wrong while fetching resultId")
            else:
                instAdmRow.set_resultId(id)

            try:
                #instName = adm.find_all("td", {"class": "instcol tcol1"})
                for con in adm.contents:
                    print(con['class'])
                    if("instcol" in con['class']):
                        inst.set_instName(con.string)

                    elif("tcol2" in con['class'] ):
                        prog, deg, sea = self._getProgramAndDegree(con.string)
                        program.set_program(prog)
                        program.set_degree(deg.lstrip().rstrip())
                        program.set_season(sea)

                    elif("tcol3" in con['class']):
                        """
                        For fetching info related to notification type and notification date
                        """
                        resultInfo.set_infoType(con['class'][1])
                        notifMethod, notifDate = self._getDecisionDate(con.contents)
                        resultInfo.set_decisionDate(notifDate.lstrip().rstrip())
                        resultInfo.set_notifMethod(notifMethod.lstrip().rstrip())
                        print(resultInfo.notifMethod, resultInfo.decisionDate)

                    elif("tcol4" in con['class']):
                        resultInfo.set_nationality(con.string)

                    elif ("tcol5" in con['class']):
                        resultInfo.set_infoDate(con.string)

                    elif ("tcol6" in con['class']):
                        try:
                            print(con.find_all("li")[1].string)
                        except:
                            logging.error("Error in fetching notes")
            except:
                logging.error("Error while fetching some fields")
            else:
                instAdmRow.set_inst(inst)
                instAdmRow.set_program(program)
                instAdmRow.set_resultInfo(resultInfo)
                admResultRows.append(instAdmRow)


    def _scrapId(self, idString):
        id = re.search("^showControlsBox\(this,(\d+)\);$", idString)
        return id

    def _getProgramAndDegree(self, proString):
        program = re.search("^(.*),(.*)\((.*)\)$", proString)
        return program.group(1), program.group(2), program.group(3)

    def _getDecisionDate(self, decisionStringList):
        print(decisionStringList)
        decisionString = decisionStringList[min(len(decisionStringList)-1,1)]
        print(decisionString+"<----dstring")
        decRE = re.search("^.*via(.*)on(.*)$", decisionString)
        return decRE.group(1), decRE.group(2)

