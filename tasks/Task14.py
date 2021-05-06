import re
import json

class Interactor:
    def __init__(self):
        self.storage: set = set()
        self.current_id = 0
        self.stopped = False
        self.file = "src/storage.json"

    def command_quit(self):
        self.stopped = True

    def command_add(self):
        if self.current_args != None:
            decoded_args: str = re.match(r"^(\s*)?((?:\w+)(?:,\s*))*((\w+)(\s*)?)?$", self.current_args)
            decoded_args = decoded_args[0].replace(" ", "")
            decoded_args = decoded_args.replace("\t", "")
            decoded_args = set(decoded_args.split(","))
            self.storage |= decoded_args
        else:
            print("Invalid keys")

    def command_find(self):
        if self.current_args != None:
            decoded_args: str = re.match(r"^(\s*)?((?:\w+)(?:,\s*))*((\w+)(\s*)?)?$", self.current_args)
            decoded_args = decoded_args[0].replace(" ", "")
            decoded_args = decoded_args.replace("\t", "")
            decoded_args = set(decoded_args.split(","))
            print("Search result:")
            for element in self.storage & decoded_args:
                print(f"\t{element}")
        else:
            print("Invalid keys")

    def command_remove(self):
        if self.current_args != None:
            decoded_args: str = re.match(r"^(\s*)?((?:\w+)(\s*))?$", self.current_args)
            decoded_args = decoded_args[0].replace(" ", "")
            decoded_args = decoded_args.replace("\t", "")
            self.storage.discard(decoded_args)
        else:
            print("Invalid key")

    def command_list(self):
        if self.current_args != None:
            print("Warning 'list' command do not use arguments")
        idx = 0
        for el in self.storage:
            print(f"{el}")
            idx += 1

    def command_grep(self):
        if self.regex != None:
            for element in self.storage:
                if re.match(self.regex, element) != None:
                    print(f"{element}")
        else:
            print("Invalid regular expression")

    def command_save(self):
        if self.regex == None:
            self.regex = self.file
            with open(self.regex, "w") as writer:
                writer.write(json.dumps(list(self.storage)))
        else:
            print("Stored in 'storage.json'")

    def command_load(self):
        if self.regex == None:
            self.regex = self.file
            try:
                with open(self.regex, "r") as reader:
                    self.storage = set(json.loads(reader.read()))
            except FileExistsError as err:
                print(f"{err.strerror}")
        else:
            print("Fetching from 'storage.json'")

    def get_command(self):
        print("> ", end='')
        str = input()
        return str

    def decode_command(self, command: str):
        decode_result = re.match(r"^(\s*)?(?P<command>\w+)?(\s+)?((?P<command_args>[\w\s,]+)|(\"(?P<regexp>.*)\")|(?:.*))$", command)
        self.current_command = decode_result["command"]
        self.current_args = decode_result["command_args"]
        self.regex = decode_result["regexp"]

    def execute_command(self):
        command_name = self.current_command
        if command_name == None:
            print("Inavalid command format")
        else:
            executor = getattr(self, f"command_{command_name}", None)
            if executor != None:
                executor()
            else:
                print(f"Invalid command: '{command_name}'")

    def run(self):
        while not self.stopped:
            try:
                command = self.get_command()
                self.decode_command(command)
                self.execute_command()
            except EOFError:
                print('\n|--> Stopped <--|')
                self.stopped = True
                continue
            except KeyboardInterrupt:
                print('\n|--> Stopped <--|')
                self.stopped = True
                continue

def __main__():
    inter = Interactor()
    inter.run()

__main__()