from http.server import HTTPServer
from multiprocessing import freeze_support

import coordinator
import gui_webinterface

if __name__ == '__main__':
    freeze_support()

print("------ 1 --------")
gui_webinterface.MyHandler.start()  # will stop here
# print("------- 2 -------")
# data = coordinator.Coordinator().query("https://www.kleinanzeigen.de/s-sortierung:preis/preis:2:/Schraubzwinge/k0", "")
# print("---------- 3 ----")
