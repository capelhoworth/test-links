import os
import re
import requests
import csv
import time
from collections import defaultdict
import shutil

# Define a list of file extensions that should be ignored
ignored_extensions = [
    '.css', '.js', '.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico', '.webp', '.pdf',
    '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.mp3', '.wav', '.mp4', '.avi',
    '.mov', '.webm', '.ttf', '.woff', '.woff2', '.eot', '.xml', '.json', '.zip', '.scc'
]

# Function to clean up the error.csv fiel if it exists
def cleanup_error_file():
    for file_name in ['error.csv', 'tested_links.csv', 'changed_links.csv', 'failed_changed_links.csv']:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"Cleaned up previous {file_name}.")


# Function to check and update HTTP to HTTPS links in a file
def update_http_links_in_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()

        # Regex to find HTTP links
        # http_links = re.findall(r'http://[^\s]+', file_content)
        http_links = re.findall(r'(?:http)://[^\s<>"\'\{\}\[\]`]+(?:\.[^\s<>"\'\{\}\[\]`]+)*', file_content)

        # Skip if no HTTP links are found
        if not http_links:
            return True

        links_updated = False
        
        for link in http_links:
            try:

                # Test the HTTP link
                response_http = requests.get(link)
                http_status = response_http.status_code

                # Record the HTTP link and response in the tested_links.csv
                record_tested_link(link, http_status)

                # Convert HTTP to HTTPS and test again
                https_link = link.replace("http://", "https://")
                response_https = requests.get(https_link)
                https_status = response_https.status_code

                # If the status codes are the same and it's still HTTP, update to HTTPS
                if http_status == https_status:
                    file_content = file_content.replace(link, https_link)
                    # Record the HTTPS link and response in the changed_links.csv
                    record_changed_link(link, http_status, https_link, https_status)
                    links_updated = True
                else:
                    # Record the HTTPS link and response in the failed_changed_links.csv
                    record_failed_changed_link(link, http_status, https_link, https_status)

            except requests.RequestException as e:
                # Track errors related to link testing (both HTTP and HTTPS failures)
                track_error(file_path, link, None, f"Error testing link {link}: {str(e)}")

        # Save changes to the file if links were updated
        if links_updated:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file_content)

        return True

    except Exception as e:
        track_error(file_path, None, None, f"Error processing file {file_path}: {str(e)}")
        return False


# Function to track errors in error.csv
def track_error(file_path, link, status, error_message):
    with open('error.csv', mode='a', newline='', encoding='utf-8') as error_file:
        error_writer = csv.writer(error_file)

        # Record the error 
        error_writer.writerow([file_path, link, status, error_message])


# Function to record a tested link and its response in tested_links.csv
def record_tested_link(link, status):
    with open('tested_links.csv', mode='a', newline='', encoding='utf-8') as tested_file:
        tested_writer = csv.writer(tested_file)
        tested_writer.writerow([link, status])


# Function to record a changed link and its response in changed_links.csv
def record_changed_link(link, status, new_link, new_status):
    with open('changed_links.csv', mode='a', newline='', encoding='utf-8') as changed_file:
        changed_writer = csv.writer(changed_file)
        changed_writer.writerow([link, status, new_status, new_link])


# Function to record changed links and their responses in changed_links.csv
def record_failed_changed_link(link, status, new_link, new_status):
    with open('failed_changed_links.csv', mode='a', newline='', encoding='utf-8') as failed_changed_file:
        changed_writer = csv.writer(failed_changed_file)
        changed_writer.writerow([link, status, new_status, new_link])


# Function to walk through directory and get file paths
def get_files_in_directory(folder_path):
    file_paths = []
    file_names = []
    try:
        for root, _, files in os.walk(folder_path):
            #skip git files
            if ".git" in root:
                continue

            for file in files:
                file_path = os.path.join(root, file)
                file_extension = os.path.splitext(file)[1].lower()

                # Only add the file if it doesn't have an ignored extension
                if file_extension not in ignored_extensions:
                    file_paths.append(file_path)
                    file_names.append(file)

        return file_names, file_paths
    except Exception as e:
        track_error(folder_path, None, None, f"Error walking through directory: {str(e)}")
        return [], []


# Main function
def main():
    # Record start time, failure count, and total count
    start_time = time.time()
    total_count = 0
    fail_count = 0

    # Clean up prior run data before starting
    cleanup_error_file()

    folder_path = input("Enter the folder path to scan: ")

    # Get files in the specified folder
    file_names, file_paths = get_files_in_directory(folder_path)

    # Loop through each file and process it
    for i, file_path in enumerate(file_paths):
        print(f"Processing file {file_names[i]}...")
        total_count += 1

        # Try to update links in the file
        if not update_http_links_in_file(file_path):
            print(f"Failed to process {file_names[i]}")
            fail_count += 1
        # else:
        #     print(f"Successfully processed {file_names[i]}")

    # Calculate execution time
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Processing complete. Execution time: {execution_time} seconds.")
    print(f"Total files processed: {total_count}")
    print(f"Files failed to process: {fail_count}")

if __name__ == '__main__':
    main()