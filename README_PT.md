![Imagem](img/封面.png)

<div align="center">
  <a href="https://space.bilibili.com/26978344">Tutorial em vídeo</a> ·
  <a href="how_to_use_nodes_ZH.md">Tutorial em texto</a> ·
  <a href="workflow_tutorial/">Tutorial de fluxo de trabalho</a> ·
  <a href="https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu">Link do Baidu Pan</a> ·
  <a href="img/Q群.jpg">Grupo do QQ</a> ·
  <a href="https://discord.gg/gxrQAYy6">Discord</a> ·
  <a href="https://dcnsxxvm4zeq.feishu.cn/wiki/IyUowXNj9iH0vzk68cpcLnZXnYf">Sobre nós</a>
</div>

####

<div align="center">
  <a href="./README_ZH.md"><img src="https://img.shields.io/badge/简体中文-d9d9d9"></a>
  <a href="./README.md"><img src="https://img.shields.io/badge/English-d9d9d9"></a>
  <a href="./README_RU.md"><img src="https://img.shields.io/badge/Русский-d9d9d9"></a>
  <a href="./README_FR.md"><img src="https://img.shields.io/badge/Français-d9d9d9"></a> 
  <a href="./README_DE.md"><img src="https://img.shields.io/badge/Deutsch-d9d9d9"></a>
  <a href="./README_JA.md"><img src="https://img.shields.io/badge/日本語-d9d9d9"></a>
  <a href="./README_KO.md"><img src="https://img.shields.io/badge/한국어-d9d9d9"></a>
  <a href="./README_AR.md"><img src="https://img.shields.io/badge/العربية-d9d9d9"></a>
  <a href="./README_ES.md"><img src="https://img.shields.io/badge/Español-d9d9d9"></a>
  <a href="./README_PT.md"><img src="https://img.shields.io/badge/Português-d9d9d9"></a>
</div>

####

