import re
import csv

def extract_links(input_file, output_csv):
    urls = []

    # Read the file content
    with open(input_file, 'r') as file:
        content = file.read()

    # Use regex to find all href links
    matches = re.findall(r'href="(https?://[^"]+)"', content)
    urls.extend(matches)

    # Write the URLs to a CSV file
    with open(output_csv, 'w', newline='') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(['URL'])  # Add header
        for url in urls:
            writer.writerow([url])

    print(f"Extracted {len(urls)} URLs and saved them to {output_csv}")

# Specify the input and output files
input_file = 'code_file.txt'  # Replace with your input file name
output_csv = 'links.csv'      # Output CSV file for the URLs

# Run the extraction function
extract_links(input_file, output_csv)
