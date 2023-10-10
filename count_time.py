from datetime import datetime, timedelta


def find_lines_with_runtime(filename):
    result = []
    with open(filename, 'r') as file:
        for line in file:
            if 'Runtime:' in line:
                result.append(line.strip().replace('Runtime: ', ''))
    return result


filename = 'grid_search_result_time.txt'
lines_with_runtime = find_lines_with_runtime(filename)

time_format = "%H:%M:%S.%f"
runtimes = [datetime.strptime(runtime, time_format) for runtime in lines_with_runtime]
runtimes = [timedelta(minutes=r.minute, seconds=r.second) for r in runtimes]

count = timedelta(seconds=0)
for r in runtimes:
    try:
        count += r
    except:
        print(r)

print(count)
