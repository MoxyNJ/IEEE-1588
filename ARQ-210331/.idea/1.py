import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# 求 erfc
#erfc = math.erfc(x)

# P 误码率
# SNR 信噪比
# P = 1 / 2 * erfc *  sqrt(10 ^ (0.1 * SNR))

class getSNR:
    def __init__(self):
        self.res1 = []
        self.res2 = []

    def getP1(self, SNR, x):
        temp = []
        for i in range(36):
            j =  i * i
            temp.append(j)
        temp = list(reversed(temp))
        print(temp)
        erfc = math.erfc(x)
        t1 = math.pow(10, (0.1 * SNR))
        t2 = - math.sqrt(t1)
        t3 = np.abs(1 / (1 + 0.1j * SNR * (SNR)))
        # return 0.5 * x * t2 * t3
        return t3

    def getP2(self, SNR, x):
        erfc = math.erfc(x)
        t1 = math.pow(10, (0.1 * SNR))
        t2 = - math.sqrt(t1)
        t3 = np.abs(1 / (1 + 0.1j * SNR * (SNR / 2)))
        # return 0.5 * x * t2 * t3
        return t3


if __name__ == '__main__':
    getSNR = getSNR()
    x = np.linspace(0, 6, 36)

    for i in x:
        res1 = getSNR.getP1(i, 1.0)
        res2 = getSNR.getP2(i, 1.0)
        getSNR.res1.append(res1)
        getSNR.res2.append(res2)
        tm = []
        tm.append(math.log(2))

    print('tm: ',tm)



    # tmp = [math.pow(10, -2), math.pow(10, -4), math.pow(10, -6), math.pow(10, -8), math.pow(10, -10), math.pow(10, -12)]
    # print(tmp)

    y = getSNR.res1
    y2 = getSNR.res2
    plt.semilogy(x, y,'-v', label='org')
    plt.semilogy(x, y2,'--s', label='now')
    plt.ylim(-0.4, 1.1)
    # plt.plot(x, y)
    # plt.yscale('log')
    plt.legend()
    plt.show()
