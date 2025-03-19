import os
from traceableai.config import config_pb2


def _is_true(env_key):
    value = os.environ.get(env_key)
    if value is None:
        return False
    return value.lower() == 'true'


def overwrite_with_environment(config):  # pylint: disable=R0912,R0914,R0915
    # Blocking Configurations
    if "TA_BLOCKING_CONFIG_ENABLED" in os.environ:
        config.blocking_config.enabled.value = _is_true("TA_BLOCKING_CONFIG_ENABLED")

    if "TA_BLOCKING_CONFIG_DEBUG_LOG" in os.environ:
        config.blocking_config.debug_log.value = _is_true("TA_BLOCKING_CONFIG_DEBUG_LOG")

    if "TA_BLOCKING_CONFIG_EVALUATE_BODY" in os.environ:
        config.blocking_config.evaluate_body.value = _is_true("TA_BLOCKING_CONFIG_EVALUATE_BODY")

    if "TA_BLOCKING_CONFIG_MODSECURITY_ENABLED" in os.environ:
        config.blocking_config.modsecurity.enabled.value = _is_true("TA_BLOCKING_CONFIG_MODSECURITY_ENABLED")

    if "TA_BLOCKING_CONFIG_REGION_BLOCKING_ENABLED" in os.environ:
        config.blocking_config.region_blocking.enabled.value = _is_true("TA_BLOCKING_CONFIG_REGION_BLOCKING_ENABLED")

    if "TA_BLOCKING_CONFIG_MAX_RECURSION_DEPTH" in os.environ:
        config.blocking_config.max_recursion_depth.value = int(os.environ["TA_BLOCKING_CONFIG_MAX_RECURSION_DEPTH"])

    # Remote Configuration
    if "TA_REMOTE_CONFIG_ENABLED" in os.environ:
        config.remote_config.enabled.value = _is_true("TA_REMOTE_CONFIG_ENABLED")
    elif "TA_BLOCKING_CONFIG_REMOTE_CONFIG_ENABLED" in os.environ:
        config.remote_config.enabled.value = _is_true("TA_BLOCKING_CONFIG_REMOTE_CONFIG_ENABLED")

    if "TA_REMOTE_CONFIG_ENDPOINT" in os.environ:
        config.remote_config.endpoint.value = os.environ["TA_REMOTE_CONFIG_ENDPOINT"]
    elif "TA_BLOCKING_CONFIG_REMOTE_CONFIG_ENDPOINT" in os.environ:
        config.remote_config.endpoint.value = os.environ["TA_BLOCKING_CONFIG_REMOTE_CONFIG_ENDPOINT"]

    if "TA_REMOTE_CONFIG_POLL_PERIOD_SECONDS" in os.environ:
        config.remote_config.poll_period_seconds.value = int(os.environ["TA_REMOTE_CONFIG_POLL_PERIOD_SECONDS"])
    elif "TA_BLOCKING_CONFIG_REMOTE_CONFIG_POLL_PERIOD_SECONDS" in os.environ:
        config.remote_config.poll_period_seconds.value = int(os.environ["TA_BLOCKING_CONFIG_REMOTE_CONFIG_POLL_PERIOD_SECONDS"]) # pylint:disable=C0301

    if "TA_BLOCKING_CONFIG_SKIP_INTERNAL_REQUEST" in os.environ:
        config.blocking_config.skip_internal_request.value = _is_true("TA_BLOCKING_CONFIG_SKIP_INTERNAL_REQUEST")

    # OPA Configuration
    if "TA_OPA_ENABLED" in os.environ:
        config.opa.enabled.value = _is_true("TA_OPA_ENABLED")

    if "TA_OPA_ENDPOINT" in os.environ:
        config.opa.endpoint.value = os.environ["TA_OPA_ENDPOINT"]

    if "TA_OPA_POLL_PERIOD_SECONDS" in os.environ:
        config.opa.poll_period_seconds.value = int(os.environ["TA_OPA_POLL_PERIOD_SECONDS"])

    # Service Name
    service_name = os.environ.get("TA_SERVICE_NAME")
    if service_name:
        config.service_name.value = service_name

    # Reporting Configuration
    reporting_endpoint = os.environ.get("TA_REPORTING_ENDPOINT")
    if reporting_endpoint:
        config.reporting.endpoint.value = reporting_endpoint

    reporter_type = os.environ.get("TA_REPORTING_TRACE_REPORTER_TYPE")
    if reporter_type:
        config.reporting.trace_reporter_type = reporter_type

    # Corrected: Pass the environment key to _is_true
    if "TA_REPORTING_SECURE" in os.environ:
        config.reporting.secure.value = _is_true("TA_REPORTING_SECURE")

    reporting_token = os.environ.get("TA_REPORTING_TOKEN")
    if reporting_token:
        config.reporting.token = reporting_token

    # Data Capture Configuration
    headers_request = os.environ.get("TA_DATA_CAPTURE_HTTP_HEADERS_REQUEST")
    if headers_request:
        config.data_capture.http_headers.request.value = _is_true("TA_DATA_CAPTURE_HTTP_HEADERS_REQUEST")

    headers_response = os.environ.get("TA_DATA_CAPTURE_HTTP_HEADERS_RESPONSE")
    if headers_response:
        config.data_capture.http_headers.response.value = _is_true("TA_DATA_CAPTURE_HTTP_HEADERS_RESPONSE")

    body_request = os.environ.get("TA_DATA_CAPTURE_HTTP_BODY_REQUEST")
    if body_request:
        config.data_capture.http_body.request.value = _is_true("TA_DATA_CAPTURE_HTTP_BODY_REQUEST")

    body_response = os.environ.get("TA_DATA_CAPTURE_HTTP_BODY_RESPONSE")
    if body_response:
        config.data_capture.http_body.response.value = _is_true("TA_DATA_CAPTURE_HTTP_BODY_RESPONSE")

    rpc_metadata_request = os.environ.get("TA_DATA_CAPTURE_RPC_METADATA_REQUEST")
    if rpc_metadata_request:
        config.data_capture.rpc_metadata.request.value = _is_true("TA_DATA_CAPTURE_RPC_METADATA_REQUEST")

    rpc_metadata_response = os.environ.get("TA_DATA_CAPTURE_RPC_METADATA_RESPONSE")
    if rpc_metadata_response:
        config.data_capture.rpc_metadata.response.value = _is_true("TA_DATA_CAPTURE_RPC_METADATA_RESPONSE")

    rpc_body_request = os.environ.get("TA_DATA_CAPTURE_RPC_BODY_REQUEST")
    if rpc_body_request:
        config.data_capture.rpc_body.request.value = _is_true("TA_DATA_CAPTURE_RPC_BODY_REQUEST")

    rpc_body_response = os.environ.get("TA_DATA_CAPTURE_RPC_BODY_RESPONSE")
    if rpc_body_response:
        config.data_capture.rpc_body.response.value = _is_true("TA_DATA_CAPTURE_RPC_BODY_RESPONSE")

    body_max_size_bytes = os.environ.get("TA_DATA_CAPTURE_BODY_MAX_SIZE_BYTES")
    if body_max_size_bytes:
        config.data_capture.body_max_size_bytes.value = int(body_max_size_bytes)

    # Propagation Formats
    propagation_formats = os.environ.get("TA_PROPAGATION_FORMATS")
    if propagation_formats:
        tmp_propagation_formats = set()
        configured_propagation_formats = propagation_formats.split(",")

        if "TRACECONTEXT" in configured_propagation_formats:
            tmp_propagation_formats.add(config_pb2.PropagationFormat.TRACECONTEXT)
        if "B3" in configured_propagation_formats:
            tmp_propagation_formats.add(config_pb2.PropagationFormat.B3)

        # Default to TRACECONTEXT if no valid formats are specified
        if not tmp_propagation_formats:
            tmp_propagation_formats.add(config_pb2.PropagationFormat.TRACECONTEXT)

        config.propagation_formats[:] = list(tmp_propagation_formats)

    # Enable Config
    enabled = os.environ.get("TA_ENABLED")
    if enabled:
        config.enabled.value = _is_true("TA_ENABLED")

    # Resource Attributes
    resource_attributes = os.environ.get("TA_RESOURCE_ATTRIBUTES")
    if resource_attributes:
        groups = resource_attributes.split(",")
        for group in groups:
            key, value = group.split("=")
            config.resource_attributes[key] = value

    return config
