EMPLOYEE_INFO = 'employee_info'
DEVICE_INFO = 'device_info'
EMPLOYEE_ADDRESS_INFO = 'employee_address_info'
VALIDATION_PROGRESS_INFO = 'validation_progress_info'
NOT_STARTED = 'NOT STARTED'
LOKTRA_MAIL = 'aubusiness@loktra.com'

CELERY_WORKER_DEFAULT = 'celeryd'
CELERY_WORKER_TWO = 'trigger'
CELERY_WORKER_THREE = 'celeryd-retry'

CELERY_WORKER_DEF = 'default'
CELERY_WORKER_3 = 'retry'

CELERY_WORKERS = [CELERY_WORKER_DEF, CELERY_WORKER_3, CELERY_WORKER_TWO]


REQUEST_TIMEOUT = 300


TABLE_OWNER_DEVELOPER_EMAIL = {
    'anuj' : 'anuj@loktra.com'
}


EXCEL_FORMAT_FILE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

ZERO = 0

PAGE_NUM = 'page_num'
PAGE_COUNT = 'per_page'
FILTERS = 'filters'
STATUS = 'status'
MSG = 'msg'
DATA = 'data'
RESULTS = 'results'
TOTAL_COUNT = 'total_count'
FROM = 'from'
TO = 'to'
CREATED_ON = 'created_on'



# NAME_SORT = {'key': NAME, 'label': 'Name[A-Z]'}
CREATED_DATE_SORT = {'key': CREATED_ON, 'label': 'Created On'}

# QUEUES
CELERY_QUEUE_DEFAULT = 'default'
CELERY_QUEUE_TRIGGER = 'trigger'
CELERY_QUEUE_RETRY = 'retry'
