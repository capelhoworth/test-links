import requests
import csv

def test_links(input_csv, output_csv):
    results = []
    
    # Open the CSV file and read the links
    with open(input_csv, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header row, if present
        
        for row in reader:
            if row:  # Ensure the row isn't empty
                url = row[1].strip()
                print(row[1])
                try:
                    # Test the link
                    response = requests.head(url, allow_redirects=True, timeout=5)
                    print(response)
                    results.append((url, response.status_code, response.url))
                except requests.exceptions.RequestException as e:
                    results.append((url, 'Error', str(e)))

    # Write the results to a new CSV file
    with open(output_csv, 'w', newline='') as out_file:
        writer = csv.writer(out_file)
        # writer.writerow(['Original URL', 'Status Code', 'Final URL/Message'])  # Add header row
        writer.writerows(results)

# Define the input and output file paths
input_csv = 'links.csv'  # Your input CSV file
output_csv = 'output.csv'  # File to save the results

# Run the function
test_links(input_csv, output_csv)

print(f"Results have been saved to {output_csv}")
