from apex import ApexPackage
from plantuml import PlantUmlDocument

doc = PlantUmlDocument('Class Diagram')
pkg = ApexPackage('nFORCE', '../nforce/src/classes')

for cls in pkg.classes:
    doc.add_class(cls)

doc.save('output.txt')