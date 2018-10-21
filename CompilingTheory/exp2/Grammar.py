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

	@debug(2)
	def get_first(self, alpha: str):
		log('当前正在计算{}的First集'.format(alpha))
		if alpha in self.firsts:
			log('\t已经计算过，直接返回')
			log()
			return self.firsts[alpha]
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
