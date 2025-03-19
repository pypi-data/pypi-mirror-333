'''Hypertrace wrapper around OTel postgresql instrumentor'''
import sys
import os.path
import logging
import traceback
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
from traceableai.instrumentation import BaseInstrumentorWrapper

from traceableai.custom_logger import get_custom_logger
logger = get_custom_logger(__name__)

class PostgreSQLInstrumentorWrapper(Psycopg2Instrumentor, BaseInstrumentorWrapper):
    '''Hypertrace wrapper around OTel postgresql instrumentor class'''
