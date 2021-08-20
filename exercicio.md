# Exercício para avaliação

### Individual ou em grupos até 3 estudantes

# Objetivo geral: capturar informações referentes a patentes nos Estados Unidos. 
1. Salvar base de dados em vários formatos ('persistência'). 
2. Fazer *upload* ('post') do código para a internet.
3. Apresentar relatório geral do quantitativo de patentes ano a ano ('tratamento')
4. (Opcional) Desenvolver boas práticas de código entregando um ('script' e 'git')
5. Entrega: envio para o e-mail do professor: furtadobb @ gmail.com
   1. Link da página `pastebin` com o código utilizado para o exercício e o JSON salvo
      1. Alternativamente, link do repositório público no GitHub
   2. Relatório contendo:
      1. Número total de arquivos zip contendo os textos das patentes no período 1997-2015
      2. Número de arquivos por ano.
6. (Opcional) Gráfico
7. (Opcional) Código para dar download e unzip os arquivos 
8. (Opcional) Como o resultado é pouco informativo, utilize a expressão abaixo, dentro de 
um loop pelas keys do dicionário, loop link a link, identifique o tamanho do arquivo e some ao total 
de dados para aquele ano. 

       with urllib.request.urlopen(link) as handler:
           output_size[key] += int(handler.getheader('Content-Length'))

## Sugestão de procedimentos

1. Importe as bibliotecas necessárias `requests` e `BeautifulSoup` from `bs4`
2. Utilize a página de referência: 'https://www.google.com/googlebooks/uspto-patents-grants-text.html'
3. Examine no *browser* a página de referência
4. Utilize a função `get` da biblioteca `requests` para capturar os dados da página
5. Utilize a biblioteca `BeautifulSoup` para interpretar ('parse') o `content` da página.
   1. Dica: utilize o intérprete `'html5lib'`
6. Sobre o resultado interpretado (`soup`) busque por todas (`find_all`) as seções do tipo `a`, 
utilizando a opção do atributo `href=True`: `find_all('a', href=True)`
7. Faça um *loop* na lista de links encontrada mantendo apenas os links que contém a expressão `'href'`
   1. Dica: use `if 'http' in elemento_do_loop`
8. Com outro *loop*, limpe o resultado para conter apenas os links para os arquivos do tipo `*.zip` que 
contenham o texto `grant_full_text`
9. Há várias maneiras de separar a lista por anos.
   1. Uma possibilidade:
      1. Use: `from collections import defaultdict`
      2. Crie um dicionário do tipo `my_dict = defaultdict(list)`
         1. Assim, será possível adicionar elementos em uma lista, para cada **ano** (chave do dicionário)
         2. Faça um loop que vai de 1976 a 2016
            1. Dentro desse loop, faça outro loop que passa por todos os links da lista
               1. Teste se o ano está presente no elemento do loop
                  1. Caso verdadeiro, adicione ao seu dicionário, com a chave do ano o elemento
         3. Algo assim (*pseudocodigo*)
            1. Cria dicionário
            2. Para o ano entre os anos de 1976 a 2015 inclusive,
               1. Para o link dentro da lista que contém todos os links
                  1. Se o ano estiver contido no link
                     1. Então, adicione ao dicionário, utilizando a chave ano
                     2. `my_dic[ano].append(link)`
   2. Imprime o tamanho da lista de cada ano para saber o número de links daquele ano
10. Salve o dicionário em `pickle`
11. Transforme o dicionário em JSON e salve em JSON
