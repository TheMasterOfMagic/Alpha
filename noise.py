import numpy as np


def gs(img: np.ndarray, s, m=0):
  rv = img.copy()
  rv = rv.astype(np.float64)
  rv += np.random.normal(m, s, rv.shape)
  rv[rv > 255] = 255
  rv[rv < 0] = 0
  rv = rv.astype(np.uint8)
  return rv


def sp(img: np.ndarray, r):
  rv = img.copy()
  rv = rv.astype(np.float64)
  indexes = np.random.random(rv.shape)
  r /= 100  # 百分比->小数
  r /= 2  # 椒盐各半
  salt_indexes, pepper_indexes = indexes < r, indexes >= (1 - r)
  rv[salt_indexes] = 255
  rv[pepper_indexes] = 0
  rv = rv.astype(np.uint8)
  return rv
