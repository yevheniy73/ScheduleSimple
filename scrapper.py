from bs4 import BeautifulSoup
import requests
import sqlite3
import numpy as np
import os

has_conflict = False
course_colors = ["#ff9999", "#99FF99", "#ff99cc", "#FFFF99", "#99CCFF", "#CC99FF", "#CC9999", "#CCFF99", "#ffcc99"]
day_letters = ["M", "T", "W", "H", "F"]

schedule_monday = []
schedule_tuesday = []
schedule_wednesday = []
schedule_thursday = []
schedule_friday = []
schedule = [schedule_monday, schedule_tuesday, schedule_wednesday, schedule_thursday, schedule_friday]

##########################################################################################################################

courses_requested = [('phil', '120'), ('cmput', '466'), ('cmput', '365'), ('cmput', '291'), ('cmput', '340'), ('cmput', '256'), ('cmput', '325'), ('cmput', '379'), ('cmput', '404'), ('engl', '103'), ('engl', '103')]

##########################################################################################################################

mySql_insert_query = '''INSERT OR IGNORE INTO cmput_courses VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

con = sqlite3.connect('scheduleSimple.db')
cur = con.cursor()

# cur.execute('''DROP TABLE cmput_courses''')

cur.execute('''CREATE TABLE IF NOT EXISTS cmput_courses
                (course_name text, section_type text, section_name text, section_num int PRIMARY KEY, capacity int, start_date text, 
                end_date text, week_days text, start_time text, end_time text, location text)''')

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


base = os.path.dirname(os.path.abspath(__file__))

html_sched =open(os.path.join(base, 'SampleTemplate.html'))
html_sched_text = BeautifulSoup(html_sched, 'lxml')


day_name_pointer = 0

for day in schedule:
    day_name_pointer += 1
    day_name = day_letters[day_name_pointer - 1]

    for course in day:

        course_start_time = course[1].replace(":","")
        course_end_time = course[2].replace(":","")

        time_difference_hours = int(course_end_time[:2]) - int(course_start_time[:2])
        time_difference_mins = int(course_end_time[-2:]) - int(course_start_time[-2:]) + 10
        time_difference = time_difference_hours * 60 + time_difference_mins

        sched_block = html_sched_text.find("td", {"id": f"{day_name}{course_start_time}a"})
        sched_block_b = html_sched_text.find("td", {"id": f"{day_name}{course_start_time}b"})
        sched_block_b['class'] = sched_block.get('class', []) + ['HIDE_ME']

        sched_block.string = f"{course[0]} LEC {course[3]}"
        sched_block['class'] = "CHEDSTD"
        sched_block['height'] = time_difference
        sched_block['width'] = "100"
        sched_block['rowspan'] = (time_difference / 15)
        sched_block['colspan'] = "2"
        sched_block['bgcolor'] = course_colors[course_names_selected.index(course[0])]

        sched_pointer = 15

        while sched_pointer< time_difference:

            sched_hour = course_start_time[:2]
            sched_minute = int(course_start_time[-2:]) + sched_pointer
            extra_hour, extra_minute = divmod(sched_minute, 60)

            sched_hour = str(int(course_start_time[:2]) + extra_hour).zfill(2)
            extra_minute = str(extra_minute).zfill(2)

            sched_block = html_sched_text.find("td", {"id": f"{day_name}{sched_hour}{extra_minute}a"})
            sched_block['class'] = sched_block.get('class', []) + ['HIDE_ME']

            sched_block = html_sched_text.find("td", {"id": f"{day_name}{str(sched_hour).zfill(2)}{str(extra_minute).zfill(2)}b"})
            sched_block['class'] = sched_block.get('class', []) + ['HIDE_ME']

            sched_pointer += 15

with open("output1.html", "w") as file:
    file.write(str(html_sched_text.prettify()))