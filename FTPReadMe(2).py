import ftplib
import os
from io import StringIO
print("Connecting to database")

try:
	ftp = ftplib.FTP("ftp.ncdc.noaa.gov")
	ftp.login()
	print("Connection established!")
except ftplib.all_errors as e:
	print(str(e).split(None, 1)[0])

print(f"Current directory: {ftp.pwd()}")
print("Moving to /pub/data/noaa/")
ftp.cwd("/pub/data/noaa/")
print(f"Current working directory is {ftp.pwd()}")

file_name = "isd-history.txt"
with open(os.getcwd() + r"/data/isd-history.txt", "wb") as f:
	try:
		ftp.retrbinary(f"RETR {file_name}", f.write)
		print("isd-history.txt successfully created")
	except ftplib.all_errors as e:
		print(str(e).split(None, 1)[0])
ftp.close()