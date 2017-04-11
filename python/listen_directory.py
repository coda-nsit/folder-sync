import sys, time, os, glob, logging, shutil
from watchdog.observers import Observer
from watchdog.events import *
from connector import ModifyFile, CreateFile, RenameFile, DeleteFile

# sequence of events when file created 
''' 
    created event /home/bloodynacho/Documents/SocialCops/DeviceA/Untitled Document
    modified event /home/bloodynacho/Documents/SocialCops/DeviceA
'''
# sequence of events when file renamed
'''
    moved event /home/bloodynacho/Documents/SocialCops/DeviceA/Untitled Document /home/bloodynacho/Documents/SocialCops/DeviceA/hello
    modified event /home/bloodynacho/Documents/SocialCops/DeviceA
'''
# sequence of events when file deleted
'''
    deleted event /home/bloodynacho/Documents/SocialCops/DeviceA/hello
    modified event /home/bloodynacho/Documents/SocialCops/DeviceA
'''
# sequence of events when file edited
'''
    created event /home/bloodynacho/Documents/SocialCops/DeviceA/.goutputstream-ALJKYY
    modified event /home/bloodynacho/Documents/SocialCops/DeviceA
    modified event /home/bloodynacho/Documents/SocialCops/DeviceA/.goutputstream-ALJKYY
    moved event /home/bloodynacho/Documents/SocialCops/DeviceA/.goutputstream-ALJKYY /home/bloodynacho/Documents/SocialCops/DeviceA/f1L
    modified event /home/bloodynacho/Documents/SocialCops/DeviceA
'''



class EventHandlder(FileSystemEventHandler):
    def dispatch(self, event):
        if event.event_type == 'created':
            self.on_created(event)
        elif event.event_type == 'moved':
            self.on_moved(event)
        elif event.event_type == 'deleted':
            self.on_deleted(event)
        else:
            self.on_modified(event)

    def on_created(self, event):
        location = event.src_path.split(".duplicates/")[0]
        # race condition: above line commented because of race condition, the file name is always Untitled Document, so file_name='Untitled Document' so adjust for this use the file that is latest 
        file_name = ''
        try:
            file_name = max(glob.iglob(location + '.duplicates/*'), key=os.path.getctime).split(".duplicates/")[1]
        except Exception:
            pass
        # creation by foreign device
        if ".duplicates" in event.src_path:
            x = raw_input("request for creation of file Y/n: ")
            while x not in ['Y', 'n']:
                print "invalid entry"
                x = raw_input("request for creation of file Y/n: ")
            if x == 'Y':
                # create the file in local device
                f = open(location + file_name,'w+')
                f.close()
            else:
                print "file not created but devices have become unsynced"
        # creation by local device
        else:
            # file modified don't do anything let things be handled by system
            if 'goutputstream' in event.src_path.split('/')[-1]:
                pass
            # user created a file sync it to the other device 
            else:
                path = event.src_path[:event.src_path.rfind('/')+1]
                file_name = event.src_path.split('/')[-1]
                file_creater = CreateFile()
                file_creater.create_file(path, file_name)

    def on_deleted(self, event):
        # delete by foreign device
        if ".duplicates" in event.src_path:
            x = raw_input("request for deletion of file Y/n: ")
            while x not in ["Y", "n"]:
                print "invalid entry"
                x = raw_input("request for deletion of file Y/n: ")
            if x == "Y":
                file_name = event.src_path.split("/")[-1]
                location =  event.src_path.split(".duplicates/")[0]
                try:
                    f = open(location + file_name, 'r')
                    f.close()
                    os.remove(location + file_name)
                except IOError:
                    print "file absent in local device, possible cause: the file was not created in local device when it was created in foreign device"
            else:
                print "file not deleted but devices have become unsynced"
        # delete in local device delete the file in other device also 
        else:
            path = event.src_path[:event.src_path.rfind('/')+1]
            file_name = event.src_path.split('/')[-1]
            file_deleter = DeleteFile()
            file_deleter.delete_file(path, file_name)

    def on_moved(self, event):
        # move by foreign device
        if ".duplicates" in event.src_path:
            # reflect this change in FolderB
            if '.goutputstream'  in event.src_path:
                x = raw_input("request for modificaion of file Y/n: ")
                while x not in ["Y", "n"]:
                    print "invalid entry"
                    x = raw_input("request for modificaion of file Y/n: ")
                if x == "Y":
                    file_name = event.src_path.split('/')[-1]
                    location = event.src_path.split('.duplicates/')[0]
                    try:
                        f = open(location + file_name, 'r')
                        f.close()
                        shutil.copy(event.src_path, location + file_name)
                    except IOError:
                        print "file absent in local device, possible cause: the file was either not created in this device when created in the other device or not renamed when renamed in other device"
            # file renamed
            else:
                x = raw_input("request for renaming of file Y/n: ")
                while x not in ['Y', 'n']:
                    print "invalid entry"
                    x = raw_input("request for renaming of file Y/n: ")
                if x == 'Y':
                    # try finding the file and if found rename it else raise exception
                    before = event.src_path.split('/')[-1]
                    after = event.dest_path.split('/')[-1]
                    location = event.src_path.split(".duplicates/")[0]
                    try:
                        f = open(location + before, 'r')
                        f.close()
                        os.rename(location + before, location + after)
                    except IOError:
                        print "file absent in local device, possible causes: the file was renamed earlier in foreign device but renaming was not done in local device or file was deleted in local device but not in foreign device"
                else:
                    print "file not renamed but devices have become unsynced"
        # move in local device
        else:
            # file modified reflect change in the foreign file of the other device
            if 'goutputstream'  in event.src_path.split('/')[-1]:
                path = event.dest_path[:event.dest_path.rfind('/')+1]
                file_name = event.dest_path.split('/')[-1]
                file_modifier = ModifyFile()
                file_modifier.modify_file(path, file_name)
            # file renamed
            else:
                path = event.src_path[:event.src_path.rfind('/')+1]
                before = event.src_path.split('/')[-1]
                after = event.dest_path.split('/')[-1]
                file_renamer = RenameFile()
                file_renamer.rename_file(path, before, after) 

    def on_modified(self, event):
        pass



class Watcher():
    def __init__(self):
        self.observer = Observer()

    def assign_event_handler(self, event='action'):
        if event == 'log':
            logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
            return LoggingEventHandler()
        elif event == 'action':
            return EventHandlder()            

    def listen(self, path):
        event_handler = self.assign_event_handler()
        self.observer.schedule(event_handler, path, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()