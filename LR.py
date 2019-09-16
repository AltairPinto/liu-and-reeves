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
        
def initial_solution(n, m, instance, cpu_1, cpu_2):    
    filename = "dataset1.txt"
    f = open(filename, 'r')
    l = f.readline().split()

    # number of jobs
    n = int(l[0])

    # number of machines
    m = int(l[1])
    # ith job's processing time at jth machine 
    cost = []
        
    for i in range(n):
        temp = []
        for j in range(m):
            temp.append(0)
        cost.append(temp)
        
    # print(cost)

    for i in range(n):
        line = f.readline().split()
        for j in range(int(len(line)/2)):
            cost[i][j] = int(line[2*j+1])
    print(cost)

def set_jobs():
    for index, line in enumerate(instance):
        if index == (n):
            break
        
        # print(line)
        item = line.split()

        # if (cpu_1.timestamp <= cpu_2.timestamp):
        #     cpu_1.jobs.append([int(item[0]), int(item[1]), int(item[2])])
        #     cpu_1.timestamp += int(item[0])
        # else:
        #     cpu_2.jobs.append([int(item[0]), int(item[1]), int(item[2])])
        #     cpu_2.timestamp += int(item[0])

        jobs.append([int(item[0]), int(item[1]), int(item[2])])
        
#                     | 1st column	     |   2nd column	  |   3rd column
# 1st line	          | number of jobs	 | 	              |
# 2nd and later lines |	processing time	 |    duedate	  |   tardiness weight

instance = open('./2m/wt40-2m-1.txt', 'r')
n = int(instance.readline()) # N number of jobs, because jobs are selected by n or i
m = 2                        # M number of machines, because machines are selected by m or j
jobs = []
cpu_1 = Cpu([], 0)           # To represent the CPU 1 and 2
cpu_2 = Cpu([], 0)

initial_solution(n, m, instance, cpu_1, cpu_2)

# Initial solution

# print('Jobs da CPU_1: ', cpu_1.jobs, ' com Time de: ', cpu_1.timestamp)

# print(jobs[0])
instance.close()
