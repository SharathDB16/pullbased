from libutils.base.config.configuration import config_obj
from libutils.base.log import log

# create namespace specific logger
log = log.getLogger(__name__)

connection_string = 'mysql://{}:{}@{}/{}?charset=utf8mb4'.format(
    config_obj.database_user_name,
    config_obj.database_password,
    config_obj.database_host,
    config_obj.database_name
)
