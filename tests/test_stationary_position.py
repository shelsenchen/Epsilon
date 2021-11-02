import copy
from epsilon import cn0_drop_monitor
from epsilon import cn0_spoofing_monitor
from epsilon import cn0_threshold_monitor
from epsilon import stationary_position_monitor
import math
TEST_RX_STR = 'Test Receiver'
BASIC_MESSAGE = {'receiver_id': TEST_RX_STR, 'rxTime': 1, 'validity': True}
EARTH_RADIUS = 6378.137#地球半径
def torad(deg):
    return deg/180*math.acos(-1)
def get_coordinate(lat,ns,lng,ew):#纬度，南北，经度，东西
    lat=torad(lat);
    lng=torad(lng);
    x = EARTH_RADIUS * math.cos(lat) * math.cos(lng);
    y = EARTH_RADIUS * math.cos(lat) * math.sin(lng);
    z = EARTH_RADIUS * math.sin(lat);
    if ns=='S':
        y=-y;
    if ew=='W':
        x=-x;
    return [x,y,z]
#每输入一个位置，计算位置的平均值，如果新的位置与平均值差值绝对值超过阈值，报警
if __name__ == '__main__':
    tester = stationary_position_monitor.StationaryPositionMonitor(receiver_id=TEST_RX_STR, rejection_threshold=3,
                                           spoofing_threshold=5,
                                           min_detections=3,
                                           sample_window=4,
                                           monitor_timeout=60,
                                           num_init_samples=4)
    pos_data=[];

    f=open('test1.txt',encoding='utf-8')
    #去除第一组数组前不需要的数据
    while 1:
        line=f.readline();
        if line[0]=='-':
            break;
    while 1:
        line = f.readline()
        if not line:
            break;
        if line[0]!='$':
            continue;
        data=line.split(',');
        if data[0]=='$GNGGA':
            lat=math.floor(float(data[2]) / 100.0) + math.fmod(float(data[2]), 100.0)/60
            lng=math.floor(float(data[4]) / 100.0) + math.fmod(float(data[4]), 100.0)/60
            pos=get_coordinate(lat,data[3],lng,data[5])#纬度，南北，经度，东西转化为xyz坐标
            pos_data.append(pos)#将新的位置信息加入
    message = copy.deepcopy(BASIC_MESSAGE)
    for pos in pos_data:
        message['ecef_position'] = pos
        tester.update(message)
        print(tester._status['alarm'])
        print(tester._status['spoofing_flag'])
        message['rxTime'] += 1

    f.close()

