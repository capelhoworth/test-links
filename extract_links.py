# TODO: get URLs sending to links.csv
# TODO: line 25 code working - skip .css, .js, and .png files (optional for optimization)

import re
import csv

def extract_links(input_files, output_csv):
    urls = []
   
    # First time writing to CSV - create with header
    with open(output_csv, 'w', newline='') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(['URL'])
   
    # Process each input file
    for input_file in input_files:
        try:
            # Read the file content
            with open(input_file.strip(), 'r') as file:
                content = file.read()
                print(f"Reading file: {input_file}")
                print(f"First 200 characters of content: {content[:200]}")  # Debug line

            # # Skip .css, .js, and .png files
            # if not input_file.endswith(('.html', '.cfm', '.htm')):
            #     print(f"Skipping file: {input_file} (not an HTML or CFM file)")
            #     continue

            # ^^^not working because skipping .cfm files. rewrite.^^^

               
            # Use regex to find all href links
            matches = re.findall(r'(https?://[^"]+)"', content)
            print(f"Number of matches found: {len(matches)}")  # Debug line
            if len(matches) == 0:
                # Print href examples
                print("Looking for any href patterns in the content:")
                href_examples = re.findall(r'href="[^"]+"', content)
                print(f"Sample hrefs found (up to 3): {href_examples[:3]}")  # Debug line
            
            urls.extend(matches)
           
            # Append the URLs to the CSV file
            with open(output_csv, 'a', newline='') as out_file:
                writer = csv.writer(out_file)
                for url in matches:
                    writer.writerow([url])
                   
            print(f"Extracted {len(matches)} URLs from {input_file}")
            print("-" * 50)  # Separator line
           
        except Exception as e:
            print(f"Error processing {input_file}: {str(e)}")
   
    print(f"Total URLs extracted: {len(urls)}")

# Read the list of files
with open('wf_files.txt', 'r') as file_list:
    input_files = file_list.readlines()
    print(f"Number of files to process: {len(input_files)}")  # Debug line

output_csv = 'links.csv'
extract_links(input_files, output_csv)