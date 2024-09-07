import numpy as np

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

def extract_coordinates(atom):
    return np.array([float(atom[30:38]), float(atom[38:46]), float(atom[46:54])])

def get_chain(atom):
    return atom[72]

def get_layer(atom):
    return int(atom[73:76])

def align_crystal(atoms):
    # Group atoms by chain and layer
    chains = {}
    for atom in atoms:
        chain = get_chain(atom)
        layer = get_layer(atom)
        if chain not in chains:
            chains[chain] = {}
        if layer not in chains[chain]:
            chains[chain][layer] = []
        chains[chain][layer].append(atom)

    # Calculate average x-position of chain A for each layer
    chain_a_x_positions = {}
    for layer in chains['A']:
        x_positions = [extract_coordinates(atom)[0] for atom in chains['A'][layer]]
        chain_a_x_positions[layer] = np.mean(x_positions)

    # Calculate x-offsets for other chains
    chain_x_offsets = {chain: {} for chain in chains if chain != 'A'}
    for chain in chain_x_offsets:
        for layer in chains[chain]:
            if layer in chain_a_x_positions:
                x_positions = [extract_coordinates(atom)[0] for atom in chains[chain][layer]]
                avg_x_position = np.mean(x_positions)
                chain_x_offsets[chain][layer] = chain_a_x_positions[layer] - avg_x_position

    # Apply x-offsets and create new atom list
    new_atoms = []
    for atom in atoms:
        chain = get_chain(atom)
        layer = get_layer(atom)
        coords = extract_coordinates(atom)
        if chain != 'A':
            if layer in chain_x_offsets[chain]:
                coords[0] += chain_x_offsets[chain][layer]
        new_atom = f"{atom[:30]}{coords[0]:8.3f}{coords[1]:8.3f}{coords[2]:8.3f}{atom[54:]}"
        new_atoms.append(new_atom)

    return new_atoms

def main():
    # Read the crystal PDB file
    atoms = read_pdb('Outputs/cellulose_20L.pdb')

    # Align the crystal structure
    aligned_atoms = align_crystal(atoms)

    # Write the aligned structure to a new PDB file
    write_pdb('Outputs/aligned_cellulose_20L.pdb', aligned_atoms)

if __name__ == '__main__':
    main()