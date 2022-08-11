day_letters = {"M" : 0, "T" : 1, "W" : 2, "H" : 3, "F" : 4}

#=========================================================================================================================

def military_time(var_time):
    return int(str(var_time).replace(":",""))


def schedule_courses(schedule, course_names_selected, cur):
    for db_course in cur.execute('''SELECT * FROM cmput_courses WHERE section_type = "LECTURE" AND start_date = "2023-01-05"'''):
        has_conflict = False

        if db_course[0] in course_names_selected:
            continue

        for a_day in list(db_course[7]):
            for course in schedule[day_letters[a_day]]:

                existing_start_time = military_time(course[1])
                existing_end_time = military_time(course[2])

                db_course_start_time = military_time(db_course[8])
                db_course_end_time = military_time(db_course[9])

                if db_course_start_time <= existing_end_time and db_course_end_time >= existing_start_time:
                    has_conflict = True

        if not has_conflict:
            for a_day in list(db_course[7]):
                schedule[day_letters[a_day]].append([db_course[0], db_course[8], db_course[9], db_course[3]])
            course_names_selected.append(db_course[0])

    return schedule, course_names_selected
    
#=========================================================================================================================