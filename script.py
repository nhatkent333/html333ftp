from google.colab import auth
import gspread
from google.auth import default
from ftplib import FTP
import os

# Autenticating to Google
auth.authenticate_user()
creds, _ = default()
gc = gspread.authorize(creds)

# ID của bảng Google Sheets và tên của tab
sheet_id = '1VM8WL63eMLcHHxmrDjGpkCDQqGQMKiyeUIU8JCj9Fbw'
tab_name = 'export'

# Mở tab cụ thể trong bảng và lấy dữ liệu
worksheet = gc.open_by_key(sheet_id).worksheet(tab_name)
data = worksheet.get_all_records()

# Kết nối đến FTP
ftp = FTP('103.42.57.100', 'tool', 'aaztZ5FWATmmXiyF')

# Đặt thư mục trên FTP để tải lên
upload_directory = '/currency'
ftp.cwd(upload_directory)  

# Duyệt qua từng dòng trong dữ liệu và tạo file HTML
for row in data:
    slug = row['slug']
    html_code = row['html']
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

# Đóng kết nối FTP
ftp.quit()
