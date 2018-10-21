from graphviz import Digraph
from DFA import DFA


def dfa_to_png(dfa: DFA, filename: str):
    dot = Digraph(format='png', engine='neato')
    dot.attr(overlap='False', sep='1.5')

    # 绘制终态节点
    dot.attr('node', shape='doublecircle')
    for end in dfa.ends:
        dot.node(str(end))

    # 绘制非终态节点及各个弧
    dot.attr('node', shape='circle')
    for prev_node, forward_map in dfa.table.items():
        for symbol, next_node in forward_map.items():
            dot.edge(str(prev_node), str(next_node), label=symbol, concentrate='True')

    # 绘制指向起点的箭头
    dot.attr('node', shape='none', height='.0', width='.0')
    dot.edge('', str(dfa.start))

    # 添加正则式并保存
    dot.attr(label=r'\n%s' % dfa.pattern)
    dot.attr(fontsize='20')
    dot.render(filename, cleanup=True)
