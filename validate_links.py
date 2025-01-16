import requests
import csv
import os

def validate_links(input_csv, working_csv, error_csv):
    working_results = []
    error_results = []

    # Check if output files exist and delete them if so
    for file in [working_csv, error_csv]:
        if os.path.exists(file):
            print(f"Removing existing file: (file)")
            os.remove(file)
    
    # Open the links.csv and read the links
    with open(input_csv, 'r') as file:
        reader = csv.reader(file)
        header = next(reader) 
        
        for row in reader:
            if row:  # Ensure the row isn't empty
                url = row[1].strip()
                print(f"Testing: {url}")
                try:
                    # Test the link
                    response = requests.head(url, allow_redirects=True, timeout=5)
                    print(response)

                    if response.status_code == 200:
                        working_results.append((url, str(response.status_code), response.url))
                    else:
                        error_results.append((url, str(response.status_code), response.url))

                except requests.exceptions.RequestException as e:
                    error_msg = str(e).replace('"', '').replace("'", "")
                    error_results.append((url, 'Error', error_msg))
                    

    # Write the working results into working-links.csv
    with open(working_csv, 'w', newline='') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(('URL', 'Status Code', 'Final URL/Error Message'))
        writer.writerows(working_results)

    # Write the error results into error-links.csv
    with open(error_csv, 'w', newline='') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(('URL', 'Status Code', 'Final URL/Error Message'))
        for result in error_results:
            writer.writerow((
                result[0],
                result[1],
                result[2]
            ))

# Define input and output file paths
input_csv = 'links.csv'
working_csv = 'working-links.csv'
error_csv = 'error-links.csv'

# Run the function
validate_links(input_csv, working_csv, error_csv)
print(f"Working links have been saved to {working_csv}")
print(f"Error links have been saved to {error_csv}")
