import scrape_courses_to_db as sdb
import build_time_table as btt
import schedule_courses as scheduler
import sqlite3

has_conflict = False
day_letters = ["M", "T", "W", "H", "F"]
schedule = [[], [], [], [], []]
course_names_selected = []

#=========================================================================================================================
courses_requested = [('cmput', '291'), ('cmput', '365'), ('cmput', '291'), ('cmput', '340'), ('cmput', '256'), ('cmput', '325'), ('cmput', '379'), ('cmput', '404')]
#=========================================================================================================================

def console_print_schedule(schedule):
    for i in range(len(schedule)):
        print(day_letters[i])
        for j in range(len(schedule[i])):
            print(schedule[i][j])
        print("")

#=========================================================================================================================

con = sqlite3.connect('scheduleSimple.db')
cur = con.cursor()

# Comment this line to prevent scraping new information to the db 
# sdb.scrape_to_db(courses_requested)

schedule, course_names_selected = scheduler.schedule_courses(schedule, course_names_selected, cur)

btt.build_time_table(schedule, course_names_selected)
console_print_schedule(schedule)