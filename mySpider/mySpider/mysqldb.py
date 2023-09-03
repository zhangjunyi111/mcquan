import sqlalchemy
import pandas as pd
import logging


class CreateLogger():
    def __init__(self):
        pass

    def create_logger(self):
        logger = logging.getLogger(__name__)
        file_formatter = logging.Formatter('%(asctime)s %(message)s')
        stream_formatter = logging.Formatter('%(asctime)s %(funcName)s %('
                                             'levelname)s %('
                                             'message)s')
        file_halder = logging.FileHandler('log_file.log')
        file_halder.setFormatter(file_formatter)
        logger.addHandler(file_halder)


        stream_halder = logging.StreamHandler()
        stream_halder.setFormatter(stream_formatter)
        logger.addHandler(stream_halder)
        return  logger


class MysqlDb(object):
    def __init__(self):
        pass

    def connect_mysql(self, logger):
        '''
        :return: 返回数据库连接
        '''
        engine = sqlalchemy.create_engine(
            'mysql+pymysql://root:HONGhong1225@123.56.254.64'
            '/mcquant'
            '', echo=True)
        logger.info('创建引擎成功')
        return engine

    def to_mysql(self, df, table_name, engine, logger):
        df.to_sql(table_name, con=engine
                  , if_exists='append', index=False)
        logger.info('插入数据库成功')




