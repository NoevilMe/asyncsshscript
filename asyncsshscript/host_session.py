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
""" Host authorized by password connection session """

import asyncio

import asyncssh
import asyncsshscript.script_type as ast


class _Password:
    def __init__(self, password):
        self._password = password


class VariantCommand(_Password):
    """A variant command to resolve sudo problem

    Args:
        _Password (_Password): A password is required
    """
    def __init__(self, password, command, content=None, sudo=False):
        """VariantCommand constructor

        Args:
            password (str): password for user
            command (str): original command
            content (str, optional): script file content if a script is provided. Defaults to None.
            sudo (bool, optional): sudo or. Defaults to False.
        """

        super().__init__(password)
        self._command = command
        self._sudo = sudo

        if sudo and content is None:
            self._variety = 'echo {} | sudo -k  -S '.format(
                self._password) + self._command
        elif sudo and content is not None:
            self._variety = "echo -e \"{}\r{}\" | sudo -k -S ".format(
                self._password, content) + self._command
        else:
            self._variety = None

    @property
    def sudo(self):
        """Whether 'sudo' is applied

        Returns:
            bool: sudo is required or not
        """

        return self._sudo

    @property
    def command(self):
        """Original command

        Returns:
            str: command user provided
        """

        return self._command

    @property
    def variety(self):
        """The real command which is going to be executed

        Returns:
            str: command to be executed
        """

        return self._variety if self._variety is not None else self._command

    @property
    def variant(self):
        """Variant or not

        Returns:
            bool: variant or not
        """

        return self._variety is not None


class _PasswordAuth(_Password):
    def __init__(self, username, password):
        super().__init__(password)
        self._username = username


class PasswordAuthHost(_PasswordAuth):
    """Host information including IP, username and password

    Args:
        _PasswordAuth (_PasswordAuth): username and password
    """
    def __init__(self, host, username, password):
        super().__init__(username, password)
        self.host = host


class AuthHostSession(PasswordAuthHost):
    """Remote host connection session which is authorized by username and password

    Args:
        PasswordAuthHost (PasswordAuthHost): Host information including IP, username and password
    """
    def __init__(self, host, username, password):
        """Constructor

        Args:
            host (str): host ip address
            username (str): username for host
            password (str): password for username
        """
        super().__init__(host, username, password)

        self._client_conn = None
        self._sudo_prompt = '[sudo] password for {}: '.format(username)

    @property
    def sudo_prompt(self):
        """sudo_prompt English sudo prompt

        Returns:
            string: usually it is '[sudo] password for XXX: '
        """

        return self._sudo_prompt

    def create_variant_command(self, command, content=None, sudo=False):
        """Create the variant command

        Args:
            command (str): original command
            content (str, optional): script content. Defaults to None.
            sudo (bool, optional): need 'sudo' or not. Defaults to False.

        Returns:
            VariantCommand: new created VariantCommand instance
        """

        return VariantCommand(self._password,
                              command,
                              content=content,
                              sudo=sudo)

    async def connect(self, timeout=5, known_hosts=None, **kwargs):
        """Connect to the remote host. Additional arguments could be provided, please refer to
        [asyncssh.connect](https://asyncssh.readthedocs.io/en/latest/api.html#connect)

        Args:
            timeout (int, optional): a seconds timeout . Defaults to 5.

        Returns:
            bool: success
        """
        try:
            self._client_conn = await asyncio.wait_for(asyncssh.connect(
                self.host,
                username=self._username,
                password=self._password,
                known_hosts=known_hosts,
                **kwargs),
                                                       timeout=timeout)
            return True
        except asyncio.TimeoutError as e:
            self._client_conn = None
            raise
        except Exception as e:
            self._client_conn = None
            raise

    async def close(self):
        """Disconnect from the remote host
        """

        if self._client_conn is not None:
            self._client_conn.close()
            await self._client_conn.wait_closed()

    async def _execute(self, variant_command, input=None):
        async with self._client_conn.create_process(
                variant_command.variety, env={'LANG':
                                              'en_US.UTF-8'}) as process:

            done = asyncssh.SSHCompletedProcess()
            done.stdout, done.stderr = await process.communicate(input=input)

            done.command = variant_command.command
            done.env = process.env
            done.exit_status = process.exit_status
            done.exit_signal = process.exit_signal
            done.returncode = process.returncode
            return done

    async def command(self, command, sudo=False):
        """Execute command on remote host

        Args:
            command (str): command line string
            sudo (bool, optional): sudo or not. Defaults to False.

        Returns:
            `asyncssh.SSHCompletedProcess`: Results from running an SSH process
        """

        return await self._execute(
            self.create_variant_command(command, None, sudo))

    async def script(self, script_type, content, sudo=False):
        """Execute script file content on remote host

        Args:
            script_type (ScriptType): AsyncSSHScript ScriptType
            content (str): script file content
            sudo (bool, optional): sudo or not. Defaults to False.

        Returns:
            `asyncssh.SSHCompletedProcess`: Results from running an SSH process
        """
        if sudo:
            return await self._execute(
                self.create_variant_command(
                    ast.get_script_stdin_executor(script_type), content, True))
        else:
            return await self._execute(
                self.create_variant_command(
                    ast.get_script_stdin_executor(script_type), None, False),
                content)

    async def bash(self, content, sudo=False):
        """Execute bash file content on remote host

        Args:
            content (str): bash file content
            sudo (bool, optional): sudo or not. Defaults to False.

        Returns:
            `asyncssh.SSHCompletedProcess`: Results from running an SSH process
        """
        return await self.script(ast.ScriptType.BASH, content, sudo=sudo)

    async def bash_file(self, file, sudo=False):
        """Execute a local bash on remote host according to its path

        Args:
            file (str): bash file path
            sudo (bool, optional): sudo or not. Defaults to False.

        Returns:
            `asyncssh.SSHCompletedProcess`: Results from running an SSH process
        """
        with open(file, 'r') as rf:
            return await self.bash(rf.read(), sudo=sudo)
        return None


    async def python(self, content, sudo=False):
        """Execute python file content on remote host

        Args:
            content (str): python file content
            sudo (bool, optional): sudo or not. Defaults to False.

        Returns:
            `asyncssh.SSHCompletedProcess`: Results from running an SSH process
        """
        return await self.script(ast.ScriptType.PYTHON3, content, sudo=sudo)

    async def python_file(self, file, sudo=False):
        """Execute a local python on remote host according to its path

        Args:
            file (str): python file path
            sudo (bool, optional): sudo or not. Defaults to False.

        Returns:
            `asyncssh.SSHCompletedProcess`: Results from running an SSH process
        """
        with open(file, 'r') as rf:
            return await self.python(rf.read(), sudo=sudo)
        return None