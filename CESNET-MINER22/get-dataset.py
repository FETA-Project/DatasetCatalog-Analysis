import requests
from zipfile import ZipFile
import tarfile
import shutil
import os
import gzip

def clean_directory(base_dir):
    shutil.rmtree(base_dir)

def get_dataset_csv(base_dir):
    """
    Get sample dataset csv for analysis
    """
    uncompressed_file = os.path.join(base_dir,"DeCryptoDatasets","decrypto_dataset_design.csv")
    shutil.copy(uncompressed_file,".")
    uncompressed_file = os.path.join(base_dir,"DeCryptoDatasets","decrypto_dataset_evaluation.csv")
    shutil.copy(uncompressed_file,".")
    print(f"Uncompressed file saved to: ",os.path.abspath("."))

def download_and_extract_tar_gz(url, extract_to='.'):
    """
    Downloads a .tar.gz file from a URL, saves it to disk, and
    extracts all its contents to the specified directory.

    Args:
        url: The URL of the .tar.gz file.
        extract_to: The directory to extract the files to (defaults to current directory).
    """
    try:
        tar_gz_filename = "downloaded.tar.gz"

        # Download with streaming to handle large files
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(tar_gz_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

        # Extract the contents
        with tarfile.open(tar_gz_filename, 'r:gz') as tar_ref:
            tar_ref.extractall(extract_to)
        print(f"Files extracted to: {extract_to}")

        # Remove the tar.gz file after extraction
        os.remove(tar_gz_filename)
        print(f"Tar.gz file removed: {tar_gz_filename}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading the file: {e}")
    except Exception as e:
        print(f"Error processing the file: {e}")

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

    # Remove the zip file after extraction
    os.remove(zip_filename)
    print(f"Zip file removed: {zip_filename}")

  except requests.exceptions.RequestException as e:
    print(f"Error downloading the file: {e}")
  except Exception as e:
    print(f"Error processing the file: {e}")

# Run action
zenodo_url = "https://zenodo.org/records/7189293/files/DeCryptoDatasets.tar.gz?download=1"
base_directory = 'extracted_data'
download_and_extract_tar_gz(zenodo_url, base_directory)
get_dataset_csv(base_directory)
clean_directory(base_directory)
