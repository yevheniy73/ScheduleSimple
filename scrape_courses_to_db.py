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
            db_entry = text.split()
            db_entry[:] = (value for value in db_entry if value != '-')
            db_entry[:] = (value for value in db_entry if value != 'ONLINE')

            record = (f'{course[0].upper()} {course[1]}', db_entry[0], db_entry[1], db_entry[2].strip("()"), db_entry[3],
                        db_entry[4], db_entry[5], db_entry[6], db_entry[7], db_entry[8], str(db_entry[9] + " " + db_entry[10]).strip("()"))
            cur.execute(mySql_insert_query, record)

    con.commit()
    return None