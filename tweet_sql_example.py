import os
import sqlite3

from twitter_API import connect_to_endpoint, search_url


def create_table(path, table):
    sql_create_table = f"""CREATE TABLE IF NOT EXISTS {table} (
                                    id integer PRIMARY KEY,
                                    texto text NOT NULL,
                                    author_id NOT NULL
                                );"""
    # Rode somente uma vez para criar a table.
    with connect_db(path) as conn:
        conn.execute(sql_create_table)
        conn.commit()
    print(f'Base criada em {path}')


def collect_basics(conn, table):
    # Note que a condição abaixo é necessária para verificar se há algum item com id na base
    sql = f"""SELECT * FROM {table} ORDER BY id DESC LIMIT 5;"""
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


def connect_db(database):
    conn = sqlite3.connect(database)
    print(f'Conexão realizada com sucesso.')
    return conn


def insere_tweet(conn, tweet):
    sql = """INSERT INTO tweets(author_id,id,texto)
              VALUES(?,?,?)"""
    cur = conn.cursor()
    # Note que 'tweet' precisa ser recebido como sequência de id, author_id e texto
    cur.executemany(sql, tweet)
    conn.commit()
    return cur.lastrowid


def check_since_id(conn, table):
    sql = f"""SELECT MAX(id) FROM {table};"""
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchone()[0]


def main(database, table, query_params):
    # Abre a conexão com SQL
    with connect_db(database) as conn:
        next_token = True
        # # Note que a condição abaixo é necessária para verificar se há algum item com id na base
        while next_token:
            # Verificando se o tweet mais recente já está na base
            max_value = check_since_id(conn, table)
            if max_value and next_token is True:
                query_params['since_id'] = max_value
            json_response = connect_to_endpoint(search_url, query_params)
            # Verificando se é necessária mais de uma conexão, ou se já é a última ou única.
            if 'next_token' in json_response['meta']:
                next_token = json_response['meta']['next_token']
                print(next_token)
                query_params['next_token'] = next_token
            else:
                next_token = False
            if 'data' in json_response:
                # Novamente. json_response['data'] é uma lista.
                # Vamos precisar dos dicionários que estão dentro da lista.
                tweets = [list(x.values()) for x in json_response['data']]
                insere_tweet(conn, tweets)


if __name__ == '__main__':
    twitter_handle = 'folha'

    query = {'query': f'(from:{twitter_handle})',
             'tweet.fields': 'author_id'}

    p = 'data'
    t = 'tweets'
    f = f'{twitter_handle}.db'
    if not os.path.exists(p):
        os.mkdir(p)

    f = os.path.join(p, f)
    if not os.path.exists(f):
        create_table(f, t)

    main(f, t, query)

    with connect_db(f) as con:
        res = collect_basics(con, t)

    for each in res:
        print(each)
