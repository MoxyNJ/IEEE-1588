# date: 2021/3/24

# 发布者
class Subject:
    def __init__(self):
        self.__observers = []

    # 登记
    def register(self, observer):
        self.__observers.append(observer)

    # 广播通知
    def notifyAll(self, *args, **kwargs):
        for observer in self.__observers:
            # *args: 传递一个tuple，收集无名参数；**kwargs: 传递一个dict，收集有名参数。
            observer.notify(self, *args, **kwargs)

# 订阅者 1
class Observer1:
    def __init__(self, subject):
        subject.register(self)

    def notify(self, subject, *args):
        print(type(self).__name__, '::Got', args, 'From', subject)

# 订阅者 2
class Observer2:
    def __init__(self, subject):
        subject.register(self)

    def notify(self, subject, *args):
        print(type(self).__name__, '::Got', args, 'From', subject)

subject = Subject()
observer1 = Observer1(subject)
observer2 = Observer2(subject)

subject.notifyAll('notification')