import os
import requests
import shutil
from io import BytesIO
import subprocess

class PDFDownloader:
    def __init__(self, url):
        self.url = url
    
    def download_pdf(self,compress=True):
        # Ensures the cache directory exists
        os.makedirs('pdf_cache', exist_ok=True)

        # Get the filename from the URL
        filename = self.url.split('/')[-1]
        if not filename.lower().endswith('.pdf'):
            filename += '.pdf'
        filepath = os.path.join('pdf_cache', filename)

        response = requests.get(self.url, stream=True)
        if response.status_code == 200:
            with open(filepath, 'wb') as pdf_file:
                for chunk in response.iter_content(chunk_size=1024 * 1024):  # Read in 1MB chunks
                    pdf_file.write(chunk)
            if compress:
                file_size_mb = os.path.getsize(filepath) / (1024 * 1024)
                if file_size_mb > 25:
                    self.compress_pdf(filepath)

            return filepath
        else:
            raise Exception(f"Error downloading file, status code {response.status_code}")

    
    def compress_pdf(self, input_path, quality_level=2):
        # Base case: if quality level is at its lowest, give up compression
        if quality_level < 0:
            print("Unable to compress the file further.")
            return
    
        temp_output = 'temp_compressed.pdf'
        
        gs_command = [
            'gs',
            '-sDEVICE=pdfwrite',
            '-dCompatibilityLevel=1.4',
            '-dPDFSETTINGS={}'.format({
                0: '/default',
                1: '/prepress',
                2: '/printer',
                3: '/ebook',
                4: '/screen'
            }.get(quality_level, '/default')),
            '-dNOPAUSE',
            '-dBATCH',
            '-dQUIET',
            '-sOutputFile={}'.format(temp_output),
            input_path
        ]
    
        try:
            subprocess.run(gs_command, check=True)
    
            compressed_size = os.path.getsize(temp_output)
            if compressed_size < 25000000:
                os.replace(temp_output, input_path)
                print(f"File compressed successfully at quality level {quality_level}.")
            else:
                # If file size is still not acceptable, delete temporary file and call recursively with lower quality
                os.remove(temp_output)
                print(f"Compressed file size is still too large at quality level {quality_level}. Trying a lower quality...")
                compress_pdf(input_path, quality_level-1)
        
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
            if os.path.exists(temp_output):
                os.remove(temp_output)
    