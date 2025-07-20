import os,shutil


def save_server_code(directory_name, json_data):

    print("Saving server code...")
    # Ensure the directory path is within the current working directory
    directory_path = os.path.join(os.getcwd(), directory_name)

    # If the directory exists, remove it and all its contents
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)

    # Create a fresh directory
    os.makedirs(directory_path)

    # Iterate through the dictionary and write files
    for relative_path, content in json_data.items():
        file_path = os.path.join(directory_path, relative_path)

        # Create any necessary subdirectories
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Write the content to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

    print(f"Files created successfully in {directory_path}.")