import copy
from epsilon import cn0_drop_monitor
from epsilon import cn0_spoofing_monitor
from epsilon import cn0_threshold_monitor
import io
import pynmea2
TEST_RX_STR = 'Test Receiver'
BASIC_MESSAGE = {'receiver_id': TEST_RX_STR, 'rxTime': 1, 'validity': True}
#测试单个通道的载噪比是否超过阈值，是则返回true否则返回false
if __name__ == '__main__':
    tester = cn0_spoofing_monitor.CnoSpoofingMonitor(receiver_id=TEST_RX_STR, channel_id='0.1', threshold=42)
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
            print(tester.metric,end=' ')
            print(tester.alarm)
            message['svs'] = [];
    tester.update(message)
    print(message)
    print(tester.metric,end=' ')
    print(tester.alarm)
    message['svs'] = [];

    f.close()
