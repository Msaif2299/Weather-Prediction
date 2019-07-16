from subprocess import call
import os
call(["py", os.getcwd() + '/BuildChecker(1).py'])
call(["py", os.getcwd() + '/FTPReadMe(2).py'])
call(["py", os.getcwd() + '/FTPScraper(3).py'])
print("Please extract all the .tar files in the folder with 7zip, please extract into the /data/ folder.")
input()
call(["py", os.getcwd() + '/StationFinder2008-2019(4).py'])
call(["py", os.getcwd() + '/StationList(5)'])
call(["py", os.getcwd() + '/UnknownPurpose(6).py'])
call(["py", os.getcwd() + '/date_checker(7).py'])
call(["py", os.getcwd() + '/MultiStationBuilder.py'])
print("You should now be set up for running the main.py")