Comfyui_llm_party tem como objetivo, com base na [comfyui](https://github.com/comfyanonymous/ComfyUI), uma interface de usuário extremamente minimalista, desenvolver um conjunto completo de biblioteca de nós para a construção de fluxos de trabalho de LLM. Isso permitirá que os usuários construam seus próprios fluxos de trabalho de LLM de forma mais rápida e conveniente, além de integrar facilmente em seus próprios fluxos de trabalho de imagem.

## Demonstração de resultados
https://github.com/user-attachments/assets/945493c0-92b3-4244-ba8f-0c4b2ad4eba6

## Visão Geral do Projeto
ComfyUI LLM Party permite desde a chamada de múltiplas ferramentas LLM, configuração rápida de personagens para construir seu assistente de IA personalizado, até a aplicação de Word Vector RAG e GraphRAG para gerenciamento local de bancos de dados de conhecimento da indústria; desde um pipeline de agentes inteligentes simples, até a construção de modos de interação complexos entre agentes inteligentes em padrão radial e circular; desde a necessidade de usuários individuais de integrar seus aplicativos sociais (QQ, Feishu, Discord), até o fluxo de trabalho tudo-em-um LLM+TTS+ComfyUI que os trabalhadores de streaming precisam; desde o primeiro aplicativo LLM que alunos comuns precisam para um fácil início, até as diversas interfaces de ajuste de parâmetros frequentemente utilizadas por pesquisadores e a adaptação de modelos. Tudo isso, você pode encontrar respostas no ComfyUI LLM Party.

## Atualizações Recentes
1. Na festa comfyui LLM, o sistema de morango do modelo da série chatgpt-o1 foi reproduzido, referindo-se aos prompts de [Llamaberry](https://huggingface.co/spaces/martinbowling/Llamaberry/blob/main/app.py). Exemplo de fluxo de trabalho: [Sistema de morango comparado ao o1](workflow\草莓系统与o1对比.json).
2. Foi adicionado um novo nó GPT-sovits, permitindo chamar o modelo GPT-sovits para converter texto em fala com base no seu áudio de referência. Você também pode preencher o caminho do seu modelo ajustado (se não preenchido, o modelo base será usado para inferência) para obter qualquer voz desejada. Para usá-lo, você precisa baixar o projeto [GPT-sovits](https://github.com/RVC-Boss/GPT-SoVITS) e o modelo base correspondente localmente, depois iniciar o serviço API com `runtime\python.exe api_v2.py` na pasta do projeto GPT-sovits. Além disso, o nó chatTTS foi movido para [comfyui LLM mafia](https://github.com/heshengtao/comfyui_LLM_mafia). A razão é que o chatTTS tem muitas dependências, e sua licença no PyPi é CC BY-NC 4.0, que é uma licença não comercial. Embora o projeto chatTTS no GitHub esteja sob a licença AGPL, movemos o nó chatTTS para comfyui LLM mafia para evitar problemas desnecessários. Esperamos que todos entendam!
3. Agora suporta o modelo mais recente da OpenAI, a série o1!
4. Foi adicionada uma ferramenta de controle de arquivos locais que permite ao LLM controlar arquivos na pasta especificada, como ler, escrever, adicionar, excluir, renomear, mover e copiar arquivos.Devido ao perigo potencial deste nó, ele está incluído em [comfyui LLM mafia](https://github.com/heshengtao/comfyui_LLM_mafia).
5. Novas ferramentas SQL permitem que o LLM consulte bancos de dados SQL.
6. Atualizada a versão multilíngue do README. Fluxo de trabalho para traduzir o documento README: [translate_readme](workflow/文档自动翻译机.json)
7. Atualizados quatro nós iteradores (iterador de texto, iterador de imagem, iterador de tabela, iterador JSON), onde os modos de iteração são: sequencial, aleatório e infinito. O modo sequencial irá gerar saídas em ordem, até que exceda o limite do índice e interrompa automaticamente o processo, reiniciando o valor do índice para 0; o modo aleatório escolherá um índice aleatório para saída; o modo infinito irá gerar saídas em um loop infinito.
8. Adicionado o nó carregador de API Gemini, agora compatível com a API oficial do Gemini! Se você estiver em um ambiente de rede nacional e encontrar problemas de restrição geográfica da API, por favor, altere o nó para os Estados Unidos e use o modo TUN. Devido ao fato de que, ao chamar ferramentas, se os parâmetros retornados contiverem caracteres chineses, ocorrerá um erro com código de retorno 500, portanto, alguns nós de ferramentas podem não estar disponíveis. Fluxo de trabalho de exemplo: [start_with_gemini](workflow/start_with_gemini.json)
9. Adicionado o nó de livro de lore, que permite inserir seu cenário de fundo durante a conversa com o LLM, fluxo de trabalho de exemplo: [lorebook](workflow/lorebook.json)
10. Adicionado o nó gerador de prompts FLUX, que pode gerar prompts em diversos estilos, como cartas de Hearthstone, cartas de Yu-Gi-Oh, pôsteres, quadrinhos, etc., permitindo que o modelo FLUX gere diretamente. Fluxo de trabalho de referência: [FLUX提示词](https://openart.ai/workflows/comfyui_llm_party/flux-by-llm-party/sjME541i68Kfw6Ib0EAD)

## Instruções de Uso
1. Para instruções sobre o uso dos nós, consulte: [怎么使用节点](how_to_use_nodes.md)

2. Se houver problemas com o plugin ou se você tiver outras dúvidas, sinta-se à vontade para entrar no grupo QQ: [931057213](img/Q群.jpg)
3. Para o tutorial de fluxo de trabalho, por favor, consulte: [工作流教程](workflow_tutorial/)，agradecemos a contribuição de [HuangYuChuh](https://github.com/HuangYuChuh)!

4. Conta para o uso avançado do fluxo de trabalho: [openart](https://openart.ai/workflows/profile/comfyui_llm_party?sort=latest&tab=creation)

4. Para mais fluxos de trabalho, você pode consultar a pasta [workflow](workflow).

## Tutoriais em vídeo
1. [Um guia passo a passo sobre como construir agentes modulares (super fácil!)](https://www.bilibili.com/video/BV1JZ421v7Tw/?vd_source=f229e378448918b84afab7c430c6a75b)

2. [Como conectar o GPT-4o ao comfyui | Permitir que um fluxo de trabalho chame outro fluxo de trabalho | Transformar LLM em uma ferramenta](https://www.bilibili.com/video/BV1JJ4m1A789/?spm_id_from=333.999.0.0&vd_source=f229e378448918b84afab7c430c6a75b)

3. [Como disfarçar seu fluxo de trabalho como GPT conectado ao WeChat | Compatível com Omost! Crie seu próprio dalle3 de forma flexível](https://www.bilibili.com/video/BV1DT421a7KY/?spm_id_from=333.999.0.0)

4. [Como jogar jogos de novela interativa no comfyui](https://www.bilibili.com/video/BV15y411q78L/?spm_id_from=333.999.0.0&vd_source=f229e378448918b84afab7c430c6a75b)

5. [Namorada de IA, e na sua forma | Implementação de graphRAG no comfyui, interagindo com neoa4j | Integração do fluxo de trabalho comfyui com o front-end streamlit](https://www.bilibili.com/video/BV1dS421R7Au/?spm_id_from=333.999.0.0&vd_source=f229e378448918b84afab7c430c6a75b)
## Suporte ao Modelo
1. Suporte a todas as chamadas de API no formato openai (combinado com [oneapi](https://github.com/songquanpeng/one-api), é possível chamar quase todas as APIs LLM, além de suportar todas as APIs de encaminhamento), a escolha do base_url deve seguir o exemplo em [config.ini.example](config.ini.example), atualmente testados incluem:
* [ollama](https://github.com/ollama/ollama) (recomendado! Se você está chamando localmente, é altamente aconselhável usar o método ollama para hospedar seu modelo local!)
* [通义千问/qwen](https://help.aliyun.com/zh/dashscope/developer-reference/compatibility-of-openai-with-dashscope/?spm=a2c4g.11186623.0.0.7b576019xkArPq)
* [智谱清言/glm](https://open.bigmodel.cn/dev/api#http_auth)
* [deepseek](https://platform.deepseek.com/api-docs/zh-cn/)
* [kimi/moonshot](https://platform.moonshot.cn/docs/api/chat#%E5%9F%BA%E6%9C%AC%E4%BF%A1%E6%81%AF)
* [豆包](https://www.volcengine.com/docs/82379/1263482)

2. Suporte a chamadas de API no formato Gemini:
* [Gemini](https://aistudio.google.com/app/prompts/new_chat)
3. Compatível com a maioria dos modelos locais suportados pela classe AutoModelForCausalLM da biblioteca transformer (se você não souber qual tipo de modelo escolher no nó do modelo local, opte por llama, que provavelmente será compatível), os modelos testados até o momento incluem:
* [ClosedCharacter/Peach-9B-8k-Roleplay](https://huggingface.co/ClosedCharacter/Peach-9B-8k-Roleplay) (recomendado! modelo de interpretação de papéis)
* [omost-llama-3-8b-4bits](https://huggingface.co/lllyasviel/omost-llama-3-8b-4bits) (recomendado! modelo de sugestões ricas)
* [meta-llama/Llama-2-7b-chat-hf](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)
* [Qwen/Qwen2-7B-Instruct](https://huggingface.co/Qwen/Qwen2-7B-Instruct)
* [xtuner/llava-llama-3-8b-v1_1-gguf](https://huggingface.co/xtuner/llava-llama-3-8b-v1_1-gguf)
* [THUDM/chatglm3-6b](https://huggingface.co/THUDM/chatglm3-6b) (devido à nova formatação de chamada do GLM4, os desenvolvedores não conseguem manter todas as chamadas de grandes modelos locais, portanto, recomenda-se que todos utilizem o método ollama para chamadas locais!)

4. Download do modelo:
* [Link do Baidu Cloud](https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu), código de extração: qyhu

## Download
Utilize um dos métodos abaixo para instalar
### Método 1:
1. No [gerenciador comfyui](https://github.com/ltdrdata/ComfyUI-Manager), pesquise por `comfyui_LLM_party` e instale com um clique
2. Reinicie o comfyui
### Método Dois:
1. Navegue até a pasta raiz do ComfyUI e acesse a subpasta `custom_nodes`.
2. Clone este repositório: `git clone https://github.com/heshengtao/comfyui_LLM_party.git`

### Método Três:
1. Clique em `CODE` no canto superior direito.
2. Clique em `download zip`.
3. Extraia o arquivo compactado baixado na subpasta `custom_nodes` da pasta raiz do ComfyUI.

## Implantação do Ambiente
1. Navegue até a pasta do projeto `comfyui_LLM_party`.
2. No terminal, digite `pip install -r requirements.txt` para implantar as bibliotecas de terceiros necessárias para este projeto no ambiente do ComfyUI. Verifique se você está instalando no ambiente do ComfyUI e fique atento a erros do `pip` no terminal.
3. Se você estiver usando o lançador do ComfyUI, você precisará digitar no terminal `caminho na configuração do lançador\python_embeded\python.exe -m pip install -r requirements.txt` para realizar a instalação. A pasta `python_embeded` geralmente está no mesmo nível da sua pasta `ComfyUI`.
4. Se você encontrar problemas de configuração do ambiente, pode tentar usar as dependências do `requirements_fixed.txt`.
## Configuração
* A linguagem pode ser configurada no `config.ini`, atualmente disponíveis apenas o Chinês (zh_CN) e o Inglês (en_US), sendo o padrão a língua do seu sistema.
* Você pode configurar o APIKEY utilizando um dos métodos a seguir:
### Método Um:
1. Abra o arquivo `config.ini` na pasta do projeto `comfyui_LLM_party`.
2. Insira seu `openai_api_key` e `base_url` no `config.ini`.
3. Se você estiver utilizando o modelo ollama, insira `http://127.0.0.1:11434/v1/` em `base_url`, coloque `ollama` em `openai_api_key` e insira o nome do seu modelo em `model_name`, por exemplo: llama3.
4. Se você deseja utilizar ferramentas de busca do Google ou Bing, insira seu `google_api_key`, `cse_id` ou `bing_api_key` no `config.ini`.
5. Se você pretende usar entrada de imagem para LLM, recomenda-se o uso do serviço de hospedagem de imagens imgbb, insira seu `imgbb_api` no `config.ini`.
6. Cada modelo pode ser configurado separadamente no arquivo `config.ini`, utilizando como referência o arquivo `config.ini.example`. Após a configuração, basta inserir `model_name` no nó.

### Método Dois:
1. Abra a interface do comfyui.
2. Crie um nó de modelo de linguagem grande (LLM) e insira diretamente seu `openai_api_key` e `base_url` no nó.
3. Se você estiver utilizando o modelo ollama, utilize o nó LLM_api, insira `http://127.0.0.1:11434/v1/` em `base_url`, coloque `ollama` em `api_key` e insira o nome do seu modelo em `model_name`, por exemplo: llama3.
4. Se você deseja usar entrada de imagem para LLM, recomenda-se o uso do serviço de hospedagem de imagens imgbb, insira seu `imgbb_api_key` no nó.
## Registro de Atualizações
1. Você pode clicar com o botão direito na interface do comfyui e selecionar `llm` no menu do botão direito para encontrar os nós deste projeto. [Como usar os nós](how_to_use_nodes_ZH.md)
2. Suporte para integração de API ou integração de grandes modelos locais. Implementação modular da funcionalidade de chamada de ferramentas. Ao preencher o base_url, insira um URL que termine com `/v1/`. Você pode usar [ollama](https://github.com/ollama/ollama) para gerenciar seus modelos e, em seguida, preencher `http://127.0.0.1:11434/v1/` no base_url, colocar ollama em api_key e o nome do seu modelo em model_name, por exemplo: llama3.
- Exemplo de fluxo de trabalho para integração de API: [start_with_LLM_api](workflow/start_with_LLM_api.json)
- Exemplo de fluxo de trabalho para integração de modelo local: [start_with_LLM_local](workflow/start_with_LLM_local.json)
- Exemplo de fluxo de trabalho para integração de ollama: [ollama](workflow/ollama.json)
3. Integração de repositório local de conhecimento, suporte a RAG. Exemplo de fluxo de trabalho: [Busca RAG no Repositório](workflow/知识库RAG搜索.json)
4. Capacidade de chamar um interpretador de código.
5. Capacidade de consulta online, suporte a pesquisa no Google. Exemplo de fluxo de trabalho: [Fluxo de Trabalho de Consulta de Filmes](workflow/电影查询工作流.json)
6. Possibilidade de implementar declarações condicionais no comfyui, permitindo classificar perguntas dos usuários antes de responder de forma direcionada. Exemplo de fluxo de trabalho: [Atendimento ao Cliente Inteligente](workflow/智能客服.json)
7. Suporte para links de feedback de grandes modelos, permitindo que dois grandes modelos debate. Exemplo de fluxo de trabalho: [Debate sobre o Dilema do Trem](workflow/电车难题辩论赛.json)
8. Suporte para anexar qualquer máscara de personalidade, permitindo a personalização de modelos de prompt.
9. Suporte para diversas chamadas de ferramentas; atualmente, foram desenvolvidas funcionalidades para verificar clima, hora, repositório de conhecimento, execução de código, pesquisa online e pesquisa em uma única página da web, entre outras.
10. Suporte para usar o LLM como um nó de ferramenta. Exemplo de fluxo de trabalho: [LLM Matryoshka](workflow/LLM套娃.json)
11. Suporte para desenvolvimento rápido de aplicações web próprias através de API + streamlit.
12. Adição de um nó interpretador universal perigoso, permitindo que o grande modelo faça qualquer coisa.
13. Recomenda-se o uso do nó de exibição de texto (show_text) no subdiretório de funções (function) do menu do botão direito como saída do nó LLM.
14. Suporte para a funcionalidade visual do GPT-4O! Exemplo de fluxo de trabalho: [GPT-4o](workflow/GPT-4o.json)  
15. Adicionado um intermediário de fluxo de trabalho, que permite que seu fluxo de trabalho chame outros fluxos de trabalho! Exemplo de fluxo de trabalho: [Chamar outro fluxo de trabalho](workflow/调用另一个工作流.json)  
16. Compatível com todos os modelos que possuem interfaces semelhantes à openai, como: Tongyi Qianwen/qwen, Zhiyu Qingyan/GLM, deepseek, kimi/moonshot. Preencha o base_url, api_key e model_name desses modelos no nó LLM para chamá-los.  
17. Adicionado um carregador LVM, agora é possível chamar modelos LVM localmente, suportando o modelo [llava-llama-3-8b-v1_1-gguf](https://huggingface.co/xtuner/llava-llama-3-8b-v1_1-gguf); outros modelos LVM no formato GGUF devem teoricamente também funcionar. O exemplo de fluxo de trabalho está aqui: [start_with_LVM.json](workflow/start_with_LVM.json).  
18. Foi escrito um arquivo `fastapi.py`, se você executá-lo diretamente, você terá uma interface openai em `http://127.0.0.1:8817/v1/`, qualquer aplicativo que possa chamar o GPT poderá acessar seu fluxo de trabalho comfyui! Irei preparar um tutorial detalhado para demonstrar como operar isso~  
19. O carregador LLM e a cadeia LLM foram separados, permitindo que o carregamento do modelo e a configuração do modelo sejam distintos, o que possibilita o compartilhamento de modelos entre diferentes nós LLM!  
20. Atualmente, já são suportados dispositivos macOS e mps! Agradecimentos a [bigcat88](https://github.com/bigcat88) por sua contribuição!  
21. Agora é possível criar seu próprio jogo de novela interativa, com diferentes finais dependendo das escolhas dos usuários! Exemplo de fluxo de trabalho: [Novela Interativa](workflow/互动小说.json)  
22. Compatível com as funcionalidades de whisper e tts da openai, permitindo entrada e saída de voz. Exemplo de fluxo de trabalho: [Entrada de voz + Saída de voz](workflow/语音输入+语音输出.json)  
23. Compatível com [Omost](https://github.com/lllyasviel/Omost)!!! Por favor, baixe [omost-llama-3-8b-4bits](https://huggingface.co/lllyasviel/omost-llama-3-8b-4bits) e experimente agora mesmo! Para referência de fluxo de trabalho, consulte: [start_with_OMOST](workflow/start_with_OMOST.json)  
24. Adicionadas ferramentas LLM para enviar mensagens ao WeChat empresarial, DingTalk e Feishu, além de funções externas que podem ser chamadas.  
25. Um novo iterador de texto foi adicionado, que pode gerar apenas uma parte dos caracteres a cada vez, dividindo o texto de forma segura com base no caractere de nova linha e no tamanho do bloco (chunk size), sem cortar o texto no meio. O chunk_overlap refere-se à quantidade de caracteres que se sobrepõem na divisão do texto. Isso permite a entrada em massa de textos muito longos, bastando clicar sem pensar, ou ativar a execução em loop no comfyui para que a execução seja feita automaticamente. Lembre-se de ativar o atributo is_locked para que, ao final da entrada, o fluxo de trabalho seja automaticamente bloqueado e não continue a execução. Fluxo de trabalho de exemplo: [文本迭代输入](workflow/文本迭代输入.json)  
26. Adicionado o atributo model name no carregador LLM local e no carregador llava local; se estiver vazio, será utilizado o caminho local de diversos tipos contido no nó. Se não estiver vazio, será utilizado o parâmetro de caminho que você preencheu no `config.ini`. Se não estiver vazio e não estiver no `config.ini`, será feito o download do Hugging Face ou carregado do diretório de modelos do Hugging Face. Se você deseja baixar do Hugging Face, preencha o atributo model name no formato: `THUDM/glm-4-9b-chat`. Atenção! O modelo carregado dessa forma deve ser compatível com a biblioteca transformer.  
27. Adicionados nós de análise de arquivos JSON e nós de obtenção de valores JSON, que permitem obter o valor de uma chave específica de um arquivo ou texto. Agradecimentos a [guobalove](https://github.com/guobalove) pela contribuição!
28. O código de chamada de ferramentas foi aprimorado, agora LLMs que não possuem a funcionalidade de chamada de ferramentas também podem ativar o atributo is_tools_in_sys_prompt (LLM local não precisa ser ativado por padrão, se adapta automaticamente). Quando ativado, as informações da ferramenta serão adicionadas ao prompt do sistema, permitindo que o LLM faça chamadas de ferramentas. O artigo relacionado ao princípio de implementação: [Achieving Tool Calling Functionality in LLMs Using Only Prompt Engineering Without Fine-Tuning](https://arxiv.org/abs/2407.04997)
29. Foi criada a pasta custom_tool para armazenar o código das ferramentas personalizadas, podendo ser consultado o código na pasta [custom_tool](custom_tool). Basta colocar o código da ferramenta personalizada na pasta custom_tool para que ela possa ser chamada no LLM.
30. Foi adicionada a ferramenta de gráfico de conhecimento, permitindo uma interação perfeita entre o LLM e o gráfico de conhecimento. O LLM pode modificar o gráfico de conhecimento com base na sua entrada e inferir para obter as respostas que você precisa. Para um fluxo de trabalho exemplo, consulte: [graphRAG_neo4j](workflow/graphRAG_neo4j.json)
31. Foi introduzida a funcionalidade de AI de personalidade, permitindo o desenvolvimento de sua própria AI de namorada ou namorado sem necessidade de código, com diálogos infinitos, memória permanente e personagens estáveis. Para um fluxo de trabalho exemplo, consulte: [麦洛薇人格AI](workflow/麦洛薇人格AI.json)
32. Você pode usar esta máquina de ferramentas LLM para gerar automaticamente ferramentas LLM, salvando o código da ferramenta gerada em um arquivo python e copiando o código para a pasta custom_tool, criando assim um novo nó. Fluxo de trabalho exemplo: [LLM工具生成器](workflow/LLM工具制造机.json).
33. O suporte à busca no duckduckgo foi adicionado, mas com grandes limitações; parece que só é possível inserir palavras-chave em inglês, e as palavras-chave não podem conter múltiplos conceitos, com a vantagem de não haver restrições de qualquer API key.
34. Foi implementada a funcionalidade de chamada separada de múltiplos repositórios de conhecimento, permitindo especificar qual repositório de conhecimento utilizar para responder perguntas dentro do prompt. Para um fluxo de trabalho exemplo, consulte: [多知识库分别调用](workflow/多知识库分别调用.json).
35. Suporte para que o LLM receba parâmetros adicionais, incluindo json out e outros parâmetros avançados. Para um fluxo de trabalho exemplo, consulte: [LLM输入额外参数](workflow/LLM额外参数eg_JSON_OUT.json). [用json_out分离提示词](workflow/用json_out分离提示词.json).
36. Foi adicionada a funcionalidade de conectar agentes ao Discord. (Ainda em teste)
37. Foi adicionada a funcionalidade de conectar agentes ao Feishu, agradecemos imensamente a contribuição de [guobalove](https://github.com/guobalove)! Consulte o fluxo de trabalho [Robô Feishu](workflow/飞书机器人.json).
38. Foi adicionado um nó de chamada de API universal e uma grande quantidade de nós auxiliares, utilizados para construir o corpo da solicitação e capturar informações da resposta.
39. Foi adicionado um nó de limpeza de modelo, que permite descarregar o LLM da memória a qualquer momento!
40. Foi adicionado o nó [chatTTS](https://github.com/2noise/ChatTTS), agradecemos imensamente a contribuição de [guobalove](https://github.com/guobalove)! O parâmetro `model_path` pode ser deixado vazio! Recomenda-se usar o modo HF para carregar o modelo, que será baixado automaticamente do Hugging Face, sem necessidade de download manual; se usar o modo local, coloque as pastas `asset` e `config` do modelo no diretório raiz. [Endereço do Baidu Cloud](https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu), código de extração: qyhu; se usar o modo `custom`, coloque as pastas `asset` e `config` do modelo dentro de `model_path`.
## Próximos passos:
1. Maior adaptação de modelos, cobrindo pelo menos as principais interfaces de API de grandes modelos e chamadas locais de modelos de código aberto populares, além de mais adaptações de modelos LVM. Atualmente, só adaptei a funcionalidade visual do GPT-4.
2. Mais maneiras de construir agentes inteligentes. Até agora, completei o trabalho de importar um LLM como uma ferramenta para outro LLM, permitindo a construção radial de fluxos de trabalho LLM, onde um fluxo de trabalho é importado como um nó para outro fluxo de trabalho. No futuro, posso desenvolver funcionalidades ainda mais interessantes nessa área.
3. Mais funcionalidades de automação. No futuro, lançarei mais nós que automaticamente enviam imagens, texto, vídeo e áudio para outros aplicativos, além de implementar nós de escuta para permitir respostas automáticas em redes sociais e fóruns populares.
4. Mais funcionalidades de gerenciamento de banco de dados de conhecimento. Atualmente, este projeto já suporta busca em arquivos locais e busca na web. No futuro, lançarei busca em gráficos de conhecimento e busca em memória de longo prazo, permitindo que os agentes realizem um raciocínio lógico sobre conhecimentos especializados e retenham informações-chave em conversas com os usuários.
5. Mais ferramentas e mais personas. Esta área é a mais fácil de desenvolver, mas também a que mais precisa de acumulação. Espero que, no futuro, este projeto possa ter, assim como o comfyui, uma variedade de nós personalizáveis, oferecendo numerosas ferramentas e personas.

## Isenção de responsabilidade:
Este projeto de código aberto e seu conteúdo (doravante denominado "projeto") são fornecidos apenas para fins de referência e não implicam em qualquer garantia expressa ou implícita. Os contribuintes do projeto não assumem qualquer responsabilidade pela integridade, precisão, confiabilidade ou adequação do projeto. Qualquer ação que dependa do conteúdo do projeto deve ser realizada por sua própria conta e risco. Em nenhuma circunstância os contribuintes do projeto serão responsáveis por quaisquer perdas ou danos indiretos, especiais ou consequenciais decorrentes do uso do conteúdo do projeto.
## Agradecimentos Especiais
<a href="https://github.com/bigcat88">
  <img src="https://avatars.githubusercontent.com/u/13381981?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://github.com/guobalove">
  <img src="https://avatars.githubusercontent.com/u/171540731?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://github.com/HuangYuChuh">
  <img src="https://avatars.githubusercontent.com/u/167663109?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>

## Agradecimentos
Alguns nós deste projeto foram inspirados pelos seguintes projetos, agradecemos suas contribuições à comunidade de código aberto!
1. [pythongosssss/ComfyUI-Custom-Scripts](https://github.com/pythongosssss/ComfyUI-Custom-Scripts)
2. [lllyasviel/Omost](https://github.com/lllyasviel/Omost)

## Suporte:

### Junte-se à Comunidade
Se houver problemas com o plugin ou se você tiver outras dúvidas, sinta-se à vontade para se juntar à nossa comunidade.

1. Grupo QQ: `931057213`
<div style="display: flex; justify-content: center;">
    <img src="img/Q群.jpg" style="width: 48%;" />
</div>

2. Grupo WeChat: `Choo-Yong` (adicione o assistente no WeChat antes de entrar no grupo)

3. Discord: [discord链接](https://discord.gg/gxrQAYy6)

### Siga-nos
1. Se desejar acompanhar as últimas funcionalidades deste projeto, fique à vontade para seguir nossa conta no Bilibili: [派对主持BB机](https://space.bilibili.com/26978344)
2. A conta OpenArt atualiza continuamente os workflows de festa mais úteis: [openart](https://openart.ai/workflows/profile/comfyui_llm_party?sort=latest&tab=creation)

### Apoio à doação
Se meu trabalho lhe trouxe valor, considere me convidar para um café! Seu apoio não apenas energiza o projeto, mas também aquece o coração do criador.☕💖 Cada xícara conta!
<div style="display:flex; justify-content:space-between;">
    <img src="img/zhifubao.jpg" style="width: 48%;" />
    <img src="img/wechat.jpg" style="width: 48%;" />
</div>

## Histórico de Estrelas

[![Star History Chart](https://api.star-history.com/svg?repos=heshengtao/comfyui_LLM_party&type=Date)](https://star-history.com/#heshengtao/comfyui_LLM_party&Date)
