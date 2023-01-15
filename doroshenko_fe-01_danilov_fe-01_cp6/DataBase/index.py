from DataBase.Table import Table
from prettytable import PrettyTable


class DataBase:
    def __init__(self):
        self.dataBase = {}
        self.allTablesName = []

    def PrintDB(self):
        for Table in self.allTablesName:
            Tab = self.dataBase[Table]
            print(Tab.columns)
            print(Tab.indexedColumns)
            print(Tab.table)
            for key in Tab.indexes.keys():
                print(key, end=": ")
                Tab.indexes[key].PrintTree()
                print()

    def CreateTable(self, name, columns, indexes):
        if name not in self.allTablesName:
            self.allTablesName.append(name)
            self.dataBase[name] = Table(columns, indexes)
            print(f'Table "{name}" created successfully')
        else:
            raise Exception('Table with this name already exists')

    def Insert(self, name, varsToInsert):
        self.DoseTableExist(name)
        self.dataBase[name].CheckNumberOfColumns(len(varsToInsert))
        self.dataBase[name].Insert(varsToInsert)
        print('row inserted in table', name)

    def Select(self, table_name, column_where, column_equals):
        self.DoseTableExist(table_name)
        data = self.dataBase[table_name].Select(column_where, column_equals)
        print('====', table_name.upper(), '====')
        self.PrintTable(data[0], data[1])

    def DoseTableExist(self, name):
        if name not in self.allTablesName:
            raise Exception('There is no table with name', name)

    def PrintTable(self, names, rows):
        table = PrettyTable()
        table.field_names = names
        table.add_rows(rows)
        print(table)

    def Full_Join(self, table_name1, table_name2, column_1, column_2):
        if table_name1 not in self.allTablesName or table_name2 not in self.allTablesName:
            raise Exception("One or both of the specified tables do not exist in the database.")
        if column_1 not in self.dataBase[table_name1].columns or column_2 not in self.dataBase[table_name2].columns:
            raise Exception("One or both of the specified columns do not exist in the respective tables.")

        join_result = []
        column_table_1 = self.dataBase[table_name1].columns[column_1]['ID']
        column_table_2 = self.dataBase[table_name2].columns[column_2]['ID']
        for row1 in self.dataBase[table_name1].table:
            match_found = False
            for row2 in self.dataBase[table_name2].table:
                if row1[column_table_1] == row2[column_table_2]:
                    join_result.append(row1 + row2)
                    match_found = True
                    break
            if not match_found:
                join_result.append(row1 + ["" for _ in range(len(self.dataBase[table_name2].columns))])

        for row2 in self.dataBase[table_name2].table:
            match_found = False
            for row in join_result:
                if row2[column_table_2] == row[column_table_1]:
                    match_found = True
                    break
            if not match_found:
                join_result.append(["" for _ in range(len(self.dataBase[table_name1].columns))] + row2)
        columns = list(self.dataBase[table_name1].columns.keys()) + list(self.dataBase[table_name2].columns.keys())
        self.PrintTable(columns, join_result)
