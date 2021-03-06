from pc import ils, _c_sum
import taillard1990
import sys

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
    'ta011': taillard1990.ta011,
    'ta012': taillard1990.ta012,
    'ta013': taillard1990.ta013,
    'ta014': taillard1990.ta014,
    'ta015': taillard1990.ta015,
    'ta016': taillard1990.ta016,
    'ta017': taillard1990.ta017,
    'ta018': taillard1990.ta018,
    'ta019': taillard1990.ta019,
    'ta020': taillard1990.ta020,
    'ta021': taillard1990.ta021,
    'ta022': taillard1990.ta022,
    'ta023': taillard1990.ta023,
    'ta024': taillard1990.ta024,
    'ta025': taillard1990.ta025,
    'ta026': taillard1990.ta026,
    'ta027': taillard1990.ta027,
    'ta028': taillard1990.ta028,
    'ta029': taillard1990.ta029,
    'ta030': taillard1990.ta030,
    'ta031': taillard1990.ta031,
    'ta032': taillard1990.ta032,
    'ta033': taillard1990.ta033,
    'ta034': taillard1990.ta034,
    'ta035': taillard1990.ta035,
    'ta036': taillard1990.ta036,
    'ta037': taillard1990.ta037,
    'ta038': taillard1990.ta038,
    'ta039': taillard1990.ta039,
    'ta040': taillard1990.ta040,
    'ta041': taillard1990.ta041,
    'ta042': taillard1990.ta042,
    'ta043': taillard1990.ta043,
    'ta044': taillard1990.ta044,
    'ta045': taillard1990.ta045,
    'ta046': taillard1990.ta046,
    'ta047': taillard1990.ta047,
    'ta048': taillard1990.ta048,
    'ta049': taillard1990.ta049,
    'ta050': taillard1990.ta050,
    'ta051': taillard1990.ta051,
    'ta052': taillard1990.ta052,
    'ta053': taillard1990.ta053,
    'ta054': taillard1990.ta054,
    'ta055': taillard1990.ta055,
    'ta056': taillard1990.ta056,
    'ta057': taillard1990.ta057,
    'ta058': taillard1990.ta058,
    'ta059': taillard1990.ta059,
    'ta060': taillard1990.ta060,
    'ta061': taillard1990.ta061,
    'ta062': taillard1990.ta062,
    'ta063': taillard1990.ta063,
    'ta064': taillard1990.ta064,
    'ta065': taillard1990.ta065,
    'ta066': taillard1990.ta066,
    'ta067': taillard1990.ta067,
    'ta068': taillard1990.ta068,
    'ta069': taillard1990.ta069,
    'ta070': taillard1990.ta070,
    'ta071': taillard1990.ta071,
    'ta072': taillard1990.ta072,
    'ta073': taillard1990.ta073,
    'ta074': taillard1990.ta074,
    'ta075': taillard1990.ta075,
    'ta076': taillard1990.ta076,
    'ta077': taillard1990.ta077,
    'ta078': taillard1990.ta078,
    'ta079': taillard1990.ta079,
    'ta080': taillard1990.ta080,
    'ta081': taillard1990.ta081,
    'ta082': taillard1990.ta082,
    'ta083': taillard1990.ta083,
    'ta084': taillard1990.ta084,
    'ta085': taillard1990.ta085,
    'ta086': taillard1990.ta086,
    'ta087': taillard1990.ta087,
    'ta088': taillard1990.ta088,
    'ta089': taillard1990.ta089,
    'ta090': taillard1990.ta090,
    'ta091': taillard1990.ta091,
    'ta092': taillard1990.ta092,
    'ta093': taillard1990.ta093,
    'ta094': taillard1990.ta094,
    'ta095': taillard1990.ta095,
    'ta096': taillard1990.ta096,
    'ta097': taillard1990.ta097,
    'ta098': taillard1990.ta098,
    'ta099': taillard1990.ta099,
    'ta100': taillard1990.ta100,
    'ta101': taillard1990.ta101,
    'ta102': taillard1990.ta102,
    'ta103': taillard1990.ta103,
    'ta104': taillard1990.ta104,
    'ta105': taillard1990.ta105,
    'ta106': taillard1990.ta106,
    'ta107': taillard1990.ta107,
    'ta108': taillard1990.ta108,
    'ta109': taillard1990.ta109,
    'ta110': taillard1990.ta110,
    'ta111': taillard1990.ta111,
    'ta112': taillard1990.ta112,
    'ta113': taillard1990.ta113,
    'ta114': taillard1990.ta114,
    'ta115': taillard1990.ta115,
    'ta116': taillard1990.ta116,
    'ta117': taillard1990.ta117,
    'ta118': taillard1990.ta118,
    'ta119': taillard1990.ta119,
    'ta120': taillard1990.ta120,
}

bks = [ 14033, 15151, 13301, 15447, 13529, 13123, 13548, 13948, 14295, 12943, 
20911, 22440, 19833, 18710,18541, 19245, 18363, 20241, 20330, 21320, 33623, 
31587, 33920, 31611, 34557, 32564, 32922, 32412, 33600, 32262, 64802, 68051, 
63162, 68226, 69351, 66841, 66253, 64332, 62981, 68770, 87114, 82820, 79931, 
86446, 86377, 86587, 88750, 86727, 85441, 87998, 125831, 119247, 116459, 120261,
118184, 120586, 122880, 122489, 121872, 123954, 253266, 242281, 237832, 227738,
240301, 232342, 240366, 230945, 247921, 242933, 298385, 274384, 288114, 301044,
284681, 269686, 279463, 290908, 301970, 291283, 365463, 372449, 370027, 372393,
368915, 370908, 373408, 384525, 374423, 379296, 1046314, 1034195, 1046902,1030481,
1034027, 1006195, 1053051, 1044875, 1026137, 1030299, 1227733, 1245271, 1269673,
1238349, 1227214, 1227604, 1243707, 1246123, 1234936, 1250596, 6698656, 6770735,
6739645, 6785991, 6729486, 6724085, 6691468, 6783916, 6711305, 6755722 ]

# 90mn milisegundos, como ta no artigo do ILS
time = lambda p: .4 * p.shape[0] * p.shape[1]  # seconds

# print('instance', 'schedule', 'flowtime', sep='\t')
print('instance', 'flowtime', 'bks', 'gap ((flowtime - bks) / bks)', sep='\t')
i = 0
for name, instance in instances.items():
    # print(name, file=sys.stderr)
    sched = ils(instance, time(instance))
    # print(name, sched.tolist(), _c_sum(instance, sched), sep='\t')
    print(name, _c_sum(instance, sched), bks[i], (_c_sum(instance, sched) - bks[i])/ bks[i] , sep='\t')
    i+=1

