AsyncSSHScript: running remote commands or scripts with asyncssh
================================================================

AsyncSSHScript is a Python package which provides an ability to run command or script directly on remote host with [AsyncSSH](https://github.com/ronf/asyncssh)
even `sudo` is required.

```python
import asyncio
import asyncsshscript

async def run_client_test():
    conn = asyncsshscript.AuthHostSession('10.10.10.178',
                               username='yourname',
                               password='yourpassword')
    ret = await conn.connect()
    if not ret:
        print("connection error")
        return


    print("----------command start--------------")
    print( await conn.command('ip a'))
    print("----------command done--------------")

    print("----------sudo command start--------------")
    print(await conn.command('dmidecode', sudo=True))
    print("----------sudo command done--------------")

    print("----------local bash file start--------------")
    print(await conn.bash_file('script_test.sh'))
    print("----------local bash file done--------------")

    print("----------sudo local bash file start--------------")
    print(await conn.bash_file('script_test_sudo.sh', sudo=True))
    print("----------sudo local bash file done-------------")

    print("----------local python file start--------------")
    print(await conn.python_file('script_test.py'))
    print("----------local python file done--------------")

    print("----------local sudo python file start--------------")
    print(await conn.python_file('script_test_sudo.py', sudo=True))
    print("----------local sudo python file done--------------")
    await conn.close()


try:
    asyncio.get_event_loop().run_until_complete(run_client_test())
except (OSError, asyncssh.Error) as exc:
    sys.exit('SSH connection failed: ' + str(exc))
```

License
-------

Copyright (c) 2020 by NoevilMe and others.

This program and the accompanying materials are made available under
the terms of the Eclipse Public License v2.0 which accompanies this
distribution and is available at:

 > http://www.eclipse.org/legal/epl-2.0/

 This program may also be made available under the following secondary
 licenses when the conditions for such availability set forth in the
 Eclipse Public License v2.0 are satisfied:

> GNU General Public License, Version 2.0, or any later versions of
    that license

SPDX-License-Identifier: EPL-2.0 OR GPL-2.0-or-later

Prerequisites
-------------

* Python 3.6+
* Asyncssh 2.2+

Installation
------------

Install AsyncSSHScript by running:

 `pip install asyncsshscript`
