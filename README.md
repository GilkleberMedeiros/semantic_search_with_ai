# Sobre o projeto
Este é um simples projeto cli que te permite passar seus próprios documentos para uma IA e fazer perguntas sobre eles. Quase um pequeno [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/).

## Documentos aceitos
Os documentos aceitos são arquivos pdf ou textos passados diretamente pelo terminal.

## Modelos utilizados
Os modelos de IA utilizados são os modelos do google que em sua versão gratuita tem limites de requisições. Por isso mais de duas requisições não podem ser feitas por minuto, a não ser que se usa uma api key com plano pago vinculado.

# Configurando o ambiente
Primeiramente, use `pip install -r requirements.txt` para instalar todas as bibliotecas necessárias, em seguida obtenha sua própria api key para acessar os modelos de IA da google, registe-a nas variáveis de ambiente do seu computador e, se necessário, corrija o nome da api key em [[configs.json]].

# Uso
Para usar rode `python ./search.py`, você entrará em um terminal personalizado quando a menssagem aparecer. A partir daí você possui três opções de comandos:

**train** "arg1" 'arg2' ... @argN: Usado para passar documentos para "treinar" o modelo de chat.
Dicas: 
    1. Use "" ou '' para evitar que seus argumentos sejam divididos pelos espaços em branco. arg1 arg2 são dois argumentos diferentes, mas "arg1 arg2" são passados como o mesmo argumento.
    2. Use @ na frente de um argumento para indicar o caminho de um arquivo. "@Arquivo PDF.pdf" indica o nome de um arquivo ignorando o espaço em branco.

**ask**: Irá abrir um sub-terminal personalizado que que permite passar qualquer menssagem, `>>> <menssagem>`. Com esta menssagem, o comando fará uma busca de similaridade no vectorDB que retornará os `k` elementos mais próximos (chunks mais próximos). O `k` pode ser alterado em [[configs.json]] `vector_store.search.k`.

**aksWithAI**: Irá funcionar praticamente idêntico ao ask, mas ao invés de apenas retornar uma consulta no vectorDB, ele passará o retorno do vectorDB para um modelo de IA llm do google, que pode ser alterado em [[configs.json]] `chat_model.name`, que tentará dar uma resposta mais humana.

# Exemplos de QA
