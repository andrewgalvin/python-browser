import inquirer
from subprocess import Popen
import constants


def open_browser(command):
    """
    This function opens a new browser (in a new parallel process) window with the given command.

    Parameters:
        - command (str): a string that can be executed in the command line
    """
    return Popen(command)


def load_proxies():
    """
    This function loads a list of proxies from a file. The file path is specified in a constant variable PROXIES_FILE.
    Each line in the file should contain a single proxy. The function reads the file, removes the newline characters
    from each proxy, and returns the list of proxies.

    Correct format for a proxy is: HOSTNAME:PORT:USERNAME:PASSWORD

    Parameters:
        - None
    Raises:
        - FileNotFoundError: If the file cannot be found
        - Exception: if the file does not contain any proxies
    """
    proxy_data = open(constants.PROXIES_FILE).readlines()

    if len(proxy_data) > 0:
        return [proxy.replace("\n", "") for proxy in proxy_data]
    else:
        raise Exception(
            f"{constants.PROXIES_FILE} contains no proxies. Please add proxies before running the program"
        )


if __name__ == "__main__":
    questions = [
        inquirer.Checkbox(
            "proxy",
            message="Select a proxy (CTRL + C to CLOSE program)",
            choices=load_proxies(),
        ),
    ]

    while True:
        """
        The program will prompt the user to select one or more proxies from the list of available proxies.
        For each selected proxy, the program will open a new browser window using the open_browser function,
        passing in a command that includes the proxy, the browser file and the links file.
        The program will run indefinitely until the user stops it manually.
        """
        for proxy in inquirer.prompt(questions)["proxy"]:
            proc = open_browser(
                f"python {constants.BROWSER_FILE} {proxy} {constants.LINKS_FILE}"
            )
