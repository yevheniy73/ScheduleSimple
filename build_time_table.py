from bs4 import BeautifulSoup
import os

course_colors = ["#ff9999", "#99FF99", "#ff99cc", "#FFFF99", "#99CCFF", "#CC99FF", "#CC9999", "#CCFF99", "#ffcc99"]
day_letters = ["M", "T", "W", "H", "F"]

#=========================================================================================================================

def add_course_to_table(sched_block, course, course_names_selected, time_difference):
    sched_block.string = f"{course[0]} LEC {course[3]}"
    sched_block['class'] = "CHEDSTD"
    sched_block['height'] = time_difference
    sched_block['width'] = "100"
    sched_block['rowspan'] = (time_difference / 15)
    sched_block['colspan'] = "2"
    sched_block['bgcolor'] = course_colors[course_names_selected.index(course[0])]
    sched_block['onClick'] = f'window.open("https://apps.ualberta.ca/catalogue/course/{course[0].split()[0]}/{course[0].split()[1]}")'
    return None

#=========================================================================================================================

def hide_block(html_sched_text, day_name, sched_hour, sched_minute, AB):
    sched_block = html_sched_text.find("td", {"id": f"{day_name}{sched_hour}{sched_minute}{AB}"})
    sched_block['class'] = sched_block.get('class', []) + ['HIDE_ME']

#=========================================================================================================================

def build_time_table(schedule, course_names_selected):
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
            add_course_to_table(sched_block, course, course_names_selected, time_difference)

            hide_block(html_sched_text, day_name, course_start_time[:2], course_start_time[-2:], "b")

            sched_pointer = 15

            while sched_pointer < time_difference:

                sched_hour = course_start_time[:2]
                sched_minute = int(course_start_time[-2:]) + sched_pointer
                extra_hour, extra_minute = divmod(sched_minute, 60)

                sched_hour = str(int(course_start_time[:2]) + extra_hour).zfill(2)
                sched_minute = str(extra_minute).zfill(2)

                hide_block(html_sched_text, day_name, sched_hour, sched_minute, "a")
                hide_block(html_sched_text, day_name, sched_hour, sched_minute, "b")

                sched_pointer += 15

    with open("time_table.html", "w") as file:
        file.write(str(html_sched_text.prettify()))
    return None

#=========================================================================================================================