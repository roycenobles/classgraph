'''
This is a somewhat brut-force way of search for and recording class dependencies.
'''
import glob, os

class Class(object):
    name = ''
    extension = ''
    code = ''
    isTest = False
    dependencies = []

    def __init__(self, fullname, text):
        self.name = fullname.replace('.cls', '')
        self.extension = 'cls'
        self.code = text
        if "@ISTEST" in text.upper(): #inconclusive, but works for now
            self.isTest = True

    def analyze_dependencies(self, classes):
        text = self.code.upper()
        for key in classes.keys():
            if (key + '.' in text) or (key + '(' in text):
                self.dependencies.append(classes.get(key))

    def to_json(self):
        json = '{' + '"name": "' + self.name + '"'
        json += ', "dependencies": ['
        for dep in self.dependencies:
            #if self != dep:
                #json += dep.to_json()
        json += ']'
        json += '}'
        return json

class Package(object):
    namespace = ''
    classes = []

    def analyze_classes(self):
        classes = self.get_class_dictionary()
        for cls in self.classes:
            cls.analyze_dependencies(classes)

    def get_class_dictionary(self):
        classes = {}
        for cls in self.classes:
            classes[cls.name.upper()] = cls
        return classes

    def to_json(self):
        json = '{'
        json += '"namespace": "' + self.namespace + '"'
        json += ', "classes": ['
        for cls in self.classes:
            json += cls.to_json() + ','
        json = json[:-1]
        json += ']' 
        json += '}'
        return json

class PackageFactory(object):

    @staticmethod
    def create_from_folder(path, namespace, includeTests):
        pkg = Package()
        pkg.namespace = namespace
        os.chdir(path)
        for clsname in glob.glob("*.cls"):
            with open(clsname, 'r') as file:
                cls = Class(clsname, file.read())
                if ((cls.isTest == False) or includeTests):
                    pkg.classes.append(cls)
        pkg.analyze_classes()
        return pkg

pkg = PackageFactory().create_from_folder('./nforce/src/classes', 'nFORCE', False)

f = open('temp.json', 'w')
f.write(pkg.to_json())
f.close()