🤖 Chatbot Assistência Farmacêutica Tatuí

Um assistente virtual inteligente para descomplicar o acesso a informações sobre o Componente Especializado da Assistência Farmacêutica de Tatuí, SP. Desenvolvido em Python com a potência da API Google Gemini.

✨ Sobre o Projeto

Navegar pelas informações sobre medicamentos de alto custo e a documentação necessária pode ser complexo.

Este chatbot visa simplificar esse processo, oferecendo respostas rápidas e precisas sobre o Componente Especializado da Assistência Farmacêutica do município de Tatuí, SP. Combinando respostas pré-definidas para as perguntas mais comuns com a capacidade de gerar informações adicionais via Google Gemini, ele se torna uma ferramenta valiosa para pacientes e seus responsáveis.

🚀 Funcionalidades

Respostas Rápidas: Obtenha informações instantâneas sobre horários, endereço, documentos necessários e contato telefônico.

Guia de Documentação: Detalhes completos sobre a documentação para nova solicitação e renovação de medicamentos.

Consulta Inteligente: Utilize a inteligência do Google Gemini para responder perguntas mais específicas ou não cobertas pelas respostas fixas.

Verificação de Medicamentos (Estadual): Ajuda a verificar a disponibilidade de medicamentos nas listas estaduais (com ressalva para confirmação local).

🛠️ Tecnologias Utilizadas

Python: Linguagem de programação principal.

Google Generative AI SDK: Integração com o modelo Gemini (versão 2.0 Flash).

🔌 Instalação e Uso

Clone o Repositório:

git clone https://github.com/TenisonJr/Chat_CEAF cd <Chat_CEAF>

Configure sua API Key do Google:

Obtenha sua API Key no Google AI Studio.

Se estiver usando Google Colab, armazene a chave nos "Secrets" (🔑) com o nome GOOGLE_API_KEY.

Se estiver rodando localmente, defina a variável de ambiente GOOGLE_API_KEY antes de executar o script, ou modifique o código para carregar a chave de outra forma segura (NUNCA exponha sua chave diretamente no código).

Execute o Chatbot:

python Chat_CEAF_v0.5.py

💡 Como Usar

Ao executar o script, o chatbot apresentará um menu com opções. Você pode digitar o número da opção desejada ou fazer sua pergunta diretamente. Digite sair a qualquer momento para encerrar a conversa.

========================================================================

🤖 Olá! Bem-vindo ao Chatbot da Assistência Farmacêutica de Tatuí. Estou aqui para te ajudar com suas dúvidas sobre a documentação para solicitação de medicamentos de alto custo.

========================================================================

Posso te ajudar com algumas informações sobre medicamentos e documentação

do Componente Especializado (Alto Custo) da Assistência Farmacêutica de Tatuí.

Por favor, escolha uma das opções abaixo ou digite sua pergunta:

Documentos para Nova Solicitação de medicamento.
Documentos para Renovação de medicamento.
Verificar se um medicamento está na lista do Componente Especializado (nível estadual).
Horário de funcionamento e contato da Assistência Farmacêutica de Tatuí.
O que significa ser legalmente incapaz?
Como acompanhar meu pedido em Tatuí?
Tenho outra pergunta (digite sua dúvida).
Digite 'sair' a qualquer momento para encerrar.

========================================================================

👉 Sua opção ou pergunta:

🤝 Contribuição

Contribuições são bem-vindas! Se você tiver sugestões de melhoria, novas perguntas frequentes ou quiser corrigir algo, sinta-se à vontade para abrir uma Issue ou enviar um Pull Request.

✉️ Contato

Se tiver dúvidas ou sugestões, entre em contato:

[TenisonJr] - [@tenisonjr]

⭐ Deixe uma estrela no projeto se ele for útil para você!
