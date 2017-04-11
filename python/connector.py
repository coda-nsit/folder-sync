# connects the two folders that need to be synced up
import shutil, os, difflib, sys
from difflib import Differ
# from __init__ import s1, s2 
# explicitely mention s1 and s2 to break circular dependency
s1 = "/home/bloodynacho/Documents/SocialCops/DeviceA/"
s2 = "/home/bloodynacho/Documents/SocialCops/DeviceB/"



# shutil doesn't raise FileModificationEvent in OS, hence handle it manually 
class ModifyFile():
	def modify_file(self, path, file_name):
		# file modified in DeviceA reflect change in DeviceB .duplicates
		if path == s1:
			# self.manual_copy(path + file_name, s2 + '.duplicates/' + file_name)
			shutil.copy(path + file_name, s2 + '.duplicates/' + file_name)
			# this change in the .duplicates folder is not being detected, so manually handle this case of asking user if DeviceB also should apply these changes to its local copy
			x = self.dup_to_real_copy(s2 + '.duplicates/' + file_name, s2 + file_name)
			# file modification sucessful change the foreign file in orginal device
			if x == True:
				shutil.copy(path + file_name, path + '.duplicates/' + file_name)
			# file modification not sucessful, do nothing 
			else:
				pass
		# file modified in DeviceB reflect change in DeviceA .duplicates
		else:
			# self.manual_copy(path + file_name, s1 + '.duplicates/' + file_name)
			shutil.copy(path + file_name, s1 + '.duplicates/' + file_name)
			# this change in the .duplicates folder is not being detected, so manually handle this case of asking user if DeviceA also should apply these changes to its local copy
			x = self.dup_to_real_copy(s1 + '.duplicates/' + file_name, s1 + file_name)
			# file modification sucessful change the foreign file in orginal device
			if x == True:
				shutil.copy(path + file_name, path + '.duplicates/' + file_name)
			# file modification not sucessful, do nothing 
			else:
				pass

	# def manual_copy(self, src, dest):
	# 	src = open(src, 'r')
	# 	dest = open(dest, 'w+')
	# 	for line in src.readlines():
	# 		dest.write(line)
	# 	src.close()
	# 	dest.close()

	def dup_to_real_copy(self, src, dest):
		try:
			f = open(dest, 'r')
			f.close()
			d = Differ()
			# diff = d.compare(open(src).readlines(), open(dest).readlines())
			diff = difflib.unified_diff(open(src).readlines(), open(dest).readlines())
			# diff = difflib.ndiff(open(src).readlines(), open(dest).readlines())
			sys.stdout.writelines(diff)
			shutil.copy(src, dest)
			return True
		except IOError:
			print "file absent in local device, possible cause: the file was either not created in this device when created in the other device or not renamed when renamed in other device"
			return False



class CreateFile():
	def create_file(self, path, file_name):
		# orginal file created in DeviceA
		# create a file in .duplicates of DeviceB
		if path == s1:
			f = open(s2 + '.duplicates/' + file_name, 'w+')
			f.close()
		# orginal file created in DeviceB
		else:
			f = open(s1 + '.duplicates/' + file_name, 'w+')
			f.close()			
		# f = open(dest + file_name,'w+')
		# f.close()



class RenameFile():
	def rename_file(self, path, before, after):
		print path, before, after
		# orginal file renamed in DeviceA
		if path == s1:
			# rename the copy in foreign of DeviceB
			os.rename(s2 + '.duplicates/' + before, s2 + '.duplicates/' + after)	
		else:
			# rename the copy in foreign of DeviceB
			os.rename(s1 + '.duplicates/' + before, s1 + '.duplicates/' + after)	
			
		



class DeleteFile():
	def delete_file(self, path, file_name):
		# orginal file deleted in DeviceA
		# delete the copy in foreign of DeviceB
		if path == s1:
			# remove local copy 
			os.remove(s2 + '.duplicates/' + file_name)
		# original file deleted in DeviceB
		# delete the copy in foreign of DeviceA
		else:
			# remove foreign copy
			os.remove(s1 + '.duplicates/' + file_name)