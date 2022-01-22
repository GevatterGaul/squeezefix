import piexif
from wand.image import Image


def has_adobergb_colorspace(img: Image) -> bool:
    if 'exif:ColorSpace' in img.metadata and img.metadata['exif:ColorSpace'] == '65535':
        exif_bytes = img.profiles['exif']
        exif = piexif.load(exif_bytes)

        if 'Interop' in exif:
            return exif['Interop'][1] == b'R03'

    return False


def has_srgb_colorspace(img: Image) -> bool:
    return 'exif:ColorSpace' in img.metadata and \
           img.metadata['exif:ColorSpace'] == '1'