import logging.config

TG_TOKEN = "1192087203:AAFP_3APkguAegMQYqydYDKXicLCeSqBFqQ"
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

CHAT_ID_COMPANY = -1001413848914
CHAT_ID_BUGS = -1001490831454
url_site = 'просто-вода.рус'