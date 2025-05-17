# -*- coding: utf-8 -*-
"""
Chatbot para auxiliar com informações sobre o Componente Especializado
da Assistência Farmacêutica de Tatuí, com integração Gemini.

Este script implementa um chatbot de linha de comando que:
- Fornece respostas pré-definidas para perguntas frequentes sobre a
  Assistência Farmacêutica de Tatuí.
- Utiliza a API do Google Gemini para responder a perguntas mais abertas
  ou que não estão no escopo das respostas pré-definidas.
- Apresenta um menu de opções para guiar o usuário.
"""

# Importações necessárias
# Instala a biblioteca do Google Generative AI caso não esteja presente
!pip install -q google-genai
import os
from google.colab import userdata # Para buscar a API Key no ambiente Colab
from google import genai
from google.genai import types # Tipos específicos da API Gemini

# Configuração da API Key do Google
# Busca a chave da API armazenada nos 'secrets' do Google Colab
os.environ['GOOGLE_API_KEY'] = userdata.get('GOOGLE_API_KEY')

# Inicialização do cliente Gemini
# Cria uma instância do cliente da API Gemini
client = None
# gemini_model_instance = None # Esta variável não é mais necessária para iniciar o chat dessa forma
chat_session = None
MODEL_ID = "gemini-2.0-flash" # Modelo Gemini a ser utilizado, conforme solicitado.

try:
    # Tenta inicializar o cliente
    # Use genai diretamente, como você importou no código completo
    client = genai.Client() # Mantendo genai_google conforme seu código original

    # Cria a sessão de chat diretamente usando client.chats.create
    # O objeto retornado por client.chats.create JÁ É a sessão de chat
    chat_session = client.chats.create(model=MODEL_ID) # <-- CORREÇÃO AQUI: Atribui o resultado diretamente a chat_session

    print(f"🤖 Cliente Gemini inicializado com o modelo: {MODEL_ID} e sessão de chat criada.")
except Exception as e:
    print(f"⚠️ Erro ao inicializar o modelo Gemini ou criar sessão de chat: {e}")
    print("O chatbot poderá ter funcionalidades limitadas (apenas respostas pré-definidas).")
    chat_session = None # Garante que chat_session existe mesmo em caso de falha

