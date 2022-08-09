from bs4 import BeautifulSoup
import os

course_colors = ["#ff9999", "#99FF99", "#ff99cc", "#FFFF99", "#99CCFF", "#CC99FF", "#CC9999", "#CCFF99", "#ffcc99"]
day_letters = ["M", "T", "W", "H", "F"]

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

            while sched_pointer < time_difference:

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

    with open("time_table.html", "w") as file:
        file.write(str(html_sched_text.prettify()))
    return None

#=========================================================================================================================

# print out the schedule at the end
# for i in range(len(schedule)):
#     print(day_letters[i])
#     for j in range(len(schedule[i])):
#         print(schedule[i][j])
#     print("")