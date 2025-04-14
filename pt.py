#! /usr/bin/env python3

#Importing libraries
import os
import sys
import json
import chardet
import readline
from unilog import *
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter

#MAIN PROGRAM
# ---------------------------------------------------------------------------------------------------------------------
#Blank class to pass error
class EncodingError(Exception):
    pass

# ---------------------------------------------------------------------------------------------------------------------

#Class for specifying commands
class cCommand:
    def __init__(self, title, function, category="default", tldr=None, synopsis=None, example=None):
        self.title      = title
        self.function   = function
        self.category   = category
        self.tldr       = tldr
        self.synopsis   = synopsis
        self.example    = example

# =====================================================================================================================

#Main class with commands
class cPT:
    def __init__(self, dev="luks", date="1997-08-09", major="1", minor="5", patch="a", config=None, cache=None):
        self.DEV    = dev
        self.DATE   = date
        self.MAJOR  = major
        self.MINOR  = minor
        self.PATCH  = patch

        self.RegisterCommand(cCommand("exit",self.Exit,"System","Exit the program","exit","exit"))
        self.RegisterCommand(cCommand("clear",self.Clear,"System","Clear the screen","clear","clear"))
        self.RegisterCommand(cCommand("help",self.Help,"System","Display this menu","help","help"))
        self.RegisterCommand(cCommand("credits",self.Credits,"System","Display credits","credits","credits"))

        basename = (os.path.basename(sys.argv[0]).split(".")[0])
        self.CACHEDIR   = cache if cache != None else basename
        self.CONFDIR    = config if config != None else basename

        print(f"{UTIL.CLEAR}")

    
    CONFDIR     = "/home/<user>/.config/<name>"
    CACHEDIR    = "/home/<user>/.cache/<name>"
    DEV         = None
    DATE        = None
    MAJOR       = None
    MINOR       = None
    PATCH       = None
    HEADER      = None
    COMMANDS    = []
    LOGO = [
        "██████╗ ████████╗",
        "██╔══██╗╚══██╔══╝",
        "██████╔╝   ██║   ",
        "██╔═══╝    ██║   ",
        "██║        ██║   ",
        "╚═╝        ╚═╝   "
    ]

    # ---------------------------------------------------------------------------------------------------------------------

    def PrintDict(self, color, content):
        try:
            for item in content:
                buffer = (17 - len(item[0])) * " "
                print(f"{color} │ {UTIL.RESET}{UTIL.BOLD}{item[0]}:{buffer}{UTIL.RESET}{item[1]}")
        except:
            print(" sheesh")
    # ---------------------------------------------------------------------------------------------------------------------

    def PrintList(self, color, content):
        try:
            for item in content:
                print(f"{color} │ {UTIL.RESET}{UTIL.BOLD}{item[0]}")
        except:
            print(" sheesh")
    # ---------------------------------------------------------------------------------------------------------------------

    def SelectItem(self, items):
        if type(items) != list or items == None:
            return None
        completer   = FuzzyWordCompleter(items)
        item        = prompt(f" Select Item (tab to show all): ", completer=completer)
        return item
    # ---------------------------------------------------------------------------------------------------------------------

    def Credits(self, args):
        content = []
        content.append(["Dev",self.DEV])
        content.append(["Date",self.DATE])
        content.append(["Dev",f"v{self.MAJOR}.{self.MINOR}:{self.PATCH}"])
        self.PrintDict(FG.CYAN, content)
    # ---------------------------------------------------------------------------------------------------------------------

    def SetLogo(self, logo):
        if type(logo) == list:
            self.LOGO = logo
        else:
            Log(LVL.WARN, "SetLogo(): Invalid Datatype!")
    # ---------------------------------------------------------------------------------------------------------------------

    def RegisterCommand(self, command):
        self.COMMANDS.append(command)
        self.COMMANDS = sorted(self.COMMANDS, key=lambda COMMAND: (COMMAND.category != 'System', COMMAND.category))
    # ---------------------------------------------------------------------------------------------------------------------

    def SearchCommand(self, cmd):
        for command in self.COMMANDS:
            if command.title == cmd:
                return command
        return None
    # ---------------------------------------------------------------------------------------------------------------------

    def ParseCommand(self, command):
        cmd, args = command, None
        if " " in command:
            cmd, args = command.split(" ", 1)
        print(f"{UTIL.UP}{UTIL.BOLD} >> {UTIL.RESET}{FG.GREEN}{cmd}{UTIL.RESET}")

        command = self.SearchCommand(cmd)

        if args != None and args == "?":
            content = []
            content.append(["Title",command.title])
            content.append(["TLDR",command.tldr])
            content.append(["Synopsis",command.synopsis])
            content.append(["Example",command.example])
            self.PrintDict(FG.YELLOW, content)
            return

        if command != None: command.function(args)
        elif cmd == "":     print(f"{UTIL.UP}{UTIL.CLEARLINE}")
        else:               print(f"{UTIL.UP}{UTIL.BOLD} >> {UTIL.RESET}{FG.RED}{cmd}{UTIL.RESET}")
    # ---------------------------------------------------------------------------------------------------------------------

    def Prompt(self, command=None):
        print(f"{UTIL.TOP}{UTIL.CLEARLINE}")
        for line in self.LOGO:
            print(f"{UTIL.CLEARLINE}{UTIL.BOLD}{FG.BLUE} {line}{UTIL.RESET}")
        print(f" {UTIL.CLEARLINE}v{self.MAJOR}.{self.MINOR}:{self.PATCH} - by {self.DEV} ({self.DATE})")

        for i in range(os.get_terminal_size().lines - len(self.LOGO)):
            print(f"{UTIL.DOWN}",end="")

        if command == None:
            command = input(f"{UTIL.BOLD} >> {UTIL.RESET}") 
        self.ParseCommand(command)
    # ---------------------------------------------------------------------------------------------------------------------

    def Exit(self, args):
        print(f"{UTIL.CLEAR}{UTIL.TOP}",end="")
        sys.exit(args)
    # ---------------------------------------------------------------------------------------------------------------------

    def Clear(self, args):
        print(f"{UTIL.CLEAR}{UTIL.TOP}",end="")
    # ---------------------------------------------------------------------------------------------------------------------

    def Help(self, args):
        sym     = "─"
        first   = True
        last    = ""
        for command in self.COMMANDS:
            buffer = (32 - len(command.category)) * sym
            if first:
                print(f"{FG.CYAN} ╭──── {UTIL.RESET}{UTIL.BOLD}{command.category}{UTIL.RESET}{FG.CYAN} {buffer}{UTIL.RESET}")
                first   = False
                last    = command.category
            elif last != command.category:
                print(f"{FG.CYAN} ├──── {UTIL.RESET}{UTIL.BOLD}{command.category}{UTIL.RESET}{FG.CYAN} {buffer}{UTIL.RESET}")
                last    = command.category
            buffer = (16 - len(command.title)) * " "
            print(f"{FG.CYAN} │ {UTIL.RESET}{UTIL.BOLD}{command.title}{UTIL.RESET}{buffer}{command.tldr}{UTIL.RESET}")
        print(f"{FG.CYAN} ╰──────────────────────────────────────{UTIL.RESET}")
    # ---------------------------------------------------------------------------------------------------------------------

    def GetEncoding(self, file_path):
        with open(file_path, "rb") as f:
            raw_data = f.read()
        result = chardet.detect(raw_data)
        return result['encoding']
    # ---------------------------------------------------------------------------------------------------------------------
    
    def CreateFileIfNotExists(self, filepath, filename):
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        if not os.path.isfile(full_path):
            with open(full_path, 'w') as file:
                print(f"File created at {full_path}")
    # ---------------------------------------------------------------------------------------------------------------------
    
    def ParseFile(self, file_path):
        valid_encodings = ["utf-8", "ascii"]
        try:
            encoding = self.GetEncoding(file_path)
            if encoding not in valid_encodings:
                raise EncodingError(f"Unsupported encoding: {encoding}")
            
            with open(file_path, "r", encoding=encoding) as file:
                if not file.readable():
                    raise IOError("File cannot be read.")
                content = file.read()
                return content
    
        except FileNotFoundError:
            print(f"No such file: {file_path}")
            exit(2)
        except PermissionError:
            print(f"Insufficient permissions to read file: {file_path}")
            exit(3)
        except UnicodeDecodeError:
            print(f"File is not a valid UTF-8 or ASCII encoded text file: {file_path}")
            exit(4)
        except EncodingError as e:
            print(f"{e} Please use a valid encoding.")
            print(f"Valid encodings: {valid_encodings}")
            exit(5)
        except IOError as e:
            print(f"IO error: {e}")
            exit(6)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            exit(99)

# =====================================================================================================================
# =====================================================================================================================
# =====================================================================================================================

#running main program
if __name__ == "__main__":
    pt = cPT()
    while True:
        pt.Prompt()
