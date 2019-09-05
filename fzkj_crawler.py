import requests
from fzkj_login import selenium_login
from pipelines import MySQLPipeLine

SemIdPatterns = ['59', '58', '55', '54']
# '2018-2019学年度春季学期','2018-2019学年度秋季学期','2017-2018学年度春季学期','2017-2018学年度秋季学期',
SemesterPatterns = ['2018-2019-2', '2018-2019-1', '2017-2018-2', '2017-2018-1']
ClassTimePatterns = [96, 122, 168, 194, 228]
WeekDayPatterns = ['OnMonday', 'OnTuesday', 'OnWednesday', 'OnThursday', 'OnFriday', 'OnSaturday', 'OnSunday']


def parse(cookies):
    for i, semId in enumerate(SemIdPatterns):
        semester = SemesterPatterns[i]
        print(f'开始爬取{semester}学期的课程表')
        data = {
            'action': 'getTeacherTimeTable',
            'isShowStudent': '1',
            'semId': semId,
            'testTeacherTimeTablePublishStatus': '1',
        }
        r = requests.post('http://jw.cidp.edu.cn/Teacher/TimeTableHandler.ashx', cookies=cookies, data=data)
        res = r.json()['Data']
        for course in res:
            for week_num in range(course['WeekStart'], course['WeekEnd'] + 1, course['WeekInterval'] + 1):
                weekly_times = week_num
                for week_day in WeekDayPatterns:
                    if course[week_day]:
                        week = week_day[2:5].lower()
                for index, class_num in enumerate(ClassTimePatterns):
                    if course['TimeSlotStart'] == class_num:
                        class_times = index + 1
                curriculum = course['LUName'] + course['Remark']
                yield {
                    'student_id': '175041108',
                    'semester': semester,
                    'weekly_times': weekly_times,
                    'week': week,
                    'class_times': class_times,
                    'curriculum': curriculum
                }


if __name__ == '__main__':
    cookies = selenium_login()
    for data in parse(cookies):
        MySQLPipeLine.save_to_mysql(data)
