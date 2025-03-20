import numpy as np
import cv2


def rescale_to_8bit(image, min=2, max=98):
    """
    Rescales an image to an 8-bit unsigned integer representation by stretching
    and clamping its intensity values between specified percentile ranges. This
    transformation enhances the dynamic range of the image and is useful for
    various image processing tasks.

    :param image: A NumPy array representing the input image to be rescaled.
                  This image should have intensity values that need adjustment.
    :param min: The lower percentile cutoff for rescaling, with a default
                value of 2, indicating that the intensity values below this
                percentile will be clipped.
    :param max: The upper percentile cutoff for rescaling, with a default
                value of 98, indicating that the intensity values above this
                percentile will be clipped.
    :return: A NumPy array of the same shape as the input image, with the
             intensity values rescaled to the range [0, 255] as 8-bit
             unsigned integers.
    """
    p_min, p_max = np.percentile(image, (min, max))

    if p_min == p_max:
        return np.zeros(image.shape, dtype=np.uint8)

    scaled_image = 255 * (image - p_min) / (p_max - p_min)

    scaled_image = np.clip(scaled_image, 0, 255)

    return scaled_image.astype(np.uint8)


def apply_histogram_equalization(image):
    """
    Apply histogram equalization to the input image. Histogram equalization
    enhances the contrast of an image by effectively spreading out the most
    frequent intensity values. This function supports both grayscale and
    RGB images, converting them to grayscale before applying the equalization
    process. The equalized grayscale image is then stacked into a 3-channel
    image.

    :param image:
        The image to be equalized. It can be a 2D array for grayscale or a
        3D array for RGB images.
    :type image: numpy.ndarray

    :return:
        A new image where the histogram has been equalized. The returned
        image will be a 3-channel RGB image irrespective of whether the
        input was grayscale or RGB.
    :rtype: numpy.ndarray
    """
    if image.ndim == 3:
        image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        image_gray = image

    equalized_img = cv2.equalizeHist(image_gray)

    return np.stack((equalized_img,) * 3, axis=-1)


def apply_clahe(image):
    """
    Applies CLAHE (Contrast Limited Adaptive Histogram Equalization) to an
    image for improving contrast in both grayscale and color images.

    CLAHE works by dividing the image into small tiles and enhancing each
    tile separately. It is particularly useful for improving the visibility
    of features in images with varying lighting conditions or shadows.

    :param image: The input image to which CLAHE should be applied. This can
                  be either a grayscale or a color image. If the image has
                  three dimensions, it is assumed to be in the BGR color
                  format where CLAHE is applied to each channel separately.
    :return: The image with applied CLAHE, having enhanced contrast compared
             to the original input.
    """
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

    if image.ndim == 3:
        channels = cv2.split(image)
        clahe_channels = [clahe.apply(ch) for ch in channels]
        image_clahe = cv2.merge(clahe_channels)
    else:
        image_clahe = clahe.apply(image)

    return image_clahe
