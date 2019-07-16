import ftplib
import os

start_year = looping_year = 2008
end_year = 2019

print('Connecting to NOAA database')

try:
	ftp = ftplib.FTP('ftp.ncdc.noaa.gov')
	ftp.login()
	print('Connection established')
except ftplib.all_errors as e:
	print(str(e).split(None, 1)[0])

print(f"Current working directory is {ftp.pwd()}")
print("Listing all the files in the current directory: ")
ftp.retrlines('LIST')

print("Changing to the GSOD directory")
ftp.cwd('/pub/data/gsod/')
print(f"Current working directory is {ftp.pwd()}")

all_files = ftp.nlst()

directory_name = os.getcwd() + f'/data/GSOD_data'
if not os.path.exists(directory_name):
	os.makedirs(directory_name)
directory_path = directory_name + '/'
os.chdir(directory_path)

print('Searching for the individual weather directories')
while looping_year<=end_year:
	temp_directory = f"/pub/data/gsod/{looping_year}"
	temp_file_name = f"gsod_{looping_year}.tar"
	file = open(temp_file_name, "wb")
	ftp.cwd(temp_directory)
	print(f"Downloading year: {looping_year}")
	try:
		ftp.retrbinary(f"RETR {temp_file_name}", file.write)
		print(f"Successfully downloaded year: {looping_year}")
	except ftplib.all_errors as e:
		print(f"Error downloading year: {looping_year}")
		print(str(e).split(None, 1)[0])
	looping_year += 1
print("All files downloaded")
print("Closing connection")
ftp.close()
