import multiprocessing
import argparse
import requests


def download_image(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        file_name = url.split("/")[-1]
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"The image at {url} is uploaded as {file_name}")
    else:
        print(f"Failed to upload image at {url}")

def main(args):
    urls = args.urls

    processes = []
    for url in urls:
        process = multiprocessing.Process(target=download_image, args=(url,))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Loading images from the URL list with parallel processing.")
    parser.add_argument("urls", nargs='+', help="List of URLs for uploading images")
    args = parser.parse_args()
    main(args)
