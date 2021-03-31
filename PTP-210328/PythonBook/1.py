import time

def timeCall():
    for i in range(100):
        time.sleep(0.1)
        print(f'Time: {i}')


timeCall()
