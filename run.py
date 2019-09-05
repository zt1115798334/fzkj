import logging
import pymysql
import requests
from fzkj_login import selenium_login
from pipelines import MySQLPipeLine

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S'
)

SemIdPatterns = [str(i) for i in range(54, 62) if i != 56]
SemesterPatterns = ['2017-2018-1', '2017-2018-2', '2017-2018-3', '2018-2019-1', '2018-2019-2', '2018-2019-3',
                    '2019-2020-1']
ClassTimePatterns = [96, 122, 168, 194, 228]
WeekDayPatterns = ['OnMonday', 'OnTuesday', 'OnWednesday', 'OnThursday', 'OnFriday', 'OnSaturday', 'OnSunday']


def parse(cookies, student_id):
    for i, semId in enumerate(SemIdPatterns):
        semester = SemesterPatterns[i]
        logging.info(f'开始爬取{semester}学期的课程表')
        data = {
            'action': 'getTeacherTimeTable',
            'isShowStudent': '1',
            'semId': semId,
            'testTeacherTimeTablePublishStatus': '1',
        }
        r = requests.post('https://jw.cidp.edu.cn/Teacher/TimeTableHandler.ashx', cookies=cookies, data=data)
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
                    'student_id': student_id,
                    'semester': semester,
                    'weekly_times': weekly_times,
                    'week': week,
                    'class_times': class_times,
                    'curriculum': curriculum
                }


def main():
    db = pymysql.connect(host='152.136.145.193', user='root', password='School@2018', port=3306, db='free_school')
    # db = pymysql.connect(host='127.0.0.1', user='root', password='Root@2018', port=3306, db='free_school')
    cursor = db.cursor()
    sql = "SELECT student_id,student_pwd FROM t_school_administration WHERE fresh_state = 0 and abnormal_state = 0 and school_code = 2 and usable_state = 0 GROUP BY student_id,student_pwd"
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        cookies = selenium_login(row[0], row[1])
        logging.info(f'开始爬取学号为{row[0]}的课程表')
        for res in parse(cookies, row[0]):
            MySQLPipeLine.save_to_mysql(res)
        logging.info(f'学号为{row[0]}的课程表爬取完毕')
        cursor.execute("UPDATE t_school_administration SET fresh_state = 1 WHERE student_id = '%s'" % (row[0]))
        db.commit()
    db.close()


if __name__ == '__main__':
    main()
