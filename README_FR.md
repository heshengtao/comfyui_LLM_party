![Image](img/封面.png)

<div align="center">
  <a href="https://space.bilibili.com/26978344">bilibili</a> ·
  <a href="https://www.youtube.com/@LLM-party">youtube</a> ·
  <a href="https://github.com/heshengtao/Let-LLM-party">Tutoriel écrit</a> ·
  <a href="https://pan.quark.cn/s/190b41f3bbdb">Adresse du disque cloud</a> ·
  <a href="img/Q群.jpg">Groupe QQ</a> ·
  <a href="https://discord.gg/f2dsAKKr2V">Discord</a> ·
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
https://github.com/user-attachments/assets/945493c0-92b3-4244-ba8f-0c4b2ad4eba6

## Aperçu du projet
ComfyUI LLM Party permet de construire rapidement votre propre assistant AI personnalisé, allant des appels multi-outils de LLM aux configurations de rôle, en passant par la gestion localisée des bases de connaissances du secteur grâce aux vecteurs de mots RAG et GraphRAG. De la chaîne d'agents intelligents unique à la construction de modes d'interaction complexes entre agents intelligents, y compris les modes d'interaction radiaux et circulaires ; des besoins des utilisateurs individuels qui souhaitent intégrer leurs applications sociales (QQ, Feishu, Discord) à un flux de travail tout-en-un LLM+TTS+ComfyUI pour les travailleurs des médias en continu ; des premières applications LLM simples pour les étudiants ordinaires aux diverses interfaces de réglage de paramètres utilisées par les chercheurs, ainsi que l'adaptation des modèles. Tout cela peut être découvert lors de ComfyUI LLM Party.

