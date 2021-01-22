# PhotoImage class from PIL.ImageTk, my pc does notwant to install this class appearently

try:
    import tkinter
except ImportError:
    import Tkinter
    tkinter = Tkinter
    del Tkinter

from PIL import Image

class PhotoImage:
    """
    A Tkinter-compatible photo image.  This can be used
    everywhere Tkinter expects an image object.  If the image is an RGBA
    image, pixels having alpha 0 are treated as transparent.

    The constructor takes either a PIL image, or a mode and a size.
    Alternatively, you can use the **file** or **data** options to initialize
    the photo image object.

    :param image: Either a PIL image, or a mode string.  If a mode string is
                  used, a size must also be given.
    :param size: If the first argument is a mode string, this defines the size
                 of the image.
    :keyword file: A filename to load the image from (using
                   ``Image.open(file)``).
    :keyword data: An 8-bit string containing image data (as loaded from an
                   image file).
    """

    def __init__(self, image=None, size=None, **kw):

        # Tk compatibility: file or data
        if image is None:
            if "file" in kw:
                image = Image.open(kw["file"])
                del kw["file"]
            elif "data" in kw:
                from io import BytesIO
                image = Image.open(BytesIO(kw["data"]))
                del kw["data"]

        if hasattr(image, "mode") and hasattr(image, "size"):
            # got an image instead of a mode
            mode = image.mode
            if mode == "P":
                # palette mapped data
                image.load()
                try:
                    mode = image.palette.mode
                except AttributeError:
                    mode = "RGB"  # default
            size = image.size
            kw["width"], kw["height"] = size
        else:
            mode = image
            image = None

        if mode not in ["1", "L", "RGB", "RGBA"]:
            mode = Image.getmodebase(mode)

        self.__mode = mode
        self.__size = size
        self.__photo = tkinter.PhotoImage(**kw)
        self.tk = self.__photo.tk
        if image:
            self.paste(image)

    def __del__(self):
        name = self.__photo.name
        self.__photo.name = None
        try:
            self.__photo.tk.call("image", "delete", name)
        except:
            pass  # ignore internal errors

    def __str__(self):
        """
        Get the Tkinter photo image identifier.  This method is automatically
        called by Tkinter whenever a PhotoImage object is passed to a Tkinter
        method.

        :return: A Tkinter photo image identifier (a string).
        """
        return str(self.__photo)


    def width(self):
        """
        Get the width of the image.

        :return: The width, in pixels.
        """
        return self.__size[0]


    def height(self):
        """
        Get the height of the image.

        :return: The height, in pixels.
        """
        return self.__size[1]


    def paste(self, im, box=None):
        """
        Paste a PIL image into the photo image.  Note that this can
        be very slow if the photo image is displayed.

        :param im: A PIL image. The size must match the target region.  If the
                   mode does not match, the image is converted to the mode of
                   the bitmap image.
        :param box: A 4-tuple defining the left, upper, right, and lower pixel
                    coordinate.  If None is given instead of a tuple, all of
                    the image is assumed.
        """

        # convert to blittable
        im.load()
        image = im.im
        if image.isblock() and im.mode == self.__mode:
            block = image
        else:
            block = image.new_block(self.__mode, im.size)
            image.convert2(block, image)  # convert directly between buffers

        tk = self.__photo.tk

        try:
            tk.call("PyImagingPhoto", self.__photo, block.id)
        except tkinter.TclError:
            # activate Tkinter hook
            try:
                from PIL import _imagingtk
                try:
                    _imagingtk.tkinit(tk.interpaddr(), 1)
                except AttributeError:
                    _imagingtk.tkinit(id(tk), 0)
                tk.call("PyImagingPhoto", self.__photo, block.id)
            except (ImportError, AttributeError, tkinter.TclError):
                raise  # configuration problem; cannot attach to Tkinter
