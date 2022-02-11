import logging

class Log:

    def __init__(self, name: str):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.handler = logging.FileHandler(f'../Logs/{name}.log')
        self.formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)
