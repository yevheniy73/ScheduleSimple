from bs4 import BeautifulSoup
import requests
import sqlite3
import numpy as np

has_conflict = False
day_letters = ["M", "T", "W", "H", "F"]

schedule_monday = []
schedule_tuesday = []
schedule_wednesday = []
schedule_thursday = []
schedule_friday = []
schedule = [schedule_monday, schedule_tuesday, schedule_wednesday, schedule_thursday, schedule_friday]

##########################################################################################################################

courses_requested = [('cmput', '466'), ('cmput', '365'), ('cmput', '291'), ('cmput', '340'), ('cmput', '256'), ('cmput', '325'), ('cmput', '379'), ('cmput', '404')]

##########################################################################################################################

# mySql_insert_query = '''INSERT OR IGNORE INTO cmput_courses VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

con = sqlite3.connect('scheduleSimple.db')
cur = con.cursor()

# cur.execute('''DROP TABLE cmput_courses''')

# cur.execute('''CREATE TABLE IF NOT EXISTS cmput_courses
#                 (course_name text, section_type text, section_name text, section_num int PRIMARY KEY, capacity int, start_date text, 
#                 end_date text, week_days text, start_time text, end_time text, location text)''')

#=========================================================================================================================

def convert_day(day):
    days = list(day)
    return_days = []
    for a_day in days:
        return_days.append(day_letters.index(a_day))
    return return_days

#=========================================================================================================================

# for course in courses_requested:
#     url = f"https://apps.ualberta.ca/catalogue/course/{course[0]}/{course[1]}"
#     result = requests.get(url)
#     doc = BeautifulSoup(result.text, 'lxml')
#     datesTimes = doc.find_all("td",  {"data-card-title":"Section"})

#     for date in datesTimes:

#         text = "  ".join(date.parent.text.split())
#         textArr = text.split()
#         textArr[:] = (value for value in textArr if value != '-')
#         textArr[:] = (value for value in textArr if value != 'ONLINE')

#         record = (f'{course[0].upper()} {course[1]}', textArr[0], textArr[1], textArr[2].strip("()"), textArr[3],
#                     textArr[4], textArr[5], textArr[6], textArr[7], textArr[8], str(textArr[9] + " " + textArr[10]).strip("()"))
#         cur.execute(mySql_insert_query, record)

# con.commit()


url = f"https://www.beartracks.ualberta.ca/psc/uahebprd_4/EMPLOYEE/HRMS/c/SSR_STUDENT_FL.SSR_MD_SP_FL.GBL?Action=U&MD=Y&GMenu=SSR_STUDENT_FL&GComp=SSR_START_PAGE_FL&GPage=SSR_START_PAGE_FL&scname=CS_SSR_MANAGE_CLASSES_NAV"
result = requests.get(url)
doc = BeautifulSoup(result.text, 'lxml')
datesTimes = doc.find_all("td",  {"data-card-title":"Section"})

#=========================================================================================================================

course_names_selected = []

for db_course in cur.execute('''SELECT * FROM cmput_courses WHERE section_type = "LECTURE" AND start_date = "2023-01-05"'''):
    has_conflict = False

    if db_course[0] in course_names_selected:
        continue

    for a_day in convert_day(db_course[7]):
        for course in schedule[a_day]:

            existing_start_time = int(str(course[1]).replace(":",""))
            existing_end_time = int(str(course[2]).replace(":",""))

            db_course_start_time = int(str(db_course[8]).replace(":",""))
            db_course_end_time = int(str(db_course[9]).replace(":",""))

            if db_course_start_time <= existing_end_time and db_course_end_time >= existing_start_time:
                has_conflict = True

    if not has_conflict:
        for a_day in convert_day(db_course[7]):
            schedule[a_day].append([db_course[0], db_course[8], db_course[9], db_course[3]])
            course_names_selected.append(db_course[0])
#=========================================================================================================================

# print out the schedule at the end
for i in range(len(schedule)):
    print(day_letters[i])
    for j in range(len(schedule[i])):
        print(schedule[i][j])
    print("")

# for db_course in cur.execute('''SELECT * FROM cmput_courses WHERE section_type="LECTURE"'''):
#     print(db_course)

#=========================================================================================================================