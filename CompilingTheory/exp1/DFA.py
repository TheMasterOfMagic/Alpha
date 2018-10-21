from typing import *
from CompilingTheory.utils import *

DFATable = Dict[int, Dict[str, int]]


class DFA:
    def __init__(self, table: DFATable, start: int, ends: Set[int]):
        self.table, self.start, self.ends = table, start, ends
        self.__is_minimal = False  # 是否是最小化过的DFA（对于非最小化的DFA不支持调用其check函数和generate函数）
        self.pattern = None

    def step(self, node: int, symbol: str):
        """
        查询从给定节点经过给定符号将达到哪个节点
        """
        return self.table[node].get(symbol, None)

    def show(self):
        print('Start: %d' % self.start)
        print('Ends: %s' % str(self.ends))
        print('Table: ')
        print_table(self.table)
        print()

    @debug(0)
    def minimum(self):
        """
        最小化
        """
        # step 1 划分出终态集与非终态集
        parts = tuple(self.ends), tuple(set(self.table).difference(self.ends))
        node_to_part = dict()
        for part in parts:
            for node in part:
                node_to_part[node] = part

        # step 2 进行分割
        symbols = get_column_titles(self.table)
        one_more_time = True
        while one_more_time:
            one_more_time = False
            for symbol in symbols:
                log('开始用符号%s对各部分进行分割' % symbol)
                log('待分割的部分有: %s' % str(parts))
                new_parts = []
                for part in parts:
                    log('\t当前待分割部分: %s' % str(part))
                    if len(part) == 1:
                        log('\t\t(忽略)')
                        new_parts += [part]
                    else:
                        node_to_result = dict((node, self.step(node, symbol)) for node in part)
                        result_to_node = reversed_dict(node_to_result)
                        split_result = tuple(result_to_node.values())
                        log('\t\t分割结果: %s' % str(split_result))
                        new_parts += list(split_result)
                        if not one_more_time and len(split_result) > 1:
                            log('\t\t由于发生了实质性分割，所以稍后需再用各符号对各部分进行分割')
                            one_more_time = True
                parts = tuple(map(tuple, new_parts))
        log('分割结束')
        log('最终分割结果: %s' % str(parts))

        # step 3 根据分割结果制作新转移表
        node_to_part = dict()
        for part in parts:
            for node in part:
                node_to_part[node] = part
        table = dict()
        for node, next_map in self.table.copy().items():
            part = node_to_part[node]
            new_map = dict((symbol, node_to_part[next_node]) for symbol, next_node in next_map.items())
            if part in table:
                assert table[part] == new_map
            else:
                table[part] = new_map

        # step 4 重新编号
        start = None
        ends = set()
        for i, key in enumerate(table):
            if self.start in key:
                start = i+1
            if any(end in key for end in self.ends):
                ends.add(i+1)
            table = replaced_table(table, key, i + 1)

        rv = DFA(table, start, ends)
        rv.__is_minimal = True
        rv.pattern = self.pattern
        return rv

    def check(self, string):
        """
        使用该DFA检测一个字符串是否符合其正则文法
        """
        assert self.__is_minimal
        current = self.start
        while len(string):
            c, string = string[0], string[1:]
            current = self.step(current, c)
            if current is None:
                rv = False
                break
        else:
            rv = current in self.ends
        return rv

    def generate(self, p=0.3):
        """
        使用该DFA生成一个符合其正则文法的字符串
        参数p为当转移至某终态时终止移动的概率
        """
        from random import choice, random
        assert self.__is_minimal
        rv = []
        current = self.start
        while True:
            if current in self.ends and random() <= p:
                break
            if not len(self.table[current]):
                break
            symbol = choice(tuple(self.table[current]))
            rv.append(symbol)
            current = self.step(current, symbol)
        rv = ''.join(rv)
        return rv
