
class BMPReader(object):
    def __init__(self, filename):
        self._filename = filename
        self._read_img_data()

    def to_string(self):
        """
        Prints a string represenation of the image, returns nothing
        """
        print('Filename: ' + self._filename)
        print('Width: ' + str(self.width))
        print('Height: ' + str(self.height))
        print('Start position: ' + str(self._start_pos))
        print('End position: ' + str(self._end_pos))

    def _get_pixel(self, x, y, offset):
        return self._pixel_data[(x * 3) + (y * self.width * 3) + offset]

    def get_pixel_r(self, x, y):
        """
        Returns an integer with the red value at position (x,y)
        """
        return self._get_pixel(x, self.height-y-1, 2)
        
    def get_pixel_g(self, x, y):
        """
        Returns an integer with the green value at position (x,y)
        """
        return self._get_pixel(x, self.height-y-1, 1)
        
    def get_pixel_b(self, x, y):
        """
        Returns an integer with the blue value at position (x,y)
        """
        return self._get_pixel(x, self.height-y-1, 0)

    def get_pixels(self):
        """
        Returns a multi-dimensional array of the RGB values of each pixel in the
        image, arranged by rows and columns from the top-left.  Access any pixel
        by its location, eg:

        pixels = BMPReader(filename).get_pixels()
        top_left_px = pixels[0][0] # [255, 0, 0]
        bottom_right_px = pixels[8][8] # [0, 255, 255]
        """
        pixel_grid = []
        pixel_data = list(self._pixel_data) # So we're working on a copy

        for x in range(self.width):
            col = []
            for y in range(self.height):
                r = pixel_data.pop()
                g = pixel_data.pop()
                b = pixel_data.pop()
                col.append((r, g, b))
            col.reverse()
            pixel_grid.append(col)

        return pixel_grid

    def _lebytes_to_int(self, bytes):
        n = 0x00
        while len(bytes) > 0:
            n <<= 8
            n |= bytes.pop()
        return int(n)

    def _read_img_data(self):
        with open(self._filename, 'rb') as f:
            img_bytes = list(bytearray(f.read(38)))

        # Before we proceed, we need to ensure certain conditions are met
        assert img_bytes[0:2] == [66, 77], "Not a valid BMP file"
        assert self._lebytes_to_int(img_bytes[30:34]) == 0, \
            "Compression is not supported"
        assert self._lebytes_to_int(img_bytes[28:30]) == 24, \
            "Only 24-bit colour depth is supported"

        self._start_pos = self._lebytes_to_int(img_bytes[10:14])
        self._end_pos = self._lebytes_to_int(img_bytes[34:38])

        self.width = self._lebytes_to_int(img_bytes[18:22])
        self.height = self._lebytes_to_int(img_bytes[22:26])

        img_bytes.clear()

        # As per https://en.wikipedia.org/wiki/BMP_file_format for BI_RGB
        # images, length can be 0, so it can be inferred from the image size
        if self._end_pos == 0:
            self._end_pos = self.width * self.height * 3

        self._end_pos = self._start_pos + self._end_pos

        with open(self._filename, 'rb') as f:
           f.read(self._start_pos)
           self._pixel_data = f.read(self._end_pos)
