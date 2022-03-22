# from django.test import TestCase
#
# # Create your tests here.
# import datetime
#
#
# def get_time_schedule_by_requirements(r):
#     time_schedule = []
#     for x in range(r['numDaysRequested']):
#         _d = r['startDate'] + datetime.timedelta(x)
#         if _d.weekday() + 1 in r['daysRequested']:
#             if r['flexibleTime']:
#                 s_h, s_m, s_s = 0, 0, 0
#                 e_h, e_m, e_s = 23, 59, 59
#             else:
#                 s_h, s_m, s_s = r['startTime'].hour, r['startTime'].minute, r['startTime'].second
#                 e_h, e_m, e_s = r['endTime'].hour, r['endTime'].minute, r['endTime'].second
#             time_schedule.append({
#                 "start": datetime.datetime(_d.year, _d.month, _d.day, s_h, s_m, s_s),
#                 "end": datetime.datetime(_d.year, _d.month, _d.day, e_h, e_m, e_s)
#             })
#     return time_schedule
#
#
# r = {
#     "daysRequested": [3],
#     "startDate": datetime.date(2022, 3, 20),
#     "startTime": datetime.time(8, 0, 0),
#     "endTime": datetime.time(18, 0, 0),
#     "numDaysRequested": 5,
#     "flexibleTime": True
# }
# ex=get_time_schedule_by_requirements(r)[0]
# print(ex['start'].date()==ex['end'].date())
