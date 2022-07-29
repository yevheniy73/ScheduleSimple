from bs4 import BeautifulSoup
import requests
import sqlite3
import re

con = sqlite3.connect('scheduleSimple.db')
cur = con.cursor()

# cur.execute('''DROP TABLE cmput_courses''')

cur.execute('''CREATE TABLE IF NOT EXISTS cmput_courses
                (section_type text, section_name text, section_num int PRIMARY KEY, capacity int, start_date text, 
                end_date text, week_days text, start_time text, end_time text, location text)''')

url = "https://apps.ualberta.ca/catalogue/course/cmput/291"

result = requests.get(url)
doc = BeautifulSoup(result.text, 'lxml')
datesTimes = doc.find_all("td",  {"data-card-title":"Section"})

mySql_insert_query = '''INSERT OR IGNORE INTO cmput_courses VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

for date in datesTimes:

    text = "  ".join(date.parent.text.split())
    textArr = text.split()
    textArr[:] = (value for value in textArr if value != '-')

             #['LECTURE',      'A1',          '(36739)',        '75',   '2022-09-01', '2022-12-08', 'MWF',    '13:00',   '13:50',           '(CAB', '239)',                        'Rupam', 'Mahmood']
    #record = (textArr[0], textArr[1], textArr[2].strip("()"), textArr[3], textArr[4], textArr[5], textArr[6], textArr[7], textArr[8], str(textArr[9] + " " + textArr[10]).strip("()"), str(textArr[13] + " " + textArr[14]))
    record = (textArr[0], textArr[1], textArr[2].strip("()"), textArr[3], textArr[4], textArr[5], textArr[6], textArr[7], textArr[8], str(textArr[9] + " " + textArr[10]).strip("()"))
    cur.execute(mySql_insert_query, record)

con.commit()

for row in cur.execute('''SELECT * FROM cmput_courses WHERE section_type="LECTURE";'''):
    print(row)