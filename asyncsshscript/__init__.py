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

from .host_session import VariantCommand, AuthHostSession
from .script_type import ScriptType, get_script_executor

from .version import __author__, __version__