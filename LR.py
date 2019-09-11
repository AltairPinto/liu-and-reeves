class Job: 
    'Class to represent a job' # doc
    def __init__(self, processing_time, duedate, tardiness_weight): 
        self.processing_time  = processing_time 
        self.duedate = duedate 
        self.tardiness_weight  = tardiness_weight

class Cpu: 
    'Class to represent a CPU' # doc
    def __init__(self, jobs, timestamp): 
        self.jobs = jobs 
        self.timestamp = timestamp 
        
#                     | 1st column	     |   2nd column	  |   3rd column
# 1st line	          | number of jobs	 | 	              |
# 2nd and later lines |	processing time	 |    duedate	  |   tardiness weight

instance = open('./2m/wt40-2m-1.txt', 'r')
num_of_jobs = int(instance.readline()) # N jobs, because jobs are selected by n or i
num_of_machines = 2                    # M machines, because machines are selected by m or j
jobs = []
cpu_1 = Cpu([], 0)                     # To represent the CPU 1 and 2
cpu_2 = Cpu([], 0)

for index, line in enumerate(instance):
    if index == (num_of_jobs):
        break
    
    print(line)
    item = line.split()

    jobs.append(Job(int(item[0]), int(item[1]), int(item[2])))

#print(jobs.__init__)