from PIL import Image
from os.path import exists
from os import stat
import numpy


def change_bit(bit: int, val: int) -> int:
    """
    Function that changes last bit in r,g or b value
    :param bit: int to be encoded
    :param val: int value of r,g or b
    :return: edited value of r,g or b
    """
    if bit == 0:
        val = val & ~1
    else:
        val = val | 1

    return val


def encode_text(input_image: Image, text: str) -> Image:
    """
    Function that encodes text to image
    :param input_image: input_image in which the text is encoded
    :param text: text to be encoded - already transformed to bites
    :return: Image
    """
    return encode_loop(input_image, text)


def encode_file(input_image: Image, file_name: str) -> Image:
    """
    Function that encodes file to image
    :param input_image: input_image in which the file is encoded
    :param file_name: name of file to be encoded
    :return: Image
    """
    f_bytes = numpy.fromfile(file_name, dtype="uint8")
    f_bits = numpy.unpackbits(f_bytes)

    return encode_loop(input_image, f_bits)


def encode_loop(input_image: Image, bits_data) -> Image:
    """
    Function that loops through every pixel of image and puts new bits to LSB
    :param input_image: input_image in which the data are encoded
    :param bits_data: data of bits (either string of bits or array of bits)
    :return: Image
    """
    changed = 0
    for x in range(input_image.width):
        for y in range(input_image.height):
            r, g, b = input_image.getpixel((x, y))

            # change r
            r = change_bit(int(bits_data[changed]), r)
            changed += 1

            # check if there is more to change
            if changed >= len(bits_data):
                input_image.putpixel((x, y), (r, g, b))
                break

            # change g
            g = change_bit(int(bits_data[changed]), g)
            changed += 1

            # check if there is more to change
            if changed >= len(bits_data):
                input_image.putpixel((x, y), (r, g, b))
                break

            # change b
            b = change_bit(int(bits_data[changed]), b)
            changed += 1

            # check if there is more to change
            if changed >= len(bits_data):
                input_image.putpixel((x, y), (r, g, b))
                break

            input_image.putpixel((x, y), (r, g, b))

        # check if there is more to change
        if changed >= len(bits_data):
            break

    return input_image


def decode_text():
    pass


def decode_file():
    pass


def detect_steganography():
    pass


def convert_text(text: str) -> str:
    """
    Converts text to string of bits
    :param text: text to be converted
    :return: converted string
    """
    res = ''.join(format(ord(i), '08b') for i in text)
    return str(res)


# !! TODO definition of header
def get_header():
    return ""


def is_image_big_enough(file_size: int, image_size: int) -> bool:
    """
    Function that checks if file/text size is bigger than image available size
    :param file_size:
    :param image_size:
    :return: bool
    """
    if file_size > image_size:
        print('Text is too big')
        return False

    return True


def validate_and_get_size(u_input: str) -> int:
    """
    File that validates user input and returns it size in bits
    :param u_input: user input
    :return: int size in bits
    """
    size = 0
    # if it is file (not checking png for now)
    if '.jpg' in u_input or '.jpeg' in u_input or '.txt' in u_input:
        if exists(u_input):
            file_stats = stat(u_input)
            # get file size in bits
            size = file_stats.st_size * 8
        else:
            print('File which you want to encode does not exist.\n')
            exit(2)
    else:
        # get text input size in bits
        size = len(u_input) * 8

    return size


def main():
    # get user input
    user_input = input('What do you want to encode?\n')

    # check if it is file or string, validate if exists, get size in bits
    size_in_bits = validate_and_get_size(user_input)

    # get image to encode in name
    image_to_encode_in = input('In what file do you want to encode it?\n')

    # try to open image
    try:
        image = Image.open(image_to_encode_in)
    except FileNotFoundError:
        print('File in which you want to encode does not exist.\n')
        exit(2)

    # image max bits to encode in
    # not checking png for now ( * 4 )
    max_bits = image.width * image.height * 3

    # check if image is big enough to encode data in it
    if is_image_big_enough(size_in_bits, max_bits):
        file_output = input('What should be the output file name?(without extension)\n')

        if '.jpg' in user_input or '.jpeg' in user_input or '.txt' in user_input:
            # can do this as in this point I know it exist
            changed_image = encode_file(image, user_input)
        else:
            text_input_binary = convert_text(user_input)
            changed_image = encode_text(image, text_input_binary)
    else:
        # suggest making image bigger
        exit(4)

    # save changed image
    changed_image.save(file_output + '.png')


if __name__ == '__main__':
    main()
