import sys
import os
from loguru import logger

sys.path.append('..')
rootpath = os.path.abspath(os.path.pardir)


class log_danmuku:
    def __init__(self, DEBUG: bool = False, log_file_path='logs/INFO_LOG/{time:YYYY-MM-DD}.log', init: bool = False):
        if not init:
            self.conf_init()
        elif init:
            self.logger = logger.bind(user="danmuku")
            self.logger.remove()
            self.logger.add(sys.stdout,
                            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                                   "<level>{level}</level>: "
                                   "<level>{message}</level>",
                            level='INFO'
                            )
            self.logger.add(sink=log_file_path, level='INFO',
                            format='{time:YYYY-MM-DD HH:mm:ss} - '
                                   ' - {level} -{message}',
                            rotation='00:00',
                            enqueue=True,
                            encoding="utf-8",
                            retention="30 days")
            if DEBUG:
                self.model_DEBUG('logs/DEBUG_LOG/DEBUG-{time:YYYY-MM-DD}.log')
            logger.success('log模块导入成功')

    def get_logger(self):
        return self.logger

    def model_DEBUG(self, path):
        self.logger.remove()
        self.logger.add(sys.stdout,
                        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                               "{process.name} | "
                               "{thread.name} | "
                               "{module}.{function}:{line} | "
                               "<level>{level}</level>: "
                               "<level>{message}</level>",
                        level='DEBUG'
                        )
        self.logger.add(path, level='DEBUG',
                        format='{time:YYYY-MM-DD HH:mm:ss} - '
                               "{process.name} | "
                               "{thread.name} | "
                               'module.func.line: {module}.{function}:{line} - {level} -{message}',
                        rotation='00:00',
                        enqueue=True,
                        encoding="utf-8",
                        retention="30 days")
        self.logger.debug('当前为DEBUG模式')

    def conf_init(self):
        self.logger = logger.bind(user="danmuku")
        self.logger.remove()


if __name__ == '__main__':
    print(rootpath)
