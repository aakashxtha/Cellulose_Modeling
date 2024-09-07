# Cellulose_Modeling Project

## Overview
This project focuses on computational modeling of cellulose crystal structures with graphene layers. It includes scripts for rotating graphene, building and aligning cellulose crystals, and combining cellulose with graphene layers.

## Table of Contents
1. [Files](#files)
2. [Dependencies](#dependencies)
3. [Installation](#installation)
4. [Usage](#usage)
   - [Rotate Graphene](#rotate-graphene)
   - [Build Crystal](#build-crystal)
   - [Align Crystal](#align-crystal)
   - [Add Graphenes](#add-graphenes)
5. [Output](#output)
6. [Modeling Process](#modeling-process)
7. [Notes](#notes)
8. [License](#license)

## Files
* **Main Scripts**:
   * `rotate_graphene.py`: Transforms graphene coordinates to align with the yz-plane
   * `build_crystal.py`: Generates a 20-layer cellulose crystal structure
   * `align_crystal.py`: Aligns the cellulose crystal structure along the x-axis
   * `add_graphenes.py`: Adds graphene layers to the cellulose structure
* **Input Files**:
   * `Inputs/cellulose_4L.pdb`: Initial 4-layer cellulose structure
   * `Inputs/graphene.pdb`: Initial graphene structure
* **Output Files**:
   * `Outputs/`: Directory where generated files are saved
   * `Example_Outputs/`: Directory containing example output files

## Dependencies
* Python 3.x
* NumPy

## Installation
1. Clone the repository:
```
git clone https://github.com/aakashxtha/Cellulose_Modeling.git
cd Cellulose_Modeling
mkdir Outputs
```

2. Ensure NumPy is installed in your Python environment:
```
pip install numpy
```

## Usage
### Rotate Graphene
```
python rotate_graphene.py
```

### Build Crystal
```
python build_crystal.py
```

### Align Crystal
```
python align_crystal.py
```

### Add Graphenes
```
python add_graphenes.py
```

## Output
Results are generated in the `Outputs/` directory:
* `graphene_yz.pdb`: Rotated graphene structure
* `cellulose_20L.pdb`: 20-layer cellulose crystal structure
* `aligned_cellulose_20L.pdb`: Aligned cellulose crystal structure
* `cellulose_graphene_structure.pdb`: Final combined cellulose-graphene structure

## Modeling Process
1. Rotate the graphene structure to align with the yz-plane
2. Build a 20-layer cellulose crystal from the initial 4-layer structure
3. Align the cellulose crystal structure along the x-axis
4. Add graphene layers to the cellulose structure at specific positions

## Notes
- Scripts should be run in the order listed in the Usage section
- The `Example_Outputs/` directory contains sample output files for reference

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
