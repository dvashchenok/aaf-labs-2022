"""
Core file
"""
import pickle
from prettytable import PrettyTable
from itertools import groupby


class Table:
    def __init__(self, name_table: str, titles: list, index=None):
        if index is None:
            index = {}
        self.name_table = name_table
        self.titles = []
        self.index = index
        for pos in range(len(titles)):
            if titles[pos] != titles[pos].upper():
                self.titles.append(titles[pos])
        self.items = []

    def __lt__(self, other):
        return self.name_table < other.name_table

    def __str__(self):
        return self.name_table

    def add_items(self, items: list):
        if len(items) != len(self.titles) and len(self.titles) > len(items):
            for num in range(len(self.titles) - len(items)):
                items.append("")
            self.items.append(items)
        elif len(self.titles) < len(items):
            self.items.append(items[:len(self.titles)])
        else:
            self.items.append(items)

    def get_titles(self):
        return self.titles

    def get_items(self):
        return self.items

    def get_name(self):
        return self.name_table

    def print(self):
        # +----+--------+----------------+
        # | id | name   | favourite_food |
        # +----+--------+----------------+
        # | 1  | Murzik | Sausages       |
        # | 2  | Pushok | Fish           |
        # +----+--------+----------------+
        if len(self.items) == 0:
            table = PrettyTable([self.name_table])
            table.add_row([" --- No items --- "])
            print(table)
            return False
        table = PrettyTable(self.titles)
        for item in self.items:
            table.add_row(item)
        print(table)


class SQL:
    def __init__(self):
        self.tables = []

    def __add__(self, table: Table):
        self.tables.append(table)
        self.tables.sort()

    def append(self, table: Table):
        self.tables.append(table)
        self.tables.sort()

    def print_tables(self):
        table = PrettyTable(["TABLES"])
        if len(self.tables) == 0:
            table.add_row([" --- No table --- "])
        else:
            for table_name in self.tables:
                table.add_row([str(table_name)])
        print(table)

    def print_table(self, title):
        for table in self.tables:
            if str(table) == title:
                table.print()
                return True
        print(f"Sorry... no table {title} :(")
        return False

    def function_print_table(self, title, vars: list, symbols: list):

        def uniq(lst):
            last = object()
            for item in lst:
                if item == last:
                    continue
                yield item
                last = item

        try:
            if len(vars) >= 2:
                # and_check = None
                # Складання до списку
                l = []
                for table in self.tables:
                    if str(table) == title:
                        l += [table.get_titles()]
                        l += table.get_items()
                        break
                pdframe = []
                for i in range(len(symbols)):
                    pdframe += [l]
                s = 0
                for num_var in range(0, len(vars), 3):
                    temp_list = []
                    try:
                        title_pos = pdframe[s][0].index(vars[num_var])
                    except ValueError:
                        pdframe.pop(s)
                        break
                    for i in pdframe[s][1:]:
                        if symbols[s] == "<=":
                            if i[title_pos] <= vars[num_var + 1]:
                                temp_list.append(i)
                        elif symbols[s] == ">=":
                            if i[title_pos] >= vars[num_var + 1]:
                                temp_list.append(i)
                        elif symbols[s] == "=" or symbols[s] == "==":
                            if i[title_pos] == vars[num_var + 1]:
                                temp_list.append(i)
                        elif symbols[s] == "<":
                            if i[title_pos] < vars[num_var + 1]:
                                temp_list.append(i)
                        elif symbols[s] == ">":
                            if i[title_pos] > vars[num_var + 1]:
                                temp_list.append(i)
                        else:
                            continue
                    pdframe[s] = temp_list
                    s += 1
                data = []
                and_check = False
                for num in range(vars.count("OR") + vars.count("AND") + 1):
                    # print(pdframe)
                    # [
                    # [['2', 'Pushok', 'Fish'], ['3', 'X', 'xxx']],
                    # [['2', 'Pushok', 'Fish']],
                    # [['2', 'Pushok', 'Fish']]
                    # ]
                    temp_data_1 = data
                    temp_data_2 = pdframe[num]
                    if and_check:
                        for global_item in temp_data_1:
                            check = True
                            for temp_items in temp_data_2:
                                if global_item not in temp_items:
                                    check = False
                            if check:
                                temp_data_2.append(global_item)
                        data = temp_data_2
                    else:
                        temp_data_2 += temp_data_1
                        data = [el for el, _ in groupby(temp_data_2)]

                    vars = vars[2:]

                    # print(f"DATA: {data}")
                    # print(vars)
                    # print(and_check)

                    # if vars.count("OR") != 0 and
                    if vars:
                        if "OR" == vars[0]:
                            and_check = False
                            vars.pop(vars.index("OR"))
                        elif "AND" == vars[0]:
                            vars.pop(vars.index("AND"))
                            and_check = True
                        else:
                            pass

                if len(data) == 0:
                    table = PrettyTable([title])
                    table.add_row([" --- No items --- "])
                    print(table)
                    return False
                table = PrettyTable(l[0])
                # print(data)
                table.add_rows(data)
                print(table)
            return False
        except ZeroDivisionError:
            print(f"Sorry... Check your input! :(")

    def get_tables(self):
        return self.tables

    def get_table(self, title):
        for table in self.tables:
            if str(table) == title:
                return table
        return False


if __name__ == '__main__':
    with open("MySQL.pickle", 'rb') as f:
        MySQL = pickle.load(f)
    MySQL.print_table("cats")
    MySQL.function_print_table("cats", ['name', 'Pushok', 'AND', 'name', 'Pushok', 'OR', 'name', 'Murzik'],
                               ['=', '=', '<'])
    MySQL.function_print_table("cats", ['name', 'Murzik', 'OR', 'name', 'Pushok', 'AND', 'name', 'Pushok'],
                               ['>', '=', '='])
    MySQL.function_print_table("cats", ['name', 'Murzik', 'OR', 'name', 'AAA'],
                               ['>', '='])
