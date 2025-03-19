import os

def get_env_value(target_key):
    env_var_key = f"TA_{target_key}"
    if env_var_key in os.environ:
        return os.environ[env_var_key]
    return None
