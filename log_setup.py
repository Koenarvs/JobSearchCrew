import os
import logging

def setup_logging(debug_mode=False):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(script_dir, 'logs')
    
    # Ensure logs directory exists
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    log_file_path = os.path.join(logs_dir, 'app.log')
    
    # Set logging level based on debug_mode
    log_level = logging.DEBUG if debug_mode else logging.INFO
    
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
