from functools import reduce
from typing import *
from utils import *
from DFA import DFA

NFATable = Dict[int, Dict[str, Set[int]]]


class NFA:
    def __init__(self, table: NFATable, start: int, end: int):
        self.table, self.start, self.end = table, start, end
        self.pattern = None

    @property
    def nodes(self):
        """
        获取自己的节点列表
        """
        return tuple(set(self.table).union({self.end}))

    def link(self, prev_node, symbol, next_node):
        """
        连接一条边
        """
        self.table.setdefault(prev_node, dict())
        self.table[prev_node].setdefault(symbol, set())
        self.table[prev_node][symbol].add(next_node)

    def unlink(self, prev_node, symbol, next_node):
        """
        断开一条边
        """
        self.table[prev_node][symbol].remove(next_node)
        if not len(self.table[prev_node][symbol]):
            self.table[prev_node].pop(symbol)
            if not len(self.table[prev_node]):
                self.table.pop(prev_node)

    def step(self, node: int, symbol: str):
        """
        获取给定节点经过给定符号后可以到达哪些节点
        """
        return self.__step(node, symbol)

    def __step(self, node: int, symbol: str, visited: set=None):
        rv = set() if symbol != '' else {node}
        visited = visited or rv.copy()
        if node in self.table:
            nodes = self.table[node].get(symbol, set())
            for node_ in nodes:
                if node_ not in visited:
                    visited.add(node_)
                    rv = rv.union(self.__step(node_, '', visited))
        return rv

    def epsilon_closure_of(self, node):
        """
        求某节点的epsilon闭包
        """
        return self.step(node, '')

    def show(self):
        print('Start: %d' % self.start)
        print('End: %s' % str(self.end))
        print('Table: ')
        print_table(self.table)
        print()

    @debug(0)
    def transfer(self):
        """
        转换成DFA
        """

        # step 1 生成转移表
        symbols = get_column_titles(self.table)
        if '' in symbols:
            symbols.remove('')
        queue = [self.epsilon_closure_of(self.start)]
        table = dict()
        while len(queue):
            current = tuple(queue.pop(0))
            if current not in table:
                log(current)
                table.setdefault(current, dict())
                for symbol in symbols:
                    content = set()
                    for node in current:
                        content = content.union(self.step(node, symbol))
                    content = tuple(content)
                    log('\t + %s = %s' % (symbol, str(content)))
                    if content:
                        table[current][symbol] = content
                        if content not in table:
                            queue.append(content)

        # step 2 将转移表中的内容重新编号
        start = None
        ends = set()
        for i, key in enumerate(table):
            if self.start in key:
                start = i+1
            if self.end in key:
                ends.add(i+1)
            table = replaced_table(table, key, i + 1)

        rv = DFA(table, start, ends)
        rv.pattern = self.pattern
        return rv

    def be_compatible_with(self, other):
        """
        变得与另一个NFA兼容（即不使用相同的数字）
        """
        new_numbers = get_some_new_number(set(other.nodes).union(set(self.nodes)), len(self.nodes))
        replace_table = dict((a, b) for a, b in zip(self.nodes, new_numbers))
        self.replace_numbers(replace_table)

    def update_numbers(self):
        """
        将自己的节点重新编号
        """
        new_numbers = get_some_new_number([], len(self.nodes))
        replace_table = dict((a, b) for a, b in zip(self.nodes, new_numbers))
        self.replace_numbers(replace_table)

    def __add__(self, other):
        """
        NFA的加运算符
        """
        x, y = self.copy(), other.copy()
        y.be_compatible_with(x)
        x.link(x.end, '', y.start)
        x.table.update(y.table)
        x.end = y.end
        x.update_numbers()
        x.pattern += y.pattern
        return x

    def __or__(self, other):
        """
        NFA的或运算符
        """
        x, y = self.copy(), other.copy()
        y.be_compatible_with(x)
        start, end = get_some_new_number(set(x.nodes).union(set(y.nodes)), 2)
        table = x.table
        table.update(y.table)
        rv = NFA(table, start, end)
        rv.link(start, '', x.start)
        rv.link(start, '', y.start)
        rv.link(x.end, '', end)
        rv.link(y.end, '', end)
        rv.update_numbers()
        rv.pattern = '%s|%s' % (x.pattern, y.pattern)
        return rv

    def closure(self):
        """
        NFA的闭包运算符
        """
        rv = self.copy()
        new_numbers = get_some_new_number((1, 2), len(rv.nodes))
        replace_table = dict((o, n) for o, n in zip(rv.nodes, new_numbers))
        rv.replace_numbers(replace_table)
        start, end = 1, 2
        rv.link(rv.end, '', end)
        rv.link(start, '', rv.start)
        rv.link(rv.end, '', rv.start)
        rv.link(start, '', end)
        rv.start, rv.end = start, end
        pattern = self.pattern
        if len(pattern) > 1:
            pattern = '(%s)' % pattern
        pattern = '%s*' % pattern
        rv.pattern = pattern
        return rv

    def replace_numbers(self, replace_table):
        """
        根据替换表替换替换自己所用到的数字
        """
        blacklist = set(replace_table).union(set(replace_table.values()))
        new_numbers = get_some_new_number(blacklist, len(replace_table))
        replace_table1 = dict((a, b) for a, b in zip(replace_table, new_numbers))
        replace_table2 = dict((a, b) for a, b in zip(new_numbers, replace_table.values()))
        self._replace_numbers(replace_table1)
        self._replace_numbers(replace_table2)

    def _replace_numbers(self, replace_table):
        for o, n in replace_table.items():
            self.table = replaced_set_table(self.table, o, n)
        if self.start in replace_table:
            self.start = replace_table[self.start]
        if self.end in replace_table:
            self.end = replace_table[self.end]

    def copy(self):
        rv = NFA(self.table.copy(), self.start, self.end)
        rv.pattern = self.pattern
        return rv


