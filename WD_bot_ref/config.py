import logging.config

TG_TOKEN = "1192087203:AAFS_q5p-gj04n4c0vtuB7vCPLY9sonTiIE"
TG_API_URL = "https://telegg.ru/orig/bot"

LOGGING = {
    "disable_existing_loggers": True,
    "version": 1,
    "formatters": {
        "verbose": {
            "format": '%(levelname)s %(module)s.%(funcName)s | %(asctime)s | %(message)s',
            "datefmt": '%Y-%m-%d %H:%M:%S',
        },
    },
    "handlers": {
        "console": {
            "class": 'logging.StreamHandler',
            "level": 'DEBUG',
            "formatter": 'verbose',
        },
    },
    "loggers": {
        "": {
            "handlers": ['console'],
            "level": 'INFO',
            "propagate": False,
        },
    },
}
logging.config.dictConfig(LOGGING)

url_site = ' *cсылка на сайт '