# --- Respostas Pré-definidas Específicas de Tatuí ---
# Dicionário contendo respostas para perguntas frequentes e específicas
# sobre a Assistência Farmacêutica de Tatuí.
respostas_fixas_tatui = {
    "Olá": "Olá! Bem-vindo ao Chatbot da Assistência Farmacêutica de Tatuí. Estou aqui para te ajudar com suas dúvidas sobre a documentação para solicitação de medicamentos de alto custo.",
    "sair": "Obrigado pelo contato! Se precisar, estou à disposição.",
    "Tenho dúvidas sobre a documentação.": "Para te ajudar com a documentação, preciso saber se você está fazendo uma nova solicitação ou renovando uma solicitação existente. Você pode escolher 'Nova Solicitação' ou 'Renovação'.",
    "Nova solicitação.": """Para você dar entrada no pedido do seu medicamento pela primeira vez, você vai precisar de alguns documentos. Preste bastante atenção para não esquecer de nada, assim você não perde a viagem!

**Primeiro, você vai precisar do Laudo Médico (nós chamamos ele de LME).**
* Ele precisa ser o original, preenchido todinho e com a letra bem legível pelo médico que te acompanha.
* É muito importante que ele tenha sido feito nos últimos 90 dias, viu? Olhe bem a data!
* Se você quiser ver um modelo desse laudo, é só clicar neste link: https://portal.saude.sp.gov.br/resources/ses/perfil/gestor/assistencia-farmaceutica/medicamentos-do-componente-especializado-da-assistencia-farmaceutica/lme.pdf

**Depois, você vai precisar da Receita do seu médico (a prescrição).**
* Ela também precisa ser a original e ter **duas vias** (uma fica com a gente, outra é pra você).
* Atenção! Ela precisa estar completinha e com a letra fácil de ler.
* Na receita, tem que ter:
    * Seu nome completo.
    * O nome e o número do registro do seu médico (CRM ou outro). Tem que ter a assinatura e o carimbo dele também!
    * O nome e o endereço do lugar onde você foi atendido (o posto de saúde, o hospital, etc.).
    * **Muito importante!** O nome do medicamento tem que ser o nome do **PRINCÍPIO ATIVO** (aquele nome mais complicado, não pode ser o nome fantasia/comercial).
    * A quantidade que você usa do medicamento por dia (ou por dose, se for o caso) tem que ser igualzinha à que está pedindo no Laudo Médico (LME). Fique de olho nisso!
* E fique atento à validade da receita: ela só vale por **30 dias**!
* Se o seu medicamento for controlado (aqueles que precisam de receita especial), você vai ter que trazer uma receita nova todo mês, na hora de pegar o medicamento.

**Você também vai precisar de cópias de alguns documentos seus:**
* Um documento de identidade que valha (RG, Carteira de Motorista...). Ele precisa ter o número do seu CPF, viu?
* Um comprovante de que você mora aqui (conta de luz, água, telefone...). Ele tem que estar no seu nome e ter o CEP da sua rua. Se não estiver no seu nome, não se preocupe! Você pode trazer uma declaração de residência ou outro documento que mostre que você mora com a pessoa que está no comprovante.
* O seu Cartão Nacional de Saúde (CNS).

**Se a pessoa que vai receber o medicamento for menor de idade ou for legalmente incapaz, também vamos precisar:**
* Da cópia do documento de identidade (com CPF) da mãe ou de quem é o responsável legal.
* Da cópia do Cartão Nacional de Saúde (CNS) da mãe ou do responsável legal também.
* Se você tem dúvidas sobre o que seria considerado incapaz, podemos te explicar.

**E atenção!** Só você ou o seu responsável legal podem vir retirar o medicamento. Se você quiser que outra pessoa retire, você precisa pegar uma Declaração na Assistência Farmacêutica, preencher, assinar e trazer cópias dos documentos de identidade (com CPF) das pessoas que você quer autorizar, **no dia em que for retirar o medicamento**. Você pode pegar o modelo dessa declaração aqui: https://saude.sp.gov.br/resources/ses/perfil/gestor/assistencia-farmaceutica/medicamentos-do-componente-especializado-da-assistencia-farmaceutica/modelo_de_declaracao_autorizadora_v1.pdf

Ufa! Parece muita coisa, mas juntando tudo com atenção, não tem erro! Se ficou alguma dúvida sobre algum documento, é só perguntar!
""",
    "Renovação.": """Para que tudo continue certinho, você vai precisar de alguns documentos. Vamos dar uma olhadinha neles para garantir que não falte nada, ok?

**Para renovar, você vai precisar:**
* Do Laudo de Solicitação, Avaliação e Autorização de Medicamentos do Componente Especializado da Assistência Farmacêutica (LME) original. Ele precisa estar completinho, sem rasuras, e com a letra bem legível, viu? E não se esqueça de verificar a data, ele vale por 90 dias a partir do preenchimento.
* Da Receita do seu médico (a prescrição) original, em duas vias. Uma via fica aqui com a gente, e a outra é sua. A receita também precisa estar completa, legível e deve conter:
    * Seu nome completo, para não haver dúvidas.
    * A identificação do médico que fez a receita, com o nome, número do registro no Conselho Regional (CRM ou outro), assinatura e carimbo.
    * O nome e o endereço do local onde você foi atendido.
    * O nome do medicamento, e aqui é superimportante que seja o **princípio ativo**, aquele nome mais "complicadinho", e não o nome de marca, combinado?
    * A quantidade que você usa do medicamento, que deve ser igualzinha à que está no Laudo Médico (LME).
* Lembre-se que a receita tem validade de 30 dias, então fique de olho na data! Se o seu medicamento for controlado, você vai precisar trazer uma receita nova a cada vez que vier retirar.
* Cópia dos seus documentos pessoais:
    * Um documento de identidade válido, como RG ou Carteira de Motorista, com o número do seu CPF.
    * Um comprovante de residência atualizado, com o CEP, e de preferência no seu nome. Se não for possível, pode ser no nome de outra pessoa, mas aí você precisa trazer algo que mostre que você mora com ela, como uma declaração de residência.

**Atenção:** Para renovar, você **não** precisa trazer a cópia do Cartão Nacional de Saúde (CNS), ok?

**Sobre os exames:** Pode ser que os exames necessários para renovar o medicamento sejam diferentes dos da primeira vez. Para saber direitinho quais você precisa, consulte a Assistência Farmacêutica ou converse com seu médico, tá bem?

**Se quem for retirar o medicamento for menor de idade ou tiver alguma dificuldade legal para decidir,** também vamos precisar:
* Da cópia do documento de identidade (com CPF) da mãe ou de quem for o responsável legal.
* Da cópia do Cartão Nacional de Saúde (CNS) da mãe ou do responsável legal.
* Se você tiver alguma dúvida sobre o que significa ser legalmente incapaz, podemos te explicar.

**E lembre-se:** O medicamento só pode ser retirado por você ou pelo seu responsável legal. Se você quiser que outra pessoa retire, precisa pegar uma Declaração na Assistência Farmacêutica, preencher, assinar e trazer cópias dos documentos de identidade (com CPF) das pessoas que você quer autorizar, e isso deve ser feito no dia em que a pessoa vier retirar o medicamento, certo? O modelo da declaração está disponível aqui: https://saude.sp.gov.br/resources/ses/perfil/gestor/assistencia-farmaceutica/medicamentos-do-componente-especializado-da-assistencia-farmaceutica/modelo_de_declaracao_autorizadora_v1.pdf

Junte todos os documentos com cuidado, e se pintar qualquer dúvida, pode perguntar, combinado? Estamos aqui para ajudar!
""",
    "O que significa ser legalmente incapaz?": """Entendemos que esse termo pode gerar dúvidas. Uma pessoa é considerada legalmente incapaz quando ela não tem plena capacidade de exercer seus direitos e deveres civis, precisando de representação ou assistência para realizar alguns atos da vida civil. Os casos mais comuns são:

* **Menores de 16 anos:** São considerados absolutamente incapazes, precisando ser representados pelos pais ou responsáveis legais em todos os atos.
* **Pessoas com enfermidade ou deficiência mental:** Aquelas que, por causa de alguma condição de saúde, não conseguem entender o que estão fazendo ou decidindo.
* **Pessoas que, mesmo por causa transitória, não podem exprimir sua vontade:** Isso pode acontecer em situações como coma ou uso de medicamentos que alterem a consciência.

Se você tiver alguma dúvida se você ou alguém que você conhece se enquadra em alguma dessas situações, procure a Assistência Farmacêutica ou um profissional da área da saúde ou do direito para obter mais informações e orientações.""",
    "Qual o horário de funcionamento e contato da Assistência Farmacêutica?": """A Assistência Farmacêutica de Tatuí está localizada na Avenida Sales Gomes, número 163, no bairro Dr. Laurindo. O horário de funcionamento é de segunda a sexta-feira, das 8h às 16h. O telefone de contato é: (15) 3251-1999. Se precisar, a forma mais garantida de obter informações é comparecendo pessoalmente à Assistência Farmacêutica, pois em alguns dias o movimento por telefone é muito grande e pode ser difícil conseguir falar na primeira tentativa.""",
    "O medicamento que preciso está disponível no programa?": """Para saber se o medicamento que você precisa está disponível no programa, você pode ir pessoalmente à Assistência Farmacêutica ou consultar as listas online.
A Assistência Farmacêutica de Tatuí está localizada na Avenida Sales Gomes, número 163, no bairro Dr. Laurindo. O horário de funcionamento é de segunda a sexta-feira, das 8h às 16h.
Você também pode consultar as listas de medicamentos disponíveis nos seguintes links (nível estadual):
    * Consulta por MEDICAMENTO (fornecidos de acordo com PCDTs do Ministério da Saúde): https://www.saude.sp.gov.br/ses/perfil/gestor/assistencia-farmaceutica/medicamentos-dos-componentes-da-assistencia-farmaceutica/links-do-componente-especializado-da-assistencia-farmaceutica/relacao-estadual-de-medicamentos-do-componente-especializado-da-assistencia-farmaceutica/consulta-por-medicamento
    * Lista de Medicamentos para Tratamento de Glaucoma (de acordo com PCDTs do Ministério da Saúde): https://saude.sp.gov.br/ses/perfil/gestor/assistencia-farmaceutica/medicamentos-dos-componentes-da-assistencia-farmaceutica/links-do-componente-especializado-da-assistencia-farmaceutica/consulta-por-medicamento/medicamentos-para-tratamento-de-glaucoma
    * Consulta por MEDICAMENTO (fornecidos de acordo com PCDTs da Secretaria de Saúde do Estado de São Paulo): https://www.saude.sp.gov.br/ses/perfil/gestor/assistencia-farmaceutica/links-dos-medicamentos-dos-protocolos-e-normas-tecnicas-estaduais/medicamento
Se precisar de ajuda para consultar as listas ou tiver qualquer outra dúvida, é só perguntar!""",
    "Minha receita está correta?": """Para que sua receita esteja correta, ela precisa conter as seguintes informações:
* Seu nome completo;
* Nome e número de registro do seu médico (CRM ou outro);
* Assinatura e carimbo do seu médico;
* Nome e endereço do local onde você foi atendido (posto de saúde, hospital, etc.);
* Nome do princípio ativo do medicamento (não pode ser o nome fantasia/comercial);
* Quantidade do medicamento por dia (ou por dose, se for o caso), equivalente à quantidade solicitada no Laudo Médico (LME).
Além disso, a receita deve ser original, ter duas vias e estar com a letra legível. A validade da receita é de 30 dias. Em caso de medicamentos controlados, você precisará apresentar uma receita nova a cada retirada.""",
    "Como posso acompanhar meu pedido?": "Para acompanhar o andamento do seu pedido, você deve ir pessoalmente à Assistência Farmacêutica de Tatuí, localizada na Avenida Sales Gomes, número 163, no bairro Dr. Laurindo. Ao comparecer à Assistência Farmacêutica, tenha em mãos o seu protocolo para facilitar a consulta. Os atendentes poderão te informar sobre o status do seu pedido."
}

