import scrape_courses_to_db as sdb
import build_time_table as btt
import schedule_courses as scheduler
import schedule_combinations as sched_comb
import sqlite3
import itertools

has_conflict = False
schedule = [[], [], [], [], []]
course_names_selected = []

#=========================================================================================================================
# courses_requested = [('cmput', '204'), ('cmput', '301'), ('cmput', '365'), ('cmput', '366'), ('cmput', '411'), ('cmput', '414'), ('cmput', '415'), ('cmput', '428'), ('cmput', '455'), ('cmput', '466')]
courses_requested = [('cmput', '204'), ('cmput', '301'), ('cmput', '201'), ('cmput', '174'), ('cmput', '272')]
#=========================================================================================================================

con = sqlite3.connect('scheduleSimple.db')
cur = con.cursor()

# Comment this line to prevent scraping new information to the db 
sdb.scrape_to_db(courses_requested)

# course_sem_combs = sched_comb.get_combinations(courses_requested)
# # divider = ["        "]
# combo_counter = []
# counter_for_combo = 1

# for combo in course_sem_combs:
#     count = [counter]
#     print(count + divider + combo[0] + divider + combo[1])
#     counter += 1

# for course_combo in course_sem_combs:
#     courses_requested = course_combo[0]
#     combo_counter = [counter_for_combo]

possible_schedules = scheduler.course_combinations(schedule, courses_requested, course_names_selected, cur)

table_counter = 0

for course_combination in possible_schedules:

    schedule = [[], [], [], [], []]
    course_names_selected = []

    constructed_schedule, course_names_selected = scheduler.schedule_courses(course_combination, schedule, course_names_selected, cur)

    if len(course_names_selected) == len(courses_requested):
        btt.build_time_table(constructed_schedule, course_names_selected, table_counter)
        table_counter += 1