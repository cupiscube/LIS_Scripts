import psycopg2 as pg


class DBConnect:
    host = input('Введите IP адрес сервера: ')
    port = input('Введите порт базы постгрес (если порт 5433 можно пропустить нажав Enter): ')
    if port == '':
        port = 5433
    else:
        port = int(port)
    db_name = input('Введите название БД (если БД bregis_lis данный шаг можно пропустить нажав Enter): ')
    if db_name == '':
        db_name = 'SOME DB NAME'
    db_user = 'SOME BD USER'
    db_password = 'SOME PASSWORD'
    connect = pg.connect(f"host={host} port={port} dbname={db_name} user={db_user} password={db_password}")

