# date: 2021/3/24
from threading import Timer

# def timerA():
#     for i in range(0, 100):
#         r = Timer(1.0, showTime, (i))
#         r.start()

def showTime(*args):
    for each in args:
        print(each)


r = Timer(1.0, showTime, "10")
r.start()

# timerA()
print('end')