import threading
import time


class Monitor():

    def __init__(self):
        self.stop = False
        self.blocked_emails = []

    def start_monitor(self):
        print("child : start_monitor")
        rows = []
        while not self.stop:
            self.check_rows(rows)
            print("child : inside while")
            time.sleep(1)

    def check_rows(self, rows):
        print('child : check_rows')

    def stop_monitoring(self):
        print("child : stop_monitoring")
        self.stop = True


if __name__ == '__main__':
    monitor = Monitor()

    print('parent: define child')
    b = threading.Thread(name='background_monitor', target=monitor.start_monitor)
    print('parent: start child')
    b.start()

    for i in range(1, 3):
        print('parent: Wait 2 sec.(' + str(i)+' of 10)')
        time.sleep(2)
    print('parent: stop child')
    #monitor.stop_monitoring()
    #b.join() # wait until monitor.start_monitor() is finished ...
    print('parent: stopped')
