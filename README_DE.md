![Bild](img/封面.png)

<div align="center">
  <a href="https://space.bilibili.com/26978344">bilibili</a> ·
  <a href="https://www.youtube.com/@comfyui-LLM-party">youtube</a> ·
  <a href="https://github.com/heshengtao/Let-LLM-party">Texttutorial</a> ·
  <a href="https://pan.quark.cn/s/190b41f3bbdb">Cloud-Disk-Adresse</a> ·
  <a href="img/Q群.jpg">QQ-Gruppe</a> ·
  <a href="https://discord.gg/f2dsAKKr2V">Discord</a> ·
  <a href="https://dcnsxxvm4zeq.feishu.cn/wiki/IyUowXNj9iH0vzk68cpcLnZXnYf">Über uns</a>
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

Comfyui_llm_party beabsichtigt, basierend auf [comfyui](https://github.com/comfyanonymous/ComfyUI), einer äußerst minimalistischen Benutzeroberfläche, eine vollständige Bibliothek von Knoten für den Aufbau von LLM-Workflows zu entwickeln. Dies ermöglicht es den Benutzern, ihre eigenen LLM-Workflows schneller und einfacher zu erstellen und diese nahtlos in ihre Bild-Workflows zu integrieren.

## Effektpräsentation
https://github.com/user-attachments/assets/945493c0-92b3-4244-ba8f-0c4b2ad4eba6

## Projektübersicht
ComfyUI LLM Party bietet Ihnen von den grundlegendsten LLM-Multitoolaufrufen und der schnellen Einrichtung Ihres eigenen AI-Assistenten bis hin zu branchenspezifischen Lösungen wie Wortvektor-RAG und GraphRAG zur lokalen Verwaltung von Wissensdatenbanken eine umfassende Palette. Von einfachen Agenten-Pipelines bis hin zu komplexen Interaktionsmodellen zwischen Agenten, wie radialen und zirkulären Interaktionen; von den Anforderungen individueller Nutzer, ihre sozialen Apps (QQ, Feishu, Discord) anzubinden, bis hin zu den Bedürfnissen von Streamern nach einem One-Stop-LLM+TTS+ComfyUI-Workflow; von den einfachen Einstiegsmöglichkeiten für gewöhnliche Studierende bis zu den verschiedenen Parametereinstellungs-Interfaces, die von Forschenden häufig genutzt werden, und der Modellanpassung – all dies finden Sie in der ComfyUI LLM Party.

## Schnellstart
0. Wenn Sie ComfyUI noch nie verwendet haben und beim Installieren von LLM Party in ComfyUI auf einige Abhängigkeitsprobleme stoßen, klicken Sie [hier](https://drive.google.com/file/d/1T9C7gEbd-w_zf9GqZO1VeI3z8ek8clpX/view?usp=sharing), um das **Windows**-Portable-Paket mit LLM Party herunterzuladen. Achtung! Dieses tragbare Paket enthält nur die beiden Plugins Party und Manager und ist nur für das Windows-System geeignet.(Wenn Sie LLM party auf einem bestehenden ComfyUI installieren müssen, kann dieser Schritt übersprungen werden.)
1. Ziehen Sie die folgenden Workflows in Ihr comfyui und verwenden Sie dann [comfyui-Manager](https://github.com/ltdrdata/ComfyUI-Manager), um die fehlenden Knoten zu installieren.
  - Verwenden Sie die API, um LLM aufzurufen: [start_with_LLM_api](workflow/start_with_LLM_api.json)
  - Verwendung von aisuite zur Aufruf von LLM: [start_with_aisuite](workflow/start_with_aisuite.json)
  - Verwalten Sie lokale LLMs mit ollama: [start_with_Ollama](workflow/ollama.json)
  - Verwenden Sie lokale LLMs im verteilten Format: [start_with_LLM_local](workflow/start_with_LLM_local.json)
  - Verwenden Sie lokale LLMs im GGUF-Format: [start_with_LLM_GGUF](workflow/start_with_GGUF.json)
  - Verwenden Sie lokale VLMs im verteilten Format: [start_with_VLM_local](workflow/start_with_VLM_local.json) （Derzeit wird Unterstützung für [Llama-3.2-Vision](https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct)/[Qwen/Qwen2.5-VL](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct)/[deepseek-ai/Janus-Pro](https://huggingface.co/deepseek-ai/Janus-Pro-1B) geboten）
  - Verwenden Sie lokale VLMs im GGUF-Format: [start_with_VLM_GGUF](workflow/start_with_llava.json)
  - Verwenden Sie die API, um LLM aufzurufen, um SD-Stichwörter zu generieren und Bilder zu erstellen: [beginnen_mit_VLM_API_für_SD](workflow/start_with_VLM_API_for_SD.json)
  - Verwenden Sie ollama, um minicpm aufzurufen, um SD-Stichwörter zu generieren und Bilder zu erstellen: [beginnen_mit_ollama_minicpm_für_SD](workflow/start_with_ollama_minicpm_for_SD.json)
  - Verwenden Sie qwen-vl lokal, um SD-Stichwörter zu generieren und Bilder zu erstellen: [beginnen_mit_qwen_vl_lokal_für_SD](workflow/start_with_qwen_vl_local_for_SD.json)
2. Wenn Sie die API verwenden, füllen Sie im API LLM-Ladeknoten Ihre `base_url` (es kann eine Relay-API sein, stellen Sie sicher, dass sie mit `/v1/` endet) und `api_key` aus. Beispiel: `https://api.openai.com/v1/`
3. Wenn Sie ollama verwenden, aktivieren Sie die Option `is_ollama` im API LLM-Ladeknoten, ohne `base_url` und `api_key` auszufüllen.
4. Wenn Sie ein lokales Modell verwenden, geben Sie im lokalen Modell-Ladeknoten Ihren Modellpfad ein, z.B.: `E:\model\Llama-3.2-1B-Instruct`. Sie können auch die Huggingface Modell-Repo-ID im lokalen Modell-Ladeknoten eingeben, z.B.: `lllyasviel/omost-llama-3-8b-4bits`.
5. Aufgrund der hohen Nutzungsschwelle dieses Projekts hoffe ich, dass Sie sich die Zeit nehmen, die Projektseite gründlich zu lesen, auch wenn Sie den Schnellstart gewählt haben.

## Neueste Updates
1. Der LLM-API-Knoten unterstützt jetzt den Stream-Ausgabemodus, wobei der von der API zurückgegebene Text in der Konsole in einem Stream angezeigt wird, sodass Sie die Ausgabe der API in Echtzeit sehen können, ohne auf den Abschluss der gesamten Anfrage warten zu müssen.
2. Der LLM-API-Knoten hat eine Ausgabe von reasoning_content hinzugefügt, die in der Lage ist, das Reasoning und die Antwort des R1-Modells automatisch zu trennen.
3. Ein neues Repository-Zweig namens only_api wurde hinzugefügt, das nur den Teil enthält, der die API aufruft, was es Nutzern, die nur API-Aufrufe benötigen, erleichtert. Sie müssen lediglich im `custom tool`-Ordner von `comfyui` den Befehl `git clone -b only_api https://github.com/heshengtao/comfyui_LLM_party.git` verwenden und dann den Umgebungsbereitstellungsplan der Hauptseite dieses Projekts befolgen, um diesen Zweig zu verwenden. Achtung! Wenn Sie sicherstellen möchten, dass im `custom tool`-Ordner keine anderen Ordner mit dem Namen `comfyui_LLM_party` vorhanden sind.
1. Der VLM lokale Ladegerät-Knoten unterstützt nun [deepseek-ai/Janus-Pro](https://huggingface.co/deepseek-ai/Janus-Pro-1B), Beispiel-Workflow : [Janus-Pro](workflow/deepseek-janus-pro.json)
1. Der lokale VLM-Loader-Knoten unterstützt jetzt [Qwen/Qwen2.5-VL-3B-Instruct](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct), jedoch müssen Sie den Transformer auf die neueste Version aktualisieren (```pip install -U transformers```), Beispiel-Workflow : [qwen-vl](workflow/qwen-vl.json)
1. Es wurde ein neuer Bildspeicher-Knoten hinzugefügt, der den Bildhosting-Dienst https://sm.ms (das Domain für China ist https://smms.app) sowie https://imgbb.com unterstützt. In Zukunft werden weitere Bildhosting-Dienste unterstützt. Beispiel-Workflow: [Bildhosting](workflow/图床.json)
1. ~~Der standardmäßig kompatible Bildhosting-Dienst für party wurde auf die Domain [imgbb](https://imgbb.io) aktualisiert. Der vorherige Dienst war für Nutzer aus dem chinesischen Festland nicht benutzerfreundlich, daher wurde er ersetzt.~~ Es tut mir leid, der API-Dienst für Bildhosting von https://imgbb.io scheint eingestellt worden zu sein, weshalb der Code auf das ursprüngliche https://imgbb.com zurückgesetzt wurde. Vielen Dank für Ihr Verständnis. In Zukunft werde ich einen Knoten aktualisieren, der mehr Bildhosting-Dienste unterstützt.
1. Das [MCP](https://modelcontextprotocol.io/introduction) Tool wurde aktualisiert. Sie können die Konfiguration in der Datei '[mcp_config.json](mcp_config.json)' im Party-Projektordner ändern, um den MCP-Server anzupassen, mit dem Sie sich verbinden möchten. Hier finden Sie verschiedene Konfigurationsparameter für MCP-Server, die Sie hinzufügen möchten: [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers). Die Standardkonfiguration dieses Projekts ist der Everything-Server, der dazu dient, zu überprüfen, ob der MCP-Server ordnungsgemäß funktioniert. Referenz-Workflow: [start_with_MCP](workflow/start_with_MCP.json). Hinweis für Entwickler: Der MCP-Toolknoten kann sich mit dem von Ihnen konfigurierten MCP-Server verbinden und die Werkzeuge des Servers in direkt verwendbare Werkzeuge für LLM umwandeln. Durch die Konfiguration verschiedener lokaler oder Cloud-Server können Sie alle LLM-Werkzeuge erleben, die es auf der Welt gibt.

## Gebrauchsanweisung
1. Bitte beziehen Sie sich auf die Anweisungen zur Verwendung der Knoten: [怎么使用节点](https://github.com/heshengtao/Let-LLM-party)

2. Bei Problemen mit dem Plugin oder anderen Fragen freuen wir uns über Ihren Beitritt zur QQ-Gruppe: [931057213](img/Q群.jpg) | discord：[discord](https://discord.gg/f2dsAKKr2V).

4. Weitere Workflows finden Sie im Ordner [workflow](workflow).

## Video-Tutorials
<a href="https://space.bilibili.com/26978344">
  <img src="img/B.png" width="100" height="100" style="border-radius: 80%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://www.youtube.com/@comfyui-LLM-party">
  <img src="img/YT.png" width="100" height="100" style="border-radius: 80%; overflow: hidden;" alt="octocat"/>
</a>

## Modellunterstützung
1. Unterstützung aller API-Aufrufe im OpenAI-Format (in Kombination mit [oneapi](https://github.com/songquanpeng/one-api) können nahezu alle LLM-APIs aufgerufen werden, ebenso alle Transfer-APIs). Die Auswahl der base_url erfolgt nach [config.ini.example](config.ini.example). Bisher getestete Modelle sind:
* [openai](https://platform.openai.com/docs/api-reference/chat/create) (Perfekt kompatibel mit allen OpenAI-Modellen, einschließlich der 4o- und o1-Serien!)
* [ollama](https://github.com/ollama/ollama) (Empfohlen! Wenn Sie lokal aufrufen, wird dringend empfohlen, die ollama-Methode zu verwenden, um Ihr lokales Modell zu hosten!)
* [Azure OpenAI](https://azure.microsoft.com/zh-cn/products/ai-services/openai-service/)
* [llama.cpp](https://github.com/ggerganov/llama.cpp?tab=readme-ov-file#web-server) (Empfohlen! Wenn Sie das lokale gguf-Formatmodell verwenden möchten, können Sie die API des llama.cpp-Projekts verwenden, um auf dieses Projekt zuzugreifen!)
* [Grok](https://x.ai/api)
* [Tongyi Qianwen/qwen](https://help.aliyun.com/zh/dashscope/developer-reference/compatibility-of-openai-with-dashscope/?spm=a2c4g.11186623.0.0.7b576019xkArPq)
* [Zhipu Qinyan/glm](https://open.bigmodel.cn/dev/api#http_auth)
* [deepseek](https://platform.deepseek.com/api-docs/zh-cn/)
* [kimi/moonshot](https://platform.moonshot.cn/docs/api/chat#%E5%9F%BA%E6%9C%AC%E4%BF%A1%E6%81%AF)
* [doubao](https://www.volcengine.com/docs/82379/1263482)
* [讯飞星火/spark](https://xinghuo.xfyun.cn/sparkapi?scr=price)
* [Gemini](https://developers.googleblog.com/zh-hans/gemini-is-now-accessible-from-the-openai-library/) (Der ursprüngliche Gemini API LLM Ladepunkt wurde in der neuen Version eingestellt, bitte verwenden Sie den LLM API Ladepunkt mit der gewählten Basis-URL: https://generativelanguage.googleapis.com/v1beta/openai/)

2. Unterstützung aller API-Aufrufe, die mit [aisuite](https://github.com/andrewyng/aisuite) kompatibel sind:
* [anthropic/claude](https://www.anthropic.com/) 
* [aws](https://docs.aws.amazon.com/solutions/latest/generative-ai-application-builder-on-aws/api-reference.html)
* [vertex](https://cloud.google.com/vertex-ai/docs/reference/rest)
* [huggingface](https://huggingface.co/)

3. Kompatibel mit den meisten lokalen Modellen in der Transformer-Bibliothek (der Modelltyp auf dem lokalen LLM-Modellkettenknoten wurde in LLM, VLM-GGUF und LLM-GGUF geändert, was dem direkten Laden von LLM-Modellen, dem Laden von VLM-Modellen und dem Laden von LLM-Modellen im GGUF-Format entspricht). Wenn Ihr VLM- oder GGUF-Format-LLM-Modell einen Fehler meldet, laden Sie bitte die neueste Version von llama-cpp-python von [llama-cpp-python](https://github.com/abetlen/llama-cpp-python/releases) herunter. Derzeit getestete Modelle umfassen:
* [ClosedCharacter/Peach-9B-8k-Roleplay](https://huggingface.co/ClosedCharacter/Peach-9B-8k-Roleplay) (empfohlen! Rollenspiel-Modell)
* [lllyasviel/omost-llama-3-8b-4bits](https://huggingface.co/lllyasviel/omost-llama-3-8b-4bits) (empfohlen! Reichhaltiges Prompt-Modell)
* [meta-llama/Llama-2-7b-chat-hf](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)
* [Qwen/Qwen2-7B-Instruct](https://huggingface.co/Qwen/Qwen2-7B-Instruct)
* [openbmb/MiniCPM-V-2_6-gguf](https://huggingface.co/openbmb/MiniCPM-V-2_6-gguf/tree/main)
* [lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF](https://huggingface.co/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/tree/main)
* [meta-llama/Llama-3.2-11B-Vision-Instruct](https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct)
* [Qwen/Qwen2.5-VL-3B-Instruct](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct)
* [deepseek-ai/Janus-Pro](https://huggingface.co/deepseek-ai/Janus-Pro-1B)

4. Modells download:
* [Quark Cloud Adresse](https://pan.quark.cn/s/190b41f3bbdb)
* [Baidu Cloud Adresse](https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu), Entnahmecode: qyhu

## Download
Verwenden Sie eine der folgenden Methoden zur Installation
### Methode eins:
1. Suchen Sie im [ComfyUI-Manager](https://github.com/ltdrdata/ComfyUI-Manager) nach `comfyui_LLM_party` und installieren Sie es mit einem Klick.
2. Starten Sie ComfyUI neu.
### Methode zwei:
1. Navigieren Sie zum Unterordner `custom_nodes` im Hauptordner von ComfyUI.
2. Klonen Sie dieses Repository: `git clone https://github.com/heshengtao/comfyui_LLM_party.git`

### Methode drei:
1. Klicken Sie oben rechts auf `CODE`.
2. Klicken Sie auf `download zip`.
3. Entpacken Sie das heruntergeladene Zip-Archiv in den Unterordner `custom_nodes` des Hauptordners von ComfyUI.

## Umgebungsbereitstellung
1. Navigieren Sie zum Projektordner von `comfyui_LLM_party`.
2. Geben Sie im Terminal `pip install -r requirements.txt` ein, um die benötigten Drittanbieterbibliotheken in der ComfyUI-Umgebung zu installieren. Bitte beachten Sie, ob Sie in der ComfyUI-Umgebung installieren, und achten Sie auf `pip`-Fehlermeldungen im Terminal.
3. Wenn Sie den ComfyUI-Launcher verwenden, müssen Sie im Terminal `Pfad im Launcher-Konfigurationsdatei\python_embeded\python.exe -m pip install -r requirements.txt` eingeben, um die Installation durchzuführen. Der Ordner `python_embeded` befindet sich in der Regel auf derselben Ebene wie Ihr `ComfyUI`-Ordner.
4. Wenn Sie auf einige Umgebungsprobleme stoßen, können Sie versuchen, die Abhängigkeiten aus `requirements_fixed.txt` zu verwenden.
## Konfiguration
* Sie können die Sprache in der Datei `config.ini` konfigurieren, gegenwärtig sind nur Chinesisch (zh_CN) und Englisch (en_US) verfügbar, die Standardeinstellung entspricht der Sprache Ihres Systems.
* Sie können die Schnellinstallation in der Datei `config.ini` konfigurieren, `fast_installed` hat standardmäßig den Wert `False`. Wenn Sie das GGUF-Modell nicht verwenden müssen, können Sie es auf `True` einstellen.
* Du kannst eine der folgenden Methoden verwenden, um den APIKEY zu konfigurieren.
### Methode Eins:
1. Öffne die Datei `config.ini` im Projektordner von `comfyui_LLM_party`.
2. Gib in der `config.ini` deinen `openai_api_key` und `base_url` ein.
3. Wenn du das Ollama-Modell verwendest, trage in `base_url` `http://127.0.0.1:11434/v1/` ein, in `openai_api_key` schreibe `ollama` und in `model_name` gib deinen Modellnamen ein, z. B.: llama3.
4. Wenn du Google Search oder Bing Search Tools verwenden möchtest, gib in der `config.ini` deinen `google_api_key`, `cse_id` oder `bing_api_key` ein.
5. Wenn du Bildeingaben für LLM verwenden möchtest, wird empfohlen, den Bilddienst imgBB zu nutzen. Trage in der `config.ini` deinen `imgbb_api` ein.
6. Jedes Modell kann in der Datei `config.ini` separat konfiguriert werden. Du kannst die Datei `config.ini.example` als Referenz verwenden. Nachdem du alles konfiguriert hast, musst du nur noch `model_name` im Knoten eingeben.

### Methode Zwei:
1. Öffne die Benutzeroberfläche von ComfyUI.
2. Erstelle einen neuen LLM-Knoten und gib direkt in den Knoten deinen `openai_api_key` und `base_url` ein.
3. Wenn du das Ollama-Modell verwendest, benutze den LLM_api-Knoten, trage in `base_url` `http://127.0.0.1:11434/v1/` ein, in `api_key` schreibe `ollama` und in `model_name` gib deinen Modellnamen ein, z. B.: llama3.
4. Wenn du Bildeingaben für LLM verwenden möchtest, wird empfohlen, den Bilddienst imgBB zu nutzen. Gib in dem Knoten deinen `imgbb_api_key` ein.
## Änderungsprotokoll
**[Click here](change_log.md)**

## Nächste Schritte:
1. Mehr Modellanpassungen;
2. Mehr Möglichkeiten zum Aufbau von Agenten;
3. Mehr Automatisierungsfunktionen;
4. Mehr Funktionen zur Verwaltung von Wissensdatenbanken;
5. Mehr Werkzeuge, mehr Personas.

## Haftungsausschluss:
Dieses Open-Source-Projekt und seine Inhalte (im Folgenden „Projekt“) dienen nur zu Informationszwecken und bedeuten keine ausdrückliche oder stillschweigende Garantie. Die Projektbeitragsleistenden übernehmen keine Verantwortung für die Vollständigkeit, Genauigkeit, Zuverlässigkeit oder Anwendbarkeit des Projekts. Jegliche Handlungen, die auf den Inhalten des Projekts basieren, erfolgen auf eigenes Risiko. Unter keinen Umständen haften die Projektbeitragsleistenden für indirekte, spezielle oder zufällige Verluste oder Schäden, die aus der Nutzung der Inhalte des Projekts resultieren.
## Besonderer Dank
<a href="https://github.com/bigcat88">
  <img src="https://avatars.githubusercontent.com/u/13381981?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://github.com/guobalove">
  <img src="https://avatars.githubusercontent.com/u/171540731?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://github.com/SpenserCai">
  <img src="https://avatars.githubusercontent.com/u/25168945?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>

## Entlehnungen
Einige Knoten in diesem Projekt basieren auf den folgenden Projekten. Wir danken ihnen für ihren Beitrag zur Open-Source-Community!
1. [pythongosssss/ComfyUI-Custom-Scripts](https://github.com/pythongosssss/ComfyUI-Custom-Scripts)
2. [lllyasviel/Omost](https://github.com/lllyasviel/Omost)

## Unterstützung:

### Treten Sie der Gemeinschaft bei
Wenn es Probleme mit dem Plugin gibt oder Sie andere Fragen haben, sind Sie herzlich eingeladen, unserer Gemeinschaft beizutreten.

1. QQ-Gruppe: `931057213`
<div style="display: flex; justify-content: center;">
    <img src="img/Q群.jpg" style="width: 48%;" />
</div>

2. WeChat-Gruppe: `we_glm` (Fügen Sie den kleinen Assistenten zu WeChat hinzu, um der Gruppe beizutreten)

3. Discord:[discord链接](https://discord.gg/f2dsAKKr2V)

### Folgen Sie uns
1. Wenn Sie die neuesten Funktionen dieses Projekts kontinuierlich verfolgen möchten, heißen wir Sie herzlich willkommen, unseren Bilibili-Account zu abonnieren: [派酱](https://space.bilibili.com/26978344)
2. [youtube@comfyui-LLM-party](https://www.youtube.com/@comfyui-LLM-party)

### Unterstützung durch Spenden
Wenn meine Arbeit Ihnen einen Mehrwert bietet, ziehen Sie bitte in Betracht, mir einen Kaffee auszugeben! Ihre Unterstützung belebt nicht nur das Projekt, sondern erwärmt auch das Herz der Kreatoren.☕💖 Jede Tasse zählt!
<div style="display:flex; justify-content:space-between;">
    <img src="img/zhifubao.jpg" style="width: 48%;" />
    <img src="img/wechat.jpg" style="width: 48%;" />
</div>

## Sternenverlauf

[![Star History Chart](https://api.star-history.com/svg?repos=heshengtao/comfyui_LLM_party&type=Date)](https://star-history.com/#heshengtao/comfyui_LLM_party&Date)
