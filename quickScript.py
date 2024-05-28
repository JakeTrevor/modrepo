import os
import zipfile
import re
import csv

def create_zip_with_mods_folder_and_extract_info(jar_directory, csv_filename, output_directory):
    # Ensure the provided directory exists
    if not os.path.isdir(jar_directory):
        print(f"The directory {jar_directory} does not exist.")
        return

    # Prepare the CSV file
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['mod_slug', 'version', 'zip_filename']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Loop through each file in the provided directory
        for filename in os.listdir(jar_directory):
            if filename.endswith('.jar'):
                fixed_filename = filename.replace("_", "-").lower()
                # Extract mod slug and version
                mod_slug, version = extract_mod_info(fixed_filename)

                # Define the full path to the jar file
                jar_file_path = os.path.join(jar_directory, filename)

                # Define the name of the zip file
                zip_file_name = fixed_filename.replace('.jar', '.zip')
                mod_folder = os.path.join(output_directory, mod_slug)
                os.mkdir(mod_folder)
                zip_file_path = os.path.join(mod_folder, zip_file_name)

    

                # Create the zip file and add the jar file into a /mods/ folder
                with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    # Add the jar file to the /mods/ folder inside the zip
                    zipf.write(jar_file_path, os.path.join('mods', filename))

                # Write the extracted information to the CSV file
                writer.writerow({'mod_slug': mod_slug, 'version': version, 'zip_filename': zip_file_name})

                print(f"Created {zip_file_path} containing {jar_file_path} in /mods/ folder")
                print(f"Extracted mod_slug: {mod_slug}, version: {version}, zip_filename: {zip_file_name}")

def extract_mod_info(filename):
    # Remove the .jar extension
    base_name = filename[:-4]
    # Use regex to split the string into mod slug and version
    match = re.match(r'([a-zA-Z-]+)-(\d.*)', base_name)
    if match:
        mod_slug = match.group(1)
        version = match.group(2)
        return mod_slug, version
    else:
        return base_name, ""

# Specify the directory containing the jar files
jar_directory = os.path.abspath('C:/Users/Jake/Downloads/newmods')
# Specify the output directory
output_directory = os.path.abspath('C:/Users/Jake/Desktop/modpack/mods')
csv_filename = 'C:/Users/Jake/Desktop/modpack/mods_info.csv'


# Call the function to create the zip files and extract mod info
create_zip_with_mods_folder_and_extract_info(jar_directory, csv_filename, output_directory)
