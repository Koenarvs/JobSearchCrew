import os
import sys
import logging

def load_configuration():
    required_env_vars = ["OPENAI_API_BASE", "OPENAI_MODEL_NAME", "OPENAI_API_KEY", "SERPER_API_KEY"]
    config = {}
    for var in required_env_vars:
        value = os.getenv(var)
        if value is None:
            logging.error(f"Environment Variable Error: {var} is not set.")
            sys.exit("Please set the required environment variables.")
        config[var] = value
    return config
