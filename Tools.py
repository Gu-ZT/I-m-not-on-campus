import sys

from tools import dailyInspectionReport, healthCheckIn, locationCheckIn

tip = '''1.日检日报
2.健康打卡
3.定位打卡
0.退出\n'''

argv = sys.argv


def dowhile():
    while True:
        choose = input(tip)
        if choose == '0':
            exit()
        elif choose == '1':
            dailyInspectionReport.answer().run()
        elif choose == '2':
            healthCheckIn.answer().run()
        elif choose == '3':
            locationCheckIn.main_handler("__main__")
        else:
            pass


if __name__ == '__main__':
    try:
        get = argv[1]
        if get == 'daily':
            dailyInspectionReport.answer().run()
        elif get == 'health':
            healthCheckIn.answer().run()
        elif get == 'location':
            locationCheckIn.main_handler("__main__")
        else:
            dowhile()
    except:
        dowhile()
