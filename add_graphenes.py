import numpy as np

# File names and parameters
cellulose_file = 'Outputs/aligned_cellulose_20L.pdb'
graphene_file = 'Outputs/graphene_yz.pdb'
output_file = 'Outputs/cellulose_graphene_structure.pdb'
angstrom_separation = 2.0

def read_pdb(filename):
    atoms = []
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('ATOM'):
                atoms.append(line.strip())
    return atoms

def write_pdb(filename, atoms):
    with open(filename, 'w') as f:
        for atom in atoms:
            f.write(atom + '\n')

def modify_cellulose(cellulose_atoms):
    modified_atoms = []
    for atom in cellulose_atoms:
        x = float(atom[30:38])
        y = float(atom[38:46])
        z = float(atom[46:54])
        chain = atom[72]
        layer = int(atom[73:76])
        
        if layer > 10:
            x += 2 * angstrom_separation  # Translate layers above 10 by 2A
        
        modified_atom = f"{atom[:30]}{x:8.3f}{y:8.3f}{z:8.3f}{atom[54:]}"
        modified_atoms.append(modified_atom)
    
    return modified_atoms

def align_graphene_layer(graphene_atoms, cellulose_atoms):
    # Get the dimensions of the cellulose structure
    cellulose_y = [float(atom[38:46]) for atom in cellulose_atoms]
    cellulose_z = [float(atom[46:54]) for atom in cellulose_atoms]
    cellulose_y_min, cellulose_y_max = min(cellulose_y), max(cellulose_y)
    cellulose_z_min, cellulose_z_max = min(cellulose_z), max(cellulose_z)

    # Get the dimensions of the graphene layer
    graphene_y = [float(atom[38:46]) for atom in graphene_atoms]
    graphene_z = [float(atom[46:54]) for atom in graphene_atoms]
    graphene_y_min, graphene_y_max = min(graphene_y), max(graphene_y)
    graphene_z_min, graphene_z_max = min(graphene_z), max(graphene_z)

    # Calculate scaling factors
    y_scale = (cellulose_y_max - cellulose_y_min) / (graphene_y_max - graphene_y_min)
    z_scale = (cellulose_z_max - cellulose_z_min) / (graphene_z_max - graphene_z_min)

    # Align and scale graphene layer
    aligned_atoms = []
    for atom in graphene_atoms:
        x = float(atom[30:38])
        y = (float(atom[38:46]) - graphene_y_min) * y_scale + cellulose_y_min
        z = (float(atom[46:54]) - graphene_z_min) * z_scale + cellulose_z_min
        aligned_atom = f"{atom[:30]}{x:8.3f}{y:8.3f}{z:8.3f}{atom[54:]}"
        aligned_atoms.append(aligned_atom)

    return aligned_atoms

def create_graphene_layer(graphene_atoms, x_offset):
    new_layer = []
    for atom in graphene_atoms:
        x = x_offset
        y = float(atom[38:46])
        z = float(atom[46:54])
        
        new_atom = f"{atom[:30]}{x:8.3f}{y:8.3f}{z:8.3f}{atom[54:]}"
        new_layer.append(new_atom)
    
    return new_layer

def fix_atom_numbers(atoms):
    fixed_atoms = []
    for i, atom in enumerate(atoms, start=1):
        fixed_atom = f"{atom[:6]}{i:5d}{atom[11:]}"
        fixed_atoms.append(fixed_atom)
    return fixed_atoms

def main():
    # Read input files
    cellulose_atoms = read_pdb(cellulose_file)
    graphene_atoms = read_pdb(graphene_file)
    
    # Modify cellulose structure
    modified_cellulose = modify_cellulose(cellulose_atoms)
    
    # Align graphene layer with cellulose structure
    aligned_graphene = align_graphene_layer(graphene_atoms, modified_cellulose)
    
    # Find the x-coordinates of the first and last layers
    x_min = min(float(atom[30:38]) for atom in modified_cellulose)
    x_max = max(float(atom[30:38]) for atom in modified_cellulose)
    x_middle = (x_min + x_max) / 2
    
    # Create graphene layers at specific x-coordinates
    bottom_graphene = create_graphene_layer(aligned_graphene, x_min - angstrom_separation)
    middle_graphene = create_graphene_layer(aligned_graphene, x_middle)
    top_graphene = create_graphene_layer(aligned_graphene, x_max + angstrom_separation)
    
    # Combine all structures
    final_structure = (
        bottom_graphene +
        modified_cellulose[:len(modified_cellulose)//2] +
        middle_graphene +
        modified_cellulose[len(modified_cellulose)//2:] +
        top_graphene
    )
    # Fix atom numbers
    final_structure_fixed = fix_atom_numbers(final_structure)
        
    # Write the final structure to a new PDB file
    write_pdb(output_file, final_structure_fixed)

if __name__ == '__main__':
    main()