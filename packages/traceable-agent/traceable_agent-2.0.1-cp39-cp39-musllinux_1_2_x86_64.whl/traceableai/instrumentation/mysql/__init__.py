'''Traceableai wrapper around OTel MySQL Instrumentor''' # pylint: disable=R0801
import logging
from opentelemetry.instrumentation.mysql import MySQLInstrumentor
from traceableai.instrumentation import BaseInstrumentorWrapper

from traceableai.custom_logger import get_custom_logger
logger = get_custom_logger(__name__)

# The main entry point
class MySQLInstrumentorWrapper(MySQLInstrumentor, BaseInstrumentorWrapper):
    '''Hypertrace wrapper around OTel MySQL Instrumentor class'''
