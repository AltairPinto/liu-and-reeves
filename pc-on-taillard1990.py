from pc import ils, _c_sum
import taillard1990

instances = {
    'ta001': taillard1990.ta001,
    'ta002': taillard1990.ta002,
    'ta003': taillard1990.ta003,
    'ta004': taillard1990.ta004,
    'ta005': taillard1990.ta005,
    'ta006': taillard1990.ta006,
    'ta007': taillard1990.ta007,
    'ta008': taillard1990.ta008,
    'ta009': taillard1990.ta009,
    'ta010': taillard1990.ta010,
}

for name, instance in instances.items():
    print(name, ':', sep='')

    time = 60.0  # seconds
    sched = ils(instance, time)

    print("\tsched = ", sched.tolist())
    print("\tC_sum = ", _c_sum(instance, sched), end='\n\n')
