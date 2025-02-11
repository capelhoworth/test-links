import csv
import os
import shutil
from collections import defaultdict

def sort_links(input_file='tested_links.csv'):
    
    # Create or clean output directory
    output_dir = 'sorted_links_by_status'
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    print(f"Created output directory: {output_dir}")
    
    # Dictionary to store rows by status code
    status_groups = defaultdict(list)
    
    # Read the input CSV file
    with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        
        # Group rows by status code
        for row in reader:
            link, status_code = row
            
            # Ensure status code is a string
            status_code = str(status_code).strip()
           
            # Group links by status code
            status_groups[status_code].append(link)
    
   # Write grouped links to separate text files
    for status_code, links in status_groups.items():
        output_path = os.path.join(output_dir, f'status_{status_code}_links.txt')
    
        
        with open(output_path, 'w', encoding='utf-8') as linkfile:
            for link in links:
                linkfile.write(f"{link}\n")
       
        print(f'Created {output_path} with {len(links)} links')

# Directly call the function when the script runs
if __name__ == '__main__':
    sort_links()