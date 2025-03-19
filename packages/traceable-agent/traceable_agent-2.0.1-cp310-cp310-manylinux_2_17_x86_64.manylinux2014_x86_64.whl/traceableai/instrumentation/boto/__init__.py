'''Hypertrace wrapper around OTel boto Instrumentor''' # pylint: disable=R0801
import logging
from opentelemetry.instrumentation.boto import BotoInstrumentor  # pylint:disable=E0611,E0401
from traceableai.instrumentation import BaseInstrumentorWrapper


from traceableai.custom_logger import get_custom_logger
logger = get_custom_logger(__name__)

class BotoInstrumentationWrapper(BotoInstrumentor, BaseInstrumentorWrapper):
    '''Hypertrace wrapper around OTel Boto Instrumentor class'''
