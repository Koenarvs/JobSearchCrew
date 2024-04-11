import os
import logging

def setup_logging(debug_mode=False):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(script_dir, 'logs')
    
    # Ensure logs directory exists
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    print(f"Created logs directory at {logs_dir}")  # Diagnostic print

    log_file_path = os.path.join(logs_dir, 'app.log')
    print(f"Log file path: {log_file_path}")  # Diagnostic print

    # Set logging level based on debug_mode
    log_level = logging.DEBUG if debug_mode else logging.INFO

    # Configure basic logging
    logging.basicConfig(
        filename=log_file_path, 
        level=log_level, 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filemode='a'  # Append mode
    )

    # Suppress verbose asyncio debug logs by setting its logger to a higher level
    logging.getLogger("asyncio").setLevel(logging.INFO)

    # Diagnostic prints after logging configuration
    print("Basic logging configuration set up.")
    print(f"Current logging level: {logging.getLogger().getEffectiveLevel()}")
    print(f"Current logging handlers: {logging.getLogger().handlers}")
    
    # If in debug mode, also log to console
    if debug_mode:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        logging.getLogger('').addHandler(console_handler)
        print("Console handler added for debug mode.")

    # Test log entry after configuration
    logging.info("Test log entry - if you see this, logging to file works.")
    logging.debug("Debugging mode is enabled.")