def string_to_nfa(string):
    """
    根据正则式生成NFA
    """
    # 合法性检查
    if not is_brackets_matched(string):
        raise ValueError('mismatched brackets')
    if any(sub in string for sub in ('(|', '|)', '|*', '**', '(*', '||')):
        raise ValueError('illegal usage of operators')

    # 去外层括号
    string = uncovered(string)

    # 先查看是否有最外层的或运算符，若有则返回递归调用值
    string = '(' + string + ')'
    indexes = []
    count = -1
    for i, c in enumerate(string):
        if c == '(':
            count += 1
        elif c == ')':
            count -= 1
        if count == 0 and c == '|':
            indexes.append(i)
    if len(indexes):
        indexes = [0] + indexes + [-1]
        parts = tuple(string[x+1:y] for x, y in zip(indexes[:-1], indexes[1:]))
        return reduce(lambda x, y: x | y, map(string_to_nfa, parts))

    string = uncovered(string)

    # 分解为不可再分的子串
    parts = list(string)
    # 先合并括号
    indexes = []
    count = 0
    for i, c in enumerate(parts):
        if c == '(':
            if count == 0:
                indexes.append(i)
            count += 1
        elif c == ')':
            count -= 1
            if count == 0:
                indexes.append(i)
    indexes = tuple(zip(indexes[::2], indexes[1::2]))
    for x, y in indexes[::-1]:
        parts[x:y+1] = [''.join(parts[x:y+1])]

    # 再合并星号
    indexes = tuple(i for i, c in enumerate(parts) if c == '*')
    indexes = tuple((i-1, i) for i in indexes)
    if len(indexes):
        for x, y in indexes[::-1]:
            parts[x:y+1] = [''.join(parts[x:y+1])]

    if len(parts) > 1:
        return reduce(lambda x, y: x + y, map(string_to_nfa, parts))

    if string[-1] == '*':
        return string_to_nfa(string[:-1]).closure()

    # （递归出口）对不包含任何运算符的正则式生成链式NFA
    string = string.replace(epsilon, '')
    start = 1
    end = len(string) + 1
    table = dict((i+1, {c: {i+2}}) for i, c in enumerate(string))
    rv = NFA(table, start, end)
    rv.pattern = string
    return rv
