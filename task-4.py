import concurrent.futures
import argparse
import os


def search_keyword_in_file(file_path, keyword):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, 1):
                if keyword in line:
                    print(f"Word '{keyword}' found in the file '{file_path}', line {line_number}:")
                    print(line)
    except Exception as e:
        print(f"Error processing the file '{file_path}': {e}")

def main(args):
    keyword = args.keyword
    file_paths = args.files

    if not file_paths:
        print("The list of files to search for is not specified.")
        return

    if not all(os.path.isfile(file_path) for file_path in file_paths):
        print("One or more files from the list do not exist.")
        return

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(search_keyword_in_file, file_path, keyword) for file_path in file_paths]

        for future in concurrent.futures.as_completed(futures):
            future.result()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Keyword search in text files with parallel processing.")
    parser.add_argument("keyword", type=str, help="Search keyword")
    parser.add_argument("files", type=str, nargs='+', help="List of files to search for")
    args = parser.parse_args()
    main(args)