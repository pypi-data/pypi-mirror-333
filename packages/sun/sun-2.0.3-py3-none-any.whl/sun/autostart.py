#!/usr/bin/python3
# -*- coding: utf-8 -*-

import shutil
import sys
from pathlib import Path

from sun.sys_info import get_os_info


def daemon_autostart() -> None:
    """SUN autostart enable-disable script.
    """
    data_configs = get_os_info()
    args: list[str] = sys.argv
    args.pop(0)

    enable_file: Path = Path(data_configs['xdg_autostart'], 'sun-daemon.desktop')
    disable_file: Path = Path(data_configs['xdg_autostart'], 'sun-daemon.desktop.sample')

    message: str = 'The sun-daemon autostart is'
    message_enabled: str = f'{message} enabled.'
    message_disabled: str = f'{message} disabled.'
    message_already_enabled: str = f'{message} already enabled.'
    message_already_disabled: str = f'{message} already disabled.'

    if len(args) == 1 and args[0] == 'enable':

        if disable_file.is_file():
            shutil.move(disable_file, enable_file)
            print(message_enabled)

        elif enable_file.is_file():
            print(message_already_enabled)

    elif len(args) == 1 and args[0] == 'disable':

        if enable_file.is_file():
            shutil.move(enable_file, disable_file)
            print(message_disabled)

        elif disable_file.is_file():
            print(message_already_disabled)

    elif len(args) == 1 and args[0] == 'status':

        if enable_file.is_file():
            print(message_enabled)

        elif disable_file.is_file():
            print(message_disabled)

    else:
        print("Sun autostart is a script to enable-disable sun daemon.\n"
              "\nUsage: sun-autostart [OPTIONS]\n"
              "\nOptional arguments:\n"
              "  enable      Enable autostart SUN daemon.\n"
              "  disable     Disable autostart SUN daemon.\n"
              "  status      View status for autostart SUN daemon.\n")
