from PIL import Image

# Open the JPEG image
image = Image.open("tinh.jpeg")

# Convert the image to CYMK
cymk_image = image.convert("CMYK")

# Separate the channels
c_channel, y_channel, m_channel, b_channel = cymk_image.split()

# invert the channels
c_channel = Image.eval(c_channel, lambda x: 255-x)
y_channel = Image.eval(y_channel, lambda x: 255-x)
m_channel = Image.eval(m_channel, lambda x: 255-x)

# save as png
c_channel.save("channels/c_channel.png")
y_channel.save("channels/y_channel.png")
m_channel.save("channels/m_channel.png")

# make the image black and white and extract the black channel
image = image.convert("L")
image.save("channels/black_white.png")

