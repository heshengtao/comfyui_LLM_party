![Bild](img/封面.png)

<div align="center">
  <a href="https://space.bilibili.com/26978344">Videotutorial</a> ·
  <a href="how_to_use_nodes_ZH.md">Texttutorial</a> ·
  <a href="workflow_tutorial/">Workflow-Tutorial</a> ·
  <a href="https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu">Baudisk-Link</a> ·
  <a href="img/Q群.jpg">QQ-Gruppe</a> ·
  <a href="https://discord.gg/gxrQAYy6">Discord</a> ·
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
1. Ziehen Sie die folgenden Workflows in Ihr comfyui und verwenden Sie dann [comfyui-Manager](https://github.com/ltdrdata/ComfyUI-Manager), um die fehlenden Knoten zu installieren.
  - Verwenden Sie die API, um LLM aufzurufen: [start_with_LLM_api](workflow/start_with_LLM_api.json)
  - Verwalten Sie lokale LLMs mit ollama: [start_with_Ollama](workflow/ollama.json)
  - Verwenden Sie lokale LLMs im verteilten Format: [start_with_LLM_local](workflow/start_with_LLM_local.json)
  - Verwenden Sie lokale LLMs im GGUF-Format: [start_with_LLM_GGUF](workflow/start_with_GGUF.json)
  - Verwenden Sie lokale VLMs im verteilten Format: [start_with_VLM_local](https://github.com/heshengtao/comfyui_LLM_party/blob/main/workflow_tutorial/LLM_Party%20for%20Llama3.2%20-Vision%EF%BC%88%E5%B8%A6%E8%AE%B0%E5%BF%86%EF%BC%89.json) (Testphase, derzeit nur [Llama-3.2-Vision-Instruct](https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct) unterstützt)
  - Verwenden Sie lokale VLMs im GGUF-Format: [start_with_VLM_GGUF](workflow/start_with_llava.json)
2. Wenn Sie die API verwenden, füllen Sie im API LLM-Ladeknoten Ihre `base_url` (es kann eine Relay-API sein, stellen Sie sicher, dass sie mit `/v1/` endet) und `api_key` aus. Beispiel: `https://api.openai.com/v1/`
3. Wenn Sie ollama verwenden, aktivieren Sie die Option `is_ollama` im API LLM-Ladeknoten, ohne `base_url` und `api_key` auszufüllen.
4. Wenn Sie ein lokales Modell verwenden, geben Sie im lokalen Modell-Ladeknoten Ihren Modellpfad ein, z.B.: `E:\model\Llama-3.2-1B-Instruct`. Sie können auch die Huggingface Modell-Repo-ID im lokalen Modell-Ladeknoten eingeben, z.B.: `lllyasviel/omost-llama-3-8b-4bits`.
5. Aufgrund der hohen Nutzungsschwelle dieses Projekts hoffe ich, dass Sie sich die Zeit nehmen, die Projektseite gründlich zu lesen, auch wenn Sie den Schnellstart gewählt haben.

## Neueste Updates
1. Das [searxng](https://github.com/searxng/searxng)-Tool wurde hinzugefügt, das Suchanfragen im gesamten Web aggregieren kann. Perplexica basiert ebenfalls auf diesem Aggregationssuchwerkzeug, sodass Sie auf Ihrer Party ein Perplexica einrichten können. Sie können das öffentliche Image searxng/searxng in Docker bereitstellen, es dann mit `docker run -d -p 8080:8080 searxng/searxng` starten und mit `http://localhost:8080` darauf zugreifen. Sie können diese URL `http://localhost:8080` in das searxng-Tool der Party einfügen und dann searxng als Werkzeug für LLM verwenden.
1. **Großes Update!!!** Jetzt können Sie jeden ComfyUI-Workflow in einen LLM-Toolknoten kapseln. Sie können Ihren LLM gleichzeitig mehrere ComfyUI-Workflows steuern lassen. Wenn Sie möchten, dass er einige Aufgaben erledigt, kann er basierend auf Ihrem Prompt den entsprechenden ComfyUI-Workflow auswählen, Ihre Aufgabe erledigen und Ihnen das Ergebnis zurückgeben. Beispiel-Workflow: [comfyui_workflows_tool](workflow/把任意workflow当作LLM_tool.json). Die spezifischen Schritte sind wie folgt:
   - Verbinden Sie zunächst die Texteingabeschnittstelle des Workflows, den Sie als Tool kapseln möchten, mit dem "user_prompt"-Ausgang des "Workflow starten"-Knotens. Dies ist der Ort, an dem der Prompt übergeben wird, wenn das LLM das Tool aufruft.
   - Verbinden Sie die Stellen, an denen Sie Text und Bilder ausgeben möchten, mit den entsprechenden Eingangspositionen des "Workflow beenden"-Knotens.
   - Speichern Sie diesen Workflow als API (Sie müssen den Entwicklermodus in den Einstellungen aktivieren, um diese Schaltfläche zu sehen).
   - Speichern Sie diesen Workflow im Ordner workflow_api dieses Projekts.
   - Starten Sie ComfyUI neu und erstellen Sie einen einfachen LLM-Workflow, z.B.: [start_with_LLM_api](workflow/start_with_LLM_api.json).
   - Fügen Sie diesem LLM-Knoten einen "Workflow-Tool"-Knoten hinzu und verbinden Sie ihn mit dem Tool-Eingang des LLM-Knotens.
   - Schreiben Sie im "Workflow-Tool"-Knoten den Namen der Workflow-Datei, die Sie aufrufen möchten, in das erste Eingabefeld, z.B.: draw.json. Sie können mehrere Workflow-Dateinamen schreiben. Schreiben Sie im zweiten Eingabefeld die Funktion jedes Workflows, damit das LLM versteht, wie diese Workflows verwendet werden.
   - Führen Sie es aus, um zu sehen, wie das LLM Ihren gekapselten Workflow aufruft und Ihnen das Ergebnis zurückgibt. Wenn das Ergebnis ein Bild ist, verbinden Sie den "Bildvorschau"-Knoten mit dem Bildausgang des LLM-Knotens, um das generierte Bild anzuzeigen. Achtung! Diese Methode ruft ein neues ComfyUI auf Ihrem Port 8190 auf, bitte belegen Sie diesen Port nicht. Auf Windows- und Mac-Systemen wird ein neues Terminal geöffnet, bitte schließen Sie es nicht. Das Linux-System verwendet den screen-Prozess, um dies zu erreichen. Wenn Sie es nicht benötigen, schließen Sie diesen screen-Prozess, andernfalls wird Ihr Port immer belegt.

![workflow_tool](img/workflowtool.png)

## Gebrauchsanweisung
1. Bitte beziehen Sie sich auf die Anweisungen zur Verwendung der Knoten: [怎么使用节点](how_to_use_nodes.md)

2. Bei Problemen mit dem Plugin oder anderen Fragen freuen wir uns über Ihren Beitritt zur QQ-Gruppe: [931057213](img/Q群.jpg)
3. Für das Workflow-Tutorial siehe bitte: [Workflow-Tutorial](workflow_tutorial/). Vielen Dank an [HuangYuChuh](https://github.com/HuangYuChuh) für seinen Beitrag!

4. Konto für fortgeschrittene Workflow-Anwendungen: [openart](https://openart.ai/workflows/profile/comfyui_llm_party?sort=latest&tab=creation)

4. Weitere Workflows finden Sie im Ordner [workflow](workflow).

## Video-Tutorials
1. [Schritt-für-Schritt-Anleitung zum Aufbau eines modularen intelligenten Agenten (sehr einfach!)](https://www.bilibili.com/video/BV1JZ421v7Tw/?vd_source=f229e378448918b84afab7c430c6a75b)

2. [Anleitung zur Anbindung von GPT-4o an comfyui | Ermöglichen Sie, dass ein Workflow einen anderen Workflow aufruft | Lassen Sie LLM zu einem Tool werden](https://www.bilibili.com/video/BV1JJ4m1A789/?spm_id_from=333.999.0.0&vd_source=f229e378448918b84afab7c430c6a75b)

3. [Verkleiden Sie Ihren Workflow als GPT-Anbindung an WeChat | Omost-kompatibel! Kreieren Sie flexibel Ihr eigenes dalle3](https://www.bilibili.com/video/BV1DT421a7KY/?spm_id_from=333.999.0.0)

4. [Wie man interaktive Geschichten in comfyui spielt](https://www.bilibili.com/video/BV15y411q78L/?spm_id_from=333.999.0.0&vd_source=f229e378448918b84afab7c430c6a75b)

5. [AI-Freundin, die deiner Form entspricht | Implementierung von graphRAG auf comfyui, Verknüpfung mit neoa4j | Anbindung von comfyui-Workflows an die Streamlit-Frontend](https://www.bilibili.com/video/BV1dS421R7Au/?spm_id_from=333.999.0.0&vd_source=f229e378448918b84afab7c430c6a75b)
## Modellunterstützung
1. Unterstützung aller API-Aufrufe im OpenAI-Format (in Kombination mit [oneapi](https://github.com/songquanpeng/one-api) können nahezu alle LLM-APIs aufgerufen werden, ebenso alle Transfer-APIs). Die Auswahl der base_url erfolgt nach [config.ini.example](config.ini.example). Bisher getestete Modelle sind:
* [openai](https://platform.openai.com/docs/api-reference/chat/create) (Perfekt kompatibel mit allen OpenAI-Modellen, einschließlich der 4o- und o1-Serien!)
* [ollama](https://github.com/ollama/ollama) (Empfohlen! Wenn Sie lokal aufrufen, wird dringend empfohlen, die ollama-Methode zu verwenden, um Ihr lokales Modell zu hosten!)
* [llama.cpp](https://github.com/ggerganov/llama.cpp?tab=readme-ov-file#web-server) (Empfohlen! Wenn Sie das lokale gguf-Formatmodell verwenden möchten, können Sie die API des llama.cpp-Projekts verwenden, um auf dieses Projekt zuzugreifen!)
* [Tongyi Qianwen/qwen](https://help.aliyun.com/zh/dashscope/developer-reference/compatibility-of-openai-with-dashscope/?spm=a2c4g.11186623.0.0.7b576019xkArPq)
* [Zhipu Qinyan/glm](https://open.bigmodel.cn/dev/api#http_auth)
* [deepseek](https://platform.deepseek.com/api-docs/zh-cn/)
* [kimi/moonshot](https://platform.moonshot.cn/docs/api/chat#%E5%9F%BA%E6%9C%AC%E4%BF%A1%E6%81%AF)
* [Doubao](https://www.volcengine.com/docs/82379/1263482)

2. Unterstützung von API-Aufrufen im Gemini-Format:
* [Gemini](https://aistudio.google.com/app/prompts/new_chat)

3. Kompatibel mit den meisten lokalen Modellen in der Transformer-Bibliothek (der Modelltyp auf dem lokalen LLM-Modellkettenknoten wurde in LLM, VLM-GGUF und LLM-GGUF geändert, was dem direkten Laden von LLM-Modellen, dem Laden von VLM-Modellen und dem Laden von LLM-Modellen im GGUF-Format entspricht). Wenn Ihr VLM- oder GGUF-Format-LLM-Modell einen Fehler meldet, laden Sie bitte die neueste Version von llama-cpp-python von [llama-cpp-python](https://github.com/abetlen/llama-cpp-python/releases) herunter. Derzeit getestete Modelle umfassen:
* [ClosedCharacter/Peach-9B-8k-Roleplay](https://huggingface.co/ClosedCharacter/Peach-9B-8k-Roleplay) (empfohlen! Rollenspiel-Modell)
* [lllyasviel/omost-llama-3-8b-4bits](https://huggingface.co/lllyasviel/omost-llama-3-8b-4bits) (empfohlen! Reichhaltiges Prompt-Modell)
* [meta-llama/Llama-2-7b-chat-hf](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)
* [Qwen/Qwen2-7B-Instruct](https://huggingface.co/Qwen/Qwen2-7B-Instruct)
* [xtuner/llava-llama-3-8b-v1_1-gguf](https://huggingface.co/xtuner/llava-llama-3-8b-v1_1-gguf)
* [lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF](https://huggingface.co/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/tree/main)
* [meta-llama/Llama-3.2-11B-Vision-Instruct](https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct)

4. Modells download:
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
* Die Sprache kann in der Datei `config.ini` konfiguriert werden, derzeit sind nur Chinesisch (zh_CN) und Englisch (en_US) verfügbar, standardmäßig wird die Sprache deines Systems verwendet.
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
1. Sie können im ComfyUI-Interface mit der rechten Maustaste klicken und im Kontextmenü `llm` auswählen, um den Knoten dieses Projekts zu finden. [Wie man Knoten verwendet](how_to_use_nodes_ZH.md)
2. Unterstützung für API-Integration oder lokale große Modelle. Modularer Ansatz zur Implementierung der Funktion zur Werkzeuganwendung. Bitte geben Sie beim Ausfüllen von base_url eine URL ein, die mit `/v1/` endet. Sie können [ollama](https://github.com/ollama/ollama) verwenden, um Ihre Modelle zu verwalten, und dann in base_url `http://127.0.0.1:11434/v1/` eingeben, in api_key geben Sie ollama ein und in model_name den Namen Ihres Modells, z. B.: llama3.
   - API-Integrationsbeispiel-Workflow: [start_with_LLM_api](workflow/start_with_LLM_api.json)
   - Lokales Modellintegrationsbeispiel-Workflow: [start_with_LLM_local](workflow/start_with_LLM_local.json)
   - Ollama-Integrationsbeispiel-Workflow: [ollama](workflow/ollama.json)
3. Integration eines lokalen Wissensspeichers, Unterstützung für RAG. Beispiel-Workflow: [Wissensspeicher_RAG_Suche.json](workflow/知识库RAG搜索.json)
4. Möglichkeit zur Nutzung eines Code-Interpreters
5. Möglichkeit zur Online-Abfrage, Unterstützung für Google-Suche. Beispiel-Workflow: [Filmabfrage-Workflow](workflow/电影查询工作流.json)
6. Möglichkeit, Bedingungen im ComfyUI zu implementieren, um Benutzerfragen zu kategorisieren und gezielt zu beantworten. Beispiel-Workflow: [Intelligent Kundenservice](workflow/智能客服.json)
7. Unterstützung von Rückkopplungslinks zwischen großen Modellen, um Debatten zwischen zwei großen Modellen zu ermöglichen. Beispiel-Workflow: [Trolley-Problem-Debatte](workflow/电车难题辩论赛.json)
8. Unterstützung für die Anpassung beliebiger Persönlichkeitsmasken, mit der Möglichkeit, Vorlagen für Eingabeaufforderungen zu erstellen.
9. Unterstützung für eine Vielzahl von Werkzeuganwendungen, einschließlich Wetterabfrage, Zeitabfrage, Wissensspeicher, Codeausführung, Online-Suche und gezielte Suche auf einer einzelnen Webseite.
10. Unterstützung der Nutzung von LLM als Werkzeugknoten. Beispiel-Workflow: [LLM-verschachtelung](workflow/LLM套娃.json)
11. Unterstützung für die schnelle Entwicklung eigener Webanwendungen über API+streamlit.
12. Einführung eines gefährlichen universellen Interpreternodes, der es großen Modellen ermöglicht, beliebige Aufgaben zu erledigen.
13. Es wird empfohlen, den Knoten "show_text" im Funktionsunterverzeichnis des Kontextmenüs zu verwenden, um die Ausgabe des LLM-Knotens anzuzeigen.
14. Unterstützung der visuellen Funktionen von GPT-4O! Beispiel-Workflow: [GPT-4o](workflow/GPT-4o.json)  
15. Ein neuer Workflow-Transmitter wurde hinzugefügt, der es ermöglicht, andere Workflows innerhalb Ihres Workflows aufzurufen! Beispiel-Workflow: [Aufruf eines anderen Workflows](workflow/调用另一个工作流.json)  
16. Anpassung an alle Modelle mit ähnlichen OpenAI-Schnittstellen, wie z.B.: Tongyi Qianwen/qwen, Zhiyu Qingyan/GLM, Deepseek, Kimi/Moonshot. Bitte fügen Sie die base_url, api_key und model_name dieser Modelle in den LLM-Knoten ein, um sie aufzurufen.  
17. Ein LVM-Loader wurde hinzugefügt, der es ermöglicht, LVM-Modelle lokal aufzurufen. Unterstützt wird das Modell [llava-llama-3-8b-v1_1-gguf](https://huggingface.co/xtuner/llava-llama-3-8b-v1_1-gguf); andere LVM-Modelle im GGUF-Format sollten theoretisch ebenfalls funktionieren. Beispiel-Workflow finden Sie hier: [start_with_LVM.json](workflow/start_with_LVM.json).  
18. Eine Datei `fastapi.py` wurde erstellt. Wenn Sie sie direkt ausführen, erhalten Sie eine OpenAI-Schnittstelle unter `http://127.0.0.1:8817/v1/`, sodass jede Anwendung, die GPT aufrufen kann, Ihr ComfyUI-Workflow nutzen kann! Eine detaillierte Anleitung zur Vorgehensweise wird in einem kommenden Tutorial bereitgestellt.  
19. Der LLM-Loader und die LLM-Kette wurden getrennt, sodass das Laden des Modells und die Modellspezifikation voneinander getrennt sind. Dadurch kann das Modell zwischen verschiedenen LLM-Knoten geteilt werden!  
20. Unterstützung für macOS und MPS-Geräte wurde bereits implementiert! Vielen Dank an [bigcat88](https://github.com/bigcat88) für diesen Beitrag!  
21. Es ist nun möglich, ein eigenes interaktives Erzählspiel zu erstellen, das je nach Benutzerwahl zu unterschiedlichen Enden führt! Beispiel-Workflow: [Interaktive Erzählung](workflow/互动小说.json)  
22. Anpassung an die Whisper- und TTS-Funktionen von OpenAI, die Sprachinput und -output ermöglichen. Beispiel-Workflow: [Sprachinput + Sprachausgabe](workflow/语音输入+语音输出.json)
23. Kompatibel mit [Omost](https://github.com/lllyasviel/Omost)!!! Bitte laden Sie [omost-llama-3-8b-4bits](https://huggingface.co/lllyasviel/omost-llama-3-8b-4bits) herunter und erleben Sie es sofort! Beispiel-Workflow: [start_with_OMOST](workflow/start_with_OMOST.json)  
24. Hinzugefügt wurden LLM-Tools zum Senden von Nachrichten an WeChat, DingTalk und Feishu sowie externe Funktionen, die aufgerufen werden können.  
25. Ein Text-Iterator wurde hinzugefügt, der jeweils nur einen Teil der Zeichen ausgibt. Dieser teilt den Text sicher anhand des Zeilenumbruchs und der Chunk-Größe, ohne ihn in der Mitte zu zerschneiden. chunk_overlap gibt an, wie viele Zeichen der geteilte Text überlappt. Dadurch können extrem lange Texte in großen Mengen eingegeben werden; man muss nur bedenkenlos klicken oder die Schleifen-Ausführung in ComfyUI aktivieren, um die Ausführung automatisch abzuschließen. Vergessen Sie nicht, die is_locked-Eigenschaft zu aktivieren, damit der Workflow am Ende der Eingabe automatisch gesperrt wird und nicht weiter ausgeführt wird. Beispiel-Workflow: [Text-Iterations-Eingabe](workflow/文本迭代输入.json)  
26. Im lokalen LLM-Loader und im lokalen llava-Loader wurde das Attribut model name hinzugefügt. Ist es leer, wird der lokale Pfad aus dem Knoten verwendet. Ist es nicht leer, wird der von Ihnen in `config.ini` angegebene Pfad verwendet. Ist es nicht leer und nicht in `config.ini`, wird das Modell von Hugging Face heruntergeladen oder aus dem Hugging Face-Modellspeicherverzeichnis geladen. Wenn Sie ein Modell von Hugging Face herunterladen möchten, füllen Sie das Attribut model name im Format `THUDM/glm-4-9b-chat` aus. Hinweis! Modelle, die auf diese Weise geladen werden, müssen mit der Transformer-Bibliothek kompatibel sein.  
27. Es wurden Knoten zum Parsen von JSON-Dateien und zum Abrufen von JSON-Werten hinzugefügt, mit denen Sie den Wert eines bestimmten Schlüssels aus einer Datei oder einem Text abrufen können. Vielen Dank an [guobalove](https://github.com/guobalove) für den Beitrag!
28. Der Code für den Aufruf von Werkzeugen wurde verbessert, sodass jetzt auch LLMs ohne die Funktion des Werkzeugaufrufs das Attribut is_tools_in_sys_prompt aktivieren können (lokale LLMs müssen standardmäßig nicht aktiviert werden und passen sich automatisch an). Nach der Aktivierung werden die Informationen zu den Werkzeugen in die Systemaufforderung aufgenommen, sodass das LLM auf die Werkzeuge zugreifen kann. Relevante Arbeiten zur Funktionsweise: [Achieving Tool Calling Functionality in LLMs Using Only Prompt Engineering Without Fine-Tuning](https://arxiv.org/abs/2407.04997)

29. Ein neues Verzeichnis namens custom_tool wurde erstellt, um den Code benutzerdefinierter Werkzeuge zu speichern. Sie können den Code im Verzeichnis [custom_tool](custom_tool) als Referenz verwenden und Ihren benutzerdefinierten Werkzeugcode in das custom_tool-Verzeichnis einfügen, um ihn im LLM aufzurufen.

30. Ein neues Werkzeug für Wissensgraphen wurde hinzugefügt, das eine perfekte Interaktion zwischen dem LLM und dem Wissensgraphen ermöglicht. Das LLM kann den Wissensgraphen basierend auf Ihren Eingaben ändern und aus dem Wissensgraphen ableiten, um die benötigten Antworten zu erhalten. Beispiel-Workflow: [graphRAG_neo4j](workflow/graphRAG_neo4j.json)

31. Eine Funktion für Persönlichkeits-AI wurde hinzugefügt, mit der Sie Ihre eigene Freundinnen- oder Freund-AI ohne Programmierkenntnisse entwickeln können. Unbegrenzte Gespräche, dauerhaftes Gedächtnis und stabile Charakterdarstellung sind möglich. Beispiel-Workflow: [麦洛薇人格AI](workflow/麦洛薇人格AI.json)

32. Mit diesem LLM-Werkzeuggenerator können Sie automatisch LLM-Werkzeuge erstellen. Speichern Sie den generierten Werkzeugcode in einer Python-Datei und kopieren Sie den Code in das custom_tool-Verzeichnis, um einen neuen Knoten zu schaffen. Beispiel-Workflow: [LLM工具生成器](workflow/LLM工具制造机.json).

33. Die Unterstützung für die DuckDuckGo-Suche wurde hinzugefügt, jedoch mit erheblichen Einschränkungen; es scheint, dass nur englische Schlüsselwörter eingegeben werden können und diese Schlüsselwörter nicht mehrere Konzepte enthalten dürfen. Der Vorteil liegt darin, dass es keine Einschränkungen durch API-Schlüssel gibt.

34. Es wurde die Funktionalität zur getrennten Abfrage mehrerer Wissensdatenbanken unterstützt, sodass in der Eingabeaufforderung klar angegeben werden kann, welche Wissensdatenbank zur Beantwortung von Fragen verwendet wird. Beispiel-Workflow: [多知识库分别调用](workflow/多知识库分别调用.json).

35. Es wird unterstützt, dass das LLM zusätzliche Parameter wie json out und andere erweiterte Parameter erhält. Beispiel-Workflow: [LLM输入额外参数](workflow/LLM额外参数eg_JSON_OUT.json). [用json_out分离提示词](workflow/用json_out分离提示词.json).
36. Neue Funktion zur Anbindung des Agenten an Discord hinzugefügt. (Noch in der Testphase)
37. Neue Funktion zur Anbindung des Agenten an Feishu hinzugefügt. Ein herzlicher Dank gilt [guobalove](https://github.com/guobalove) für seinen Beitrag! Siehe Arbeitsablauf [Feishu Bot](workflow/飞书机器人.json).
38. Neuer universeller API-Aufrufknoten sowie zahlreiche Hilfsknoten hinzugefügt, die zur Konstruktion von Anfragekörpern und zum Abrufen von Informationen aus den Antworten dienen.
39. Neuer Knoten zum Leeren des Modells hinzugefügt, der es ermöglicht, das LLM an beliebiger Stelle aus dem Grafikspeicher zu entladen!
40. Der Knoten [chatTTS](https://github.com/2noise/ChatTTS) wurde hinzugefügt, ein herzlicher Dank gilt [guobalove](https://github.com/guobalove) für seinen Beitrag! Der Parameter `model_path` kann leer sein! Es wird empfohlen, das Modell im HF-Modus zu laden, das Modell wird automatisch von Hugging Face heruntergeladen, eine manuelle Download ist nicht erforderlich; bei Verwendung des local-Loads bitte die Ordner `asset` und `config` des Modells ins Stammverzeichnis legen. [Baidu Cloud Adresse](https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu), Entschlüsselungscode: qyhu; bei Verwendung des `custom`-Modus bitte die Ordner `asset` und `config` des Modells unter `model_path` ablegen.
2. Aktualisierte eine Reihe von Konvertierungsknoten: markdown zu HTML, svg zu Bild, HTML zu Bild, mermaid zu Bild, markdown zu Excel.
1. Kompatibel mit dem llama3.2 vision Modell, unterstützt mehrstufige Dialoge, visuelle Funktionen. Modelladresse: [meta-llama/Llama-3.2-11B-Vision-Instruct](https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct). Beispiel-Workflow: [llama3.2_vision](https://github.com/heshengtao/comfyui_LLM_party/blob/main/workflow_tutorial/LLM_Party%20for%20Llama3.2%20-Vision%EF%BC%88%E5%B8%A6%E8%AE%B0%E5%BF%86%EF%BC%89.json).
1. Angepasstes GOT-OCR2, unterstützt formatierte Ausgaberesultate, unterstützt die feine Texterkennung mit Positionsboxen und Farben. Modelladresse: [GOT-OCR2](https://huggingface.co/stepfun-ai/GOT-OCR2_0). Beispiel-Workflow konvertiert einen Screenshot einer Webseite in HTML-Code und öffnet dann den Browser, um diese Webseite anzuzeigen: [img2web](workflow/图片转网页.json).
2. Die lokalen LLM-Ladernoden wurden erheblich angepasst, sodass Sie den Modelltyp nicht mehr selbst auswählen müssen. Der llava-Ladernoden und der GGUF-Ladernoden wurden erneut hinzugefügt. Der Modelltyp auf dem lokalen LLM-Modellkettenknoten wurde in LLM, VLM-GGUF und LLM-GGUF geändert, was dem direkten Laden von LLM-Modellen, dem Laden von VLM-Modellen und dem Laden von LLM-Modellen im GGUF-Format entspricht. VLM-Modelle und LLM-Modelle im GGUF-Format werden jetzt wieder unterstützt. Lokale Aufrufe können jetzt mit mehr Modellen kompatibel sein! Beispiel-Workflows: [LLM_local](workflow/start_with_LLM_local.json), [llava](workflow/start_with_llava.json), [GGUF](workflow/start_with_GGUF.json)
2. EasyOCR-Knoten hinzugefügt, um Text und Positionen in Bildern zu erkennen. Es kann entsprechende Masken erstellen und eine JSON-Zeichenfolge zur Ansicht für LLM zurückgeben. Es gibt Standard- und Premium-Versionen zur Auswahl!
2. Auf der comfyui LLM-Party wurde das Erdbeersystem des chatgpt-o1-Serienmodells reproduziert, unter Bezugnahme auf die Eingabeaufforderungen von [Llamaberry](https://huggingface.co/spaces/martinbowling/Llamaberry/blob/main/app.py). Beispiel-Workflow: [Erdbeersystem im Vergleich zu o1](workflow/草莓系统与o1对比.json).
2. Ein neuer GPT-sovits-Knoten wurde hinzugefügt, der es Ihnen ermöglicht, das GPT-sovits-Modell aufzurufen, um Text basierend auf Ihrem Referenzaudio in Sprache umzuwandeln. Sie können auch den Pfad Ihres feinabgestimmten Modells angeben (wenn nicht angegeben, wird das Basismodell für die Inferenz verwendet), um jede gewünschte Stimme zu erhalten. Um es zu verwenden, müssen Sie das [GPT-sovits](https://github.com/RVC-Boss/GPT-SoVITS)-Projekt und das entsprechende Basismodell lokal herunterladen und dann den API-Dienst mit `runtime\python.exe api_v2.py` im GPT-sovits-Projektordner starten. Außerdem wurde der chatTTS-Knoten nach [comfyui LLM mafia](https://github.com/heshengtao/comfyui_LLM_mafia) verschoben. Der Grund dafür ist, dass chatTTS viele Abhängigkeiten hat und seine Lizenz auf PyPi CC BY-NC 4.0 ist, was eine nicht-kommerzielle Lizenz ist. Obwohl das chatTTS-GitHub-Projekt unter der AGPL-Lizenz steht, haben wir den chatTTS-Knoten zu comfyui LLM mafia verschoben, um unnötige Probleme zu vermeiden. Wir hoffen, dass jeder das versteht!
3. Unterstützt jetzt das neueste Modell von OpenAI, die o1-Serie!
4. Ein lokales Dateikontrollwerkzeug hinzugefügt, das es dem LLM ermöglicht, Dateien im angegebenen Ordner zu steuern, z. B. lesen, schreiben, anhängen, löschen, umbenennen, verschieben und kopieren.Aufgrund der potenziellen Gefahr dieses Knotens ist er in [comfyui LLM mafia](https://github.com/heshengtao/comfyui_LLM_mafia) enthalten.
5. Neue SQL-Tools ermöglichen es LLM, SQL-Datenbanken abzufragen.
6. Die mehrsprachige Version der README wurde aktualisiert. Workflow zum Übersetzen des README-Dokuments: [translate_readme](workflow/文档自动翻译机.json)
7. Es wurden vier Iterator-Knoten aktualisiert (Text-Iterator, Bild-Iterator, Tabellen-Iterator, JSON-Iterator). Die Iterator-Modi umfassen: sequenziell, zufällig und unendlich. Sequenziell gibt die Werte der Reihe nach aus, bis die Indexgrenze überschritten wird, woraufhin der Prozess automatisch gestoppt und der Indexwert auf 0 zurückgesetzt wird. Zufällig wählt einen beliebigen Index aus, während unendlich eine endlose Schleife von Ausgaben erzeugt.
8. Ein neuer Gemini API-Loader-Knoten wurde hinzugefügt, der jetzt mit der offiziellen Gemini-API kompatibel ist! Sollten Sie sich in einem nationalen Netzwerkumfeld befinden und Probleme mit der regionalen Einschränkung der API auftreten, wechseln Sie bitte den Knoten auf die USA und verwenden Sie den TUN-Modus. Da es bei der Verwendung von Gemini zu einem Fehlercode 500 kommt, wenn die zurückgegebenen Parameter chinesische Zeichen enthalten, sind einige Werkzeugknoten möglicherweise nicht verfügbar. Beispiel-Workflow: [start_with_gemini](workflow/start_with_gemini.json)
9. Ein neuer Lore Book-Knoten wurde hinzugefügt, um bei der Interaktion mit dem LLM Ihre Hintergrundgeschichte einzufügen. Beispiel-Workflow: [lorebook](workflow/lorebook.json)
10. Ein neuer FLUX-Prompt-Generator-Maskenknoten wurde hinzugefügt, der Prompts in verschiedenen Stilen wie Hearthstone-Karten, Yu-Gi-Oh-Karten, Plakate und Comics generieren kann, um das FLUX-Modell direkt zu nutzen. Referenz-Workflow: [FLUX提示词](https://openart.ai/workflows/comfyui_llm_party/flux-by-llm-party/sjME541i68Kfw6Ib0EAD)

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
<a href="https://github.com/HuangYuChuh">
  <img src="https://avatars.githubusercontent.com/u/167663109?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
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

2. WeChat-Gruppe: `Choo-Yong` (Fügen Sie den kleinen Assistenten zu WeChat hinzu, um der Gruppe beizutreten)

3. Discord:[discord链接](https://discord.gg/gxrQAYy6)

### Folgen Sie uns
1. Wenn Sie die neuesten Funktionen dieses Projekts kontinuierlich verfolgen möchten, heißen wir Sie herzlich willkommen, unseren Bilibili-Account zu abonnieren: [派对主持BB机](https://space.bilibili.com/26978344)
2. Der OpenArt-Account wird kontinuierlich die nützlichsten Party-Workflows aktualisieren: [openart](https://openart.ai/workflows/profile/comfyui_llm_party?sort=latest&tab=creation)

### Unterstützung durch Spenden
Wenn meine Arbeit Ihnen einen Mehrwert bietet, ziehen Sie bitte in Betracht, mir einen Kaffee auszugeben! Ihre Unterstützung belebt nicht nur das Projekt, sondern erwärmt auch das Herz der Kreatoren.☕💖 Jede Tasse zählt!
<div style="display:flex; justify-content:space-between;">
    <img src="img/zhifubao.jpg" style="width: 48%;" />
    <img src="img/wechat.jpg" style="width: 48%;" />
</div>

## Sternenverlauf

[![Star History Chart](https://api.star-history.com/svg?repos=heshengtao/comfyui_LLM_party&type=Date)](https://star-history.com/#heshengtao/comfyui_LLM_party&Date)
