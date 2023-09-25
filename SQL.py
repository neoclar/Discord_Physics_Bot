
import sqlite3 as sql3
# Cursor
cursor = sql3.connect('messages.db')
# Функции для SQLite запросов
def execute(command, *args):
    'Function for comfort'
    with cursor:
        return cursor.execute(command, args)

def add(table='messages', user_id='1', parameter='message1', set_value='ru'):
    command_add=f'''
    INSERT OR REPLACE INTO {table} (user_id, {parameter})
    VALUES ((SELECT user_id FROM {table} WHERE user_id={user_id}), '{set_value}');
    '''
    execute(command_add)

def add_string(table='messages', user_id='1'):
    command_add=f'''
    INSERT INTO {table} (user_id)
    VALUES ({user_id});
    '''
    execute(command_add)

def delete_column(table='messages', parameter='name'):
    command_delete=f'''
    UPDATE {table}
    SET {parameter} = NULL;
    '''
    execute(command_delete)

def delete_one(table='messages', parameter='name', whom=None):
    command_delete=f'''
    UPDATE {table}
    SET {parameter} = NULL
    WHERE {parameter} = '{whom}';
    '''
    execute(command_delete)

def delete_str(table='messages', where_column=None, where_value=None):
    command_delete=f'''
    DELETE FROM {table}
    WHERE {where_column}='{where_value}';
    '''
    execute(command_delete)

def change(table='messages', parameter='message1', set_obj='ru', where_obj=None, where_value=None):
    '''Change something in table
    arguments:
    table-table to change
    parameter-which setting should be changed
    set_obj-what to change
    where_obj-filter_parameter
    where_value-filter_value'''
    command_change=f'''
    UPDATE {table}
    SET {parameter} = '{set_obj}'
    '''
    if where_obj!=None and where_value!=None:
        command_change=f'''
        UPDATE {table}
        SET {parameter} = '{set_obj}'
        WHERE {where_obj} = '{where_value}';
        '''
    else:
        command_change=f'''
        UPDATE {table}
        SET {parameter} = '{set_obj}'
        '''
     
    execute(command_change)

def get(table='messages', where_obj=None, where_value=None, tag='*'):
    '''Get informations from the table
    arguments:
    table-table to get
    where_obj-filter_parameter
    where_value-filter_value
    result requires one of functions convert_[data_type]
    '''
    cursor.row_factory = sql3.Row
    conn = cursor.cursor()
    if where_obj!=None and where_value!=None:
        command_get=f'''
        SELECT {tag}
        FROM {table}
        WHERE {where_obj} = '{where_value}';
        '''
    else:
        command_get=f'''
        SELECT {tag}
        FROM {table};
        '''      
    return conn.execute(command_get)

def convert_dict(obj_to_convert):
    'Convertation get result to dict'
    to_return = [dict(row) for row in obj_to_convert.fetchall()]
    try: return to_return[0]
    except IndexError: return {}

def convert_str(obj_to_convert):
    'Convertation get result to str'
    to_return = [list(row) for row in obj_to_convert.fetchall()]
    return to_return[0][0]

def convert_list(obj_to_convert):
    'Convertation get result to list'
    return [list[0] for list in [list(row) for row in obj_to_convert.fetchall()]]

# IF (SELECT date FROM values = '15/09/2023';)
# UPDATE "main"."values"
# SET dollar=96,1609
# WHERE date = '15/09/2023';
# ELSE INSERT INTO "main"."values"(date, euro)
# VALUES ('15/09/2023', '103,2289')
# WHERE date!='15/09/2023';


# insert or replace into Book (ID, Name, TypeID, Level, Seen) values (
#    (select ID from Book where Name = "SearchName"),
#    "SearchName",
#     4,
#     6,
#     (select Seen from Book where Name = "SearchName"));


# insert or replace into "main"."values" (date, euro)
# values((SELECT date from "main"."values" WHERE date='15/09/2023'),
# 100);

