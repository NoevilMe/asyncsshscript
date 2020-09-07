import asyncio
import asyncsshscript

async def run_client_test():
    conn = asyncsshscript.AuthHostSession('127.0.0.1',
                               username='user',
                               password='passwd')
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