# Garante que as chaves duplicadas para reutilização de respostas estejam corretamente populadas.
# Isso permite usar `.get()` de forma mais robusta e evita `KeyError` se a chave principal for alterada.
respostas_fixas_tatui["Quais são os documentos necessários para dar entrada no pedido do medicamento pela primeira vez?"] = respostas_fixas_tatui.get("Nova solicitação.", "Informação sobre nova solicitação não encontrada.")
respostas_fixas_tatui["Quais são os documentos necessários para renovar o pedido do medicamento?"] = respostas_fixas_tatui.get("Renovação.", "Informação sobre renovação não encontrada.")


# URLs prioritárias para busca (nível estadual)
# Estas URLs podem ser usadas para complementar informações locais ou
# para buscas mais amplas sobre medicamentos e protocolos estaduais.
SITES_PRIORITARIOS_ESTADUAIS = [
    "https://saude.sp.gov.br/ses/perfil/gestor/assistencia-farmaceutica/medicamentos-dos-componentes-da-assistencia-farmaceutica/links-do-componente-especializado-da-assistencia-farmaceutica/consulta-por-medicamento/medicamentos-para-tratamento-de-glaucoma",
    "https://www.saude.sp.gov.br/ses/perfil/gestor/assistencia-farmaceutica/medicamentos-dos-componentes-da-assistencia-farmaceutica/links-do-componente-especializado-da-assistencia-farmaceutica/relacao-estadual-de-medicamentos-do-componente-especializado-da-assistencia-farmaceutica/consulta-por-medicamento",
    "https://www.saude.sp.gov.br/ses/perfil/gestor/assistencia-farmaceutica/links-dos-medicamentos-dos-protocolos-e-normas-tecnicas-estaduais/medicamento"
]

