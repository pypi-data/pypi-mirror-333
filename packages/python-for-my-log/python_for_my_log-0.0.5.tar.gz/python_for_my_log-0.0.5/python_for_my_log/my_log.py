#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# DevVersion: Python3.6.8
# Date: 2025-03-13
# Author: SunXiuWen
# Des: 构建日志文件记录通用中间件
# PyCharm|log_config
import os
import re
import json
import socket
import inspect
import logging
import datetime
import platform
import threading
from logging.handlers import TimedRotatingFileHandler

# 日志级别权重值
LOG_LEVEL = {
    "NOTSET": 0,
    "DEBUG": 10,
    "INFO": 20,
    "WARNING": 30,
    "WARN": 30,
    "ERROR": 40,
    "FATAL": 50,
    "CRITICAL": 50,
    "EXTERNAL": 60,
    "INTERNAL": 60,
}


class DateEncoder(json.JSONEncoder):
    """
    json 无法序列化datetime类型，自定义进行序列化
    """

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self, obj)


class LogMiddleware(object):
    _instance_lock = threading.Lock()
    log_dict = {}

    def __init__(self,
                 log_dir_path,
                 app_name="Test_app",
                 hostname=socket.gethostname(),
                 log_level="DEBUG",
                 log_format_model="elk",
                 log_when="H",
                 log_interval=1,
                 log_backup_count=30 * 24
                 # log_dir_path="/app/logs/{}".format(os.path.basename(SERVER_DIR_BASENAME))):
                 ):
        """
        :param app_name:  标识日志归属与那个app
        :param hostname:  实例的主机名
        :param log_level: 日志最低输出的级别
        :param log_format_model: 日志记录的格式,可以选设置好的default或elk，也可以自定义
        :param log_when: 日志分割的模式：H 小时，M 分钟，S 秒
        :param log_interval: 日志分割的维度，仅支持天D、小时H，分钟M，秒S
        :param log_backup_count: 日志最多保留的个数，默认按小时分割，保留30天的日志
        :param log_dir_path: 日志存放的基目录
        """
        self.app_name = app_name
        self.hostname = hostname
        self.log_level = log_level
        self.log_dir_path = log_dir_path
        self.log_format_model = log_format_model
        self.log_when = log_when.upper()
        self.log_interval = log_interval
        self.log_backup_count = log_backup_count
        self.logger = self.__class__.__name__  # 类名

    def __new__(cls, *args, **kwargs):
        """单例模式，log对象多进程/线程实例化一次"""
        if not hasattr(LogMiddleware, "_instance"):
            with LogMiddleware._instance_lock:
                if not hasattr(LogMiddleware, "_instance"):
                    cls._instance = object.__new__(cls)
        return cls._instance

    def get_logger(self):
        """
        构建日志对象
        :return:
        """
        p_id = str(os.getpid())
        logger_ = self.log_dict.get("p" + p_id)
        if not logger_:
            # 日志记录的格式
            log_format_dict = {
                "default": "[%(levelname)s]:[%(asctime)s]:(thread_id:%(thread)d):[%(filename)s:%(lineno)d]-%(message)s",
                "elk": "%(message)s"
            }
            def_format = logging.Formatter(
                log_format_dict[
                    self.log_format_model] if self.log_format_model in log_format_dict.keys() else self.log_format_model)

            # 配置日志文件输出目录及日志文件名
            if platform.system() == 'Windows':
                log_path_prefix = os.path.join(self.log_dir_path, "log")
            else:
                log_path_prefix = os.path.join("/app/log/", os.path.basename(self.log_dir_path))

            if not os.path.exists(log_path_prefix):
                os.makedirs(log_path_prefix)
            log_path_debug = "{}/{}_code-debug-{}.log".format(log_path_prefix, self.app_name, self.hostname)
            log_path_error = "{}/{}_code-error-{}.log".format(log_path_prefix, self.app_name, self.hostname)
            log_path_info = "{}/{}_info-info-{}.log".format(log_path_prefix, self.app_name, self.hostname)
            log_path_warn = "{}/{}_code-warn-{}.log".format(log_path_prefix, self.app_name, self.hostname)

            # 设置分割日志后文件名的后缀格式及不符合日志文件名规则的删除日志文件
            split_log_file_prefix_dict = {
                "D": {"suffix": "%Y-%m-%d.log", "extMatch": r"^\d{4}-\d{2}-\d{2}.log$"},
                "H": {"suffix": "%Y-%m-%d_%H.log", "extMatch": r"^\d{4}-\d{2}-\d{2}_\d{2}.log$"},
                "M": {"suffix": "%Y-%m-%d_%H-%M.log", "extMatch": r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}.log$"},
                "S": {"suffix": "%Y-%m-%d_%H-%M-%S.log", "extMatch": r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}.log$"}
            }

            # 构建各级别日志处理对象
            debug_handler = logging.handlers.TimedRotatingFileHandler(
                # 文件名
                log_path_debug,
                # 分割的维度
                when=self.log_when,
                # 如按秒分割，间隔5秒，从执行程序开始计时，如第1开始，分割就是第6
                interval=self.log_interval,
                # 保留日志个数，默认30天的日志
                backupCount=self.log_backup_count,
                encoding='utf-8')
            # 文件分割后文件名及过期文件匹配设置
            debug_handler.suffix = split_log_file_prefix_dict[self.log_when]["suffix"]
            debug_handler.extMatch = re.compile(split_log_file_prefix_dict[self.log_when]["extMatch"])
            # 构建过滤器
            log_debug_filter = logging.Filter()
            log_debug_filter.filter = lambda record: record.levelno < logging.INFO
            debug_handler.addFilter(log_debug_filter)
            # 日志手柄关联的日志级别配置及日志记录格式配置
            debug_handler.setLevel(logging.DEBUG)
            debug_handler.setFormatter(def_format)

            info_handler = logging.handlers.TimedRotatingFileHandler(log_path_info,
                                                                     when=self.log_when,
                                                                     interval=self.log_interval,
                                                                     backupCount=self.log_backup_count,
                                                                     encoding='utf-8')
            info_handler.suffix = split_log_file_prefix_dict[self.log_when]["suffix"]
            info_handler.extMatch = re.compile(split_log_file_prefix_dict[self.log_when]["extMatch"])

            log_info_filter = logging.Filter()
            log_info_filter.filter = lambda record: record.levelno < logging.WARN
            info_handler.addFilter(log_info_filter)

            info_handler.setLevel(logging.INFO)
            info_handler.setFormatter(def_format)

            warn_handler = logging.handlers.TimedRotatingFileHandler(log_path_warn,
                                                                     when=self.log_when,
                                                                     interval=self.log_interval,
                                                                     backupCount=self.log_backup_count,
                                                                     encoding='utf-8')
            warn_handler.suffix = split_log_file_prefix_dict[self.log_when]["suffix"]
            warn_handler.extMatch = re.compile(split_log_file_prefix_dict[self.log_when]["extMatch"])

            log_warn_filter = logging.Filter()
            log_warn_filter.filter = lambda record: record.levelno < logging.ERROR
            warn_handler.addFilter(log_warn_filter)

            warn_handler.setLevel(logging.WARNING)
            warn_handler.setFormatter(def_format)

            error_handler = logging.handlers.TimedRotatingFileHandler(log_path_error,
                                                                      when=self.log_when,
                                                                      interval=self.log_interval,
                                                                      backupCount=self.log_backup_count,
                                                                      encoding='utf-8')
            error_handler.suffix = split_log_file_prefix_dict[self.log_when]["suffix"]
            error_handler.extMatch = re.compile(split_log_file_prefix_dict[self.log_when]["extMatch"])

            log_error_filter = logging.Filter()
            log_error_filter.filter = lambda record: record.levelno < logging.FATAL
            error_handler.addFilter(log_error_filter)

            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(def_format)

            # 构建日志对象
            logger_ = logging.getLogger(name=self.app_name)
            logger_.setLevel(self.log_level)
            logger_.addHandler(debug_handler)
            logger_.addHandler(info_handler)
            logger_.addHandler(warn_handler)
            logger_.addHandler(error_handler)
            self.log_dict["p" + p_id] = logger_
        return logger_

    def base_model(self, log_type, levelno, level, message, path_name, lineno, func_name, extra=None, app_name=None):
        data = {
            "app_name": app_name,
            "level": level,
            "log_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
            "logger": self.logger,
            "thread": threading.currentThread().ident,
            "host_name": self.hostname,
            "log_type": log_type,
            "level_no": levelno,  # 日志的权重值
            "code_message": message,
            "pathName": path_name,
            "lineNo": lineno,  # 程序文件记录日志所在的行数
            "funcName": func_name,
        }
        if extra:
            data.update(extra)
        return json.dumps(data, ensure_ascii=False, cls=DateEncoder)

    def debug(self, msg, log_type="desc"):
        if LOG_LEVEL[self.log_level] <= LOG_LEVEL["DEBUG"]:
            path_name, lineno, func_name = self.make_path()

            self.get_logger().debug(self.base_model(log_type=log_type,
                                                    levelno=LOG_LEVEL["DEBUG"],
                                                    level="DEBUG",
                                                    app_name="{}_code".format(str(self.app_name)),
                                                    message=msg,
                                                    path_name=path_name,
                                                    lineno=lineno,
                                                    func_name=func_name))

    def info(self, msg, log_type="desc"):
        if LOG_LEVEL[self.log_level] <= LOG_LEVEL["INFO"]:
            path_name, lineno, func_name = self.make_path()

            self.get_logger().info(self.base_model(log_type=log_type,
                                                   levelno=LOG_LEVEL["INFO"],
                                                   level="INFO",
                                                   app_name="{}_code".format(str(self.app_name)),
                                                   message=msg,
                                                   path_name=path_name,
                                                   lineno=lineno,
                                                   func_name=func_name))

    def warning(self, msg, log_type="desc"):
        if LOG_LEVEL[self.log_level] <= LOG_LEVEL["WARNING"]:
            path_name, lineno, func_name = self.make_path()

            self.get_logger().warning(self.base_model(log_type=log_type,
                                                      levelno=LOG_LEVEL["WARNING"],
                                                      level="WARNING",
                                                      app_name="{}_code".format(str(self.app_name)),
                                                      message=msg,
                                                      path_name=path_name,
                                                      lineno=lineno,
                                                      func_name=func_name))

    def error(self, msg, log_type="desc"):
        if LOG_LEVEL[self.log_level] <= LOG_LEVEL["ERROR"]:
            path_name, lineno, func_name = self.make_path()

            self.get_logger().error(self.base_model(log_type=log_type,
                                                    levelno=LOG_LEVEL["ERROR"],
                                                    level="ERROR",
                                                    app_name="{}_code".format(str(self.app_name)),
                                                    message=msg,
                                                    path_name=path_name,
                                                    lineno=lineno,
                                                    func_name=func_name))

    def external(self, msg, extra, log_type="monitor"):
        path_name, lineno, func_name = self.make_path()

        self.get_logger().info(self.base_model(log_type=log_type,
                                               levelno=LOG_LEVEL["EXTERNAL"],
                                               level="INFO",
                                               app_name="{}_info".format(str(self.app_name)),
                                               message=msg,
                                               path_name=path_name,
                                               lineno=lineno,
                                               func_name=func_name,
                                               extra=extra))

    def internal(self, msg, extra, log_type="monitor"):
        path_name, lineno, func_name = self.make_path()

        self.get_logger().info(self.base_model(log_type=log_type,
                                               levelno=LOG_LEVEL["INTERNAL"],
                                               level="INFO",
                                               app_name="{}_info".format(str(self.app_name)),
                                               message=msg,
                                               path_name=path_name,
                                               lineno=lineno,
                                               func_name=func_name,
                                               extra=extra))

    @staticmethod
    def make_path():
        d = inspect.stack()[2]  # 获取栈内调用行
        return d[1], d[2], d[3]
