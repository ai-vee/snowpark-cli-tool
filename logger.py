import logging
import datetime as dt
import sys
import colorlog
import functools

class Logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    BASIC_FORMATTER = logging.Formatter('%(asctime)s:%(levelname)s %(message)s')
    COLORED_FORMATTER = colorlog.ColoredFormatter('%(asctime)s:%(log_color)s%(levelname)-10s%(reset)s LINE%(lineno)-5d %(module)-s.%(funcName)s\n\t%(message)s\n')
    FUNC_LOG_FORMAT = '\n%(asctime)s:%(log_color)s%(status)s%(reset)s %(message)-25s %(_kwargs)s'
    # Stream Handler
    stream_hander = logging.StreamHandler()
    stream_hander.setLevel(logging.INFO)
    stream_hander.setFormatter(BASIC_FORMATTER)
    stream_hander.name = 'stream_handler'
    logger.addHandler(stream_hander)

    # File Handler
    TODAY = dt.datetime.today()
    file_name = f'./.logs/{TODAY.year}{TODAY.month:02d}{TODAY.day:02d}.log'
    file_handler = logging.FileHandler(file_name)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(BASIC_FORMATTER)
    file_handler.name = 'file_handler'
    logger.addHandler(file_handler)

    @classmethod
    def setFormatter(cls, logger: logging.Logger, fmt: logging.Formatter, _handler_name: str= None):
        for handler in logger.handlers:
            if handler.name == 'file_handler':
                # Remove Colors for File Handle
                fmt_ = fmt._fmt.replace('%(log_color)s','').replace('%(reset)s','')
                fmt = logging.Formatter(fmt_)
        
            if _handler_name is not None:
                if handler.name == _handler_name:
                    handler.setFormatter(fmt)
            else:
                handler.setFormatter(fmt)
    
    
    @classmethod
    def setLogLevel(cls, logger: logging.Logger, level: str, _handler_name: str= None):
        for handler in logger.handlers:
            if _handler_name is not None:
                if handler.name == _handler_name:
                    handler.setLevel(level)
            else:
                handler.setLevel(level)
    
    @classmethod
    def log(cls, log_args: bool = False, log_kwargs: list = None):
        def decorate(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                MAX_STATUS_LENGTH = 15
                LOG_KWARGS = list()
                if log_kwargs:
                    LOG_KWARGS = ', '.join([f"{kwa} = {kwargs.get(kwa)}" for kwa in log_kwargs])
                else:
                    LOG_KWARGS = kwargs
                    
                if log_args:
                    LOG_ARGS = ', '.join(args)
                else:
                    LOG_ARGS = ''
                    
                extra_dictionary = {"_kwargs": LOG_KWARGS or LOG_ARGS or ""}
                Logger.setLogLevel(cls.logger, logging.INFO, 'stream_handler')
                Logger.setLogLevel(cls.logger, logging.DEBUG, 'file_handler')
                
                try:
                    #* Before Execution
                    cls.setFormatter(cls.logger, colorlog.ColoredFormatter(cls.FUNC_LOG_FORMAT))
                    extra_dictionary = {**extra_dictionary,  
                                        "status": f"{'START'.ljust(MAX_STATUS_LENGTH, '.')}"}
                    cls.logger.info("%s", func.__name__, extra=extra_dictionary)
                    
                    # *Return Regular Formatter
                    Logger.setFormatter(cls.logger, Logger.COLORED_FORMATTER)
                    #* During Execution
                    result = func(*args, **kwargs)
                    
                    #* After Execution 
                    # Formmatter might have been modified during execution of decorected func
                    Logger.setFormatter(cls.logger, colorlog.ColoredFormatter(cls.FUNC_LOG_FORMAT))
                    extra_dictionary = {**extra_dictionary,
                                        "status": f"{'SUCCEEDED'.ljust(MAX_STATUS_LENGTH, '.')}"}
                    cls.logger.info("%s", func.__name__ , extra=extra_dictionary)
                    
                    # *Return Regular Formatter
                    Logger.setFormatter(cls.logger, Logger.COLORED_FORMATTER)
                    return result
                except:
                    cls.setFormatter(cls.logger, colorlog.ColoredFormatter(cls.FUNC_LOG_FORMAT))
                    extra_dictionary = {**extra_dictionary,
                                        "status": f"{'ERROR'.ljust(MAX_STATUS_LENGTH, '.')}"}
                    cls.logger.error("%s", func.__name__ , extra=extra_dictionary, exc_info=True)
                    sys.exit(1)
            return wrapper
        return decorate
            
