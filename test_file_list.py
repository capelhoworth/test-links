# test_file_list.py
with open('wf_files.txt', 'r') as file:
    files = file.readlines()
    print("Number of files:", len(files))
    print("\nFirst few files:")
    for file in files[:5]:  # Show first 5 files
        print(f"'{file.strip()}'")