## Démarrage rapide
0. Si vous n'avez jamais utilisé ComfyUI et que vous rencontrez des problèmes de dépendance lors de l'installation de LLM Party dans ComfyUI, cliquez [ici](https://drive.google.com/file/d/1T9C7gEbd-w_zf9GqZO1VeI3z8ek8clpX/view?usp=sharing) pour télécharger le package portable **Windows** contenant LLM Party. Attention ! Ce package portable ne comprend que les deux plugins Party et Manager, et il est uniquement compatible avec le système Windows.(Si vous devez installer LLM party sur un ComfyUI existant, cette étape peut être ignorée.)
1. Faites glisser les workflows suivants dans votre comfyui, puis utilisez [comfyui-Manager](https://github.com/ltdrdata/ComfyUI-Manager) pour installer les nœuds manquants.
  - Utilisez l'API pour appeler LLM : [start_with_LLM_api](workflow/start_with_LLM_api.json)
  - Utilisation de aisuite pour appeler LLM : [start_with_aisuite](workflow/start_with_aisuite.json)
  - Gérez les LLM locaux avec ollama : [start_with_Ollama](workflow/ollama.json)
  - Utilisez des LLM locaux au format distribué : [start_with_LLM_local](workflow/start_with_LLM_local.json)
  - Utilisez des LLM locaux au format GGUF : [start_with_LLM_GGUF](workflow/start_with_GGUF.json)
  - Utilisez des VLM locaux au format distribué : [start_with_VLM_local](workflow/start_with_VLM_local.json) （Actuellement, le support est disponible pour [Llama-3.2-Vision](https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct)/[Qwen/Qwen2.5-VL](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct)/[deepseek-ai/Janus-Pro](https://huggingface.co/deepseek-ai/Janus-Pro-1B)）
  - Utilisez des VLM locaux au format GGUF : [start_with_VLM_GGUF](workflow/start_with_llava.json)
  - Utiliser l'API pour appeler LLM afin de générer des mots-clés SD et produire des images : [commencer_avec_VLM_API_pour_SD](workflow/start_with_VLM_API_for_SD.json)
  - Utiliser ollama pour appeler minicpm afin de générer des mots-clés SD et produire des images : [commencer_avec_ollama_minicpm_pour_SD](workflow/start_with_ollama_minicpm_for_SD.json)
  - Utiliser le qwen-vl local pour générer des mots-clés SD et produire des images : [commencer_avec_qwen_vl_local_pour_SD](workflow/start_with_qwen_vl_local_for_SD.json)
2. Si vous utilisez l'API, remplissez votre `base_url` (cela peut être une API relais, assurez-vous qu'elle se termine par `/v1/`) et `api_key` dans le nœud de chargement de l'API LLM. Exemple : `https://api.openai.com/v1/`
3. Si vous utilisez ollama, activez l'option `is_ollama` dans le nœud de chargement de l'API LLM, sans remplir `base_url` et `api_key`.
4. Si vous utilisez un modèle local, remplissez le chemin de votre modèle dans le nœud de chargement du modèle local, par exemple : `E:\model\Llama-3.2-1B-Instruct`. Vous pouvez également remplir l'ID du dépôt du modèle Huggingface dans le nœud de chargement du modèle local, par exemple : `lllyasviel/omost-llama-3-8b-4bits`.
5. En raison du seuil d'utilisation élevé de ce projet, même si vous choisissez le démarrage rapide, j'espère que vous pourrez lire attentivement la page d'accueil du projet.

## Dernières mises à jour
1. Le nœud API LLM prend désormais en charge le mode de sortie en flux, affichant en temps réel le texte retourné par l'API dans la console, vous permettant ainsi de voir la sortie de l'API sans avoir à attendre que l'ensemble de la requête soit complété.
2. Le nœud API LLM a été enrichi d'une sortie de reasoning_content, capable de séparer automatiquement le raisonnement et la réponse du modèle R1.
3. Une nouvelle branche de dépôt, uniquement_api, a été ajoutée. Cette branche ne contient que la partie appelant l'API, facilitant ainsi l'utilisation pour les utilisateurs qui n'ont besoin que des appels API. Il vous suffit d'utiliser la commande dans le dossier `custom node` de `comfyui` : `git clone -b only_api https://github.com/heshengtao/comfyui_LLM_party.git`, puis de suivre le schéma de déploiement environnemental du site principal de ce projet pour utiliser cette branche. Attention ! Si vous souhaitez vous assurer qu'il n'existe pas d'autre dossier nommé `comfyui_LLM_party` dans le dossier `custom node`.
1. Le nœud de chargeur local VLM prend désormais en charge [deepseek-ai/Janus-Pro](https://huggingface.co/deepseek-ai/Janus-Pro-1B), exemple de flux de travail : [Janus-Pro](workflow/deepseek-janus-pro.json)  
1. Le nœud de chargeur local VLM prend désormais en charge [Qwen/Qwen2.5-VL-3B-Instruct](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct), cependant, vous devez mettre à jour le transformateur vers la dernière version (```pip install -U transformers```), flux de travail exemple : [qwen-vl](workflow/qwen-vl.json)
1. Un nouveau nœud de stockage d'images a été ajouté, prenant en charge le service d'hébergement d'images https://sm.ms (le domaine pour la Chine est https://smms.app) ainsi que https://imgbb.com. D'autres services d'hébergement d'images seront pris en charge à l'avenir. Exemple de flux de travail : [Hébergement d'images](workflow/图床.json)  
1. ~~L'hébergement d'images compatible par défaut pour party a été mis à jour vers le domaine [imgbb](https://imgbb.io). L'ancien hébergement n'était pas convivial pour les utilisateurs de la Chine continentale, il a donc été remplacé.~~ Je suis désolé, le service API d'hébergement d'images de https://imgbb.io semble avoir été interrompu, donc le code a été rétabli à l'original https://imgbb.com. Merci pour votre compréhension. À l'avenir, je vais mettre à jour un nœud qui supportera davantage d'hébergements d'images.
1. L'outil [MCP](https://modelcontextprotocol.io/introduction) a été mis à jour, vous pouvez modifier la configuration dans le fichier '[mcp_config.json](mcp_config.json)' situé dans le dossier du projet party pour ajuster la connexion au serveur MCP souhaité. Vous pouvez trouver ici divers paramètres de configuration des serveurs MCP que vous souhaitez ajouter : [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers). La configuration par défaut de ce projet est le serveur Everything, qui sert à tester si le serveur MCP fonctionne correctement. Workflow de référence : [start_with_MCP](workflow/start_with_MCP.json). Note pour les développeurs : le nœud d'outil MCP peut se connecter au serveur MCP que vous avez configuré, puis transformer les outils du serveur en outils directement utilisables par LLM. En configurant différents serveurs locaux ou cloud, vous pouvez expérimenter tous les outils LLM disponibles dans le monde.

## Instructions d'utilisation
1. Pour les instructions d'utilisation des nœuds, veuillez consulter : [怎么使用节点](https://github.com/heshengtao/Let-LLM-party)

2. Si vous rencontrez des problèmes avec le plugin ou si vous avez d'autres questions, n'hésitez pas à rejoindre le groupe QQ : [931057213](img/Q群.jpg) |discord：[discord](https://discord.gg/f2dsAKKr2V).

4. Pour plus de flux de travail, veuillez consulter le dossier [workflow](workflow).

## Tutoriels vidéo
<a href="https://space.bilibili.com/26978344">
  <img src="img/B.png" width="100" height="100" style="border-radius: 80%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://www.youtube.com/@LLM-party">
  <img src="img/YT.png" width="100" height="100" style="border-radius: 80%; overflow: hidden;" alt="octocat"/>
</a>

## Support du modèle
1. Prise en charge de tous les appels API au format OpenAI (en combinaison avec [oneapi](https://github.com/songquanpeng/one-api), il est possible d'appeler presque toutes les API LLM, ainsi que toutes les API de transit). Pour le choix de base_url, veuillez vous référer à [config.ini.example](config.ini.example). Actuellement, les API testées incluent :
* [openai](https://platform.openai.com/docs/api-reference/chat/create) (Parfaitement compatible avec tous les modèles OpenAI, y compris les séries 4o et o1!)
* [ollama](https://github.com/ollama/ollama) (Recommandé! Si vous appelez localement, il est fortement recommandé d'utiliser la méthode ollama pour héberger votre modèle local!)
* [Azure OpenAI](https://azure.microsoft.com/zh-cn/products/ai-services/openai-service/)
* [llama.cpp](https://github.com/ggerganov/llama.cpp?tab=readme-ov-file#web-server) (Recommandé! Si vous souhaitez utiliser le modèle au format gguf local, vous pouvez utiliser l'API du projet llama.cpp pour accéder à ce projet!)
* [Grok](https://x.ai/api)
* [通义千问/qwen](https://help.aliyun.com/zh/dashscope/developer-reference/compatibility-of-openai-with-dashscope/?spm=a2c4g.11186623.0.0.7b576019xkArPq)
* [智谱清言/glm](https://open.bigmodel.cn/dev/api#http_auth)
* [deepseek](https://platform.deepseek.com/api-docs/zh-cn/)
* [kimi/moonshot](https://platform.moonshot.cn/docs/api/chat#%E5%9F%BA%E6%9C%AC%E4%BF%A1%E6%81%AF)
* [doubao](https://www.volcengine.com/docs/82379/1263482)
* [讯飞星火/spark](https://xinghuo.xfyun.cn/sparkapi?scr=price)
* [Gemini](https://developers.googleblog.com/zh-hans/gemini-is-now-accessible-from-the-openai-library/) (Le nœud de chargeur API LLM d'origine Gemini a été abandonné dans la nouvelle version, veuillez utiliser le nœud de chargeur API LLM avec l'URL de base choisie : https://generativelanguage.googleapis.com/v1beta/openai/)

2. Support de tous les appels API compatibles avec [aisuite](https://github.com/andrewyng/aisuite) :
* [anthropic/claude](https://www.anthropic.com/) 
* [aws](https://docs.aws.amazon.com/solutions/latest/generative-ai-application-builder-on-aws/api-reference.html)
* [vertex](https://cloud.google.com/vertex-ai/docs/reference/rest)
* [huggingface](https://huggingface.co/)  

3. Compatible avec la plupart des modèles locaux dans la bibliothèque transformer (le type de modèle sur le nœud de chaîne de modèles LLM local a été changé en LLM, VLM-GGUF et LLM-GGUF, correspondant au chargement direct des modèles LLM, au chargement des modèles VLM et au chargement des modèles LLM au format GGUF). Si votre modèle LLM au format VLM ou GGUF signale une erreur, veuillez télécharger la dernière version de llama-cpp-python depuis [llama-cpp-python](https://github.com/abetlen/llama-cpp-python/releases). Les modèles actuellement testés incluent :
* [ClosedCharacter/Peach-9B-8k-Roleplay](https://huggingface.co/ClosedCharacter/Peach-9B-8k-Roleplay) (recommandé ! Modèle de jeu de rôle)
* [lllyasviel/omost-llama-3-8b-4bits](https://huggingface.co/lllyasviel/omost-llama-3-8b-4bits) (recommandé ! Modèle avec des invites riches)
* [meta-llama/Llama-2-7b-chat-hf](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)
* [Qwen/Qwen2-7B-Instruct](https://huggingface.co/Qwen/Qwen2-7B-Instruct)
* [openbmb/MiniCPM-V-2_6-gguf](https://huggingface.co/openbmb/MiniCPM-V-2_6-gguf/tree/main)
* [lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF](https://huggingface.co/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/tree/main)
* [meta-llama/Llama-3.2-11B-Vision-Instruct](https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct)
* [Qwen/Qwen2.5-VL-3B-Instruct](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct)
* [deepseek-ai/Janus-Pro](https://huggingface.co/deepseek-ai/Janus-Pro-1B)

4. Téléchargement des modèles :
* [Adresse du cloud Quark](https://pan.quark.cn/s/190b41f3bbdb)  
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
* Vous pouvez configurer la langue dans le fichier `config.ini`, actuellement seules le chinois (zh_CN) et l'anglais (en_US) sont disponibles, la langue par défaut étant celle de votre système.
* Vous pouvez configurer l'installation rapide dans le fichier `config.ini`, `fast_installed` est par défaut `False`. Si vous n'avez pas besoin d'utiliser le modèle GGUF, vous pouvez le régler sur `True`.
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
**[Click here](change_log.md)**

## Prochaines étapes :
1. Plus d'adaptations de modèles;
2. Plus de façons de construire des agents;
3. Plus de fonctionnalités d'automatisation;
4. Plus de fonctionnalités de gestion de la base de connaissances;
5. Plus d'outils, plus de personas.

## Un autre projet open-source utile que j'ai réalisé :
[super-agent-party](https://github.com/heshengtao/super-agent-party) est une application d'assistant de bureau 3D IA aux possibilités infinies ! Elle prend déjà en charge RAG, la recherche sur Internet, la mémoire à long terme, l'interpréteur de code, MCP, A2A, Comfyui, le robot QQ et bien plus encore !
![image](img/vrmbot.jpeg)

## Avertissement :
Ce projet open source et son contenu (ci-après dénommé "projet") sont fournis uniquement à titre de référence et ne constituent en aucun cas une garantie expresse ou implicite. Les contributeurs du projet ne sauraient être tenus responsables de l'intégrité, de l'exactitude, de la fiabilité ou de l'applicabilité du projet. Toute action reposant sur le contenu du projet se fait à vos propres risques. En aucun cas, les contributeurs du projet ne sauraient être tenus responsables des pertes ou dommages indirects, spéciaux ou consécutifs résultant de l'utilisation du contenu du projet.
## Remerciements spéciaux
<a href="https://github.com/bigcat88">
  <img src="https://avatars.githubusercontent.com/u/13381981?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://github.com/guobalove">
  <img src="https://avatars.githubusercontent.com/u/171540731?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://github.com/SpenserCai">
  <img src="https://avatars.githubusercontent.com/u/25168945?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>

## Liste des emprunts
Certaines des fonctionnalités de ce projet s'inspirent des projets suivants, nous les remercions pour leur contribution à la communauté open source !
1. [pythongosssss/ComfyUI-Custom-Scripts](https://github.com/pythongosssss/ComfyUI-Custom-Scripts)
2. [lllyasviel/Omost](https://github.com/lllyasviel/Omost)

## Support :

### Rejoignez la communauté
Si vous rencontrez des problèmes avec le plugin ou si vous avez d'autres questions, n'hésitez pas à rejoindre notre communauté.

1. Groupe QQ : `931057213`
<div style="display: flex; justify-content: center;">
    <img src="img/Q群.jpg" style="width: 48%;" />
</div>

2. Groupe WeChat : `we_glm` (ajoutez le petit assistant WeChat pour rejoindre le groupe)

3. discord : [lien discord](https://discord.gg/f2dsAKKr2V)

### Suivez-nous
1. Si vous souhaitez rester informé des dernières fonctionnalités de ce projet, n'hésitez pas à suivre notre compte Bilibili : [派酱](https://space.bilibili.com/26978344)
2. [youtube@LLM-party](https://www.youtube.com/@LLM-party)

## Historique des étoiles

[![Star History Chart](https://api.star-history.com/svg?repos=heshengtao/comfyui_LLM_party&type=Date)](https://star-history.com/#heshengtao/comfyui_LLM_party&Date)
