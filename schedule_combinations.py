def combination(n, courses_requested):
    if n<=0:
        yield []
        return
    for i in range(len(courses_requested)):
        c_num = courses_requested[i:i+1]
        for a_num in combination(n-1, courses_requested[i+1:]):
            yield c_num + a_num


def get_combinations(courses_requested):
    n = 5
    result = combination(n, courses_requested)
    course_sem_combs = []
    for e in result:
        course_sem_combs.append((e, list(set(courses_requested) - set(e))))
    return course_sem_combs
