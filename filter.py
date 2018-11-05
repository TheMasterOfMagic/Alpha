import numpy as np
import cv2


def mean(img: np.ndarray, k):
  rv = img.copy()
  rv = cv2.blur(rv, (k, k))
  return rv


def median(img: np.ndarray, k):
  rv = img.copy()
  rv = cv2.medianBlur(rv, k)
  return rv
