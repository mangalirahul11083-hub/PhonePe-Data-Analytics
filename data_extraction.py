import os
import urllib.request
import zipfile

# The direct download link for the repository zip file
zip_url = "https://github.com/PhonePe/pulse/archive/refs/heads/master.zip"
zip_path = "pulse.zip"
final_dir = "data/pulse"

# Ensure the data folder exists
os.makedirs("data", exist_ok=True)

if not os.path.exists(final_dir):
    print("Downloading the PhonePe Pulse data... This might take a minute.")
    # Download the zip file
    urllib.request.urlretrieve(zip_url, zip_path)
    
    print("Download complete! Extracting files...")
    # Extract the zip file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall("data")
    
    # GitHub names the extracted folder 'pulse-master', so we rename it to 'pulse'
    extracted_folder = "data/pulse-master"
    if os.path.exists(extracted_folder):
        os.rename(extracted_folder, final_dir)
        
    # Clean up the zip file
    os.remove(zip_path)
    print("Extraction successful! Data is ready.")
else:
    print("Repository already exists locally. Ready to process the data!")