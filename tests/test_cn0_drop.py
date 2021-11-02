import copy
from epsilon import cn0_drop_monitor
from epsilon import cn0_spoofing_monitor
from epsilon import cn0_threshold_monitor
import io
import pynmea2
TEST_RX_STR = 'Test Receiver'
BASIC_MESSAGE = {'receiver_id': TEST_RX_STR, 'rxTime': 1, 'validity': True}
#计算载噪比在一个时间窗内的下降值，如果下降值过大超过一个阈值，则报警
if __name__ == '__main__':

    tester = cn0_drop_monitor.CnoDropJammingMonitor(receiver_id=TEST_RX_STR, threshold=5, time_window=5)
    message = copy.deepcopy(BASIC_MESSAGE)
    message['svs'] = [];

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
        if line[0]!='$' and line[0]!='-':
            continue;
        data=line.split(',');
        if data[0]=='$BDCHL':
            dic = {'gnssId': 0, 'svid': float(data[2]), 'cno': float(data[6]), 'qualityInd': 5};
            message['svs'].append(dic);
        elif data[0]=='$GPCHL':
            dic = {'gnssId': 1, 'svid': float(data[2]), 'cno': float(data[6]), 'qualityInd': 5};
            message['svs'].append(dic);
        elif data[0]=='$GNDHV':
            rxtime=float(data[1])
            message['rxTime'] = rxtime
        elif data[0][0]=='-':
            tester.update(message)
            print(message)
            message['svs'] = [];
    tester.update(message)
    print(message)
    message['svs'] = [];
    print(tester.alarm)#是否报警 为什么是只要有一个没有变化，就一定不会报警了
    print(tester._drops)#跳变值
    f.close()
