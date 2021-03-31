# date: 2021/3/24

# 发布者 应当是单例模式
class NewsPublisher:
    # subscribers 订阅者名单；latestNews 最新新闻
    def __init__(self):
        # 订阅者名单、最新新闻
        self.__subscribers = []
        self.__latestNews = None
    # 添加订阅者
    def attach(self, subscriber):
        self.__subscribers.append(subscriber)
    # 删除订阅者(最新添加那个订阅者）
    def detach(self):
        return self.__subscribers.pop()
    #  广播订阅者，给订阅者发布信息，实际上是调用订阅者的方法。
    def notifySubscribers(self):
        for sub in self.__subscribers:
            sub.update()
    # 添加最新新闻
    def addNews(self, news):
        self.__latestNews = news
    # 获取最新新闻
    def getNews(self):
        return "获得最新新闻:", self.__latestNews
    # 测试用的方法
    def subscribers(self):
        list = []
        for sub in self.__subscribers:
            list.append(type(sub).__name__)
        return list

# 订阅者1
class SMSSubscriber:
    def __init__(self, publisher):
        self.publisher = publisher
        self.publisher.attach(self)

    def update(self):
        print(type(self).__name__, self.publisher.getNews())

# 订阅者2
class EmailSubscriber:
    def __init__(self, publisher):
        self.publisher = publisher
        self.publisher.attach(self)

    def update(self):
        print(type(self).__name__, self.publisher.getNews())

# 订阅者3 充当观察者
class AnyOtherSubscriber:
    def __init__(self, publisher):
        self.publisher = publisher
        self.publisher.attach(self)

    def update(self):
        print(type(self).__name__, self.publisher.getNews())




# 实例化一个发布者
news_publisher = NewsPublisher()

# 分别实例化这订阅者
for Subscribers in [SMSSubscriber, EmailSubscriber, AnyOtherSubscriber]:
    # 实例化订阅者，传递的参数为发布者。
    Subscribers(news_publisher)
print("\nSubscribers:", news_publisher.subscribers())

news_publisher.addNews("Hello World!")
news_publisher.notifySubscribers() # 广播最新新闻

print("\n已被删除的订阅者:", type(news_publisher.detach()).__name__)
print("\n目前的订阅者:", news_publisher.subscribers())

news_publisher.addNews("My second news!")
news_publisher.notifySubscribers()
