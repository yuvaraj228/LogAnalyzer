import requests
import ftplib

def logDownloader(ftp_site):
	# Separating the FTP url, path and the file name
	ftp_site = ftp_site[6:]
	url = ftp_site.split("/")
	print(url)
	if len(url)>3:
		path = "/".join(url[1:-1])
	else:
		path = url[1]+"/"
	print(path)
	# Connect to the FTP site with user credentials and download the file. Downloaded the file to my local in this case
	try :
		# connect to host, default port
		ftp = ftplib.FTP(url[0])
		# default, i.e.: user anonymous, passwd anonymous@
		ftp.login()
		ftp.encoding = "utf-8"
		# After login, navigating to working directory of file
		ftp.cwd(path)
		# Writing file to local
		with open("/app/input/"+url[-1], "wb") as file:
			ftp.retrbinary(f"RETR {url[-1]}", file.write)
	# Generic exception. This needs to be enhanced
	except ftplib.all_errors as e:
		print("Unknown Exception occured : " +str(e))

	finally:
		ftp.close()
	return True

