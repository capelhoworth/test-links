import requests
import links.csv

def test_links(file_path, output_path):
    results = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            url = row[0].strip()  # Assumes one URL per row
            try:
                response = requests.head(url, allow_redirects=True, timeout=5)
                results.append((url, response.status_code, response.url))
            except requests.exceptions.RequestException as e:
                results.append((url, 'Error', str(e)))

    with open(output_path, 'w', newline='') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(['Original URL', 'Status Code', 'Final URL/Message'])
        writer.writerows(results)

# Example Usage
input_file = 'links.csv'  # Replace with your file path
output_file = 'test_results.csv'
test_links(input_file, output_file)
