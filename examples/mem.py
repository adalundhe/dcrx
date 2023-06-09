import time
from fs.memoryfs import MemoryFS


memory_filesystem = MemoryFS()

memory_filesystem.create('test.txt')
time.sleep(60)
memory_filesystem.close()