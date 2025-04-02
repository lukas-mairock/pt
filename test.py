#! /usr/bin/env python3

from math import *
from pt import *

def SysCall(args):
    os.system(args)

def Test(args):
    print("  /\\_/\\  (")
    print(" ( ^.^ ) _)")
    print("   \\\"/  (")
    print(" ( | | )")
    print("(__d b__)")


if __name__ == "__main__":
    pt = cPT("luks","2024-07-15","1","0","a")
    pt.RegisterCommand(cCommand("test",Test,"Test","Test0"))
    pt.RegisterCommand(cCommand("syscall",SysCall,"Local","Run a command on the system","syscall <command>","syscall echo Hello World"))

    logo = [
        "████████╗███████╗███████╗████████╗",
        "╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝",
        "   ██║   █████╗  ███████╗   ██║   ",
        "   ██║   ██╔══╝  ╚════██║   ██║   ",
        "   ██║   ███████╗███████║   ██║   ",
        "   ╚═╝   ╚══════╝╚══════╝   ╚═╝   "
    ]

    pt.SetLogo(logo)
    while True:
        pt.Prompt()
