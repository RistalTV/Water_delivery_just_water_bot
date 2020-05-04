import logging.config
# ===== main bot
TG_TOKEN = "1192087203:AAFP_3APkguAegMQYqydYDKXicLCeSqBFqQ"
# ===== test bot
# TG_TOKEN = "1034943274:AAFfin_v_3ZjV2gwJmszS1BILxX3K4y7lw8"

HashTagFindLogsINFO = " #infoWaterDelivery "
HashTagFindLogsWARN = " #WarningWaterDelivery "
HashTagFindORDER = " #OrderWaterDelivery "

TG_API_URL = "https://api.telegram.org/bot"
# TG_API_URL = "https://telegg.ru/orig/bot"

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
#
CHAT_ID_COMPANY = -1001413848914
CHAT_ID_BUGS = -1001490831454
CHAT_ID_LOGS = -1001337535965
# CHAT_ID_COMPANY = -1001291381846
# CHAT_ID_BUGS = -1001291381846
# CHAT_ID_LOGS = -1001291381846

url_site = 'просто-вода.рус'
