from bs4 import BeautifulSoup as bsoup
import re

from model.institution import Institution
from model.institutionAdmissionRow import InstitutionAdmissionRow
from model.program import Program
from model.resultInfo import ResultInfo
import logging


class Manchow:
    def processData(self, rawData):
        return self._startProcessing(rawData)


    def _startProcessing(self, rawData):
        soup = bsoup(rawData, "html.parser")
        submissionsTable = soup.find_all("table", {"class": "submission-table"})
        if len(submissionsTable)>0:
            admissionsRows = (submissionsTable[0].find_all("tr", {"class": ["row0","row1"]}))
            return self._extractInstAdmissionList(admissionsRows)
        else:
            return []

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
                instAdmRow.set_resultId(int(id.lstrip().rstrip()))

            try:
                #instName = adm.find_all("td", {"class": "instcol tcol1"})
                for con in adm.contents:
                    if("instcol" in con['class']):
                        inst.set_instName(con.string)

                    elif("tcol2" in con['class'] ):
                        try:
                            prog, deg, sea = self._getProgramAndDegree(con.string)
                            program.set_program(prog)
                            program.set_degree(deg.lstrip().rstrip())
                            program.set_season(sea)
                        except:
                            logging.error("Error while fetching program information")

                    elif("tcol3" in con['class']):
                        """
                        For fetching info related to notification type and notification date
                        """
                        try:
                            resultInfo.set_infoType(con['class'][1])
                            notifMethod, notifDate = self._getDecisionDate(con.contents)
                            resultInfo.set_decisionDate(notifDate.lstrip().rstrip())
                            resultInfo.set_notifMethod(notifMethod.lstrip().rstrip())
                        except:
                            logging.error("Error while fetching resultInfo")

                    elif("tcol4" in con['class']):
                        resultInfo.set_nationality(con.string)

                    elif ("tcol5" in con['class']):
                        resultInfo.set_infoDate(con.string)

                    elif ("tcol6" in con['class']):
                        try:
                            resultInfo.set_notes(con.find_all("li")[1].string)
                        except:
                            logging.error("Error in fetching notes")
            except:
                logging.error("Error while fetching some fields")
            else:
                instAdmRow.set_inst(inst)
                instAdmRow.set_program(program)
                instAdmRow.set_resultInfo(resultInfo)
                admResultRows.append(instAdmRow)
        return admResultRows


    def _scrapId(self, idString):
        id = re.search("^showControlsBox\(this,(\d+)\);$", idString)
        return id

    def _getProgramAndDegree(self, proString):
        program = re.search("^(.*),(.*)\((.*)\)$", proString)
        return program.group(1), program.group(2), program.group(3)

    def _getDecisionDate(self, decisionStringList):
        for dString in decisionStringList:
            if "via" in dString:
                decisionString = dString
                break
        #decisionString = decisionStringList[min(len(decisionStringList)-1,1)]
        decRE = re.search("^.*via(.*)on(.*)$", decisionString)
        return decRE.group(1), decRE.group(2)

