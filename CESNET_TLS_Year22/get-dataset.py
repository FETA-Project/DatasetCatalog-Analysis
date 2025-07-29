import requests
from zipfile import ZipFile
import shutil
import os
import gzip

def clean_directory(base_dir):
    shutil.rmtree(base_dir)

def uncompress_to_csv(base_dir):
  """
  Uncompresses the .csv.gz file directly to a .csv file on disk
  without loading the entire file into memory.

  Args:
    base_dir: The base directory where the compressed file is located.
  """
  try:
    compressed_file = os.path.join(base_dir, "CESNET-TLS-Year22", "WEEK-2022-00", "2022-01-01", "flows-20220101.csv.xz")
    uncompressed_file = os.path.join("flows-20220101.csv")

    # Check if the compressed file exists
    if not os.path.exists(compressed_file):
      print(f"File not found: {compressed_file}")
      return

    # Uncompress with gzip module and shutil for efficient file copying
    with gzip.open(compressed_file, 'rb') as f_in:
      with open(uncompressed_file, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

    print(f"Uncompressed file saved to: {uncompressed_file}")

  except Exception as e:
    print(f"Error uncompressing file: {e}")



def download_and_unzip(url, extract_to='.'):
  """
  Downloads a large zip file from a URL, saves it to disk, and 
  extracts all its contents to the specified directory.

  Args:
    url: The URL of the zip file.
    extract_to: The directory to extract the files to (defaults to current directory).
  """
  try:
    zip_filename = "downloaded.zip"  # Choose a filename

    # Download with streaming to handle large files
    with requests.get(url, stream=True) as response:
      response.raise_for_status()
      with open(zip_filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192): 
          f.write(chunk)

    # Extract the contents
    with ZipFile(zip_filename, 'r') as zip_ref:
      zip_ref.extractall(extract_to)
    print(f"Files extracted to: {extract_to}")

    # Optional: Remove the zip file after extraction
    os.remove(zip_filename)
    print(f"Zip file removed: {zip_filename}")

  except requests.exceptions.RequestException as e:
    print(f"Error downloading the file: {e}")
  except Exception as e:
    print(f"Error processing the file: {e}")

# Run action
zenodo_url = "https://zenodo.org/records/10608607/files/CESNET-TLS-Year22.zip?download=1"
download_and_unzip(zenodo_url, 'extracted_data')
base_directory = 'extracted_data'
uncompress_to_csv(base_directory)
clean_directory(base_directory)
