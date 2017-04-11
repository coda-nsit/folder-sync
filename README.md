Installing Dependencies
1. virtualenv socialcops1
2. source socialcops1/bin/activate
3. pip install watchdog
4. npm init
5. npm install difflib


Fil structure
1. SocialCops contains 2 subfolders i.DeviceA ii.DeviceB, these 2 sub folders act as the 2 seperate droids (machines) which are synced up
2. SocialCops also contains a folder python which contains all the python files
3. node_modules contains the library difflib which ws installed using npm
4. links.odt contains all the links that were used while building this project
5. package.json is built by npm to keep track of all the npm packages

Architecture used
Each of DeviceA and DeviceB contain the files that need to be synced up. Each of these folders also contain .duplicate folders. These are used to keep track of the other device’s files, example: DeviceA -> .duplicates will always be in sync with the files of DeviceB and vice versa. This is done so that the device owner is always at the liberty to decide whether he/she wants to pull the changes made by the other device into his/her own device. After a new operation is done like creating a file, renaming a file and deleting a file, it will always be asked if user actually wants to do these changes in own device. This is done by comparing the files in .duplicates and the actual files and thus the .duplicates


Steps to run the program
1. Install the dependencies
2. open 2 terminal windows
in the first
cd <path to SocialCops>/
source socialcops1/bin/activate
cd python/
python m1.py /home/bloodynacho/Documents/SocialCops/DeviceA/
in the second
cd <path to SocialCops>/
source socialcops1/bin/activate
cd python/
python m2.py /home/bloodynacho/Documents/SocialCops/DeviceB/
3. now in the DeviceA or DeviceB create files (and not folders/directories) and keep a watch on the terminal which will prompt for inputs which are self understood

Limitations/Bugs
1. Recursive syncing not handled: no new directories can be created, only files can be manipulated
2. in connector.py the path DeviceA and DeviceB have been hardcoded (as s1, s3) as otherwise circular imports take place m1,m2 -> listen_directory.py -> connector.py -> m1,m2, thus so that connector.py no longer depends on m1, m2 and break the circular import s1 and s2 have been harcoded
3. in the .duplicates folders the actual files need not have been saved rather symbolic links could have been used which could have pointed to the original files in the other device as an example, DeviceA -> .duplicates could have contained pointers to DeviceB files rather than actual files
4. one extra step required   
5. creation with file name different from Untitled Document requires 2 extra steps
6. entire transfer is done not the diff, thus will require more data to be transferred

