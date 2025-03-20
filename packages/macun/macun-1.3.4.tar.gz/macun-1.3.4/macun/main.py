import sys
import subprocess
from colorama import Fore, Style, init
from io import StringIO
from macun.utils import check_command, check_internet

def main():
    init()  # Initialize Colorama for colored output
    if not len(sys.argv) > 1:
        print(
"""No input provided. To use macun: macun <command>
For more information: macun --help"""
)
        exit()


    arg = sys.argv[1:] # get rid of macun   macun python test.py -> python test.py
    output = StringIO()

    _ = check_command()
    if _ is not None:
        print(_)
        exit()


    try:
        result = subprocess.Popen(
            arg, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True
        )
        for line in result.stdout:
            print(line, end="")
            output.write(line)
        result.stdout.close()
        result.wait()

    except Exception:
        print(f"Check the spelling: {' '.join(arg)}")

    else:
        if result.returncode != 0:
            print(Fore.GREEN + "Exit Code:" + Style.RESET_ALL, result.returncode)
            print(Fore.RED + "Whoops! Looks like something went wrong with that command. Asking AI..." + Style.RESET_ALL)
            output.seek(0)
            message = f"""
Find the error and suggest a possible fix. Avoid using Markdown or any special formatting in your response.
$ {" ".join(arg)}
{output.read()}
[Command exited with {result.returncode}]
"""
            if check_internet():
                from g4f.client import Client
                gpt_client = Client()
                response = gpt_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": message}],
                    web_search=False
                )
                ai_response = "".join([choice.message.content for choice in response.choices])
                print(ai_response)
                    
            
            else:
                print("No interent connection provided")

if __name__ == "__main__":
    main()