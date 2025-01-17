import re
import csv
import os

def extract_links(input_files, output_csv):
    urls = []

    # Check if output file exists and delete it
    for file in [output_csv]:
        if os.path.exists(file):
            print(f"Removing existing {file}")
            os.remove(file)
   
    # First time writing to CSV - create with header
    with open(output_csv, 'w', newline='') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(['URL'])
   
    # Process each input file
    for input_file in input_files:
        # Skip certain files
        if input_file.strip().lower().endswith(('.css', '.js',
                                                '.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico', '.webp',
                                                '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
                                                '.mp3', '.wav', '.mp4', '.avi', '.mov', '.webm',
                                                '.ttf', '.woff', '.woff2', '.eot',
                                                '.xml', '.json')):
            print(f"Skipping file: {input_file} (undesired file type)")
            continue

        try:
            # Read the file content
            with open(input_file.strip(), 'r', encoding='utf-8') as file:
                content = file.read()
                print(f"Reading file: {input_file}")
               
            # Use regex to find all links
            url_pattern = r'(?:http|https)://[^\s<>"\'\{\}\[\]`]+(?:\.[^\s<>"\'\{\}\[\]`]+)*'
            matches = re.findall(url_pattern, content)
            print(f"Number of matches found in {input_file}: {len(matches)}") 

            # Skip URLs that are undesired files
            filtered_matches = [url for url in matches if not url.lower().endswith(('.css', '.js',
                                                                                    '.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico', '.webp',
                                                                                    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
                                                                                    '.mp3', '.wav', '.mp4', '.avi', '.mov', '.webm',
                                                                                    '.ttf', '.woff', '.woff2', '.eot',
                                                                                    '.xml', '.json'))]

            #Append URLs to CSV
            if filtered_matches:
                with open(output_csv, 'a', newline='') as out_file:
                    writer = csv.writer(out_file)
                    for url in filtered_matches:
                        writer.writerow([input_file.strip(), url])
                        urls.append(url)

            print(f"Extracted {len(filtered_matches)} URLs from {input_file}")
            print("-" * 50)
           
        except Exception as e:
            print(f"Error processing {input_file}: {str(e)}")

    print(f"Total URLs extracted: {len(urls)}")
    print(f"Results saved to {output_csv}")
    print(out_file)

# Create file list from current directory if wf_files.txt doesn't exist
if not os.path.exists('wf_files.txt'):
    print("Creating wf_files.txt with files from current directory...")
    with open('wf_files.txt', 'w') as file_list:
        for filename in os.listdir('.'):
            if filename.endswith(('.html', '.cfm', '.htm')):
                file_list.write(filename + '\n')

# Read the list of files
with open('wf_files.txt', 'r') as file_list:
    input_files = file_list.readlines()
    print(f"Number of files to process: {len(input_files)}")

output_csv = 'links.csv'
extract_links(input_files, output_csv)