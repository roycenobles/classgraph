import os, glob

class ApexClass:

    def __init__(self, name, text):
        self.name = name.replace('.cls', '')
        self.isTest = self.get_is_test(text)
        self.isInterface = self.get_is_interface(text)
        self.dependencies = []
        self.text = text

    def analyze_dependencies(self, classmap):
        utext = self.text.upper()
        for key in classmap.keys():
            ukey = key.upper()
            if (ukey + '.' in utext) or (ukey + '(' in utext):
                self.dependencies.append(key)
    
    def get_is_test(self, text):
        return '@ISTEST' in text.upper()

    def get_is_interface(self, text):
        return 'INTERFACE ' in text.upper()

class ApexPackage:

    def __init__(self, namespace, path):
        self.namespace = namespace
        self.classes = []
        self.load_class_definitions(path)
        self.analyze_classes()

    def analyze_classes(self):
        classmap = self.get_class_dictionary()
        for cls in self.classes:
            cls.analyze_dependencies(classmap)

    def get_class_dictionary(self):
        classes = {}
        for cls in self.classes:
            classes[cls.name] = cls
        return classes

    def load_class_definitions(self, path):
        curdir = os.getcwd()
        os.chdir(path)
        cfilter = SimpleClassFilter()
        for clsname in glob.glob('*.cls'):
            with open(clsname, 'r') as file:
                cls = ApexClass(clsname, file.read())
                if cfilter.matches(cls):
                    self.classes.append(cls)                
        os.chdir(curdir)

    def load_dependencies(self):
        print('ok')

class SimpleClassFilter:

    def matches(self, cls):
        if cls.isTest or cls.isInterface:
            return False
        else:
            return True