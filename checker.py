def read_fasta_file(file_path):
    sequences = {}
    current_seq_name = None
    current_seq = []

    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('>'):  # Indicates a new sequence entry
                    if current_seq_name:
                        sequences[current_seq_name] = ''.join(current_seq)
                    current_seq_name = line[1:].strip()  # Remove '>' and strip whitespace
                    current_seq = []  # Reset sequence buffer for new entry
                else:
                    current_seq.append(line)  # Append sequence lines

            # Add the last sequence after loop completion
            if current_seq_name:
                sequences[current_seq_name] = ''.join(current_seq)

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")

    return sequences

def check_letter_S_or_T (letter):
    if letter == 'S' or letter == 'T': 
        return True 
    else:
        return False
    
def check_letter_P (letter):
    if letter == 'P':
        return True 
    else:
        return False

def Position_Calculation(sliced_seq):
    aa_points = {
        "A": [-0.9, -0.8, -0.2, -0.1, 0.4, 0.00, 0.00, -1.0, -1.5, -1.1],
        "C": [-0.7, -0.9, -0.3, 0.6, 0.3, 0.00, 0.00, -1.0, -1.6, -0.8],
        "D": [-1.9, -2.0, -2.0, -2.0, -2.0, 0.00, 0.00, -2.0, -2.0, -1.8],
        "E": [-2.0, -1.9, -1.9, -1.9, -2.0, 0.00, 0.00, -2.0, -2.0, -1.2],
        "F": [-0.7, -0.9, -0.5, -1.1, -0.2, 0.00, 0.00, -1.0, -1.7, -0.7],
        "G": [-1.1, -0.9, 1.3, -0.7, 0.8, 0.00, 0.00, -0.1, -1.3, -0.2],
        "H": [-0.7, -1.0, -0.3, -1.0, -0.1, 0.00, 0.00, 0.4, 2.0, 1.4],
        "I": [-1.4, -1.5, -0.7, -1.0, -1.9, 0.00, 0.00, -1.5, -1.8, -1.4],
        "K": [-1.0, -1.0, -0.7, -1.1, 1.3, 0.00, 0.00, -0.3, -1.4, -2.0],
        "L": [-1.5, -1.4, -0.8, -1.0, -0.2, 0.00, 0.00, -1.4, -1.9, -1.8],
        "M": [-1.4, -1.3, -0.6, -0.1, 1.9, 0.00, 0.00, -1.4, -1.9, -1.3],
        "N": [-1.4, -1.4, -0.8, -1.2, -0.6, 0.00, 0.00, -0.5, -1.4, -0.9],
        "P": [-1.1, -1.1, -0.2, -0.4, 0.2, 0.00, 2.0, -1.6, -0.5, -0.9],
        "Q": [-1.4, -1.6, -0.9, -1.2, 0.1, 0.00, 0.00, -1.0, -1.1, -1.1],
        "R": [-0.7, -0.9, 1.0, -0.6, 2.0, 0.00, 0.00, 2.0, 1.2, -0.9],
        "S": [2.0, 2.0, 2.0, 2.0, 1.1, 2.00, 0.00, 1.4, -0.5, -1.9],
        "T": [0.6, 0.4, 0.4, 0.3, -0.4, 1.00, 0.00, 0.2, -1.3, -1.6],
        "V": [-1.3, -1.5, -0.7, -1.2, -1.4, 0.00, 0.00, -1.4, -1.8, -1.6],
        "W": [-0.3, -0.6, -0.6, -0.4, -0.6, 0.00, 0.00, -1.0, -0.6, 2.0],
        "Y": [-0.5, -0.8, -0.4, -0.7, -0.2, 0.00, 0.00, -0.9, -0.6, 0.1]
    }
    result = []
    for index, char in enumerate(sliced_seq):
        if char in aa_points and index < len(aa_points[char]):
            result.append(aa_points[char][index])
        else:
            # Handle the case where the index is out of range
            result.append(None)  # or any other placeholder
    
    # Calculate the sum of the result list, ignoring None values
    total_sum = sum(x for x in result if x is not None)
    
    return total_sum

def check_sequence_pattern(seq_data):

    out_index = 4

    while out_index < len(seq_data):
        char = seq_data[out_index]
        first_letter_match = check_letter_S_or_T(char)
        
        if first_letter_match:
            try:
                char2 = seq_data[out_index+1]
                second_letter_match = check_letter_P(char2)
            
                if second_letter_match:
                    print("passed both checks")
                    sliced_seq = list(seq_data[out_index-5:out_index+5])
                    print(sliced_seq)
                    total_points = Position_Calculation(sliced_seq)
                    if total_points >= 4:
                        print(total_points)
                        return True, total_points, sliced_seq 
            except:
                break
        
        out_index += 1

    return False, None, None


def find_matching_sequences(sequences):
    matching_sequences = {}

    for seq_name, seq_data in sequences.items():
        matched, score, sliced_seq = check_sequence_pattern(seq_data)
        if matched:
            matching_sequences[seq_name] = {
                'score': score,
                'sliced_seq': sliced_seq
            }

    return matching_sequences


def save_to_txt(matching_sequences, output_file):
    with open(output_file, 'w') as file:
        if matching_sequences:
            file.write("Matching Sequences:\n")
            for seq_name, seq_info in matching_sequences.items():
                file.write(f"{seq_name}; {seq_info['sliced_seq']}; {seq_info['score']}\n")
        else:
            file.write("No sequences match the pattern.\n")


# Example usage:
file_path = './protein.faa'
sequences = read_fasta_file(file_path)

# Test sequences
sequences2 = {
    "high_sequence": "SSSSSSPSSS",
    "wrong_sequence":"SSSSSSXSSS",
    "lower_4": "EEEEESPEEE",
    "4_9_score": "SSDDRSPAHH",
    "4_9_score_long": "XXXXXXXXSSDDRTPAHHXXXXXXXX",
}

matching_sequences = find_matching_sequences(sequences)

# Specify the output file path
output_file = 'matching_sequences.txt'

# Save matching sequences to the output file
save_to_txt(matching_sequences, output_file)

print("Done")
