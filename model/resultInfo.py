class ResultInfo:
    def __init__(self):
        self.infoType = ""
        self.notifMethod = ""
        self.decisionDate = ""
        self.nationality = ""
        self.infoDate = ""
        self.notes = ""


    def set_infoType(self, infoType):
        self.infoType = infoType


    def set_decisionDate(self, decisionDate):
        self.decisionDate = decisionDate

    def set_infoDate(self, infoDate):
        self.infoDate = infoDate

    def set_notes(self, notes):
        self.notes = notes

    def set_notifMethod(self,notifMethod):
        self.notifMethod = notifMethod

    def set_nationality(self, nationality):
        self.nationality = nationality