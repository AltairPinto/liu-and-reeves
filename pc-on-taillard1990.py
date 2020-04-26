from pc import ils, _c_sum
from taillard1990 import ta001

instances = {
    'ta001': ta001
}

for name, instance in instances.items():
    print(name, ':', sep='')

    time = 60.0  # seconds
    sched = ils(instance, time)

    print("\tsched = ", sched.tolist())
    print("\tC_sum = ", _c_sum(instance, sched), end='\n\n')
