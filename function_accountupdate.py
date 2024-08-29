import csv

# Define the file paths
file1 = r"C:\gamsync\automate\servicemanagement_*\accountfieldquery.csv"
file2 = r"C:\gamsync\automate\servicemanagement_*\*\accountdatabase.csv"
output_file = r"C:\gamsync\automate\servicemanagement_*\accountfieldupdate.csv"

# Read the first file into a set of rows
with open(file1, newline='') as f1:
    reader1 = csv.reader(f1)
    data1 = {tuple(row) for row in reader1}

# Read the second file and keep track of rows and their indices
with open(file2, newline='') as f2:
    reader2 = list(csv.reader(f2))  # Read all rows into a list for indexing
    data2 = {tuple(row) for row in reader2}

# Find the rows that are in file2 but not in file1
diff_rows = data2 - data1

# Prepare the output data
output_rows = []

# Include the line immediately above each changed line from file2
for i, row in enumerate(reader2):
    if tuple(row) in diff_rows:
        if i > 0:  # Check if there is a previous row
            output_rows.append(reader2[i-1])  # Add the row immediately above
        output_rows.append(row)  # Add the changed row

# Write the differences to the output CSV file
with open(output_file, 'w', newline='') as output:
    writer = csv.writer(output)
    for row in output_rows:
        writer.writerow(row)

print(f"Differences have been written to '{output_file}'")