import requests
from datetime import datetime, timedelta
import zipfile
import os
# jap_5ThOJ14yf7z1EPEUpAoZYMWoETZcmJk305719

def get_met():


    url = 'https://jatos.psychology.uiowa.edu/jatos/api/v1/results/metadata'
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer jap_5ThOJ14yf7z1EPEUpAoZYMWoETZcmJk305719',
        'Content-Type': 'application/json',
    }
    data = {
        'studyIds': 958,
        'studyIds': 973,
        'studyIds': 996,
        'studyIds': 911,
        'studyIds': 928,
        'studyIds': 945
    }

    response = requests.post(url, headers=headers, json=data)

    # If you want to print the response
    print(response.status_code)
    print(response.json())
    response_json = response.json()

    response = response_json

    # Get the current timestamp
    current_time = datetime.now().timestamp() * 1000  # Convert to milliseconds
    one_day_ago = current_time - (24 * 60 * 60 * 1000)  # 24 hours ago in milliseconds

    # Initialize an empty list to store study result IDs
    study_result_ids = []

    # Iterate through the data to check conditions and collect study result IDs
    for study in response['data']:
        for study_result in study['studyResults']:
            if study_result['studyState'] == 'FINISHED' and study_result['endDate'] >= one_day_ago:
                study_result_ids.append(study_result['id'])
                break  # No need to check other component results for this study result

    # Print the list of study result IDs
    print(study_result_ids)

    if len(study_result_ids) == 0:
        print("No study results found.")
        exit()
    
    return study_result_ids

def get_data(study_result_ids):
    headers = {
        'accept': 'application/octet-stream',
        'Authorization': 'Bearer jap_5ThOJ14yf7z1EPEUpAoZYMWoETZcmJk305719',
        'Content-Type': 'application/json',
    }
    # Get the data for each study result
    datas = {
        'studyIds': 958,
        'studyIds': 973,
        'studyIds': 996,
        'studyIds': 911,
        'studyIds': 928,
        'studyIds': 945,
        'studyResultIds': study_result_ids
    }

    url = 'https://jatos.psychology.uiowa.edu/jatos/api/v1/results/data'
    response = requests.post(url, headers=headers, json=datas)
    # Debugging information
    print(f"Status Code: {response.status_code}")


    # Save the unzip file and save .txt file to the current directory
    if response.status_code == 200:
        jrzip_file = 'response.jrzip'
        with open(jrzip_file, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded file: {jrzip_file}")

        # Verify if the file is a valid zip file
        if zipfile.is_zipfile(jrzip_file):
            print("The file is a valid zip file.")

            # Create a new zip file with only the desired files
            filtered_jrzip_file = 'filtered_response.jrzip'
            with zipfile.ZipFile(jrzip_file, 'r') as zip_ref:
                with zipfile.ZipFile(filtered_jrzip_file, 'w') as filtered_zip_ref:
                    for zip_info in zip_ref.infolist():
                        # Check if the filename contains any of the study_result_ids
                        if any(str(study_result_id) in zip_info.filename for study_result_id in study_result_ids):
                            filtered_zip_ref.writestr(zip_info, zip_ref.read(zip_info.filename))
            print(f"Filtered zip file created: {filtered_jrzip_file}")

            # Extract the filtered zip file
            with zipfile.ZipFile(filtered_jrzip_file, 'r') as zip_ref:
                zip_ref.extractall('.')
            print(f"Unzipped file: {filtered_jrzip_file}")

            # Optionally, remove the original and filtered zip files after extraction
            os.remove(jrzip_file)
            os.remove(filtered_jrzip_file)

            # Walk through the directory and find all .txt files, save paths to a list
            txt_files = []
            for root, dirs, files in os.walk("."):
                for file in files:
                    if file.endswith(".txt"):
                        txt_files.append(os.path.join(root, file))
            print(f"Found {len(txt_files)} .txt files.")
        else:
            print("The file is not a valid zip file.")
    else:
        print("Failed to retrieve or save the file.")
        print(f"Response Text: {response.text}")

def push_data():
    os.system("cd .. \
              git origin Main \
              git add -A \
              git commit -m 'Update data' \
              git push")



def main():
    study_result_ids = get_met()
    get_data(study_result_ids)
    push_data()

if __name__ == "__main__":
    main()
    