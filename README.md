# Link Extractor & Validator
This project consists of two Python scripts that work together to extract links from files, compile them into a CSV file, validate their availability, and compile those results into two CSV files for working links and those that throw an error.

## Features
- Extracts URLs from specified files.
- Compiles extracted URLs into `links.csv`.
- Tests each link to determine if it is accessible.
- Outputs results into `working-links.csv` and `error-links.csv`.

## Prerequisites
- Python 3.x
- Required Python libraries 
    - (install with `pip install -r requirements.txt` if applicable)

## Usage

### Step 1: Extract Links
Run the first script to extract links from files:
```sh
python extract_links.py
```
This will generate `links.csv`, which contains all extracted URLs.

### Step 2: Validate Links
Run the second script to test the extracted links:
```sh
python validate_links.py
```
This will generate:
- `working-links.csv`: Contains all accessible URLs.
- `error-links.csv`: Contains URLs that could not be reached.

## File Structure
```
/project-directory
│── extract_links.py      # Extracts links from files and saves to links.csv
│── validate_links.py     # Validates links from links.csv and categorizes results
│── links.csv            # Extracted links
│── working-links.csv    # Successfully validated links
│── error-links.csv      # Links that failed validation
│── README.md            # Documentation
```

