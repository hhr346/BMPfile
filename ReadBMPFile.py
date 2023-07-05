from struct import unpack

class ReadBMPFile :
    def __init__(self, filePath) :
        file = open(filePath, "rb")

        # 读取 bmp 文件的文件头 14 字节
        self.bfType = unpack("<h", file.read(2))[0]       # 0x4d42 对应BM 表示这是Windows支持的位图格式
        self.bfSize = unpack("<i", file.read(4))[0]       # 位图文件大小
        self.bfReserved1 = unpack("<h", file.read(2))[0]  # 保留字段 必须设为 0 
        self.bfReserved2 = unpack("<h", file.read(2))[0]  # 保留字段 必须设为 0 
        self.bfOffBits = unpack("<i", file.read(4))[0]    # 偏移量 从文件头到位图数据需偏移多少字节（位图信息头、调色板长度等不是固定的，这时就需要这个参数了）

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

        self.color_index = []
        self.bmp_data = []

        print('the off is ', self.bfOffBits)
        print('the pixel size is', self.biBitCount)
        print('the height is ', self.biHeight)
        print('the width is ', self.biWidth)
        print('the index of color is ', self.biClrUsed)

        if self.bfOffBits != 54:
            for i in range(int((self.bfOffBits - 54)/4)):
                self.color_index.append([unpack("<B", file.read(1))[0], unpack("<B", file.read(1))[0], unpack("<B", file.read(1))[0], unpack("<B", file.read(1))[0]])
                #print(self.color_index)

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
                    bmp_row.append(bmp_pixel)

                # the storation should be multiples of 4
                while count % 4 != 0:
                    file.read(1)
                    count += 1

                #print('the row is ', bmp_row)
                self.bmp_data.append(bmp_row)
        
        self.bmp_data.reverse()
        file.close()
