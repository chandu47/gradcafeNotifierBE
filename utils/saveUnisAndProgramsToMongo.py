from database.model.program import Program
from database.model.university import University
import csv

def saveProgramsToMongo():
    with open('./resources/programs_list.csv') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            prog = row[1]
            print("Saving "+ prog)
            Program(program = prog).save()

def saveUniversitiesToMongo():
    with open('./resources/universities_list.csv') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            uni = row[1]
            if(len(row)>2):
                uni += ","+row[-1]
            print(uni)
            University(university=uni).save()