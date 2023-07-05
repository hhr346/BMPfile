# Test for the lena

from ReadBMPFile import ReadBMPFile
from ModifyBMPFile import ModifyBMPFile

filePath = '.\\lena.bmp'
fileModified = open('.\\new.bmp', 'wb')

bmpFile = ReadBMPFile(filePath)
bmpFileNew = ModifyBMPFile(filePath)
fileModified.write(bmpFileNew.file_head)
fileModified.write(bmpFileNew.bmp_head)

for i in range(1024):
    fileModified.write(bmpFileNew.color_index_pack[i])

for i in range(256*256):
    fileModified.write(bmpFileNew.bit_map_pack[i])
