from typing import Dict, Set
from CompilingTheory.utils import *

GrammarTable = Dict[str, Set[str]]


class Grammar:
	def __init__(self, grammar_table: GrammarTable, start='S'):
		if start not in grammar_table:
			raise ValueError('start Vn not found in table')
		self.table = grammar_table
		self.start = start
		self.firsts = dict()
		self.follows = dict()
		self.selects = dict()

	def show(self):
		print('Start: {}'.format(self.start))
		print('Table: ')
		for left_part, right_part_set in self.table.items():
			for right_part in right_part_set:
				print('\t{} → {}'.format(left_part, right_part or epsilon))

	@debug(0)
	def get_first(self, alpha: str):
		if alpha in self.firsts:
			return self.firsts[alpha]
		log('当前正在计算{}的First集'.format(alpha))
		self.firsts[alpha] = set()
		rv = set()
		log('{} 有以下右部: {}'.format(alpha, '(' + ', '.join(map(lambda x: x or epsilon, self.table[alpha])) + ')'))
		for right_part in self.table[alpha]:
			log('\t当前右部: {}'.format(right_part or epsilon))
			i = 0
			while True:
				head = right_part[i:i+1]
				log('\t\t当前字符: {}'.format(head or epsilon))
				if head == '' or head.islower():
					log('\t\t是终结符')
					log('\t\t故向结果中添加{}'.format((head or epsilon)))
					rv.add(head)
					break
				elif head.isupper():
					log('\t\t是非终结符')
					if head in self.firsts:
						first = self.firsts[head]
						if first:
							log('\t\t但First({})正在计算中'.format(head))
							log('\t\t忽略')
						else:
							log('\t\t而First({})={}'.format(head, first))
					else:
						log('\t\t而First({})尚未计算'.format(head))
						log('\t\t计算之'.format(head))
						log()
						first = self.get_first(head)
						log('\t\t在计算First({})的过程计算得First({})={}'.format(alpha, head, first))
					if '' in first:
						log('\t\t其中包含了空串')
						log('\t\t故将其去除空串，并入结果，并将当前右部({})里的下一个字符({})的First集并入结果'.format(right_part, right_part[i+1:i+2] or epsilon))
						rv = rv.union(first.difference({''}))
						i += 1
					else:
						log('\t\t其中不包含空串')
						log('\t\t故直接将其并入结果')
						rv = rv.union(first)
						break
				else:
					raise Exception

		log('计算结果: First({})={}'.format(alpha, rv))
		self.firsts[alpha] = rv
		log()
		return rv

	def get_firsts(self):
		for vn in self.table.keys():
			self.get_first(vn)

	@debug(0)
	def get_follow(self, alpha: str):
		if alpha in self.follows:
			return self.follows[alpha]
		log('当前正在计算{}的Follow集'.format(alpha))
		self.follows[alpha] = set()
		rv = set()
		for left_part, right_part_set in self.table.items():
			for right_part in right_part_set:
				if alpha in right_part:
					log('\t在产生式{} → {}中发现了{}'.format(left_part, right_part, alpha))
					i = right_part.index(alpha)
					while True:
						c = right_part[i+1:i+2]
						log('\t其后面一个字符是{}'.format(c or epsilon))
						if c.islower():
							log('\t\t是非空终结符')
							log('\t\t直接将其加入结果中')
							rv.add(c)
							break
						elif c == '':
							log('\t\t是空串')
							log('\t\t故将Follow({})并入结果中'.format(left_part))
							if left_part not in self.follows:
								log('\t\t而Follow({})尚未计算'.format(left_part))
								log('\t\t计算之')
								follow = self.get_follow(left_part)
							else:
								follow = self.follows[left_part]
								if not follow:
									log('\t\t而Follow({})正在计算中'.format(left_part))
									log('\t\t忽略')
							if follow:
								log('\t\tFollow({})={}，将其并入结果'.format(left_part, follow))
								rv = rv.union(follow)
							break
						elif c.isupper():
							log('\t\t是非终结符')
							first = self.get_first(c)
							log('\t\tFirst({})={}'.format(c, first))
							if '' not in first:
								log('\t\t其中没有空串')
								log('\t\t故直接将其并入结果中')
								rv = rv.union(first)
								break
							else:
								log('\t\t其中包含空串')
								log('\t\t所以将除空串以外的内容并入结果中')
								log('\t\t再对{} → {}中{}的下一个字符进行分析'.format(left_part, right_part, c))
								rv = rv.union(first.difference({''}))
								i += 1
						else:
							raise Exception
		if alpha == self.start:
			log('由于{}是开始符，故将#加入到其Follow集中'.format(alpha))
			rv.add('#')
		log('计算得Follow({})={}'.format(alpha, rv))
		self.follows[alpha] = rv
		log()
		return rv

	def get_follows(self):
		for vn in self.table.keys():
			self.get_follow(vn)

	@debug(0)
	def get_select(self, left_part: str, right_part: str):
		log('当前正在计算{} → {}的Select集'.format(left_part, right_part or epsilon))
		log('在此之前先计算First({})'.format(right_part or epsilon))
		i = 0
		first = set()
		while True:
			c = right_part[i:i+1]
			log('\t当前字符: {}'.format(c or epsilon))
			if c.islower() or c == '':
				log('\t\t是终结符')
				log('\t\t故直接将其加入到结果中')
				first.add(c)
				break
			elif c.isupper():
				log('\t\t是非终结符')
				first_c = self.firsts[c]
				log('\t\t而First({})={}'.format(c, first_c))
				if '' not in first_c:
					log('\t\t其中不包含空串')
					log('\t\t故将其并入结果中')
					first = first.union(first_c)
					break
				else:
					log('\t\t其中包含空串')
					log('\t\t所以将除空串以外的内容并入结果中')
					log('\t\t再对{} → {}中{}的下一个字符进行分析'.format(left_part, right_part, c))
					first = first.union(first_c.difference({''}))
					i += 1
			else:
				raise Exception
		log('计算得First({})={}'.format(right_part, first))
		if '' not in first:
			log('其中不包含空串')
			rv = first
			log('故Select({} → {})=First({})={}'.format(left_part, right_part, right_part, first))
		else:
			log('其中包含空串')
			rv = first.difference({''}).union(self.follows[left_part])
			log('故Select({} → {})=First({})-{}+Follow({})={}'.format(
				left_part, right_part or epsilon, right_part or epsilon, '{' + epsilon + '}', left_part, rv))
		self.selects[(left_part, right_part)] = rv
		log()
		return rv

	def get_selects(self):
		for left_part, right_part_set in self.table.items():
			for right_part in right_part_set:
				self.get_select(left_part, right_part)
