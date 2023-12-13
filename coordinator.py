from extractor import Extractor


class Coordinator:
    def __init__(self):
        print()
        self.extractor = Extractor()
        # self.web_interface = WebInterface()


    # receive query and
    # show result ...
    def query(self, url, filters):
        # app.start()
        data = self.extractor.extract(url)

        print()

