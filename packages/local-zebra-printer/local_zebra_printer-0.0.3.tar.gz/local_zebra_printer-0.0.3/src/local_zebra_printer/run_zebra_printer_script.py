import os
import subprocess
import sys
from threading import Thread
from local_zebra_printer.local_zebra_printer import main as run_printer

def  main():
    # run_printer()
    thread = Thread(target=run_printer)
    # thread.daemon = True
    thread.start()
    # print("ok")
    # sys.exit(0)
    # return 0
    # exit(2)
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # current_dir = "/".join(current_dir.split("/")[0:-1])
    # process = subprocess.Popen(
    #     [f"{current_dir}/local_zebra_printer/local_zebra_printer.py"],
    #     stdout=subprocess.PIPE,
    #     stderr=subprocess.PIPE
    # )
    # stdout, stderr = process.communicate()
    # if stdout:
    #     print(stdout.decode())
    # if stderr:
    #     print(stderr.decode())

if __name__ == '__main__':
    sys.exit(main())