day_letters = ["M", "T", "W", "H", "F"]

def convert_day(day):
    days = list(day)
    return_days = []
    for a_day in days:
        return_days.append(day_letters.index(a_day))
    return return_days

#=========================================================================================================================
def schedule_courses(schedule, course_names_selected, cur):
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
    return schedule, course_names_selected