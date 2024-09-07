def transform_coordinates(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if line.startswith('ATOM'):
                # Extract the coordinates
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                
                # Transform coordinates: x -> 0, y -> y, z -> x
                new_x = 0.0
                new_y = y
                new_z = x
                
                # Create the new line with transformed coordinates
                new_line = (f"{line[:30]}{new_x:8.3f}{new_y:8.3f}{new_z:8.3f}"
                            f"{line[54:]}")
                outfile.write(new_line)
            else:
                outfile.write(line)

# Usage
input_file = 'Inputs/graphene.pdb'
output_file = 'Outputs/graphene_yz.pdb'
transform_coordinates(input_file, output_file)