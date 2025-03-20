import sys
from importlib.metadata import version
import socket


class HelpCommands:
    def get_version(): # macun --version
        try: return version("macun")
        except: return "Unknown"

    def show_help(): #macun --help 
        return """usage: macun <command>
commands:

--version, version, -V
    displays current macun version

--help, help, -H
    display commands

Any terminal command
    runs the command with macun
"""

def check_command():
    if sys.argv[1] in ("--version", "version", "-V"):
        output = f"macun-{HelpCommands.get_version()}"

    elif sys.argv[1] in ("--help", "help", "-H"):
        output = HelpCommands.show_help()
        
    else: return None
    return output

def check_internet(timeout=3) -> bool: #Checks if the device has an active internet connection.
    try:
        socket.setdefaulttimeout(timeout)
        socket.create_connection(("8.8.8.8", 53)) # Google's public DNS
        return True
    except OSError:
        return False
