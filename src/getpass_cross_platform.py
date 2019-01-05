import platform


def getpass(prompt):
    """Replacement for getpass.getpass() which prints asterisks for each character typed"""
    print(prompt, end='', flush=True)
    buf = ''
    while True:
        ch = getch()
        if 'Windows' == platform.system():
            if ch in [b'\r']:
                print()
                break
            elif ch in [b'\x03', b'\x06']:
                print()
                raise KeyboardInterrupt
            else:
                buf += ch.decode('utf-8')
                print('*', end='', flush=True)
        else:
            if ch in ['\r', '\n']:
                print()
                break
            elif ch in ['\x03', '\x06']:
                print()
                raise KeyboardInterrupt
            else:
                buf += ch
                print('*', end='', flush=True)
    return buf


def getch():
    if 'Windows' == platform.system():
        import msvcrt
        return msvcrt.getch()
    else:
        import sys, termios, tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            char = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return char
