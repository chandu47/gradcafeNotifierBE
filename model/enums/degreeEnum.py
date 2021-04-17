import enum

class DegreeType(enum.Enum):
    PhD = 'PhD'
    Masters = 'Masters'
    MFA = 'MFA'
    MBA = 'MBA'
    JD = 'JD'
    EdD = 'EdD'
    Other = 'Other'
    IND = 'IND'
    PsyD = 'PsyD'

    @staticmethod
    def has_value(item):
        try:
            DegreeType(item)
        except ValueError:
            return False
        return True