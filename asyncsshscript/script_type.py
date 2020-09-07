# Copyright (c) 2020 by NoevilMe <surpass168@live.com> and others.
#
# This program and the accompanying materials are made available under
# the terms of the Eclipse Public License v2.0 which accompanies this
# distribution and is available at:
#
#     http://www.eclipse.org/legal/epl-2.0/
#
# This program may also be made available under the following secondary
# licenses when the conditions for such availability set forth in the
# Eclipse Public License v2.0 are satisfied:
#
#    GNU General Public License, Version 2.0, or any later versions of
#    that license
#
# SPDX-License-Identifier: EPL-2.0 OR GPL-2.0-or-later
#
# Contributors:
#     NoevilMe - initial implementation, API, and documentation

from enum import Enum


class ScriptType(Enum):
    """Script language type class
    """
    BASH = 1 #: #!/bin/bash
    SHELL = 2  #: #!/bin/sh
    PYTHON3 = 3  #: #!/usr/bin/python3


def get_script_executor(script_type):
    """Get the script executor according to its type

    Args:
        script_type (ScriptType): Script language type class

    Raises:
        ValueError: throw if is't ScriptType

    Returns:
        str: one of "bash", "sh" and "python3"
    """
    if not isinstance(script_type, ScriptType):
        raise ValueError("not a ScriptType")

    if script_type == ScriptType.BASH:
        return "bash"
    elif script_type == ScriptType.PYTHON3:
        return "python3"
    else:
        return "sh"


def get_script_stdin_executor(script_type):
    return "{} -".format(get_script_executor(script_type))
