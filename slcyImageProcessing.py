import sys
import cv2
import numpy
import matplotlib

def Preview(image) -> None:
    """Previews an image in a new window. Press any key to close
    image <numpy.ndarray>>"""
    cv2.imshow('preview',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #matplotlib.pyplot.imshow(img)
    #matplotlib.pyplot.show()
