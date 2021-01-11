import os
import sys
import webbrowser
import pathlib

from colorama import init
from pyfiglet import figlet_format
from termcolor import cprint
from waitress import serve

from fbot.wsgi import application
from django.core import management as mg


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def run(self, **kwargs):
        try:
            if kwargs["open_browser"]:
                webbrowser.open_new_tab(f"http://{self.host}:{self.port}")
        except Exception:
            pass

        serve(
            application,
            host=self.host,
            port=self.port,
            threads=1,
        )


def check_component():
    BASE = pathlib.Path().resolve()

    CONF_DIR = [
        "db.sqlite3",
        "driver",
        "files",
        "profiles",
    ]
    LOG_DIR = ["logs"]

    for i in CONF_DIR:
        path = BASE / f"config/{i}"
        print("=> Checking", i)

        if not (BASE / "config/db.sqlite3").is_file():
            mg.call_command("makemigrations", "robot")
            mg.call_command("migrate", "robot")
            print("=> Make", i, "\n")

        if not path.exists():
            path.mkdir(exist_ok=path.exists())
            print("=> Make", i, "\n")

    for i in LOG_DIR:
        path = BASE / i
        print("=> Checking", i)

        if not path.exists():
            path.mkdir(exist_ok=path.exists())
            print("=> Make", i, "\n")


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fbot.settings")

    init(strip=not sys.stdout.isatty())
    cprint(figlet_format("FBot", font="starwars"), attrs=["bold"])

    check_component()
    print("\n")

    server = Server("localhost", 9923)
    server.run(open_browser=True)
