import re
from NFA import *
from dot import dfa_to_png


def test_dfa(dfa):
    # 让该dfa生成符合其正则文法的字符串
    # 并同时由自己和python re库判断其合法性
    # 重复多次
    p = re.compile(dfa.pattern)
    check_table = dict()
    for _ in range(30):
        string = dfa.generate()
        result1 = dfa.check(string)
        result2 = bool(p.fullmatch(string))
        check_table[string] = {
            'my check': result1,
            'python re': result2
        }
    print_table(check_table)


def main():
    strings = (
        '1(0|1)*101',
        '1(1010*|1(010)*1)*0',
        'a((a|b)*|ab*a)*b',
        'b((ab)*|bb)*ab'
    )
    for string in strings:
        nfa = string_to_nfa(string)
        dfa = nfa.transfer()
        dfa = dfa.minimum()
        dfa_to_png(dfa, dfa.pattern)


if __name__ == '__main__':
    main()
