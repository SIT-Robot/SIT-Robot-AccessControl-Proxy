from config import *

default_config = Config(
    database=DatabaseConfig(
        host='101.43.65.22',
        port=8978,
        username='root',
        password='rootroot',
        db='opendoor',
    ),
    lock=LockConfig(
        card_id='515FF572',
        mac_id='28:52:F9:18:84:67'
    ),
)
