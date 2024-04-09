import os
import logging

def setup_logging(debug_mode=False):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(script_dir, 'logs')
    
    # Ensure logs directory exists
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
        print(f"Created logs directory at {logs_dir}")  # For debugging purposes
    
    log_file_path = os.path.join(logs_dir, 'app.log')
    print(f"Log file path: {log_file_path}")  # For debugging purposes

    logging.info("Test log entry - if you see this, logging to file works.")

    # Set logging level based on debug_mode
    log_level = logging.DEBUG if debug_mode else logging.INFO
    
    print(f"Current logging level: {logging.getLogger().getEffectiveLevel()}")
    logging.debug("Debugging mode is enabled.")

    print(f"Current logging handlers: {logging.getLogger().handlers}")
    
    print("Setting up basic logging configuration...")
    logging.basicConfig(
        filename=log_file_path, 
        level=log_level, 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filemode='a'  # Append mode
    )
    
    # If in debug mode, also log to console
    if debug_mode:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        logging.getLogger('').addHandler(console_handler)
