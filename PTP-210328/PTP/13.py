import numpy as np
from decimal import Decimal
import matplotlib as mpl
import matplotlib.pyplot as plt

# 设定 t3 - t2 之间的误差是 [0.01, 0.34, 0.23, 0.03, 0.12, 0.14, 0.19, 0.6] 是标准误差时间
# 则 从时钟算下来的误差是 标注误差时间 * self.getSlaveClock()
time = [0.01, 0.34, 0.23, 0.03, 0.12, 0.14, 0.19, 0.6]

class Moster():
    def __init__(self, tm=1):
        self.__slaves = []

        # tm 是周期和主时钟的币制，cycle 是发送周期
        self.tm = tm
        self.cycle = 0
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
        print(f'[master]: got {slave.slaveName} message, send Delay_Resp')
        slave.countOffset(self, self.tm)


class Slave():
    def __init__(self, master, slaveName, ts=0.9):
        self.master = master
        self.slaveName = slaveName
        self.master.register(self)
        # slave的时钟
        self.offsetAll = 0
        self.ts = ts

        # 记录 T1 T2 T3 T4
        self.timeData = []
        self.timeReallData = []
        # 记录随机生成的 Delay; cycle为标准时间; cycle * ts 为时钟偏移
        self.realDelay = [[0.1, 0.1]]
        self.cycle = -777
        # 记录 offset
        self.offset = []
        self.offsetPrint = []

    def reInit(self, cycle):
        self.cycle = cycle
        self.timeData = []
        self.timeMasterData = []

    def setOffset(self, master, T):
        self.offset.append((master.tm - self.ts) * T)

    # 获得经过修整的 从时钟时间
    def getSlaveClock(self):
        return self.ts * self.cycle - self.offsetAll

    # 获得没有经过修正的从时钟时间:
    def getReallyClock(self):
        return self.ts * self.cycle


    def sendDelay_Req(self, master, cycle, T1):
        # 初始化数据仓库
        self.reInit(cycle)

        print(f'[{self.slaveName}]: got Sync, send Delay_Req')
        self.timeData.append(T1)
        self.timeMasterData.append(cycle)

        # 计算T2，添加 T2 = slave时钟 * cycle + delay
        print('=======>', self.getSlaveClock())
        T2 = self.getSlaveClock() + self.realDelay[0][0] * self.ts
        self.timeData.append(T2)
        # T2r = self.timeData[0] + self.realDelay[0][0]
        # self.timeMasterData.append(T2r)

        # 计算T3，添加T3 = T2 + 传输流时延 + 发送前处理时延
        # 一段传输流时延 = np.random() / 2 ； 立即发送前时延 = 0
        # T3 = self.timeData[1] + 0 + 0
        T3 = self.timeData[1] + (np.random.random() - 0.6)
        self.timeData.append(T3)
        # T3r = self.timeMasterData[1] + 0 + 0
        # self.timeMasterData.append(T3r)

        # print(f'[{self.slaveName}]: cycle:{cycle}, time T:{self.timeData}.')
        self.master.sendDelay_Resp(self)

    def countOffset(self, master, tm):
        # 计算T4，添加T4 = T2 + (T3 - T2) + slave时钟 * delay
        # 计算T4，添加 T4 = slave时钟 * (cycle + delay) + 0 + 0 + slave时钟 * (delay)
        T4 = tm * (self.cycle + self.realDelay[0][0] + self.realDelay[0][1]) + 0 + 0
        # T4 = self.timeData[2] + self.realDelay[0][1] - (master.tm - self.ts) * self.timeData[2]
        self.timeData.append(T4)
        # T4r = self.timeMasterData[2] + self.realDelay[0][1]
        # offset =
        offset = (- self.timeData[0] + self.timeData[1] + self.timeData[2] - self.timeData[3]) / 2
        self.offset.append(offset)
        self.offsetAll = self.offsetAll + offset

        print(self.timeMasterData)
        print(self.timeData)
        print(f'offset: {offset}')
        # 将数据传递给 master.count
        master.count.appendTheoryMasterClock(master.getMasterClock())
        master.count.appendReallySlaveClock(self.getReallyClock())
        master.count.appendCountSlaveClock(self.getSlaveClock())
        master.count.appendCountOffset(master.getMasterClock() - (self.getSlaveClock() + offset))
        self.offsetPrint.append(master.getMasterClock() - (self.getSlaveClock() + offset))

class Count():
    def __init__(self):
        self.sycle = 0
        self.theoryMasterClock = []
        self.reallySlaveClock = []
        self.countSlaveClock = []
        self.countOffset = []

    def appendTheoryMasterClock(self, t):
        self.theoryMasterClock.append(t)

    def appendReallySlaveClock(self, t):
        self.reallySlaveClock.append(t)

    def appendCountSlaveClock(self, t):
        self.countSlaveClock.append(t)

    def appendCountOffset(self, offset):
        self.countOffset.append(offset)

if __name__ == '__main__':
    print("start")
    master = Moster(1.0)
    slave1 = Slave(master, "slave1", 0.9)
    slave2 = Slave(master, "slave1", 0.8)
    slave3 = Slave(master, "slave1", 0.6)
    slave4 = Slave(master, "slave1", 0.5)
    slave5 = Slave(master, "slave1", 1.1)
    slave6 = Slave(master, "slave1", 1.2)
    slave7 = Slave(master, "slave1", 1.3)
    slave8 = Slave(master, "slave1", 1.4)
    # slave2 = Slave(master, "slave2")
    # print(master.showSlaves())

    # master send Sync info.
    for i in range(10):
        master.sendSync()

    print(slave1.offset)
    # plt.plot([0, 1, 2, 3, 4, 5, 6, 7, 8], master.count.theoryMasterClock, master.count.theorySlaveClock)
    # plt.xlim(0, 10)
    # plt.ylim(0, 10)


    x = np.linspace(0, 10, 10)
    # ============
    plt.plot(x, slave1.offsetPrint, label='offset1')
    plt.plot(x, slave2.offsetPrint, label='offset2')
    plt.plot(x, slave3.offsetPrint, label='offset3')
    plt.plot(x, slave4.offsetPrint, label='offset4')
    plt.plot(x, slave5.offsetPrint, label='offset5')
    plt.plot(x, slave6.offsetPrint, label='offset6')
    plt.plot(x, slave7.offsetPrint, label='offset7')
    plt.plot(x, slave8.offsetPrint, label='offset8')
    # ============
    # y1 = master.count.theoryMasterClock
    # y2 = master.count.reallySlaveClock
    # y3 = master.count.countSlaveClock
    #
    # plt.plot(x, y1, ':b', label='Master')
    # plt.plot(x, y2, label='Slave')
    # plt.plot(x, y3, label='Slave-offset')

    # y4 = master.count.countOffset
    # plt.plot(x, y4, label='offset')
    plt.axhline(y=0, ls=":", c="black")
    plt.ylim(-1, 1)

    plt.legend()
    plt.show()
    print(slave1.offset)

    # print(y1)
    # print(y2)
    # print(y3)
    print("end")
