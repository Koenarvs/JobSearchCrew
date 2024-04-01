import json
from typing import Union, List, Tuple, Dict
from langchain.schema import AgentFinish
from datetime import datetime

log_filename = None

def get_log_filename():
    global log_filename
    if log_filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"job_search_logs_{timestamp}.txt"
    return log_filename

def log_agent_output(agent_output: Union[str, List[Tuple[Dict, str]], AgentFinish], agent_name: str = 'Generic call'):
    log_file = get_log_filename()

    with open(log_file, "a") as file:
        call_number = sum(1 for _ in open(log_file)) // 7 + 1

        if isinstance(agent_output, str):
            try:
                agent_output = json.loads(agent_output)
            except json.JSONDecodeError:
                pass

        if isinstance(agent_output, list) and all(isinstance(item, tuple) for item in agent_output):
            file.write(f"-{call_number}----Dict------------------------------------------\n")
            for action, description in agent_output:
                file.write(f"Agent Name: {agent_name}\n")
                file.write(f"Tool used: {getattr(action, 'tool', 'Unknown')}\n")
                file.write(f"Tool input: {getattr(action, 'tool_input', 'Unknown')}\n")
                file.write(f"Action log: {getattr(action, 'log', 'Unknown')}\n")
                file.write(f"Description: {description}\n")
                file.write("--------------------------------------------------\n")

        elif isinstance(agent_output, AgentFinish):
            file.write(f"-{call_number}----AgentFinish---------------------------------------\n")
            file.write(f"Agent Name: {agent_name}\n")
            output = agent_output.return_values['output']
            file.write(f"AgentFinish Output: {output}\n")
            file.write("--------------------------------------------------\n")

        else:
            file.write(f"-{call_number}-Unknown format of agent_output:\n")
            file.write(f"{type(agent_output)}\n")
            file.write(f"{agent_output}\n")