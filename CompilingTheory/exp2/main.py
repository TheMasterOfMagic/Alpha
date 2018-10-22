from Grammar import Grammar
from CompilingTheory.utils import epsilon


def main():
	gt = dict(
		S={'MH', 'a'},
		H={'LSo', ''},
		K={'dML', ''},
		L={'eHf'},
		M={'K', 'bLM'}
	)
	g = Grammar(gt, 'S')

	g.get_firsts()
	for k, v in sorted(g.firsts.items()):
		print(k, v)
	print()

	g.get_follows()
	for k, v in sorted(g.follows.items()):
		print(k, v)
	print()

	g.get_selects()
	for k, v in sorted(g.selects.items()):
		if v:
			left, right = k
			print('{} → {}'.format(left, right or epsilon), v)


if __name__ == '__main__':
	main()
