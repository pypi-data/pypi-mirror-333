from collections.abc import Generator
from contextlib import contextmanager
import importlib.resources
import logging
from pathlib import Path
import re
import subprocess
import sys
from threading import Thread
import time
from typing import IO
import typer

if sys.platform == "win32":
    server_name = "server.exe"
else:
    server_name = "server"

LOGGER = logging.getLogger(__name__)

def server_binary_path() -> Path:
    with importlib.resources.as_file(importlib.resources.files(__name__)) as base:
        if (path := base / "bin" / server_name).exists():
            return path
        raise Exception("Can't find server binary")

def server_binary() -> Path:
    path = server_binary_path()
    if sys.platform == "linux":
        setcap_check(path)
    return path

def setcap_permissions() -> str:
    return "cap_net_raw,cap_net_admin,cap_net_bind_service+ep"

def setcap_check(path: Path):
    update = ["setcap", setcap_permissions(), str(path)]
    check = ["setcap", "-v", setcap_permissions(), str(path)]
    try:
        subprocess.check_output(check)
    except subprocess.CalledProcessError:
        LOGGER.warning(
            "You need to allow raw sockets and binding to low port numbers for server to function."
        )
        confirm = typer.confirm("Do you wish automatically adjust permissions using policy kit")
        if confirm:
            try:
                subprocess.check_output(["pkexec", *update])
                return
            except subprocess.CalledProcessError:
                LOGGER.error("Failed to adjust permissions")

        typer.echo()
        typer.echo("Run the following as root or privileged user:")
        typer.echo()
        typer.echo(" ".join(update))
        typer.echo()
        exit(-1)
    except FileNotFoundError:
        # System does not support setcap, could be widows for example
        pass


_osal_log_to_python = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARN": logging.WARNING,
    "ERROR": logging.ERROR,
    "FATAL": logging.FATAL,
}


@contextmanager
def server_run(interface: str) -> Generator[subprocess.Popen, None, None]:
    server = server_binary()

    process = subprocess.Popen(
        [server, interface],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        close_fds=True,
    )

    parser = re.compile(r"\[(\d+\:\d+\:\d+)? ?([a-zA-Z]+) ?] (.*)\n")

    def monitor(stream: IO[bytes]):
        while line := stream.readline():
            m = parser.match(line.decode())
            if m:
                level = _osal_log_to_python.get(m[2], logging.INFO)
                logging.log(level, m[3])
            else:
                logging.log(logging.INFO, line)

    Thread(None, target=monitor, args=[process.stdout]).start()
    Thread(None, target=monitor, args=[process.stderr]).start()

    time.sleep(1)
    try:
        yield process
    finally:
        process.kill()
        process.wait()
