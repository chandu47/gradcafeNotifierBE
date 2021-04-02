from selenium import webdriver
import time
import string
import csv


gradcafe_survey_link = "https://www.thegradcafe.com/survey/post.php"
universities = []
programs = []

def writeToCSVFile(filename, diction):
    """
        Write to file
    """
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for index, uni in enumerate(diction):
            writer.writerow([index, uni])

def openPageAndTriggerAutoFillUniversities():
    driver = webdriver.Firefox()
    driver.get(gradcafe_survey_link)
    univeristy_search = driver.find_element_by_id('institution_drop')
    for alpha in string.ascii_lowercase:
        univeristy_search.click()
        univeristy_search.clear()
        univeristy_search.send_keys(alpha)
        time.sleep(2)
        uni_search_html = driver.find_element_by_id('inst_upd')
        for uni in (uni_search_html.text).splitlines():
            print(uni)
            print("----")
            if(uni not in universities):
                universities.append(uni)
        time.sleep(5)

    writeToCSVFile('../resources/universities_list.csv', universities)

    #// *[ @ id = "inst_upd"] / ul / li[1]

def openPageAndTriggerAutoFillPrograms():
    driver = webdriver.Firefox()
    driver.get(gradcafe_survey_link)
    program_search = driver.find_element_by_id('prog_drop')
    for alpha in string.ascii_lowercase:
        program_search.click()
        program_search.clear()
        program_search.send_keys(alpha)
        time.sleep(2)
        uni_search_html = driver.find_element_by_id('prog_upd')
        for uni in (uni_search_html.text).splitlines():
            print(uni)
            print("----")
            if(uni not in programs):
                programs.append(uni)
        time.sleep(3)

    writeToCSVFile('../resources/programs_list.csv', programs)



openPageAndTriggerAutoFillPrograms()