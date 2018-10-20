from ultis import *
from functools import partial
import os


def gs(img: np.ndarray, s, m=0):
	rv = img.copy()
	l = rv[:, :, 0].astype(np.float64)
	l += np.random.normal(m, s, l.shape)
	l[l > 255] = 255
	l[l < 0] = 0
	rv[:, :, 0] = l.astype(np.uint8)
	return rv


def sp(img: np.ndarray, r):
	rv = img.copy()
	l = rv[:, :, 0].astype(np.float64)
	indexes = np.random.random(l.shape)
	r /= 100  # 百分比->小数
	r /= 2  # 椒盐各半
	salt_indexes, pepper_indexes = indexes < r, indexes >= (1 - r)
	l[salt_indexes] = 255
	l[pepper_indexes] = 0
	rv[:, :, 0] = l.astype(np.uint8)
	return rv


def mean(img: np.ndarray, k):
	img = img.copy()
	img[:, :, 0] = cv2.blur(img[:, :, 0], (k, k))
	return img


def median(img: np.ndarray, k):
	img = img.copy()
	img[:, :, 0] = cv2.medianBlur(img[:, :, 0], k)
	return img


def hist(img: np.ndarray):
	img = rgb2yuv(img)[:, :, 0]  # 只取亮度进行统计
	histogram = np.histogram(img, list(range(256)))[0]
	img = gray2rgb(img)
	h, w, d = img.shape

	n = int(w//256)
	histogram = histogram.astype(np.float64)
	_, max_val, _, _ = cv2.minMaxLoc(histogram)
	histogram /= max_val
	histogram *= h - 1

	color = (255, 230, 192)
	img = np.ones([h, w, d], np.uint8) * 128
	for i, ht in enumerate(histogram):
		ht = int(ht)
		cv2.rectangle(img, (n*i, h-1), (n*i+n-1, h-1-ht), color, -1)

	cv2.rectangle(img, (0, 0), (w-1, h-1), tuple(v//2 for v in color))
	return img


def diff(img: np.ndarray, direction: str):
	direction = direction[0].lower()
	dh = 1 if direction == 'h' else 0
	dv = 1 if direction == 'v' else 0
	img = gray2rgb(rgb2yuv(img)[:, :, 0])  # 只考虑亮度通道
	img = img.astype(np.float64)
	rv = img.copy()
	h, w, d = img.shape
	for x in range(h-dv):
		for y in range(w-dh):
			for z in range(d):
				rv[x, y, z] = img[x+dv, y+dh, z] - img[x, y, z]
	rv = rv.astype(np.uint8)
	return rv


hdiff = partial(diff, direction='h')
vdiff = partial(diff, direction='v')


def main():
	input_dir = 'input images'
	output_dir = 'output images'
	gs_ = partial(gs, s=10)
	sp_ = partial(sp, r=10)
	mean_ = partial(mean, k=3)
	median_ = partial(median, k=3)

	if not os.path.exists(output_dir):
		os.mkdir(output_dir)

	filenames = list(filter(lambda x: ' ' not in x and x.endswith('.png'), next(os.walk(input_dir))[-1]))
	for filename in filenames:
		name = filename.rsplit('.', maxsplit=1)[0]
		print('processing {} ... '.format(name), end='')
		rgb = read('{}/{}'.format(input_dir, filename))
		yuv = rgb2yuv(rgb)
		gs_yuv = gs_(yuv)
		sp_yuv = sp_(yuv)
		yuv_list = [yuv, gs_yuv, sp_yuv]
		mean_yuv_list = list(mean_(yuv) for yuv in yuv_list)
		median_yuv_list = list(median_(yuv) for yuv in yuv_list)
		yuv_mat = [yuv_list, mean_yuv_list, median_yuv_list]
		rgb_mat = list(list(yuv2rgb(yuv) for yuv in raw) for raw in yuv_mat)
		hist_mat = list(list(hist(rgb) for rgb in raw) for raw in rgb_mat)
		img = hstack([stack(rgb_mat), stack(hist_mat)])
		write(img, '{}/{} result.png'.format(output_dir, name))
		diff_rgb_list = [vdiff(rgb), hdiff(rgb)]
		diff_hist_list = list(hist(diff_rgb) for diff_rgb in diff_rgb_list)
		img = stack([diff_rgb_list, diff_hist_list])

		write(img, '{}/{} diff.png'.format(output_dir, name))
		print('done')


if __name__ == '__main__':
	main()
