import datetime
import logging


class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.setup_logger()
        return cls._instance

    def setup_logger(self):
        format = "%(asctime)s - %(levelname)s - %(message)s"
        file_name = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        logging.basicConfig(
            filename=f"{file_name}.log",
            level=logging.DEBUG,
            format=format,
        )

        # display logs to console
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter(format)
        console.setFormatter(formatter)
        logging.getLogger("").addHandler(console)

    def log_info(self, message):
        logging.info(message)

    def log_warning(self, message):
        logging.warning(message)

    def log_error(self, message):
        logging.error(message)
