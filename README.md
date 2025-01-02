# Sobre o projeto
Este é um simples projeto cli que te permite passar seus próprios documentos para uma IA e fazer perguntas sobre eles. Quase um pequeno [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/).

## Documentos aceitos
Os documentos aceitos são arquivos pdf ou textos passados diretamente pelo terminal.

## Modelos utilizados
Os modelos de IA utilizados são os modelos do google que em sua versão gratuita tem limites de requisições. Por isso mais de duas requisições não podem ser feitas por minuto, a não ser que se usa uma api key com plano pago vinculado.

## O chat
A aplicação não funciona no modelo de chat, o que significa que o modelo de IA llm não terá nenhum contexto das menssagens anteriores.

# Configurando o ambiente
Primeiramente, use `pip install -r requirements.txt` para instalar todas as bibliotecas necessárias, em seguida obtenha sua própria api key para acessar os modelos de IA da google, registe-a nas variáveis de ambiente do seu computador e, se necessário, corrija o nome da api key em [[configs.json]].

# Uso
Para usar rode `python ./search.py`, você entrará em um terminal personalizado quando a menssagem aparecer. A partir daí você possui três opções de comandos:

**train** "arg1" 'arg2' ... @argN: Usado para passar documentos para "treinar" o modelo de llm.
Dicas: 
    1. Use "" ou '' para evitar que seus argumentos sejam divididos pelos espaços em branco. arg1 arg2 são dois argumentos diferentes, mas "arg1 arg2" são passados como o mesmo argumento.
    2. Use @ na frente de um argumento para indicar o caminho de um arquivo. "@Arquivo PDF.pdf" indica o nome de um arquivo ignorando o espaço em branco.

**ask**: Irá abrir um sub-terminal personalizado que que permite passar qualquer menssagem, `>>> <menssagem>`. Com esta menssagem, o comando fará uma busca de similaridade no vectorDB que retornará os `k` elementos mais próximos (chunks mais próximos). O `k` pode ser alterado em [[configs.json]] `vector_store.search.k`.

**aksWithAI**: Irá funcionar praticamente idêntico ao ask, mas ao invés de apenas retornar uma consulta no vectorDB, ele passará o retorno do vectorDB para um modelo de IA llm do google, que pode ser alterado em [[configs.json]] `chat_model.name`, que tentará dar uma resposta mais humana.

# Exemplos de QA
Usando o documentos em [[./dafault_data/]], use `python ./search.py -d` se não quiser carrega-lós, você pode fazer as perguntas e obter respostas semelhantes as listadas abaixo.

**O que é refatoração?**
Refatoração (substantivo): uma modificação feita na estrutura interna do software para deixá-lo mais fácil de compreender e menos custoso para alterar, sem que seu comportamento observável seja alterado.

Refatorar (verbo): reestruturar um software por meio da aplicação de uma série de refatorações, sem alterar o seu comportamento observável.

**Por que refatorar?**
Para programar mais rápido, agregando mais valor com menos esforço.  Refatorar torna mais rápido adicionar funcionalidades e corrigir bugs.

**O que é SOLID? Em resumo!**
SOLID é um acrônimo para cinco princípios de design de código que visam criar software mais compreensível, flexível, e manutenível.  O texto enfatiza que usar SOLID resulta em código melhor, e que esses princípios ajudam a evitar código mal escrito, com milhares de linhas e muitos métodos ou funções em uma classe.

**Como funciona o modelo de processo de software espiral? Em resumo!**
O modelo espiral combina prototipação e ciclo de vida clássico, adicionando análise de riscos em cada iteração.  As quatro atividades principais de cada ciclo são: planejamento, análise de riscos, engenharia e avaliação do cliente.  A prototipação reduz riscos ao longo do desenvolvimento.