import json
import inspect
from .models import Command
from typing import Callable, Dict
from nyvalis.tools import stdout, log

class Invoker:
    commands: Dict[str, Command] = {}
    logger = log.get(log.LIB_NAME)

    @classmethod
    def register(cls, name: str, func: Callable):
        if cls.commands.get(name):
            cls.logger.critical(f"Command with same name was found: `{name}`")
            stdout.error(f"Command with same name was found: `{name}`", exit=True)
        
        cls.logger.info(f"Command `{name}` registered")
        cls.commands[name] = Command(name=func.__name__, allowed=False, func=func)

    @classmethod
    def process(cls, command: Command, params, state):
        try:
            signature = inspect.signature(command.func)
            if "state" in signature.parameters:
                result = command.func(state, **params)
            else:
                result = command.func(**params)

            response = json.dumps({"data": result, "error": None})
            return response
        except Exception as err:
            cls.logger.error(err)
            response = json.dumps({"data": None, "error": str(err)})
            return response

def command(func):
    Invoker.commands[func.__name__] = Command(name=func.__name__, allowed=False, func=func)
    return func