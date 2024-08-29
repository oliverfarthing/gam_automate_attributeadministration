import csv

def remove_repeated_headers(input_file, output_file):
    header = "group,type,role,id,status,email"
    header_found = False

    with open(input_file, mode='r') as infile, open(output_file, mode='w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            # Check if the current row is the header
            if ",".join(row) == header:
                if not header_found:
                    # Write the header only once
                    writer.writerow(row)
                    header_found = True
                # Skip the repeated header rows
                continue
            
            # Write the non-header rows
            writer.writerow(row)

# Example usage with raw string paths
input_file = r"C:\gamsync\automate\servicemanagement_*\accountquery.csv"
output_file = r"C:\gamsync\automate\servicemanagement_*\accountcleanedquery.csv"
remove_repeated_headers(input_file, output_file)
exit()
