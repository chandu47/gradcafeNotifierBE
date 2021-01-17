class InstitutionAdmissionRow:

    def __init__(self):
        self.resultId = ""
        self.inst = None
        self.program = None
        self.resultInfo = None

    def set_resultId(self, resultId):
        self.resultId = resultId

    def set_inst(self, inst):
        self.inst = inst

    def set_program(self, program):
        self.program = program

    def set_resultInfo(self,resultInfo):
        self.resultInfo = resultInfo
