from Grammar import Grammar


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


if __name__ == '__main__':
	main()
