# from datetime import datetime, timedelta
# from dateutil.relativedelta import relativedelta

# def get_next_recurrence(self):
#         match self.recurring_freq:
#             case RecurringFrequency.ONE_TIME:
#                 return "This transaction is one-time only"
#             case RecurringFrequency.DAILY:
#                 self.date = self.date + timedelta(days=1)
#             case RecurringFrequency.WEEKLY:
#                 self.date = self.date + timedelta(days=7)
#             case RecurringFrequency.MONTHLY:
#                 self.date = self.date + relativedelta(months=1)
#             case RecurringFrequency.YEARLY:
#                 self.date = self.date + relativedelta(years=1)
#             case _:
#                 return "Unknown recurring frequency!"
#         return f"Next recurrence updated successfully: New date is {self.date.strftime("%d-%m-%Y")}"