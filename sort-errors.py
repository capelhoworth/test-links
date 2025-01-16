import csv
import os
import shutil
from collections import defaultdict

def sort_error_links(input_file='error-links.csv'):
    
    # Create or clean output directory
    output_dir = 'sorted_errors'
    if os.path.exists(output_dir):
        print(f"Cleaning up existing output directory: {output_dir}")
        shutil.rmtree(output_dir)

    os.makedirs(output_dir)
    print(f"Created output directory: {output_dir}")
    
    # Dictionary to store rows by status code
    error_groups = defaultdict(list)
    
    # Read the input CSV file
    with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Group rows by status code
        for row in reader:
            status_code = row['Status Code'].strip()
            
            # Handle different types of status codes. Numeric and non-numeric.
            if status_code.isdigit():
                output_file = f'{status_code}.csv'
            else:
                output_file = 'error.csv'
            
            error_groups[output_file].append(row)
    
    # Write grouped rows to separate CSV files
    fieldnames = ['URL', 'Status Code', 'Final URL/Error Message']
    
    for output_file, rows in error_groups.items():
        output_path = os.path.join(output_dir, output_file)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        print(f'Created {output_path} with {len(rows)} entries')

# Directly call the function when the script runs
sort_error_links()