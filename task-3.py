import multiprocessing
import argparse
import os

def search_keyword_in_file(file_path, keyword):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, 1):
                if keyword in line:
                    print(f"The word '{keyword}' was found in the file '{file_path}', line {line_number}:")
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

    processes = []
    for file_path in file_paths:
        process = multiprocessing.Process(target=search_keyword_in_file, args=(file_path, keyword))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Keyword search in text files with parallel processing.")
    parser.add_argument("keyword", type=str, help="Search keyword")
    parser.add_argument("files", type=str, nargs='+', help="List of files to search for")
    args = parser.parse_args()
    main(args)
