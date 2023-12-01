from libutils.base.config.configuration import config_obj
import logging as log
import time

# log.basicConfig()
log.getLogger('sqlalchemy').setLevel(log.ERROR)
log.getLogger('werkzeug').setLevel(log.ERROR)


class AppLogger(log.Logger):

    def __init__(self, name):
        log.Logger.__init__(self, name)
        base_logger_name = name.split('.')[0]
        if base_logger_name == name:
            time_str = time.strftime("%Y%m%d%H%S")
            file_handler = log.FileHandler('/var/log/sugarbox/provisioningagent/application.log', mode='a')
            log_format = log.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(log_format)
            self.addHandler(file_handler)
            self.set_log_level(config_obj.log_level)
        else:
            log.getLogger(base_logger_name)

    def set_log_level(self, level):
        log_levels = {
                        "debug": log.DEBUG,
                        "info": log.INFO,
                        "warning": log.WARNING,
                        "error": log.ERROR,
                        "critical": log.CRITICAL
                     }

        level = log_levels[level] if level in log_levels  else log.DEBUG
        self.setLevel(level)


log.setLoggerClass(AppLogger)
