"""日志配置模块"""
import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

# 日志级别配置（可通过环境变量修改）
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# 获取logger对象
logger = logging.getLogger(__name__)

# 防止重复添加handler
if not logger.handlers:
    # 获取项目根目录路径
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 创建logs目录
    log_dir_path = os.path.join(root_path, 'logs')
    os.makedirs(log_dir_path, exist_ok=True)

    # 日志文件名包含日期
    log_file = os.path.join(log_dir_path, f'test_{datetime.now().strftime("%Y%m%d")}.log')

    # 创建按时间分割的日志处理器（每天凌晨分割，保留30天）
    file_log_handler = TimedRotatingFileHandler(
        log_file,
        when='midnight',
        interval=1,
        backupCount=30,
        encoding='utf-8'
    )
    # 日志文件名后缀格式
    file_log_handler.suffix = "%Y%m%d"

    # 设置日志格式
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] [%(funcName)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 控制台输出处理器
    stream_handler = logging.StreamHandler()

    # 应用格式
    file_log_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # 添加处理器
    logger.addHandler(stream_handler)
    logger.addHandler(file_log_handler)

    # 设置日志级别
    logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))

    # 防止日志向上传播
    logger.propagate = False