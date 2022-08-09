from bs4 import BeautifulSoup
import requests
import sqlite3


def scrape_to_db(courses_requested):
    mySql_insert_query = '''INSERT OR IGNORE INTO cmput_courses VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

    con = sqlite3.connect('scheduleSimple.db')
    cur = con.cursor()

    cur.execute('''DROP TABLE cmput_courses''')

    cur.execute('''CREATE TABLE IF NOT EXISTS cmput_courses
                    (course_name text, section_type text, section_name text, section_num int PRIMARY KEY, capacity int, start_date text, 
                    end_date text, week_days text, start_time text, end_time text, location text)''')

    #=========================================================================================================================

    for course in courses_requested:
        url = f"https://apps.ualberta.ca/catalogue/course/{course[0]}/{course[1]}"
        result = requests.get(url)
        doc = BeautifulSoup(result.text, 'lxml')
        datesTimes = doc.find_all("td",  {"data-card-title":"Section"})

        for date in datesTimes:

            text = "  ".join(date.parent.text.split())
            textArr = text.split()
            textArr[:] = (value for value in textArr if value != '-')
            textArr[:] = (value for value in textArr if value != 'ONLINE')

            record = (f'{course[0].upper()} {course[1]}', textArr[0], textArr[1], textArr[2].strip("()"), textArr[3],
                        textArr[4], textArr[5], textArr[6], textArr[7], textArr[8], str(textArr[9] + " " + textArr[10]).strip("()"))
            cur.execute(mySql_insert_query, record)

    con.commit()
    return None