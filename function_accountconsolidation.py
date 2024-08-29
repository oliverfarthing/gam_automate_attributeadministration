import os

# Function to read the input text file
def read_input_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

# Function to organize the data by headers
def organize_data(lines):
    data_by_header = {}
    current_header = None

    for line in lines:
        if line.startswith('primaryEmail') or line.startswith('customSchemas'):
            current_header = line.strip()  # Set the header as the current line
            if current_header not in data_by_header:
                data_by_header[current_header] = []
        else:
            if current_header:
                data_by_header[current_header].append(line.strip())

    return data_by_header

# Function to save data to multiple files based on headers
def save_data_to_files(data_by_header, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for header, data_lines in data_by_header.items():
        # Replace special characters in the header to create a valid filename
        filename = header.replace(",", "_").replace(".", "_") + ".csv"
        file_path = os.path.join(output_dir, filename)

        # Write the data lines to the corresponding file
        with open(file_path, 'w') as file:
            file.write(header + '\n')  # Write the header as the first line
            file.write('\n'.join(data_lines))  # Write the data lines

# Main script execution
input_file_path = r"C:\gamsync\automate\servicemanagement_*\accountfieldupdate.csv"  # Path to your input text file
output_directory = r"C:\gamsync\automate\servicemanagement_*"  # Directory to store the output files

# Read and organize the data
lines = read_input_file(input_file_path)
data_by_header = organize_data(lines)

# Save the organized data to multiple files
save_data_to_files(data_by_header, output_directory)

print(f"Data has been split and saved into the '{output_directory}' directory.")
