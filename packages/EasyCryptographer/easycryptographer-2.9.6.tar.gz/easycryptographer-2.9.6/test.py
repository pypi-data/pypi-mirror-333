from stegano import lsb

# 打开一个图片文件
picture = lsb.open('img.png')

# 将文本信息隐藏到图片中
data = picture.hide('your_secret_message').build('output_image.jpg')
