import sqlite3

def print_table(cmd, table_name, curr, args=()):
    """
    Prints a table in a readable format
    :param: cmd [str] -- an sqlite3 command
    :param: table_name [str] -- Title to display before the table is printed
    :param: curr [sqlite3.cursor] -- cursor in the db
    :param: args [tuple] -- any optional arguments to be passed to the cmd string
    """

    # find table
    if args == ():
        curr.execute(cmd)
    else:
        curr.execute(cmd, args)
    results = curr.fetchall()
    print('{} -- {} items'.format(table_name, len(results)))

    # get column names
    column_names = []
    for record in curr.description:
        column_names.append(record[0])

    max_column_width = 0

    # find max column width
    for i, column in enumerate(column_names):
        max_column_width = max(max_column_width, len(column))
        for result in results:
            max_column_width = max(max_column_width, len(str(result[i])))


    print_headers(column_names, max_column_width)

    # print the information for each table
    for record in results:
        for item in record:
            print('|{:<{width}}'.format(item, width=max_column_width), end='')
        print('|')

    print()

    return results

def print_headers(column_names, max_column_width):
    """
    Prints the headers for the table to be printed. used as a helper function in print_table()
    :param: column_names [list] -- the names of the columns
    :param: max_column_width [int] -- the width of the columns to be printed
    """
    for c in column_names:
        print('+{}'.format('=' * max_column_width), end='')
    print('+')

    for column in column_names:
        print('|{:^{width}}'.format(column.strip(), width=max_column_width), end='')
    print('|')

    for c in column_names:
        print('+{}'.format('=' * max_column_width), end='')
    print('+')