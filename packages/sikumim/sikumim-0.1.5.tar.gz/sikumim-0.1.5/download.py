import argparse
import os
import requests


def download_files(course, output_path):
    # Locate the course directory (case-insensitive)
    api_url = "https://api.github.com/repos/Regev32/Sikumim/contents/courses"
    response = requests.get(api_url)
    if response.status_code != 200:
        raise Exception(f"Failed to list contents from the repository. Status code: {response.status_code}")

    items = response.json()
    items = [item for item in items if item["type"]=="dir"]
    try:
        course_index = [items["name"].lower() for items in items].index(course.lower())
    except ValueError:
        print(f"Failed to find course name {course}")
        return

    # Parse the list of items in the course directory
    api_url = items[course_index]["url"]
    response = requests.get(api_url)
    if response.status_code != 200:
        raise Exception(f"Failed to list contents from {api_url}. Status code: {response.status_code}")
    items = response.json()

    # Create the output path directories (if they do not exist already)
    os.makedirs(output_path, exist_ok=True)

    # Download files
    for item in items:
        if item["type"] == "file":
            download_url = item["download_url"]
            local_path = os.path.join(output_path, item["name"])
            r = requests.get(download_url, stream=True)
            if r.status_code == 200:
                with open(local_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            else:
                print(f"Failed to download {download_url}")
    print("Done!")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("course", help="Desired course content")
    parser.add_argument("path", help="Output path for parsed content")
    args = parser.parse_args()
    download_files(args.course, args.path)


if __name__ == "__main__":
    main()