# --- Funções do Chatbot ---

def obter_resposta_gemini(pergunta_usuario):
    """
    Envia a pergunta para o modelo Gemini através da sessão de chat e retorna a resposta.

    Args:
        pergunta_usuario (str): A pergunta feita pelo usuário.

    Returns:
        str: A resposta gerada pelo modelo Gemini, ou uma mensagem de erro/aviso.
    """
    if not chat_session:
        return "Desculpe, a sessão de chat com o Gemini não está ativa. Funcionalidade limitada."

    # Prompt contextualizando o Gemini para atuar como assistente da Assistência Farmacêutica de Tatuí.
    # Este prompt é enviado junto com cada pergunta do usuário para manter o contexto da conversa.
    # Para este exemplo, vamos manter um prompt mais direto na pergunta.

    prompt_completo = f"""
    Você é um assistente virtual especializado na Assistência Farmacêutica do Componente Especializado (Alto Custo) de Tatuí, São Paulo.
    Sua principal função é fornecer informações claras e precisas sobre documentação, medicamentos disponíveis, horários e processos relacionados a ESTE SERVIÇO EM TATUÍ.
    Seja cordial e prestativo.
    Se a pergunta for sobre um tema claramente fora do escopo da assistência farmacêutica de Tatuí (ex: política nacional, outros municípios),
    informe educadamente que você só pode ajudar com questões relacionadas ao serviço de Tatuí.
    Priorize informações oficiais.

    Pergunta do Usuário: "{pergunta_usuario}"

    Por favor, forneça uma resposta útil e concisa.
    """
    try:
        # Envia a mensagem para a sessão de chat ativa
        response = chat_session.send_message(prompt_completo)
        return response.text # Retorna o texto da resposta do Gemini
    except Exception as e:
        print(f"⚠️ Erro ao enviar mensagem para o Gemini ou obter resposta: {e}")
        return "Ocorreu um erro ao tentar processar sua pergunta com o Gemini. Tente novamente."

