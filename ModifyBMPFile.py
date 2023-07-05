from struct import unpack
from struct import pack

class ModifyBMPFile :
    def __init__(self, filePath) :
        file = open(filePath, "rb")

        self.color_index = []
        self.bmp_data = []

        # 读取 bmp 文件的文件头 14 字节

        self.bfType = unpack("<h", file.read(2))[0]       # 0x4d42 对应BM 表示这是Windows支持的位图格式
        self.bfSize = unpack("<i", file.read(4))[0]       # 位图文件大小
        self.bfReserved1 = unpack("<h", file.read(2))[0]  # 保留字段 必须设为 0 
        self.bfReserved2 = unpack("<h", file.read(2))[0]  # 保留字段 必须设为 0 
        self.bfOffBits = unpack("<i", file.read(4))[0]    # 偏移量 从文件头到位图数据需偏移多少字节（位图信息头、调色板长度等不是固定的，这时就需要这个参数了）

        self.file_head = pack("<hi2hi", self.bfType, self.bfSize, self.bfReserved1, self.bfReserved2, self.bfOffBits)

        # 读取 bmp 文件的位图信息头 40 字节

        self.biSize = unpack("<i", file.read(4))[0]       # 所需要的字节数
        self.biWidth = unpack("<i", file.read(4))[0]      # 图像的宽度 单位 像素
        self.biHeight = unpack("<i", file.read(4))[0]     # 图像的高度 单位 像素
        self.biPlanes = unpack("<h", file.read(2))[0]     # 说明颜色平面数 总设为 1
        self.biBitCount = unpack("<h", file.read(2))[0]   # 说明比特数
        
        self.biCompression = unpack("<i", file.read(4))[0]  # 图像压缩的数据类型
        self.biSizeImage = unpack("<i", file.read(4))[0]    # 图像大小
        self.biXPelsPerMeter = unpack("<i", file.read(4))[0]# 水平分辨率
        self.biYPelsPerMeter = unpack("<i", file.read(4))[0]# 垂直分辨率
        self.biClrUsed = unpack("<i", file.read(4))[0]      # 实际使用的彩色表中的颜色索引数
        self.biClrImportant = unpack("<i", file.read(4))[0] # 对图像显示有重要影响的颜色索引的数目

        self.bmp_head = pack("<3i2h6i", self.biSize, self.biWidth, self.biHeight, self.biPlanes, self.biBitCount, \
                             self.biCompression, self.biSizeImage, self.biXPelsPerMeter, self.biYPelsPerMeter, self.biClrUsed, self.biClrImportant)
                            

        if self.bfOffBits != 54:
            for i in range(int((self.bfOffBits - 54)/4)):
                self.color_index.append([int(unpack("<B", file.read(1))[0]/2), int(unpack("<B", file.read(1))[0]/2), unpack("<B", file.read(1))[0], unpack("<B", file.read(1))[0]])

        self.color_index_pack = []
        for i in self.color_index:
            for j in i:
                self.color_index_pack.extend([pack("<B", j)])

        pixel_byte = int(self.biBitCount/8)
        print('the pixel byte is ', pixel_byte)
        if pixel_byte >= 1:
            for height in range(self.biHeight):
                count = 0
                bmp_row = []
                for width in range(self.biWidth):
                    bmp_pixel = []
                    for i in range(pixel_byte):
                        bmp_pixel.extend([unpack("<B", file.read(1))[0]])

                    count += pixel_byte

                    # WHY THE < OR > DON't AFFECT THE RESULT?
                    bmp_row.append(bmp_pixel)

                # the storation should be multiples of 4
                while count % 4 != 0:
                    file.read(1)
                    count += 1

                #print('the row is ', bmp_row)
                self.bmp_data.append(bmp_row)
 
        self.bit_map_pack = []
        for i in self.bmp_data:
            for j in i:
                self.bit_map_pack.extend([pack("<B", j[0])])

        file.close()
