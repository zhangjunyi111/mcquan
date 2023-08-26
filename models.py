# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class DailyStack(Base):
    __tablename__ = 'daily_stock'

    f1 = Column(INTEGER(11), primary_key=True, comment='主键自增')
    ts_code = Column(String(255, 'utf8_unicode_ci'))
    trade_date = Column(String(255, 'utf8_unicode_ci'))
    open = Column(String(255, 'utf8_unicode_ci'))
    high = Column(String(255, 'utf8_unicode_ci'))
    low = Column(String(255, 'utf8_unicode_ci'))
    close = Column(String(255, 'utf8_unicode_ci'))
    pre_close = Column(String(255, 'utf8_unicode_ci'))
    change = Column(String(255, 'utf8_unicode_ci'))
    pct_chg = Column(String(255, 'utf8_unicode_ci'))
    vol = Column(String(255, 'utf8_unicode_ci'))
    amount = Column(String(255, 'utf8_unicode_ci'))
