import numpy as np
from PIL import Image


def bits_provider(message):
    """Convert text (chars) to bits

    :param message: text message to be converted to bits
    """

    for char in message:
        ascii_value: int = ord(char)
        for power in range(7, -1, -1):
            yield 1 if ascii_value & 2 ** power else 0


def create_image(message, path) -> None:
    """Hide text message in image

    :param message: text message to be hidden
    :param path: path to the image
    """

    bits_in_msg = len(message) * 8
    img = Image.open(path)
    image_width = img.width
    image_height = img.height
    image_size = image_width * image_height
    assert image_size >= bits_in_msg, 'Image is too small or message is too long.'
    pixels = np.array(img)

    print(pixels[0])

    # clear last bits in 'Red' value of image pixels
    new_pixel_set = []
    for column in np.array(pixels):
        new_column = []
        for pixel in column:
            new_column.append([(pixel[0]) & ~(1 << 0), pixel[1], pixel[2]])
        new_pixel_set.append(new_column)
    pixels = new_pixel_set

    print(pixels[0])

    # save text bits on the last bits in 'Red' value of image pixels
    for i, bit in enumerate(bits_provider(message)):
        row = i // image_height
        col = i % image_width
        pixels[row][col][0] = (pixels[row][col][0]) | (bit << 0)

    print('after encoding')
    print(pixels[0])

    img = Image.fromarray(np.uint8(pixels))
    img.save(path)
    img.close()


def decode_image(path):
    """Decode hidden text from image

    :param path: path to image
    :return: decoded secret message
    """

    img = Image.open(path)
    image_width = img.width
    image_height = img.height
    pixels = np.array(img)

    print(pixels[0])
    bits = []

    for i in range(image_height):
        for j in range(image_width):
            bits.append(pixels[i][j][0] & ((1 << 1) - 1))

    bytes_l = [int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8)]
    decoded_message = ''.join(map(chr, bytes_l))
    img.close()

    return decoded_message