def buscar_informacao_online_com_gemini(termo_de_busca, sites_especificos=None):
    """
    Utiliza o Gemini para buscar ou gerar informações sobre um termo específico,
    com foco opcional em sites prioritários.

    Args:
        termo_de_busca (str): O termo ou pergunta para a busca.
        sites_especificos (list, optional): Lista de URLs para focar a busca (informativo para o prompt).

    Returns:
        str: A resposta gerada pelo Gemini.
    """
    print(f"\n🔍 Usando Gemini para buscar informações sobre: '{termo_de_busca}'")

    # Constrói uma query mais elaborada para o Gemini, indicando o foco da busca.
    query_para_gemini = f"Preciso de informações sobre: '{termo_de_busca}'."
    if sites_especificos:
        query_para_gemini += f" Por favor, foque sua resposta em informações que seriam encontradas ou relacionadas aos seguintes sites (contexto estadual de São Paulo): {', '.join(sites_especificos)}."
    else:
        # Se não houver sites específicos, pede para focar no contexto geral do saude.sp.gov.br
        query_para_gemini += " Por favor, foque sua resposta em informações relevantes para o sistema de saúde de São Paulo, como as encontradas no site saude.sp.gov.br."

    # Chama a função que interage com o Gemini
    return obter_resposta_gemini(query_para_gemini)


def apresentar_boas_vindas_e_opcoes():
    """
    Apresenta a mensagem de boas-vindas e as opções principais do menu do chatbot.
    """
    print("\n" + "=" * 72)
    print(f"🤖 {respostas_fixas_tatui.get('Olá', 'Bem-vindo(a) ao Assistente Virtual!')}")
    print("=" * 72)
    print("\nPosso te ajudar com algumas informações sobre medicamentos e documentação")
    print("do Componente Especializado (Alto Custo) da Assistência Farmacêutica de Tatuí.")
    print("\nPor favor, escolha uma das opções abaixo ou digite sua pergunta:")
    print("-" * 72)
    # Opções do menu formatadas para melhor leitura
    opcoes_menu = [
        "1. Documentos para Nova Solicitação de medicamento.",
        "2. Documentos para Renovação de medicamento.",
        "3. Verificar se um medicamento está na lista do Componente Especializado (nível estadual).",
        "4. Horário de funcionamento e contato da Assistência Farmacêutica de Tatuí.",
        "5. O que significa ser legalmente incapaz?",
        "6. Como acompanhar meu pedido em Tatuí?",
        "7. Tenho outra pergunta (digite sua dúvida)."
    ]
    for opcao in opcoes_menu:
        print(f"  {opcao}")
    print("-" * 72)
    print("Digite 'sair' a qualquer momento para encerrar.")
    print("=" * 72)

