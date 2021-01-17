import requests
from utils.manchow import Manchow

program_name = 'Computer+Science'

r = requests.get(
"https://www.thegradcafe.com/survey/index.php?q={collegeProgram}&t=n&o=&pp=250".format(collegeProgram = program_name)
)


print(r.status_code)
manchow = Manchow(r.text)
manchow.processData()
