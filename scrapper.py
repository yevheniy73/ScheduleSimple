import scrape_courses_to_db as sdb
import build_time_table as btt
import schedule_courses as scheduler
import sqlite3

has_conflict = False
schedule = [[], [], [], [], []]
course_names_selected = []

#=========================================================================================================================
courses_requested = [('cmput', '204'), ('cmput', '365'), ('cmput', '174'), ('cmput', '340'), ('cmput', '256')]
#=========================================================================================================================

con = sqlite3.connect('scheduleSimple.db')
cur = con.cursor()

# Comment this line to prevent scraping new information to the db 
sdb.scrape_to_db(courses_requested)

possible_schedules = scheduler.course_combinations(schedule, courses_requested, course_names_selected, cur)

table_counter = 0

for course_combination in possible_schedules:

    schedule = [[], [], [], [], []]
    course_names_selected = []

    constructed_schedule, course_names_selected = scheduler.schedule_courses(course_combination, schedule, course_names_selected, cur)

    if len(course_names_selected) == len(courses_requested):
        btt.build_time_table(constructed_schedule, course_names_selected, table_counter)
        table_counter += 1