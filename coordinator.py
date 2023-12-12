from extractor import Extractor


class Coordinator:
    def __init__(self):
        print()
        # self.web_interface = WebInterface()

    def process(self, url, filters):
        # app.start()
        data = Extractor.extract(url)

        print()

