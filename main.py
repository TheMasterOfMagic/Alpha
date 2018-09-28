import re
from NFA import *


def main():
    string = 'a(b|c)*'
    nfa = string_to_nfa(string)
    dfa = nfa.transfer()
    dfa = dfa.minimum()
    dfa.show()

    print('='*60)
    print()

    # 让该dfa生成符合其正则文法的字符串
    # 并同时由自己和python re库判断其合法性
    # 重复多次
    p = re.compile(string)
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


if __name__ == '__main__':
    main()
