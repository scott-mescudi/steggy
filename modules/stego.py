from PIL import Image
import os
import zipfile

def gen_data(data):
    """Convert binary data into a list of 8-bit binary strings."""
    return [format(byte, '08b') for byte in data]

def mod_pix(pix, data):
    """Modify pixel data based on binary data."""
    datalist = gen_data(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):
        pixels = [value for _ in range(3) for value in imdata.__next__()[:3]]
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pixels[j] % 2 != 0):
                pixels[j] -= 1
            elif (datalist[i][j] == '1' and pixels[j] % 2 == 0):
                if pixels[j] != 0:
                    pixels[j] -= 1
                else:
                    pixels[j] += 1

        if i == lendata - 1:
            if pixels[-1] % 2 == 0:
                if pixels[-1] != 0:
                    pixels[-1] -= 1
                else:
                    pixels[-1] += 1
        else:
            if pixels[-1] % 2 != 0:
                pixels[-1] -= 1

        yield pixels[:3]
        yield pixels[3:6]
        yield pixels[6:9]

def encode_enc(newimg, data):
    """Encode binary data into the image."""
    w, _ = newimg.size
    (x, y) = (0, 0)

    for pixel in mod_pix(newimg.getdata(), data):
        newimg.putpixel((x, y), tuple(pixel))
        if x == w - 1:
            x = 0
            y += 1
        else:
            x += 1

def encode_binary_image(image_path, data, new_image_path):
    """Encode binary data into an image."""
    if not data:
        raise ValueError('Data is empty')
    image = Image.open(image_path, 'r')
    newimg = image.copy()
    encode_enc(newimg, data)
    format_name = new_image_path.split(".")[-1].upper()
    newimg.save(new_image_path, format_name)

def decode_binary_image(image_path):
    """Decode binary data from an image."""
    image = Image.open(image_path, 'r')
    data = bytearray()
    imgdata = iter(image.getdata())
    while True:
        pixels = [value for _ in range(3) for value in imgdata.__next__()[:3]]
        binstr = ''.join('0' if i % 2 == 0 else '1' for i in pixels[:8])
        data.append(int(binstr, 2))
        if pixels[-1] % 2 != 0:
            return data







