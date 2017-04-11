import sys
from __init__ import s1
s1 = src = sys.argv[1]
from listen_directory import Watcher



class Main():
	def watch(self):
		w = Watcher()
		w.listen(src)


if __name__ == "__main__":
    m = Main()
    m.watch()