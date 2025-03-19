import os
import sys
import threading
import traceback

import distro

from traceableai import constants
from traceableai.agent_init import AgentInit
from traceableai.config.config import Config
from traceableai.custom_logger import get_custom_logger
from traceableai.env import get_env_value
from traceableai.filter.registry import Registry
from traceableai.instrumentation.instrumentation_definitions import SUPPORTED_LIBRARIES, get_instrumentation_wrapper, \
    FLASK_KEY, DJANGO_KEY, FAST_API_KEY, LAMBDA
from traceableai.version import __version__ # pylint:disable=C0413
logger = get_custom_logger(__name__)


class Agent():
    _instance = None
    _singleton_lock = threading.Lock()

    def __new__(cls):
        '''constructor'''
        if cls._instance is None:
            with cls._singleton_lock:
                logger.debug('Creating Agent')
                logger.debug('Python version: %s', sys.version)
                logger.debug('Traceable Agent version: %s', __version__)
                cls._instance = super(Agent, cls).__new__(cls)
        else:
            logger.debug('Using existing Agent.')
        return cls._instance

    def __init__(self):
        self._initialized = False
        if not self._initialized:  # pylint: disable=E0203:
            logger.debug('Initializing Agent.')
            if not self.is_enabled():
                return
            try:
                self._config = Config()
                self._init = AgentInit(self._config)
                self._initialized = True
            except Exception as err:  # pylint: disable=W0703
                logger.error('Failed to initialize Agent: exception=%s, stacktrace=%s',
                             err,
                             traceback.format_exc())
        self.is_lambda = False
        logger.debug("Platform: %s", distro.id())
        logger.debug("Platform version: %s", distro.version())
        logger.debug('TraceableAI Agent version: %s', __version__)
        logger.debug("successfully initialized traceableai agent")

        if hasattr(os, 'register_at_fork'):
            logger.info('Registering after_in_child handler.')
            os.register_at_fork(after_in_child=self.post_fork)  # pylint:disable=E1101

    def post_fork(self):
        logger.info("In post fork hook")
        logger.info("Calling add traceable filter during post fork")
        self._init.post_fork()
        self.add_traceable_filter()

    def instrument(self, app=None, skip_libraries=None, auto_instrument=False):
        '''used to register applicable instrumentation wrappers'''
        logger.debug("Beginning instrumentation")
        self._init.apply_config(self._config)

        if skip_libraries is None:
            skip_libraries = []
        if not self.is_initialized():
            logger.debug('agent is not initialized, not instrumenting')
            return

        for library_key in SUPPORTED_LIBRARIES:
            if library_key in skip_libraries:
                logger.debug('not attempting to instrument %s', library_key)
                continue
            logger.debug("attempting to instrument %s", library_key)
            self._instrument(library_key, app, auto_instrument)
        logger.debug("Complete instrumentation")

    def _instrument(self, library_key, app=None, auto_instrument=False):
        """only used to allow the deprecated register_x library methods to still work"""

        wrapper_instance = get_instrumentation_wrapper(library_key)
        if wrapper_instance is None:
            logger.debug("no instrumentation wrapper instance available for %s", library_key)
            return

        # Flask is a special case compared to rest of instrumentation
        # using hypertrace-instrument we can replace flask class def before app is initialized
        # however during code based instr we wrap the existing app
        # since replacing class def after app is initialized doesnt have an effect
        # the user has to pass the app in to agent.instrument()
        # we could resolve this edge case by instead having users directly add the middleware
        # ex: app = Flask();
        # app = HypertraceMiddleware(App) => this in turn does agent.instrument()
        # + we have ref to app
        if library_key == FLASK_KEY and app is not None:
            wrapper_instance.with_app(app)

        # since ht sitecustomize pushes the agent to the front of the load path django instrumentation will error
        # when using autoinstrumentation since we need the django app settings loaded to add middleware
        #
        # in order to resolve this if we detect django we wrap the wsgi/asgi app getter
        # and instrument as soon as the app is retrieved(since settings have to be configured
        # before returning loaded app)
        if library_key == DJANGO_KEY and auto_instrument is True:
            from traceableai.instrumentation.django.django_auto_instrumentation_compat import \
                add_django_auto_instr_wrappers  # pylint: disable=C0415
            add_django_auto_instr_wrappers(self, wrapper_instance)
            return

        # For FastAPI we need a handle to the user app before we can instrument fast & inject middleware
        # to make things easier for the user always add the below instrumentation wrappers
        # when FastAPI calls `.setup` take the app and then add instrumentation
        if library_key == FAST_API_KEY:
            from traceableai.instrumentation.fast_api.fast_api_auto_instrumentation_compat import \
                add_fast_api_auto_instr_wrappers # pylint: disable=C0415
            add_fast_api_auto_instr_wrappers(self, wrapper_instance)
            return

        if library_key == LAMBDA and '_HANDLER' not in os.environ:
            return
        logger.debug("registering library %s with wrapper instance", library_key)
        self.register_library(library_key, wrapper_instance)


    def register_library(self, library_name, wrapper_instance):
        """will configure settings on an instrumentation wrapper + apply"""
        logger.debug('attempting to register library instrumentation: %s', library_name)
        try:
            self._init.init_library_instrumentation(library_name, wrapper_instance)
        except Exception as err:  # pylint: disable=W0703
            logger.debug(constants.EXCEPTION_MESSAGE, library_name, err, traceback.format_exc())

    def register_processor(self, processor) -> None:  # pylint: disable=R1710
        '''Add additional span exporters + processors'''
        logger.debug('Entering Agent.register_processor().')
        logger.debug("initialized %s", self.is_initialized())
        if not self.is_initialized():
            return None
        return self._init.register_processor(processor)



    def is_enabled(self) -> bool:
        '''Is agent enabled?'''
        enabled = get_env_value('ENABLED')
        if enabled:
            if enabled.lower() == 'false':
                logger.debug("ENABLED is disabled.")
                return False
        return True

    def is_initialized(self) -> bool:
        '''Is agent initialized - if an agent fails to init we should let the app continue'''
        if not self.is_enabled():
            return False
        if not self._initialized:
            return False
        return True


    def add_traceable_filter(self):
        logger.debug("in add_traceable_filter")
        if self.is_lambda:
            logger.info('Not loading blocking extension - currently unsupported in lambda')
            return
        # We need to do a local import so that the extension is not loaded in a parent process
        from traceableai.filter.traceable import Traceable, _LIBTRACEABLE_AVAILABLE  # pylint:disable=C0413,C0412,C0415
        if not _LIBTRACEABLE_AVAILABLE:
            logger.info("libtraceable unavailable, skipping filter registration")
            return
        if Config().config.blocking_config.enabled.value is not True:
            logger.info("Not adding libtraceable filter - blocking is not enabled")
            return
        try:
            Registry().register(Traceable)
            logger.debug("successfully initialized traceable filter")
        except Exception as exc: # pylint:disable=W0703
            logger.debug(''.join(traceback.format_exception(None, exc, exc.__traceback__)))
            logger.info("failed to register traceable filter")
