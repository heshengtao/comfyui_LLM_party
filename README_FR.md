![Image](img/封面.png)

<div align="center">
  <a href="https://space.bilibili.com/26978344">Tutoriel vidéo</a> ·
  <a href="how_to_use_nodes_ZH.md">Tutoriel écrit</a> ·
  <a href="workflow_tutorial/">Tutoriel de workflow</a> ·
  <a href="https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu">Lien Baidu</a> ·
  <a href="img/Q群.jpg">Groupe QQ</a> ·
  <a href="https://discord.gg/gxrQAYy6">Discord</a> ·
  <a href="https://dcnsxxvm4zeq.feishu.cn/wiki/IyUowXNj9iH0vzk68cpcLnZXnYf">À propos de nous</a>
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

Comfyui_llm_party aspire à développer une bibliothèque complète de nœuds pour la construction de workflows LLM, basée sur l'interface utilisateur extrêmement simplifiée de [comfyui](https://github.com/comfyanonymous/ComfyUI). Cela permettra aux utilisateurs de construire plus facilement et rapidement leurs propres workflows LLM et de les intégrer de manière plus pratique dans leurs workflows d'images.

## Démonstration des effets
https://github.com/user-attachments/assets/9e627204-4626-479e-8806-cb06cd6157a6
## Aperçu du projet
ComfyUI LLM Party permet de construire rapidement votre propre assistant AI personnalisé, allant des appels multi-outils de LLM aux configurations de rôle, en passant par la gestion localisée des bases de connaissances du secteur grâce aux vecteurs de mots RAG et GraphRAG. De la chaîne d'agents intelligents unique à la construction de modes d'interaction complexes entre agents intelligents, y compris les modes d'interaction radiaux et circulaires ; des besoins des utilisateurs individuels qui souhaitent intégrer leurs applications sociales (QQ, Feishu, Discord) à un flux de travail tout-en-un LLM+TTS+ComfyUI pour les travailleurs des médias en continu ; des premières applications LLM simples pour les étudiants ordinaires aux diverses interfaces de réglage de paramètres utilisées par les chercheurs, ainsi que l'adaptation des modèles. Tout cela peut être découvert lors de ComfyUI LLM Party.

