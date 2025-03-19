'''this module acts as a driver for instrumentation definitions + application'''
from traceableai.custom_logger import get_custom_logger

FLASK_KEY = 'flask'
DJANGO_KEY = 'django'
FAST_API_KEY = 'fastapi'
GRPC_SERVER_KEY = 'grpc:server'
GRPC_CLIENT_KEY = 'grpc:client'
POSTGRESQL_KEY = 'postgresql'
MYSQL_KEY = 'mysql'
REQUESTS_KEY = 'requests'
AIOHTTP_CLIENT_KEY = 'aiohttp:client'
LAMBDA = 'lambda'
BOTO = 'boto'
BOTOCORE = 'botocore'

SUPPORTED_LIBRARIES = [
    FLASK_KEY, DJANGO_KEY, FAST_API_KEY,
    GRPC_SERVER_KEY, GRPC_CLIENT_KEY,
    POSTGRESQL_KEY, MYSQL_KEY,
    REQUESTS_KEY, AIOHTTP_CLIENT_KEY,
    LAMBDA, BOTO, BOTOCORE
]

# map of library_key => instrumentation wrapper instance
_INSTRUMENTATION_STATE = {}

logger = get_custom_logger(__name__)

def _uninstrument_all():
    for key, value in _INSTRUMENTATION_STATE.items():
        logger.debug("Uninstrumenting %s", key)
        value.uninstrument()

    _INSTRUMENTATION_STATE.clear()

def is_already_instrumented(library_key):
    """check if an instrumentation wrapper is already registered"""
    return library_key in _INSTRUMENTATION_STATE


def _mark_as_instrumented(library_key, wrapper_instance):
    """mark an instrumentation wrapper as registered"""
    _INSTRUMENTATION_STATE[library_key] = wrapper_instance


def get_instrumentation_wrapper(library_key): # pylint:disable=R0912
    """load an initialize an instrumentation wrapper"""
    if is_already_instrumented(library_key):
        logger.debug("Already instrumented %s", library_key)
        return None
    try:
        wrapper_instance = None
        if DJANGO_KEY == library_key:
            from traceableai.instrumentation.django import DjangoInstrumentationWrapper  #pylint:disable=C0415
            wrapper_instance = DjangoInstrumentationWrapper()
        elif FLASK_KEY == library_key:
            from traceableai.instrumentation.flask import FlaskInstrumentorWrapper #pylint:disable=C0415
            wrapper_instance = FlaskInstrumentorWrapper()
        elif FAST_API_KEY == library_key:
            from traceableai.instrumentation.fast_api import FastAPIInstrumentorWrapper #pylint:disable=C0415
            wrapper_instance = FastAPIInstrumentorWrapper()
        elif GRPC_SERVER_KEY == library_key:
            from traceableai.instrumentation.grpc import GrpcInstrumentorServerWrapper #pylint:disable=C0415
            wrapper_instance = GrpcInstrumentorServerWrapper()
        elif GRPC_CLIENT_KEY == library_key:
            from traceableai.instrumentation.grpc import GrpcInstrumentorClientWrapper #pylint:disable=C0415
            wrapper_instance = GrpcInstrumentorClientWrapper()
        elif POSTGRESQL_KEY == library_key:
            from traceableai.instrumentation.postgresql import PostgreSQLInstrumentorWrapper #pylint:disable=C0415
            wrapper_instance =  PostgreSQLInstrumentorWrapper()
        elif MYSQL_KEY == library_key:
            from traceableai.instrumentation.mysql import MySQLInstrumentorWrapper #pylint:disable=C0415
            wrapper_instance = MySQLInstrumentorWrapper()
        elif REQUESTS_KEY == library_key:
            from traceableai.instrumentation.requests import RequestsInstrumentorWrapper #pylint:disable=C0415
            wrapper_instance = RequestsInstrumentorWrapper()
        elif AIOHTTP_CLIENT_KEY == library_key:
            from traceableai.instrumentation.aiohttp import AioHttpClientInstrumentorWrapper #pylint:disable=C0415
            wrapper_instance = AioHttpClientInstrumentorWrapper()
        elif LAMBDA == library_key:
            from traceableai.instrumentation.aws_lambda import AwsLambdaInstrumentorWrapper #pylint:disable=C0415
            wrapper_instance = AwsLambdaInstrumentorWrapper()
        elif BOTO == library_key:
            from traceableai.instrumentation.boto import BotoInstrumentationWrapper #pylint:disable=C0415
            wrapper_instance = BotoInstrumentationWrapper()
        elif BOTOCORE == library_key:
            from traceableai.instrumentation.botocore import BotocoreInstrumentationWrapper #pylint:disable=C0415
            wrapper_instance = BotocoreInstrumentationWrapper()
        else:
            logger.debug("No instrumentation wrapper available for %s", library_key)
            return None

        _mark_as_instrumented(library_key, wrapper_instance)
        return wrapper_instance
    except Exception as _err: # pylint:disable=W0703
        logger.debug("Error while attempting to load instrumentation wrapper for %s: %s", library_key, str(_err),
                     exc_info=True)
        return None
