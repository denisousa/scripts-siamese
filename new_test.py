from datetime import datetime, timedelta
import random

start_datetime = datetime.now()

date_list = []
for _ in range(4):
    random_minutes = random.randint(20, 30)
    random_seconds = random.randint(0, 59)
    random_timedelta = timedelta(minutes=random_minutes, seconds=random_seconds)
    new_datetime = start_datetime + random_timedelta
    date_list.append(new_datetime)
    
total_time = sum(date.hour * 3600 + date.minute * 60 + date.second for date in date_list)
average_time_seconds = total_time / len(date_list)
average_time = timedelta(seconds=average_time_seconds)

print("Lista de datetimes:")
for date in date_list:
    print(date)

print("\nTempo médio da lista:", average_time)
