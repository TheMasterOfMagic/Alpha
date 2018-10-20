import cv2
import numpy as np
from typing import Iterable


def read(filename):
	return cv2.imread(filename)


def write(img, filename):
	return cv2.imwrite(filename, img)


def rgb2yuv(rgb: np.ndarray):
	return cv2.cvtColor(rgb, cv2.COLOR_BGR2YUV)


def yuv2rgb(yuv: np.ndarray):
	return cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)


def gray2rgb(gray: np.ndarray):
	return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)


def split(img: np.ndarray):
	return cv2.split(img)


def map_u(u: np.ndarray):
	return cv2.LUT(u, np.array([[[i, 255 - i, 0] for i in range(256)]], dtype=np.uint8))


def map_v(v: np.ndarray):
	return cv2.LUT(v, np.array([[[0, 255 - i, i] for i in range(256)]], dtype=np.uint8))


def vstack(imgs: Iterable[np.ndarray]):
	return np.vstack(imgs)


def hstack(imgs: Iterable[np.ndarray]):
	return np.hstack(imgs)


def stack(imgs: Iterable[Iterable[np.ndarray]]):
	return np.vstack(list(np.hstack(row) for row in imgs))
