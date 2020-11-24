from ..Errors import CommandExecutionError
from . import browser_commands, profile_commands
from .types import BaseCommand, DumpProfCommand


def execute_command(
    command: BaseCommand,
    webdriver,
    browser_params,
    manager_params,
    extension_socket,
):
    """Executes BrowserManager commands
    commands are of form (COMMAND, ARG0, ARG1, ...)
    """

    try:
        command.execute(
            webdriver,
            browser_params,
            manager_params,
            extension_socket,
        )
        return
    except NotImplementedError:
        # Using old style dispatching
        pass

    if type(command) is DumpProfCommand:
        profile_commands.dump_profile(
            browser_profile_folder=browser_params["profile_path"],
            manager_params=manager_params,
            browser_params=browser_params,
            tar_location=command.dump_folder,
            close_webdriver=command.close_webdriver,
            webdriver=webdriver,
            compress=command.compress,
        )

    elif type(command) is RunCustomFunctionCommand:
        arg_dict = {
            "command": command,
            "driver": webdriver,
            "browser_params": browser_params,
            "manager_params": manager_params,
            "extension_socket": extension_socket,
        }
        command.function_handle(*command.func_args, **arg_dict)

    else:
        raise CommandExecutionError("Invalid Command", command)