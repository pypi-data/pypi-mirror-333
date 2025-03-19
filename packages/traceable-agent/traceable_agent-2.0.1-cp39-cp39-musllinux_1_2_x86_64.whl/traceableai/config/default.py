DEFAULT = {
    'opa': {
        'enabled': False,
        'endpoint': 'http://localhost:8181',
        'poll_period_seconds': 30,
    },
    'blocking_config': {
        'enabled': True,
        'debug_log': False,
        'evaluate_body': True,
        'modsecurity': {
            'enabled': True
        },
        'skip_internal_request': True,
        'regionBlocking': {
            'enabled': True
        },
        'max_recursion_depth': 20
    },
    'remote_config': {
        'enabled': True,
        'endpoint': 'localhost:5441',
        'poll_period_seconds': 30,
    },
    'enabled': True,
    'propagation_formats': ['TRACECONTEXT'],
    'service_name': 'pythonagent',
    'reporting': {
        'endpoint': 'http://localhost:4317',
        'secure': False,
        'trace_reporter_type': 'OTLP',
        'token': '',
    },
    'data_capture': {
        'http_headers': {
            'request': True,
            'response': True,
        },
        'http_body': {
            'request': True,
            'response': True,
        },
        'rpc_metadata': {
            'request': True,
            'response': True,
        },
        'rpc_body': {
            'request': True,
            'response': True,
        },
        'body_max_size_bytes': 131072
    },
    'resource_attributes': {}
}
