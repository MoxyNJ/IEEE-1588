import numpy as np
from decimal import Decimal
import matplotlib as mpl
import matplotlib.pyplot as plt


class Moster():
    def __init__(self, tm=1):
        self.__slaves = []

        # tm 是周期和主时钟的币制，cycle 是发送周期
        self.tm = tm
        self.cycle = -1
        # 实例化一个 count
        self.count = Count()

    def getMasterClock(self):
        return self.tm * self.cycle

    def register(self, slave):
        self.__slaves.append(slave)

    def deleteS(self, slave):
        for index, value in enumerate(self.__slaves):
            # print(index, value)
            if value == slave:
                return self.__slaves.pop(index)
        return False

    def showSlaves(self):
        list = []
        for slave in self.__slaves:
            list.append(slave.slaveName)
        return list

    def sendSync(self):
        print('[master]: send Sync')

        self.cycle = self.cycle + 1
        for slave in self.__slaves:
            slave.sendDelay_Req(self, self.cycle, self.getMasterClock())

    def sendDelay_Resp(self, slave):
        print(f'[master]: got {slave.slaveName} messages, send Delay_Resp')
        slave.countOffset(self)


class Slave():
    def __init__(self, master, slaveName, ts=0.9):
        self.master = master
        self.slaveName = slaveName
        self.Stime = 0
        self.master.register(self)
        # slave的时钟
        self.ts = ts

        # 记录 T1 T2 T3 T4
        self.timeData = []
        self.timeReallData = []
        # 记录随机生成的 Delay; cycle为标准时间; cycle * ts 为时钟偏移
        self.realDelay = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        self.cycle = -777
        # 记录 offset
        self.offset = []

    def reInit(self, cycle):
        self.cycle = cycle
        self.timeData = []
        self.timeMasterData = []

    def setOffset(self, master, T):
        self.offset.append((master.tm - self.ts) * T)

    def getSlaveClock(self):
        return self.ts * self.cycle

    def sendDelay_Req(self, master, cycle, T1):
        # 初始化数据仓库
        self.reInit(cycle)

        print(f'[{self.slaveName}]: got Sync, send Delay_Req')
        self.timeData.append(T1)
        self.timeMasterData.append(cycle)

        # ===========================================
        # 看到这里了，要一步一步过，排查问题。
        # ===========================================

        # 计算T2，添加T2
        T2 = self.timeData[0] + self.realDelay[0][0] + (master.tm - self.ts) * self.timeData[0]
        self.timeData.append(T2)
        T2r = self.timeData[0] + self.realDelay[0][0]
        self.timeMasterData.append(T2r)

        # 计算T3，添加T3
        # 一段传输流时延 = np.random() / 2 ； 立即发送前时延 = 0
        T3 = self.timeData[1] + 0 + 0
        self.timeData.append(T3)
        T3r = self.timeMasterData[1] + 0 + 0
        self.timeMasterData.append(T3r)

        # print(f'[{self.slaveName}]: cycle:{cycle}, time T:{self.timeData}.')
        self.master.sendDelay_Resp(self)

    def countOffset(self, master):
        # 计算T4，添加T4
        T4 = self.timeData[2] + self.realDelay[0][1] - (master.tm - self.ts) * self.timeData[2]
        self.timeData.append(T4)
        T4r = self.timeMasterData[2] + self.realDelay[0][1]

        offset = ((self.timeData[1] - self.timeData[0]) + (self.timeData[2] - self.timeData[3])) / 2
        self.offset.append(offset)

        # ================================
        # 问题：时间 T1 到 T4 没有记录正确📝
        # ================================
        print(self.timeMasterData)
        print(self.timeData)
        print(f'offset: {offset}')
        # 将数据传递给 master.count
        master.count.appendTheoryMasterClock(master.getMasterClock())
        master.count.appendTheorySlaveClock(self.getSlaveClock())
        master.count.appendCountSlaveClock(self.getSlaveClock() + offset)
        master.count.appendCountOffset(master.getMasterClock() - (self.getSlaveClock() + offset))

class Count():
    def __init__(self):
        self.sycle = 0
        self.theoryMasterClock = []
        self.theorySlaveClock = []
        self.countSlaveClock = []
        self.countOffset = []

    def appendTheoryMasterClock(self, t):
        self.theoryMasterClock.append(t)

    def appendTheorySlaveClock(self, t):
        self.theorySlaveClock.append(t)

    def appendCountSlaveClock(self, t):
        self.countSlaveClock.append(t)

    def appendCountOffset(self, offset):
        self.countOffset.append(offset)

if __name__ == '__main__':
    print("start")
    master = Moster(1.5)
    slave1 = Slave(master, "slave1")
    # slave2 = Slave(master, "slave2")
    # print(master.showSlaves())

    # master send Sync info.
    for i in range(8):
        master.sendSync()

    print(slave1.offset)
    # plt.plot([0, 1, 2, 3, 4, 5, 6, 7, 8], master.count.theoryMasterClock, master.count.theorySlaveClock)
    # plt.xlim(0, 10)
    # plt.ylim(0, 10)

    x = np.linspace(0, 8, 8)
    y1 = master.count.theoryMasterClock
    y2 = master.count.theorySlaveClock
    y3 = master.count.countSlaveClock
    y4 = master.count.countOffset
    plt.plot(x, y1, ':b', label='Master')
    plt.plot(x, y2, label='Slave')
    plt.plot(x, y3, label='Slave-offset')
    plt.legend()
    plt.show()

    # print(y1)
    # print(y2)
    # print(y3)
    print("end")
