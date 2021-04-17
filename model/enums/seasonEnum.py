import datetime


month = datetime.datetime.today().month
year = datetime.datetime.today().year

print(month, year)

class AdmitSeason:
    validSeasons = []
    currYear = str(year)[-2:]
    nextYear = str(year+1)[-2:]
    validSeasons.append('F'+currYear)
    validSeasons.append('S'+nextYear)
    validSeasons.append('S'+currYear) if month < 7 else validSeasons.append('F'+nextYear)