## Dernières mises à jour
1. Mise à jour de la version multilingue du README. Flux de travail pour traduire le document README : [translate_readme](workflow/文档自动翻译机.json)
2. Quatre nœuds d'itérateur ont été mis à jour (itérateur de texte, itérateur d'image, itérateur de tableau, itérateur json), avec trois modes d'itérateur : séquentiel, aléatoire et infini. Le mode séquentiel produira des sorties dans l'ordre jusqu'à dépasser la limite d'index, moment où le processus s'arrête automatiquement et la valeur d'index est réinitialisée à 0 ; le mode aléatoire choisira un index aléatoire pour la sortie, et le mode infini effectuera une sortie en boucle infinie.
3. Un nouveau nœud de chargeur d'API Gemini a été ajouté, désormais compatible avec l'API officielle de Gemini ! Si vous êtes dans un environnement réseau domestique et que vous rencontrez des problèmes de restriction de région pour l'API, veuillez passer le nœud sur les États-Unis et utiliser le mode TUN. Étant donné que Gemini génère une erreur avec un code retour 500 si des caractères chinois sont présents dans les paramètres retournés lors de l'appel d'outils, certains nœuds d'outils peuvent ne pas être disponibles. Flux de travail d'exemple : [start_with_gemini](workflow/start_with_gemini.json)
4. Un nœud de livre de lore a été ajouté, permettant d'insérer vos paramètres de fond lors des dialogues avec LLM, flux de travail d'exemple : [lorebook](workflow/lorebook.json)
5. Un nœud de générateur de mots-clés FLUX a été ajouté, capable de générer des mots-clés dans divers styles, tels que des cartes Hearthstone, des cartes Yu-Gi-Oh, des affiches, des bandes dessinées, etc., facilitant la sortie directe du modèle FLUX. Flux de travail de référence : [FLUX提示词](https://openart.ai/workflows/comfyui_llm_party/flux-by-llm-party/sjME541i68Kfw6Ib0EAD)

## Instructions d'utilisation
1. Pour les instructions d'utilisation des nœuds, veuillez consulter : [怎么使用节点](how_to_use_nodes.md)

2. Si vous rencontrez des problèmes avec le plugin ou si vous avez d'autres questions, n'hésitez pas à rejoindre le groupe QQ : [931057213](img/Q群.jpg)
3. Pour le tutoriel sur les flux de travail, veuillez consulter : [Tutoriel sur les flux de travail](workflow_tutorial/), merci pour la contribution de [HuangYuChuh](https://github.com/HuangYuChuh) !

4. Compte pour les fonctionnalités avancées des flux de travail : [openart](https://openart.ai/workflows/profile/comfyui_llm_party?sort=latest&tab=creation)

4. Pour plus de flux de travail, veuillez consulter le dossier [workflow](workflow).

## Tutoriels vidéo
1. [Un guide étape par étape pour construire un agent modulaire (très simple !)](https://www.bilibili.com/video/BV1JZ421v7Tw/?vd_source=f229e378448918b84afab7c430c6a75b)

2. [Comment connecter GPT-4o à comfyui | Appeler un autre flux de travail via un flux de travail | Transformer LLM en un outil](https://www.bilibili.com/video/BV1JJ4m1A789/?spm_id_from=333.999.0.0&vd_source=f229e378448918b84afab7c430c6a75b)

3. [Masquer votre flux de travail en tant que GPT connecté à WeChat | Compatible avec Omost ! Créez votre propre dalle3 de manière flexible](https://www.bilibili.com/video/BV1DT421a7KY/?spm_id_from=333.999.0.0)

4. [Comment jouer à des jeux de romans interactifs dans comfyui](https://www.bilibili.com/video/BV15y411q78L/?spm_id_from=333.999.0.0&vd_source=f229e378448918b84afab7c430c6a75b)

5. [Une petite amie IA, et qui prend votre forme | Réaliser graphRAG sur comfyui, interagir avec neoa4j | Connexion des flux de travail comfyui à l'interface frontend streamlit](https://www.bilibili.com/video/BV1dS421R7Au/?spm_id_from=333.999.0.0&vd_source=f229e378448918b84afab7c430c6a75b)
## Support du modèle
1. Prise en charge de tous les appels API au format OpenAI (en combinaison avec [oneapi](https://github.com/songquanpeng/one-api), il est possible d'appeler presque toutes les API LLM, ainsi que toutes les API de transit). Pour le choix de base_url, veuillez vous référer à [config.ini.example](config.ini.example). Actuellement, les API testées incluent :
* [ollama](https://github.com/ollama/ollama) (fortement recommandé ! Si vous effectuez des appels locaux, il est très recommandé d'utiliser ollama pour héberger votre modèle local !)
* [通义千问/qwen](https://help.aliyun.com/zh/dashscope/developer-reference/compatibility-of-openai-with-dashscope/?spm=a2c4g.11186623.0.0.7b576019xkArPq)
* [智谱清言/glm](https://open.bigmodel.cn/dev/api#http_auth)
* [deepseek](https://platform.deepseek.com/api-docs/zh-cn/)
* [kimi/moonshot](https://platform.moonshot.cn/docs/api/chat#%E5%9F%BA%E6%9C%AC%E4%BF%A1%E6%81%AF)
* [豆包](https://www.volcengine.com/docs/82379/1263482)

2. Prise en charge des appels API au format Gemini :
* [Gemini](https://aistudio.google.com/app/prompts/new_chat)
3. Compatible avec la plupart des modèles locaux pris en charge par la classe AutoModelForCausalLM de la bibliothèque transformer (si vous ne savez pas quel type de modèle sélectionner sur le nœud du modèle local, choisissez llama, cela devrait fonctionner dans la plupart des cas), les modèles testés jusqu'à présent sont :
* [ClosedCharacter/Peach-9B-8k-Roleplay](https://huggingface.co/ClosedCharacter/Peach-9B-8k-Roleplay) (recommandé ! Modèle de jeu de rôle)
* [omost-llama-3-8b-4bits](https://huggingface.co/lllyasviel/omost-llama-3-8b-4bits) (recommandé ! Modèle avec des invites riches)
* [meta-llama/Llama-2-7b-chat-hf](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)
* [Qwen/Qwen2-7B-Instruct](https://huggingface.co/Qwen/Qwen2-7B-Instruct)
* [xtuner/llava-llama-3-8b-v1_1-gguf](https://huggingface.co/xtuner/llava-llama-3-8b-v1_1-gguf)
* [THUDM/chatglm3-6b](https://huggingface.co/THUDM/chatglm3-6b) (en raison du nouveau format d'appel du GLM4, les développeurs ne peuvent pas maintenir tous les modèles locaux, il est donc recommandé d'utiliser la méthode ollama pour les appels locaux !)

4. Téléchargement des modèles :
* [Adresse Baidu Cloud](https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu), code d'extraction : qyhu

## Téléchargement
Installez en utilisant l'une des méthodes suivantes
### Méthode 1 :
1. Recherchez `comfyui_LLM_party` dans le [gestionnaire ComfyUI](https://github.com/ltdrdata/ComfyUI-Manager) et installez-le d'un seul clic
2. Redémarrez ComfyUI
### Méthode deux :
1. Naviguez vers le sous-dossier `custom_nodes` dans le dossier racine de ComfyUI.
2. Clonez ce dépôt. `git clone https://github.com/heshengtao/comfyui_LLM_party.git`

### Méthode trois :
1. Cliquez sur `CODE` en haut à droite.
2. Cliquez sur `télécharger zip`.
3. Décompressez le fichier zip téléchargé dans le sous-dossier `custom_nodes` du dossier racine de ComfyUI.

## Déploiement de l'environnement
1. Naviguez vers le dossier du projet `comfyui_LLM_party`.
2. Dans le terminal, saisissez `pip install -r requirements.txt` pour déployer les bibliothèques tierces nécessaires à ce projet dans l'environnement de comfyui. Veuillez vérifier que vous installez dans l'environnement de comfyui et faites attention aux erreurs `pip` dans le terminal.
3. Si vous utilisez le lanceur comfyui, vous devez entrer dans le terminal `chemin dans la configuration du lanceur\python_embeded\python.exe -m pip install -r requirements.txt` pour procéder à l'installation. Le dossier `python_embeded` est généralement au même niveau que votre dossier `ComfyUI`.
4. Si vous rencontrez des problèmes de configuration de l'environnement, vous pouvez essayer d'utiliser les dépendances dans `requirements_fixed.txt`.
## Configuration
* Vous pouvez configurer la langue dans le fichier `config.ini`, actuellement seules deux langues sont disponibles : chinois (zh_CN) et anglais (en_US), la langue par défaut étant celle de votre système.
* Vous pouvez configurer l'APIKEY en utilisant l'une des méthodes suivantes :
### Méthode 1 :
1. Ouvrez le fichier `config.ini` dans le dossier du projet `comfyui_LLM_party`.
2. Dans `config.ini`, saisissez votre `openai_api_key` et `base_url`.
3. Si vous utilisez le modèle ollama, entrez `http://127.0.0.1:11434/v1/` dans `base_url`, `ollama` dans `openai_api_key`, et le nom de votre modèle dans `model_name`, par exemple : llama3.
4. Si vous souhaitez utiliser les outils de recherche Google ou Bing, saisissez votre `google_api_key`, `cse_id` ou `bing_api_key` dans `config.ini`.
5. Si vous désirez utiliser des entrées d'images pour LLM, il est recommandé d'utiliser le service d'hébergement d'images imgbb, et d'indiquer votre `imgbb_api` dans `config.ini`.
6. Chaque modèle peut être configuré individuellement dans le fichier `config.ini`, vous pouvez vous référer au fichier `config.ini.example` pour vous aider. Une fois que vous avez terminé la configuration, il vous suffit de saisir `model_name` dans le nœud.

### Méthode 2 :
1. Ouvrez l'interface comfyui.
2. Créez un nœud de grand modèle de langage (LLM) et saisissez directement votre `openai_api_key` et `base_url` dans le nœud.
3. Si vous utilisez le modèle ollama, veuillez utiliser le nœud LLM_api, entrer `http://127.0.0.1:11434/v1/` dans `base_url`, `ollama` dans `api_key`, et le nom de votre modèle dans `model_name`, par exemple : llama3.
4. Si vous souhaitez utiliser des entrées d'images pour LLM, il est recommandé d'utiliser le service d'hébergement d'images imgbb et d'indiquer votre `imgbb_api_key` dans le nœud.
## Journal des mises à jour
1. Vous pouvez cliquer avec le bouton droit dans l'interface comfyui, sélectionner `llm` dans le menu contextuel, et trouver le nœud de ce projet. [Comment utiliser les nœuds](how_to_use_nodes_ZH.md)
2. Prise en charge de l'intégration API ou de l'intégration de grands modèles locaux. Mise en œuvre modulaire de la fonctionnalité d'appel d'outils. Lors de la saisie de base_url, veuillez entrer une URL se terminant par `/v1/`. Vous pouvez utiliser [ollama](https://github.com/ollama/ollama) pour gérer vos modèles, puis entrer `http://127.0.0.1:11434/v1/` dans base_url, ollama dans api_key, et le nom de votre modèle, par exemple : llama3.
   - Exemple de flux de travail d'intégration API : [start_with_LLM_api](workflow/start_with_LLM_api.json)
   - Exemple de flux de travail d'intégration de modèle local : [start_with_LLM_local](workflow/start_with_LLM_local.json)
   - Exemple de flux de travail d'intégration ollama : [ollama](workflow/ollama.json)
3. Intégration d'une base de connaissances locale, prise en charge de RAG. Exemple de flux de travail : [Recherche RAG de la base de connaissances.json](workflow/知识库RAG搜索.json)
4. Possibilité d'appeler un interpréteur de code.
5. Possibilité de rechercher en ligne, prise en charge de la recherche Google. Exemple de flux de travail : [Flux de recherche de films](workflow/电影查询工作流.json)
6. Possibilité de mettre en œuvre des instructions conditionnelles dans comfyui, permettant de classer les questions des utilisateurs avant de répondre de manière ciblée. Exemple de flux de travail : [Service client intelligent](workflow/智能客服.json)
7. Prise en charge des liens en boucle pour les grands modèles, permettant à deux grands modèles de débattre. Exemple de flux de travail : [Débat sur le dilemme du tramway](workflow/电车难题辩论赛.json)
8. Prise en charge de l'attachement de n'importe quel masque de personnalité, possibilité de personnaliser les modèles d'invite.
9. Prise en charge de divers appels d'outils, actuellement développés pour vérifier la météo, l'heure, la base de connaissances, l'exécution de code, la recherche en ligne, et la recherche sur une seule page Web, entre autres.
10. Prise en charge de l'utilisation de LLM en tant que nœud d'outil. Exemple de flux de travail : [LLM poupée russe](workflow/LLM套娃.json)
11. Prise en charge du développement rapide de vos propres applications web via API + streamlit.
12. Ajout d'un nœud d'interpréteur universel dangereux, permettant au grand modèle de faire n'importe quoi.
13. Il est recommandé d'utiliser les fonctions dans le sous-répertoire du menu contextuel, sous le nœud de texte à afficher (show_text), comme affichage de sortie pour le nœud LLM.
14. Fonctionnalité visuelle prise en charge par GPT-4O ! Exemple de flux de travail : [GPT-4o](workflow/GPT-4o.json)
15. Un intermédiaire de flux de travail a été ajouté, permettant à votre flux de travail d'appeler d'autres flux de travail ! Exemple de flux de travail : [Appeler un autre flux de travail](workflow/调用另一个工作流.json)
16. Compatible avec tous les modèles ayant une interface similaire à OpenAI, tels que : Tongyi Qianwen/qwen, Zhipu Qingyan/GLM, deepseek, kimi/moonshot. Veuillez remplir les champs base_url, api_key et model_name des nœuds LLM pour les appeler.
17. Un chargeur LVM a été ajouté, permettant d'appeler localement des modèles LVM, prenant en charge le modèle [llava-llama-3-8b-v1_1-gguf](https://huggingface.co/xtuner/llava-llama-3-8b-v1_1-gguf), d'autres modèles LVM au format GGUF devraient également fonctionner en théorie. Exemple de flux de travail ici : [start_with_LVM.json](workflow/start_with_LVM.json).
18. Un fichier `fastapi.py` a été créé. Si vous l'exécutez directement, vous obtiendrez une interface OpenAI sur `http://127.0.0.1:8817/v1/`, toute application pouvant appeler GPT pourra alors interagir avec votre flux de travail ComfyUI ! Je fournirai un tutoriel détaillé à ce sujet.
19. Le chargeur LLM et la chaîne LLM ont été séparés, permettant de dissocier le chargement du modèle et la configuration du modèle, facilitant ainsi le partage de modèles entre différents nœuds LLM !
20. La prise en charge de macOS et des appareils MPS est désormais disponible ! Merci à [bigcat88](https://github.com/bigcat88) pour cette contribution !
21. Vous pouvez créer votre propre jeu de roman interactif, avec des fins différentes selon les choix des utilisateurs ! Exemple de flux de travail : [Roman interactif](workflow/互动小说.json)
22. Intégration des fonctionnalités Whisper et TTS d'OpenAI, permettant l'entrée et la sortie vocales. Exemple de flux de travail : [Entrée vocale + Sortie vocale](workflow/语音输入+语音输出.json)
23. Compatible avec [Omost](https://github.com/lllyasviel/Omost) ! Veuillez télécharger [omost-llama-3-8b-4bits](https://huggingface.co/lllyasviel/omost-llama-3-8b-4bits) pour vivre l'expérience immédiatement ! Pour un exemple de flux de travail, veuillez vous référer à : [start_with_OMOST](workflow/start_with_OMOST.json)
24. De nouveaux outils LLM ont été ajoutés pour envoyer des messages à WeChat d'entreprise, DingTalk et Feishu, ainsi que des fonctions externes disponibles à l'appel.
25. Un nouvel itérateur de texte a été ajouté, capable de n'afficher qu'une partie des caractères à la fois, en segmentant le texte en toute sécurité par rapport aux caractères de retour à la ligne et à la taille des morceaux, sans couper le texte au milieu. Le paramètre chunk_overlap indique combien de caractères se chevauchent lors de la segmentation du texte. Cela permet d'entrer en masse des textes très longs ; il suffit de cliquer sans réfléchir ou d'activer l'exécution en boucle dans ComfyUI, et tout sera exécuté automatiquement. N'oubliez pas d'activer l'attribut is_locked, ce qui permettra de verrouiller automatiquement le flux de travail à la fin de l'entrée, empêchant toute exécution ultérieure. Exemple de flux de travail : [Texte d'itération d'entrée](workflow/文本迭代输入.json)
26. L'attribut model name a été ajouté aux chargeurs LLM locaux et LLava locaux ; s'il est vide, divers chemins locaux dans le nœud seront utilisés pour le chargement. S'il n'est pas vide, le paramètre de chemin que vous avez rempli dans `config.ini` sera utilisé pour le chargement. S'il n'est pas vide et n'est pas dans `config.ini`, le modèle sera téléchargé depuis Hugging Face ou chargé depuis le répertoire de modèles de Hugging Face. Si vous souhaitez télécharger depuis Hugging Face, veuillez remplir l'attribut model name au format : `THUDM/glm-4-9b-chat`. Attention ! Les modèles chargés de cette manière doivent être compatibles avec la bibliothèque Transformer.
27. De nouveaux nœuds pour le parsing de fichiers JSON et l'extraction de valeurs JSON ont été ajoutés, vous permettant d'obtenir la valeur d'une clé depuis un fichier ou un texte. Merci à [guobalove](https://github.com/guobalove) pour sa contribution !
28. Le code des appels d'outils a été amélioré, permettant désormais aux LLM sans fonction d'appel d'outils d'activer l'attribut is_tools_in_sys_prompt (par défaut, les LLM locaux n'ont pas besoin d'être activés et s'adaptent automatiquement). Une fois activé, les informations sur les outils seront ajoutées à l'invite système, permettant ainsi au LLM d'appeler des outils. Un article pertinent sur le principe de mise en œuvre : [Achieving Tool Calling Functionality in LLMs Using Only Prompt Engineering Without Fine-Tuning](https://arxiv.org/abs/2407.04997)

29. Un dossier custom_tool a été créé pour stocker le code des outils personnalisés. Vous pouvez vous référer au code dans le dossier [custom_tool](custom_tool) et y placer votre code d'outil personnalisé afin de pouvoir l'appeler dans le LLM.

30. Un nouvel outil de graphe de connaissances a été ajouté, permettant une interaction parfaite entre le LLM et le graphe de connaissances. Le LLM peut modifier le graphe de connaissances en fonction de vos entrées et déduire les réponses nécessaires à partir de celui-ci. Pour un exemple de flux de travail, veuillez consulter : [graphRAG_neo4j](workflow/graphRAG_neo4j.json).

31. Une fonctionnalité d'IA de personnalité a été ajoutée, permettant de développer votre propre IA de petite amie ou d'ami sans code, avec des conversations illimitées, une mémoire permanente et une personnalité stable. Pour un exemple de flux de travail, veuillez consulter : [麦洛薇人格AI](workflow/麦洛薇人格AI.json).

32. Vous pouvez utiliser cet outil de fabrication LLM pour générer automatiquement des outils LLM. Sauvegardez le code de l'outil généré dans un fichier python, puis copiez le code dans le dossier custom_tool, créant ainsi un nouveau nœud. Exemple de flux de travail : [LLM工具生成器](workflow/LLM工具制造机.json).

33. La recherche avec DuckDuckGo est désormais prise en charge, mais avec de grandes limitations ; il semble que seuls des mots-clés en anglais puissent être saisis et qu'un seul concept soit autorisé dans les mots-clés. L'avantage réside dans l'absence de toute restriction d'API key.

34. La fonctionnalité d'appel séparé de plusieurs bases de connaissances a été ajoutée, permettant de préciser dans l'invite quelle base de connaissances doit être utilisée pour répondre aux questions. Exemple de flux de travail : [多知识库分别调用](workflow/多知识库分别调用.json).

35. La prise en charge de paramètres supplémentaires pour le LLM est désormais possible, y compris des paramètres avancés tels que json out. Exemple de flux de travail : [LLM输入额外参数](workflow/LLM额外参数eg_JSON_OUT.json). [用json_out分离提示词](workflow/用json_out分离提示词.json).
36. Ajout de la fonctionnalité permettant de connecter l'agent à Discord. (Encore en test)
37. Ajout de la fonctionnalité permettant de connecter l'agent à Feishu, un grand merci à [guobalove](https://github.com/guobalove) pour sa contribution ! Référencer le workflow [Robot Feishu](workflow/飞书机器人.json).
38. Ajout d'un nœud d'appel API universel ainsi que de nombreux nœuds auxiliaires pour construire le corps de la requête et extraire des informations de la réponse.
39. Ajout d'un nœud de videur de modèle, permettant de décharger le LLM de la mémoire vidéo à tout moment !
40. Le nœud [chatTTS](https://github.com/2noise/ChatTTS) a été ajouté, un grand merci à [guobalove](https://github.com/guobalove) pour sa contribution ! Le paramètre `model_path` peut être vide ! Il est recommandé d'utiliser le mode HF pour charger le modèle, qui sera automatiquement téléchargé depuis Hugging Face, sans besoin de téléchargement manuel ; si vous utilisez le mode local, placez les dossiers `asset` et `config` du modèle à la racine. [Adresse Baidu Cloud](https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu), code d'extraction : qyhu ; si vous utilisez le mode `custom`, placez les dossiers `asset` et `config` du modèle sous `model_path`.
## Prochaines étapes :
1. Adaptation de modèles supplémentaires, afin de couvrir au moins les principales API de grands modèles et les appels locaux des modèles open source, ainsi que d'autres adaptations de modèles LVM. À l'heure actuelle, je n'ai encore adapté que l'appel des fonctionnalités visuelles de GPT-4 ;
2. Développement de davantage de modes de construction d'agents intelligents. À ce jour, j'ai déjà complété le travail consistant à intégrer un LLM en tant qu'outil pour un autre LLM, réalisant ainsi une construction de flux de travail LLM en rayonnant, où un flux de travail est importé en tant que nœud dans un autre flux de travail. À l'avenir, je pourrais développer des fonctionnalités encore plus intéressantes dans ce domaine ;
3. Mise en place de fonctionnalités d'automatisation supplémentaires. Je prévois de lancer davantage de nœuds permettant de pousser automatiquement des images, des textes, des vidéos et des audios vers d'autres applications, ainsi que des nœuds d'écoute pour permettre des réponses automatiques sur les principaux réseaux sociaux et forums ;
4. Amélioration des fonctionnalités de gestion de la base de connaissances. Actuellement, ce projet prend déjà en charge la recherche de fichiers locaux et la recherche sur le web. Dans le futur, je compte introduire des recherches dans des graphes de connaissances et des recherches de mémoire à long terme, permettant aux agents d'avoir une réflexion logique sur des connaissances spécialisées et de se souvenir indéfiniment de certaines informations clés lors de leurs interactions avec les utilisateurs ;
5. Développement de davantage d'outils et de masques de personnalité. Cet aspect est le plus facile à réaliser mais nécessite également le plus d'accumulation. J'espère qu'à l'avenir, ce projet pourra disposer, tout comme ComfyUI, d'un grand nombre de nœuds personnalisés, ainsi que de nombreux outils et masques de personnalité.

## Avertissement :
Ce projet open source et son contenu (ci-après dénommé "projet") sont fournis uniquement à titre de référence et ne constituent en aucun cas une garantie expresse ou implicite. Les contributeurs du projet ne sauraient être tenus responsables de l'intégrité, de l'exactitude, de la fiabilité ou de l'applicabilité du projet. Toute action reposant sur le contenu du projet se fait à vos propres risques. En aucun cas, les contributeurs du projet ne sauraient être tenus responsables des pertes ou dommages indirects, spéciaux ou consécutifs résultant de l'utilisation du contenu du projet.
## Remerciements spéciaux
<a href="https://github.com/bigcat88">
  <img src="https://avatars.githubusercontent.com/u/13381981?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://github.com/guobalove">
  <img src="https://avatars.githubusercontent.com/u/171540731?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://github.com/HuangYuChuh">
  <img src="https://avatars.githubusercontent.com/u/167663109?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>

## Liste des emprunts
Certaines des fonctionnalités de ce projet s'inspirent des projets suivants, nous les remercions pour leur contribution à la communauté open source !
1. [pythongosssss/ComfyUI-Custom-Scripts](https://github.com/pythongosssss/ComfyUI-Custom-Scripts)
2. [lllyasviel/Omost](https://github.com/lllyasviel/Omost)
3. [2noise/ChatTTS](https://github.com/2noise/ChatTTS)

## Support :

### Rejoignez la communauté
Si vous rencontrez des problèmes avec le plugin ou si vous avez d'autres questions, n'hésitez pas à rejoindre notre communauté.

1. Groupe QQ : `931057213`
<div style="display: flex; justify-content: center;">
    <img src="img/Q群.jpg" style="width: 48%;" />
</div>

2. Groupe WeChat : `Choo-Yong` (ajoutez le petit assistant WeChat pour rejoindre le groupe)

3. discord : [lien discord](https://discord.gg/gxrQAYy6)

### Suivez-nous
1. Si vous souhaitez rester informé des dernières fonctionnalités de ce projet, n'hésitez pas à suivre notre compte Bilibili : [派对主持BB机](https://space.bilibili.com/26978344)
2. Le compte OpenArt est régulièrement mis à jour avec les workflows de party les plus utiles : [openart](https://openart.ai/workflows/profile/comfyui_llm_party?sort=latest&tab=creation)

### Soutien par don
Si mon travail vous apporte de la valeur, veuillez envisager de m'offrir un café ! Votre soutien insuffle non seulement de la vitalité au projet, mais réchauffe également le cœur des créateurs.☕💖 Chaque tasse compte !
<div style="display:flex; justify-content:space-between;">
    <img src="img/zhifubao.jpg" style="width: 48%;" />
    <img src="img/wechat.jpg" style="width: 48%;" />
</div>

## Historique des étoiles

[![Star History Chart](https://api.star-history.com/svg?repos=heshengtao/comfyui_LLM_party&type=Date)](https://star-history.com/#heshengtao/comfyui_LLM_party&Date)
