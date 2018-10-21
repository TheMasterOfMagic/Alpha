DEBUG = 0
epsilon = 'ϵ'


def debug(_debug):
    """
    装饰器，配合log函数使用
    根据参数改变全局变量DEBUG的值
    """
    def outer_wrapper(func):
        def wrapper(*args, **kwargs):
            global DEBUG
            DEBUG += _debug
            rv = func(*args, **kwargs)
            DEBUG -= _debug
            return rv
        return wrapper
    return outer_wrapper


def log(*args, **kwargs):
    """
    配合debug装饰器使用
    根据全局变量DEBUG的值决定是否进行输出
    """
    if DEBUG:
        print('\t' * DEBUG, end='')
        print(*args, **kwargs)


def get_column_titles(table):
    """
    获取表格的列标题
    """
    column_titles = set()
    for raw_title, raw in table.items():
        column_titles = column_titles.union(raw)
    return sorted(column_titles)


def print_table(table):
    """
    以稍微比较美观的方式打印一个二维字典
    """
    raw_titles = table.keys()
    column_titles = get_column_titles(table)
    if '' in column_titles:
        column_titles.remove('')
        column_titles.append(epsilon)
    # 统计每一列的宽度
    width_list = [max(len(str(raw_title)) for raw_title in raw_titles or [''])]
    for symbol in column_titles:
        max_width = max(len(str(table[raw_title].get(symbol, '') or '')) for raw_title in raw_titles)
        max_width = max(max_width, len(symbol))
        width_list.append(max_width)
    sep = ' | '
    # 打印第一行，即列标题
    print(sep.join(('{0: <%d}' % width).format(column_title)
                   for width, column_title in zip(width_list, ['\\'] + column_titles)))
    if epsilon in column_titles:
        column_titles.remove(epsilon)
        column_titles.append('')
    # 打印第二行
    print(sep.join(('{0: <%d}' % width).format('-'*width)
                   for width in width_list))
    # 打印剩下各行
    for raw_title in raw_titles:
        contents = (raw_title,) + tuple(table[raw_title].get(symbol, '') or '' for symbol in column_titles)
        print(sep.join(('{0: <%d}' % width).format(str(content)) for width, content in zip(width_list, contents)))


def replaced_table(table, old_content, new_content):
    """
    替换表格中的某个值，范围包括行标题和中间格
    """
    rv = table.copy()
    if old_content in rv:
        rv[new_content] = rv.pop(old_content)
    for raw_title, raw in rv.copy().items():
        raw = raw.copy()
        for column_title, content in raw.items():
            if content == old_content:
                raw[column_title] = new_content
            rv[raw_title] = raw
    return rv


def replaced_set_table(table, old_content, new_content):
    """
    替换表格中的某个值，范围包括行标题和中间格（其中中间格的值类型是被替换值的集合）
    """
    rv = table.copy()
    if old_content in rv:
        rv[new_content] = rv.pop(old_content)
    for raw_title, raw in rv.copy().items():
        raw = raw.copy()
        for column_title, content_set in raw.items():
            content_set = content_set.copy()
            if old_content in content_set:
                content_set.remove(old_content)
                content_set.add(new_content)
                raw[column_title] = content_set
            rv[raw_title] = raw
    return rv


def reversed_dict(d: dict):
    """
    反转字典。以值为键，以键的集合为值
    """
    rv = dict()
    for key, value in d.items():
        rv.setdefault(value, set())
        rv[value].add(key)
    return rv


def is_brackets_matched(string):
    """
    检查字符串中的括号是否匹配
    """
    brackets = ''.join(c for c in string if c in '()')
    while len(brackets):
        if '()' not in brackets:
            rv = False
            break
        brackets = brackets.replace('()', '')
    else:
        rv = True
    return rv


def uncovered(string):
    """
    去掉最外层的括号
    """
    next_string = string
    while is_brackets_matched(next_string):
        string = next_string
        if not (next_string and next_string[0] == '(' and next_string[-1] == ')'):
            break
        next_string = next_string[1:-1]
    return string


def get_some_new_number(blacklist, n, start=1):
    """
    获取n个不在黑名单中的数字
    """
    blacklist = set(blacklist)
    rv = []
    i = start
    while len(rv) < n:
        if i not in blacklist:
            rv.append(i)
        i += 1
    rv = tuple(rv)
    return rv
