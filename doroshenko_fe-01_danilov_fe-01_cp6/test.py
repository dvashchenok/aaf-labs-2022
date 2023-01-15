from run import run


def test(command):
    tokens, error = run(command)


command_create = 'CREATE cats (cat_id, cat_owner_id, cat_name);'
command_insert1 = 'INSERT INTO cats ("5", "Kolya3", "12");'
command_insert2 = 'INSERT INTO cats ("6", "Kolya4", "32");'
command_insert3 = 'INSERT INTO cats ("7", "Kolya98", "43");'
command_insert4 = 'INSERT INTO cats ("8", "Kolya6", "45");'
command_select = "SELECT FROM cats;"
command_where = 'SELECT FROM cats WHERE cat_name = "12";'

command2 = 'CREATE owners (owner_id, lol);'
command3 = 'INSERT INTO owners ("Kolya", "hah");'
command4 = 'INSERT INTO owners ("Kolya1", "hah");'
command5 = 'INSERT INTO owners ("Kolya3", "546");'
command6 = 'INSERT INTO owners ("Kolya98", "765");'

command_full_join = "SELECT FROM owners FULL_JOIN cats ON owner_id = cat_owner_id;"
command_full_join2 = "SELECT FROM cats FULL_JOIN owners ON cat_owner_id = owner_id;"

test(command_create)
test(command_insert1)
test(command_insert2)
test(command_insert3)
test(command_insert4)
test(command_select)
test(command_where)
test(command2)
test(command3)
test(command4)
test(command5)
test(command6)
test(command_full_join)
