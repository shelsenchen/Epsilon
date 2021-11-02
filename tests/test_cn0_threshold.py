import copy
from epsilon import cn0_drop_monitor
from epsilon import cn0_spoofing_monitor
from epsilon import cn0_threshold_monitor

TEST_RX_STR = 'Test Receiver'
BASIC_MESSAGE = {'receiver_id': TEST_RX_STR, 'rxTime': 1, 'validity': True}
#计算每个时间所有载噪比的最大值，如果小于某一阈值则判定干扰存在
if __name__ == '__main__':

    tester = cn0_threshold_monitor.CnoThresholdJammingMonitor(receiver_id=TEST_RX_STR, threshold=20,
                                                                  time_window=5)
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
            print(message)
            tester.update(message)
            print(tester.metric, end=' ')
            print(tester.alarm)
            message['svs'] = [];
    print(message)
    tester.update(message)
    message['svs'] = [];
    print(tester.metric,end=' ')
    print(tester.alarm)#是否报警

    f.close()
