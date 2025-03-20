import inspect
import os
import json
import sys


def CountFlushTerm(auto_wipe: int):
    """
        :param auto_wipe: int
        The script counts how many times it has been executed in the terminal and clears the terminal when it reaches the given limit.
    """
    caller_file = inspect.stack()[1].filename
    current_file = os.path.basename(caller_file)

    if os.name == 'nt':
        RUN_COUNT_FILE = os.path.join(os.getenv("APPDATA"), "run_counterN.json")
    else:
        RUN_COUNT_FILE = os.path.expanduser("~/.config/run_counterN.json")

    if not os.path.exists(RUN_COUNT_FILE):
        with open(RUN_COUNT_FILE, "w") as file:
            json.dump({"run_count": 0}, file)

    with open(RUN_COUNT_FILE, "r") as file:
        data = json.load(file)
        run_count = data.get("run_count", 0)

    try:
        if run_count >= auto_wipe - 1:
            if "PYCHARM_HOSTED" in os.environ:
                sys.stdout.write("\033[H\033[J")
                sys.stdout.flush()
            else:
                os.system('clear' if os.name == 'posix' else 'cls')
            with open(RUN_COUNT_FILE, "w") as file:
                json.dump({"run_count": 0}, file)
            print(f'\033[92m$ {auto_wipe} times run, and terminal has been cleared!\033[0m', end='')
            return ""
    except:
        os.system('clear' if os.name == 'posix' else 'cls')
        return
    run_count += 1
    with open(RUN_COUNT_FILE, "w") as file:
        json.dump({"run_count": run_count}, file)

    print(f"$ {current_file} | count: {run_count}", end='')
    return ""