import re
from datetime import datetime

# Validasi format email
def validasi_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Validasi format telepon
def validasi_telepon(telepon):
    # Hanya angka, minimal 10 digit
    pattern = r'^[0-9]{10,}$'
    return re.match(pattern, telepon) is not None

# Format timestamp ke format Indonesia
def format_tanggal(timestamp):
    try:
        dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        return dt.strftime('%d/%m/%Y %H:%M')
    except:
        return timestamp

# Fungsi untuk backup database
def backup_database():
    print("Backup database...")
    # Implementasi backup bisa ke ZIP atau copy file

# Generate laporan kontak
def generate_laporan():
    print("Generating laporan...")
    # Bisa implementasi export ke PDF/Excel