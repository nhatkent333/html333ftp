import os
from ftplib import FTP
import csv
import requests
from io import StringIO

# Lấy thông tin kết nối FTP từ secrets của GitHub Actions
ftp_host = os.getenv('FTP_HOST')
ftp_username = os.getenv('FTP_USERNAME')
ftp_password = os.getenv('FTP_PASSWORD')

# Kết nối đến FTP
ftp = FTP(ftp_host, ftp_username, ftp_password)

# Đặt thư mục trên FTP để tải lên
upload_directory = '/currency'
ftp.cwd(upload_directory)  

# Đường dẫn của file CSV trên Google Drive
drive_csv_url = 'https://github.com/nhatkent333/html333ftp/blob/d18a910bb9fd1698d41319b50fdea30885e84690/data.csv'

# Lấy dữ liệu từ file CSV trên Google Drive
response = requests.get(drive_csv_url)
csv_data = response.text

# Đọc dữ liệu CSV
csv_reader = csv.DictReader(StringIO(csv_data))

# Duyệt qua từng dòng trong dữ liệu CSV và tạo file HTML
for row in csv_reader:
    slug = row['slug']
    html_code = row['html']
    if html_code is not None:
        file_name = slug + '.html'

        # Tạo file HTML và ghi nội dung
        with open(file_name, 'w') as file:
            file.write(html_code)

        # Tải file lên FTP
        with open(file_name, 'rb') as file:
          try:
              ftp.storbinary(f'STOR {file_name}', file)
          except Exception as e:
              print(f"Error uploading file {file_name}: {e}")

        # Xóa file HTML cục bộ sau khi đã tải lên FTP
        os.remove(file_name)
    else:
        print(f"html_code is None for slug {slug}, skipping...")


# Đóng kết nối FTP
ftp.quit()
