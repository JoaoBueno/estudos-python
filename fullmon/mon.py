import psutil

# print("psutil.cpu_count()",psutil.cpu_count())
# print("psutil.cpu_freq()",psutil.cpu_freq())
# print("psutil.cpu_percent()",psutil.cpu_percent())
# print("psutil.cpu_stats()",psutil.cpu_stats())
# print("psutil.cpu_times()",psutil.cpu_times())
# print("psutil.cpu_times_percent()",psutil.cpu_times_percent())
# print("psutil.virtual_memory()",psutil.virtual_memory())
# print("psutil.swap_memory()",psutil.swap_memory())
# print("psutil.disk_partitions()",psutil.disk_partitions())
# print("psutil.disk_usage('c:\\')",psutil.disk_usage('c:\\'))
# print("psutil.disk_io_counters()",psutil.disk_io_counters())
# print("psutil.disk_io_counters(perdisk=True)",psutil.disk_io_counters(perdisk=True))
# print("psutil.net_io_counters()",psutil.net_io_counters())
# print("psutil.net_io_counters(pernic=True)",psutil.net_io_counters(pernic=True))
# print("psutil.net_connections()",psutil.net_connections())
p = psutil.Process()

with p.oneshot():
    p.name()  # execute internal routine once collecting multiple info
    p.cpu_times()  # return cached value
    p.cpu_percent()  # return cached value
    p.create_time()  # return cached value
    p.ppid()  # return cached value
    p.status()  # return cached value

print(p)
print("p.open_files()",p.open_files())

print('Lista de processos em execução:')
for proc in psutil.process_iter():
    # info = proc.as_dict(attrs=['pid', 'name'])
    info = proc.as_dict()
    # print('Processo: {} (PID: {})'.format(info['pid'], info['name']))
    print(info)
    