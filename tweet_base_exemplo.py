import os
import sys

import pandas as pd

from twitter_API import connect_to_endpoint, search_url, cols_names


def main(database, path, query_params):
    next_token = True
    # Note que a condição abaixo é necessária para verificar se há algum item com id na base
    if not pd.isna(database.id.max()) and next_token is True:
        # Caso afirmativo, adicione o mais recente nos parâmetros da query
        query_params['since_id'] = database.id.max()
    # Fazendo a leitura, enquanto existir 'next_token' na resposta
    while next_token:
        # Realizar a conexão com os parâmetros já estabelecidos
        json_response = connect_to_endpoint(search_url, query_params)
        # Atualizar o valor do next_token, de acordo com a resposta
        if 'next_token' in json_response['meta']:
            next_token = json_response['meta']['next_token']
            # Conferindo a atualização realizada
            print(next_token)
            # Atualizando para a conexão que precisamos capturar a página seguinte
            query_params['next_token'] = next_token
        else:
            next_token = False
        # Atualizando o DataFrame em si.
        # 1. Sabemos que o retorno tem duas keys. A key data, que contém uma lista de dicionários, precisa ser lida.
        # 2. Uma vez lida, é adicionada à base existente
        if 'data' in json_response:
            database = database.append(base.from_dict(x for x in json_response['data']))
    # Salvamos a base
    database.to_csv(path, sep=';', index=False)
    return database


if __name__ == '__main__':
    if len(sys.argv) == 2:
        twitter_handle = sys.argv[1]
    else:
        twitter_handle = 'OGlobo_Rio'

    query = {'query': f'(from:{twitter_handle})',
             'tweet.fields': 'author_id'}

    p = '/home/furtado/Documents/Professor/IDP/PosDados/Aulas/data'
    f = f'{twitter_handle}.csv'
    if not os.path.exists(p):
        os.mkdir(p)

    f = os.path.join(p, f)

    if not os.path.exists(f):
        base = pd.DataFrame(columns=cols_names)
        base.to_csv(f, sep=';', index=False)
    else:
        base = pd.read_csv(f, sep=';')
    tweet_base = main(base, f, query)
    tweet_base.id = tweet_base.id.astype('str')
    tweet_base = tweet_base.sort_values('id', ascending=False)
    print(tweet_base.head())