def processar_escolha_usuario():
    """
    Processa a entrada do usuário, seja uma escolha do menu ou uma pergunta direta.
    Direciona para a resposta apropriada (fixa ou via Gemini).

    Returns:
        bool: False se o usuário digitar 'sair', True caso contrário, para controlar o loop principal.
    """
    while True:
        escolha_input = input("\n👉 Sua opção ou pergunta: ").strip()

        # Validação básica da entrada
        if not escolha_input:
            print("Por favor, digite algo ou escolha uma opção.")
            continue

        # Condição de saída do chatbot
        if escolha_input.lower() == 'sair':
            print(f"\nChatbot: {respostas_fixas_tatui.get('sair', 'Até logo!')}")
            return False # Sinaliza para encerrar o loop principal do chatbot

        resposta_chatbot = "" # Inicializa a variável de resposta

        # Lógica para determinar a resposta:
        # 1. Verifica se a entrada é uma chave exata no dicionário de respostas fixas.
        # 2. Verifica se é uma opção numérica do menu.
        # 3. Se não for nenhuma das anteriores, trata como pergunta para o Gemini.

        if escolha_input in respostas_fixas_tatui:
            resposta_chatbot = respostas_fixas_tatui[escolha_input]
        elif escolha_input == '1':
            resposta_chatbot = respostas_fixas_tatui.get("Nova solicitação.", "Informação não encontrada.")
        elif escolha_input == '2':
            resposta_chatbot = respostas_fixas_tatui.get("Renovação.", "Informação não encontrada.")
        elif escolha_input == '3':
            medicamento = input("💊 Qual medicamento você gostaria de verificar (nome do princípio ativo)? ").strip()
            if medicamento:
                # A busca é feita pelo Gemini, com foco nos sites estaduais.
                resposta_chatbot = buscar_informacao_online_com_gemini(
                    f"O medicamento '{medicamento}' (princípio ativo) está na lista do Componente Especializado da Assistência Farmacêutica de São Paulo?",
                    sites_especificos=SITES_PRIORITARIOS_ESTADUAIS
                )
            else:
                resposta_chatbot = "Nome do medicamento não fornecido. Por favor, tente novamente."
        elif escolha_input == '4':
            resposta_chatbot = respostas_fixas_tatui.get("Qual o horário de funcionamento e contato da Assistência Farmacêutica?", "Informação não encontrada.")
        elif escolha_input == '5':
            resposta_chatbot = respostas_fixas_tatui.get("O que significa ser legalmente incapaz?", "Informação não encontrada.")
        elif escolha_input == '6':
            resposta_chatbot = respostas_fixas_tatui.get("Como posso acompanhar meu pedido?", "Informação não encontrada.")
        elif escolha_input == '7':
            pergunta_direta = input("❓ Qual sua dúvida? ").strip()
            if pergunta_direta:
                # Verifica se a pergunta direta tem uma resposta fixa antes de ir para o Gemini
                if pergunta_direta in respostas_fixas_tatui:
                    resposta_chatbot = respostas_fixas_tatui[pergunta_direta]
                else: # Se não houver resposta fixa, usa o Gemini
                    resposta_chatbot = obter_resposta_gemini(pergunta_direta)
            else:
                resposta_chatbot = "Nenhuma pergunta fornecida. Por favor, digite sua dúvida."
        else:
            # Se não for uma opção numérica nem uma chave exata, trata como pergunta direta para o Gemini.
            # (Re-verifica se a entrada já não é uma chave, embora o primeiro `if` já cubra isso)
            if escolha_input in respostas_fixas_tatui:
                 resposta_chatbot = respostas_fixas_tatui[escolha_input]
            else:
                resposta_chatbot = obter_resposta_gemini(escolha_input)

        # Exibe a resposta do chatbot
        print(f"\nChatbot: {resposta_chatbot}")

        # Apresenta um menu resumido para facilitar a próxima interação
        print("\n" + "-" * 72)
        print("Posso ajudar com mais alguma coisa? Escolha uma opção ou digite 'sair'.")
        print("1. Nova Solicitação | 2. Renovação | 3. Verificar Medicamento (Estadual)")
        print("4. Contato AF Tatuí | 5. Incapacidade Legal | 6. Acompanhar Pedido (Tatuí)")
        print("7. Outra Pergunta")
        print("-" * 72)
    # Este return True não é alcançado devido ao loop infinito interno,
    # a saída é controlada pelo `return False` na condição 'sair'.
    return True

def iniciar_chatbot():
    """
    Função principal para iniciar e controlar o loop de interação do chatbot.
    """
    apresentar_boas_vindas_e_opcoes()
    # O loop continua enquanto `processar_escolha_usuario` retornar True (ou seja, não for 'sair')
    while processar_escolha_usuario():
        pass # A lógica de continuação está dentro de processar_escolha_usuario

# --- Ponto de Entrada do Script ---
if __name__ == "__main__":
    # Verificações iniciais (API Key e inicialização do modelo)
    # A API Key já é configurada no início do script.
    # A inicialização do chat_session também já ocorre no início.
    # Uma mensagem de aviso já é impressa se houver falha na inicialização do Gemini.

    # Inicia o chatbot
    iniciar_chatbot()
