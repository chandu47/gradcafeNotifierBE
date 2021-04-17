import requests
from utils.manchow import Manchow

program_name = 'Computer Science'

r = requests.get(
"https://www.thegradcafe.com/survey/index.php?q={collegeProgram}&t=n&pp=250&p={pageNo}".format(collegeProgram = program_name, pageNo = 1)
)


print(r.status_code)
print(r.text)
manchow = Manchow()
print(manchow.processData(r.text))
