# Utilities package for Analog Integrated Circuit Modelling

This repository features ```Python®``` scripts used for performing the modelling and initial theoretical approach to the development of analogue integrated circuits. Convetinally, scientists and engineers use ```MATLAB®``` to develop models of the system they're implementing, but in it is time modelling affairs start being perfomed by using an open-source, community-supported language and associated packages - such as ```Python®```!\
The repository file tree diagram can be represented as given:
```Python
modelling_utils/
|-- modelling_utils/
|   |-- __init__.py
|   |-- read.py # read models and specifications f/ disk
|   |-- write.py # save model and specifications t/ disk
|   |-- util.py # utilities file providing graphing and timing func wrappers
|   /
/
```
## Methodology
The methodology used while developping the scripts to conceive the models of the target system, and checking afterwards if the implemented system meets the specified requirements is given by the following state diagram:
```mermaid
flowchart
A(Circuit Development) --> B(Theoretical Circuit Analysis)
B --> C(Theoretical Circuit Model Development)
C --> D(In-Code Model Implementation)
D --> E(Specifications Development)
E --> F(Specifications Translation \n to circuit's device parameters)
F --> G(Model Testing) --> J(Plot Results) --> I(Result's Analysis)
I --> H{Meets \n Specifications?}
H --> |No| E
H --> |Yes| K(End) 
```
**Dependencies**:
- poetry - package manager for Python
- unittest - unit/atomic testing package for Python
- PyYAML - Python YAML parser package for loading and saving model information.
- Matplotlib - to plot and save 2D and 3D graphs.