class File:
    def __init__(self, name : str, content="", core=False, executable=""):
        self.name = name
        self.content = content
        self.core = core
        self.executable = executable
    def getData(self):
        data = {}
        data['name'] = self.name
        data['content'] = self.content
        data['core'] = self.core
        data['executable'] = self.executable
        return data
    def __str__(self):
        return self.name

class Directory:
    def __init__(self, name : str, core=False, tag=""):
        self.name = name
        self.contents = {}
        self.core = core
        self.tag = tag
    def add(self, item):
        self.contents[item.name] = item
    def get(self, name : str):
        return self.contents.get(name)
    def getTag(self):
        return self.tag
    def delete(self, name : str):
        if name in self.contents:
            if self.contents[name.core]:
                print(f"Cannot delete core directory or file: {name}")
            else:
                del self.contents[name]
        else:
            print(f"No such file or directory: {name}")
    def listContents(self):
        return list(self.contents.keys())
    def __str__(self):
        return self.name

class FileSystem:
    def __init__(self, server_name : str):
        self.root = Directory("/")
        self.current_dir = self.root
        self.server_name = server_name
    def changeDir(self, path : str):
        if path == "/":
            self.current_dir = self.root
        else:
            parts = path.split("/")
            Dir = self.current_dir if parts[0] != "" else self.root
            for part in parts:
                if part == "..":
                    Dir = Dir.parent if Dir.parent else Dir
                elif part and part in Dir.contents and isinstance(Dir.contents[part], Directory):
                    Dir = Dir.contents[part]
                else:
                    print(f"No such directory: {path}")
                    return
            self.current_dir = Dir
    def makeDir(self, name : str, core=False, tag=""):
        if name in self.current_dir.contents:
            print(f"Directory {name} already exists.")
        else:
            new_dir = Directory(name, core, tag)
            self.current_dir.add(new_dir)
    def makeFile(self, name : str, content="", core=False, executable=""):
        if name in self.current_dir.contents:
            print(f"File {name} already exists.")
        else:
            new_file = File(name, content, core, executable)
            self.current_dir.add(new_file)
    def listDir(self):
        return self.current_dir.listContents()
    def readFile(self, name : str):
        if name in self.current_dir.contents and isinstance(self.current_dir.contents[name], File):
            return self.current_dir.contents[name].content
        else:
            print(f"No such file: {name}")
            return None
    def writeFile(self, name: str, content : str):
        if name in self.current_dir.contents and isinstance(self.current_dir.contents[name], File):
            self.current_dir.contents[name].content = content
        else:
            print(f"No such file: {name}")
    def delete(self, name : str):
        if name in self.current_dir.contents:
            del self.current_dir.contents[name]
        else:
            print(f"No such file or directory: {name}")
    def __str__(self):
        return self.server_name