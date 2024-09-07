import string

#INPUT_FILE FORMAT
#ATOM    338  C1  BGLC0   1       0.323  -0.260   0.407  1.00  0.00      0101 C

#OUTPUT_FILE FORMAT
#ATOM      1  C1  BGLC0   1       0.323  -0.260   0.407  1.00  0.00      A001 C

# File names and parameters
input_file = 'Inputs/cellulose_4L.pdb'
output_file = 'Outputs/cellulose_20L.pdb'
total_layers = 20

# Read the input PDB file
atoms = []
with open(input_file, 'r') as f:
    for line in f:
        if line.startswith('ATOM'):
            atom_data = {
                'line': line,
                'serial': int(line[6:11]),
                'name': line[12:16].strip(),
                'resName': line[17:21].strip(),
                'resSeq': int(line[22:26]),
                'x': float(line[30:38]),
                'y': float(line[38:46]),
                'z': float(line[46:54]),
                'occupancy': float(line[54:60]),
                'tempFactor': float(line[60:66]),
                'segment': line[72:76].strip(),
                'element': line[76:78].strip()
            }
            atoms.append(atom_data)

# Calculate translations
layer_atoms = {}
for atom in atoms:
    layer = int(atom['segment'][:2])
    if layer not in layer_atoms:
        layer_atoms[layer] = []
    layer_atoms[layer].append(atom)

# Calculate translation based on the difference between adjacent layers
odd_translation = layer_atoms[3][0]['x'] - layer_atoms[1][0]['x']
even_translation = layer_atoms[4][0]['x'] - layer_atoms[2][0]['x']

# Generate new layers
new_atoms = []
max_layer = max(int(atom['segment'][:2]) for atom in atoms)

for layer in range(max_layer + 1, total_layers + 1):
    base_layer = 1 if layer % 2 == 1 else 2  # Use layer 1 for odd, 2 for even
    translation = odd_translation if layer % 2 == 1 else even_translation
    translation_multiplier = (layer - base_layer) // 2
    
    for atom in atoms:
        if int(atom['segment'][:2]) == base_layer:  
            new_atom = atom.copy()
            new_x = new_atom['x'] + translation * translation_multiplier
            new_atom['x'] = new_x
            
            # Create new segment identifier
            new_segment = f"{layer:02d}{atom['segment'][2:]}"
            new_atom['segment'] = new_segment
            
            # Update the line with new x-coordinate and segment
            new_line = (
                new_atom['line'][:30] +
                f"{new_x:8.3f}" +
                new_atom['line'][38:72] +
                new_segment +
                new_atom['line'][76:]
            )
            new_atom['line'] = new_line
            new_atoms.append(new_atom)

# Combine original and new atoms
expanded_atoms = atoms + new_atoms

# Create a mapping of numbers to letters
number_to_letter = dict(enumerate(string.ascii_uppercase))

def rename_segment(old_segment):
    layer = int(old_segment[:2])
    unit = int(old_segment[2:])
    new_unit = number_to_letter[unit - 1]  # Convert to 0-based index for mapping
    return f"{new_unit}{layer:03d}"

# Fix atom numbers and rename segments
fixed_atoms = []
for i, atom in enumerate(expanded_atoms, start=1):
    old_segment = atom['segment']
    new_segment = rename_segment(old_segment)
    
    fixed_line = (
        f"{atom['line'][:6]}{i:5d}{atom['line'][11:72]}"
        f"{new_segment:>4}{atom['line'][76:]}"
    )
    fixed_atoms.append(fixed_line)

# Write the expanded PDB file
with open(output_file, 'w') as f:
    for atom_line in fixed_atoms:
        f.write(atom_line)

print(f"Expanded structure with {total_layers} layers, new segments written to {output_file}")