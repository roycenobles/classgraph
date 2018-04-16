import os

class PlantUmlDocument:

    def __init__(self, title):
        self.title = title
        self.classes = []

    def add_class(self, cls):
        self.classes.append(cls)
    
    def save(self, path):
        if os.path.exists(path): os.remove(path)
        f = open(path, 'w+')
        f.write('title ' + self.title + '\n')
        f.write('\n')
        f.write('@startuml\n')
        for cls in self.classes:
            f.write('class ' + cls.name + '\n')
            for dep in cls.dependencies:
                f.write(cls.name + ' --> ' + dep + '\n')
        f.write('@enduml\n')
        f.close()