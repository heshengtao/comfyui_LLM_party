![图片](img/封面.png)

<div align="center">
  <a href="https://space.bilibili.com/26978344">bilibili</a> ·
  <a href="https://www.youtube.com/@LLM-party">youtube</a> ·
  <a href="https://github.com/heshengtao/Let-LLM-party">Текстовые инструкции</a> ·
  <a href="https://pan.quark.cn/s/190b41f3bbdb">Адрес облачного диска</a> ·
  <a href="img/Q群.jpg">QQ группа</a> ·
  <a href="https://discord.gg/f2dsAKKr2V">Discord</a> ·
  <a href="https://dcnsxxvm4zeq.feishu.cn/wiki/IyUowXNj9iH0vzk68cpcLnZXnYf">О нас</a>
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

Comfyui_llm_party стремится на основе [comfyui](https://github.com/comfyanonymous/ComfyUI) создать полностью укомплектованную библиотеку узлов для построения рабочих потоков LLM, используя исключительно простой интерфейс. Это позволит пользователям быстрее и удобнее создавать свои рабочие потоки LLM и интегрировать их в собственные графические рабочие процессы.

## Демонстрация эффектов
https://github.com/user-attachments/assets/945493c0-92b3-4244-ba8f-0c4b2ad4eba6

## Обзор проекта
ComfyUI LLM Party предлагает от самых основ LLM, включая многопрофильное использование инструментов, быструю настройку индивидуального AI-ассистента, до внедрения в отрасль векторных представлений слов (RAG) и GraphRAG для локального управления знаниями в отрасли. От простых потоков агентов до построения сложных моделей взаимодействия между агентами, включая радиальные и кольцевые модели взаимодействия; от необходимости индивидуальных пользователей интегрировать свои социальные приложения (QQ, Feishu, Discord), до комплексного рабочего процесса для стримеров, который объединяет LLM, TTS и ComfyUI; от простого первого опыта работы с LLM, необходимого обычным студентам, до интерфейсов настройки параметров, часто используемых исследователями и адаптации моделей. Все это вы сможете найти в ComfyUI LLM Party.

## Быстрый старт
0. Если вы никогда не использовали ComfyUI и столкнулись с некоторыми проблемами зависимости при установке LLM party в ComfyUI, пожалуйста, нажмите [здесь](https://drive.google.com/file/d/1T9C7gEbd-w_zf9GqZO1VeI3z8ek8clpX/view?usp=sharing), чтобы загрузить **Windows** портативный пакет, который включает в себя LLM party. Обратите внимание, что этот портативный пакет содержит только плагины party и manager и исключительно совместим с операционной системой Windows.(Если вам необходимо установить LLM party в уже существующий comfyui, этот шаг можно пропустить.)
1. Перетащите следующие рабочие процессы в ваш comfyui, затем используйте [comfyui-Manager](https://github.com/ltdrdata/ComfyUI-Manager) для установки недостающих узлов.
  - Используйте API для вызова LLM: [start_with_LLM_api](workflow/start_with_LLM_api.json)
  - Используя aisuite для вызова LLM: [start_with_aisuite](workflow/start_with_aisuite.json)
  - Управляйте локальным LLM с помощью ollama: [start_with_Ollama](workflow/ollama.json)
  - Используйте локальный LLM в распределенном формате: [start_with_LLM_local](workflow/start_with_LLM_local.json)
  - Используйте локальный LLM в формате GGUF: [start_with_LLM_GGUF](workflow/start_with_GGUF.json)
  - Используйте локальный VLM в распределенном формате: [start_with_VLM_local](workflow/start_with_VLM_local.json) (В настоящее время поддержка расширена для [Llama-3.2-Vision](https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct)/[Qwen/Qwen2.5-VL](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct)/[deepseek-ai/Janus-Pro](https://huggingface.co/deepseek-ai/Janus-Pro-1B).)
  - Используйте локальный VLM в формате GGUF: [start_with_VLM_GGUF](workflow/start_with_llava.json)
  - Используйте API для вызова LLM для генерации подсказок SD и создания изображений: [начать_с_VLM_API_для_SD](workflow/start_with_VLM_API_for_SD.json)
  - Используйте ollama для вызова minicpm для генерации подсказок SD и создания изображений: [начать_с_ollama_minicpm_для_SD](workflow/start_with_ollama_minicpm_for_SD.json)
  - Используйте локальный qwen-vl для генерации подсказок SD и создания изображений: [начать_с_qwen_vl_локально_для_SD](workflow/start_with_qwen_vl_local_for_SD.json)
2. Если вы используете API, заполните `base_url` (это может быть промежуточный API, убедитесь, что он заканчивается на `/v1/`), например: `https://api.openai.com/v1/` и `api_key` в узле загрузчика API LLM.
3. Если вы используете ollama, включите опцию `is_ollama` в узле загрузчика API LLM, не нужно заполнять `base_url` и `api_key`.
4. Если вы используете локальную модель, заполните путь к вашей модели в узле загрузчика локальной модели, например: `E:\model\Llama-3.2-1B-Instruct`. Вы также можете заполнить идентификатор репозитория модели Huggingface в узле загрузчика локальной модели, например: `lllyasviel/omost-llama-3-8b-4bits`.
5. Из-за высокого порога использования этого проекта, даже если вы выбрали быстрый старт, я надеюсь, что вы терпеливо прочитаете домашнюю страницу проекта.

## Последние обновления
1. Узел LLM API теперь поддерживает потоковый режим вывода, который будет выводить текст, возвращаемый API, в реальном времени на консоль, позволяя вам видеть результаты работы API без необходимости ожидания завершения всего запроса.
2. Узел LLM API добавил вывод reasoning_content, который может автоматически отделять логические рассуждения и ответ модели R1.
3. Добавлена новая ветка под названием only_api в репозиторий, содержащая только компоненты вызова API. Это предназначено для пользователей, которым требуется только вызов API. Чтобы использовать эту ветку, просто выполните команду `git clone -b only_api https://github.com/heshengtao/comfyui_LLM_party.git` в папке `custom node` в `comfyui`, а затем следуйте инструкциям по развертыванию среды, приведенным на главной странице проекта. Обратите внимание! Важно убедиться, что в папке `custom node` нет других папок с названием `comfyui_LLM_party`.
1. Узел локального загрузчика VLM теперь поддерживает [deepseek-ai/Janus-Pro](https://huggingface.co/deepseek-ai/Janus-Pro-1B), с примером рабочего процесса: [Janus-Pro](workflow/deepseek-janus-pro.json).
1. Узловая локальная загрузка VLM уже поддерживает [Qwen/Qwen2.5-VL-3B-Instruct](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct), однако вам необходимо обновить трансформер до последней версии (```pip install -U transformers```), пример рабочего процесса: [qwen-vl](workflow/qwen-vl.json)
1. Добавлен совершенно новый узел хостинга изображений, который в настоящее время поддерживает услуги хостинга изображений по адресу https://sm.ms (с региональным доменным именем для Китая - https://smms.app) и https://imgbb.com. В будущем будут поддерживаться и другие услуги хостинга изображений. Пример рабочего процесса: [Хостинг изображений](workflow/图床.json)
1. ~~Сервис хостинга изображений imgbb, который по умолчанию совместим с party, был обновлён на домен [imgbb](https://imgbb.io). Предыдущий хостинг изображений был заменен из-за его недружелюбия к пользователям из материкового Китая.~~ Я искренне прошу прощения, так как, похоже, API-сервис хостинга изображений на https://imgbb.io прекратил свою работу. Поэтому код был возвращён к оригинальному https://imgbb.com. Спасибо за ваше понимание. В будущем я обновлю узел, поддерживающий больше сервисов хостинга изображений.
1. Инструмент [MCP](https://modelcontextprotocol.io/introduction) был обновлён. Вы можете изменить настройки в файле '[mcp_config.json](mcp_config.json)', расположенном в папке проекта party, чтобы подключиться к желаемому серверу MCP. Здесь вы можете найти различные параметры конфигурации серверов MCP, которые вы хотите добавить: [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers). По умолчанию данная конфигурация проекта использует сервер Everything, который служит для тестирования работоспособности сервера MCP. Рабочий процесс для справки: [start_with_MCP](workflow/start_with_MCP.json). Примечание для разработчиков: узел инструмента MCP может подключаться к настроенному вами серверу MCP и преобразовывать инструменты с сервера в инструменты, которые могут напрямую использоваться LLM. Настраивая разные локальные или облачные серверы, вы можете испытать все доступные в мире инструменты LLM.

## Инструкция по использованию
1. Пожалуйста, обратитесь к инструкции по использованию узлов: [怎么使用节点](https://github.com/heshengtao/Let-LLM-party)

2. Если у вас возникли проблемы с плагином или у вас есть другие вопросы, присоединяйтесь к нашей группе QQ: [931057213](img/Q群.jpg) |discord：[discord](https://discord.gg/f2dsAKKr2V).

4. Дополнительные рабочие процессы можно найти в папке [workflow](workflow).

## Видеоуроки
<a href="https://space.bilibili.com/26978344">
  <img src="img/B.png" width="100" height="100" style="border-radius: 80%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://www.youtube.com/@LLM-party">
  <img src="img/YT.png" width="100" height="100" style="border-radius: 80%; overflow: hidden;" alt="octocat"/>
</a>

## Поддержка моделей
1. Поддержка всех API-вызовов формата OpenAI (в сочетании с [oneapi](https://github.com/songquanpeng/one-api) можно вызывать практически все API LLM, также поддерживаются все промежуточные API). Выбор base_url можно найти в [config.ini.example](config.ini.example), на данный момент протестированы следующие:
* [openai](https://platform.openai.com/docs/api-reference/chat/create) (Идеально совместим со всеми моделями OpenAI, включая серии 4o и o1!)
* [ollama](https://github.com/ollama/ollama) (Рекомендуется! Если вы вызываете локально, настоятельно рекомендуется использовать метод ollama для размещения вашей локальной модели!)
* [Azure OpenAI](https://azure.microsoft.com/zh-cn/products/ai-services/openai-service/)
* [llama.cpp](https://github.com/ggerganov/llama.cpp?tab=readme-ov-file#web-server) (Рекомендуется! Если вы хотите использовать локальную модель формата gguf, вы можете использовать API проекта llama.cpp для доступа к этому проекту!)
* [Grok](https://x.ai/api)
* [通义千问/qwen](https://help.aliyun.com/zh/dashscope/developer-reference/compatibility-of-openai-with-dashscope/?spm=a2c4g.11186623.0.0.7b576019xkArPq)
* [智谱清言/glm](https://open.bigmodel.cn/dev/api#http_auth)
* [deepseek](https://platform.deepseek.com/api-docs/zh-cn/)
* [kimi/moonshot](https://platform.moonshot.cn/docs/api/chat#%E5%9F%BA%E6%9C%AC%E4%BF%A1%E6%81%AF)
* [doubao](https://www.volcengine.com/docs/82379/1263482)
* [Gemini](https://developers.googleblog.com/zh-hans/gemini-is-now-accessible-from-the-openai-library/)(Исходный узел загрузчика API LLM Gemini был устаревшим в новой версии. Пожалуйста, используйте узел загрузчика API LLM, выбрав base_url: https://generativelanguage.googleapis.com/v1beta/openai/)

2. Поддержка всех API вызовов, совместимых с [aisuite](https://github.com/andrewyng/aisuite):
* [anthropic/claude](https://www.anthropic.com/)
* [aws](https://docs.aws.amazon.com/solutions/latest/generative-ai-application-builder-on-aws/api-reference.html)
* [vertex](https://cloud.google.com/vertex-ai/docs/reference/rest)
* [huggingface](https://huggingface.co/)

3. Совместим с большинством локальных моделей в библиотеке transformer (тип модели на узле цепочки локальных моделей LLM изменен на LLM, VLM-GGUF и LLM-GGUF, что соответствует прямой загрузке моделей LLM, загрузке моделей VLM и загрузке моделей LLM в формате GGUF). Если ваша модель LLM в формате VLM или GGUF выдает ошибку, пожалуйста, загрузите последнюю версию llama-cpp-python с [llama-cpp-python](https://github.com/abetlen/llama-cpp-python/releases). В настоящее время протестированные модели включают:
* [ClosedCharacter/Peach-9B-8k-Roleplay](https://huggingface.co/ClosedCharacter/Peach-9B-8k-Roleplay) (рекомендуется! Модель для ролевых игр)
* [lllyasviel/omost-llama-3-8b-4bits](https://huggingface.co/lllyasviel/omost-llama-3-8b-4bits) (рекомендуется! Модель с богатым набором подсказок)
* [meta-llama/Llama-2-7b-chat-hf](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)
* [Qwen/Qwen2-7B-Instruct](https://huggingface.co/Qwen/Qwen2-7B-Instruct)
* [openbmb/MiniCPM-V-2_6-gguf](https://huggingface.co/openbmb/MiniCPM-V-2_6-gguf/tree/main)
* [lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF](https://huggingface.co/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/tree/main)
* [meta-llama/Llama-3.2-11B-Vision-Instruct](https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct)
* [Qwen/Qwen2.5-VL-3B-Instruct](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct)
* [deepseek-ai/Janus-Pro](https://huggingface.co/deepseek-ai/Janus-Pro-1B)

4. Загрузка моделей:
* [Адрес Quark облака](https://pan.quark.cn/s/190b41f3bbdb)
* [Ссылка на Baidu Cloud](https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu), код для извлечения: qyhu

## Загрузка
Используйте один из следующих методов для установки
### Метод 1:
1. В [менеджере comfyui](https://github.com/ltdrdata/ComfyUI-Manager) найдите `comfyui_LLM_party` и установите одним нажатием
2. Перезагрузите comfyui
### Способ второй:
1. Перейдите в подпапку `custom_nodes` в корневой папке ComfyUI.
2. Используйте команду для клонирования этого репозитория: `git clone https://github.com/heshengtao/comfyui_LLM_party.git`

### Способ третий:
1. Нажмите на кнопку `CODE` в правом верхнем углу.
2. Нажмите `download zip`.
3. Распакуйте загруженный архив в подпапку `custom_nodes` в корневой папке ComfyUI.

## Развертывание окружения
1. Перейдите в папку проекта `comfyui_LLM_party`.
2. В терминале введите команду `pip install -r requirements.txt`, чтобы установить необходимые сторонние библиотеки для проекта в окружение comfyui. Обратите внимание на то, что вы находитесь в окружении comfyui, и следите за ошибками `pip` в терминале.
3. Если вы используете запускатор comfyui, вам нужно ввести в терминале команду `путь к запускатору\python_embeded\python.exe -m pip install -r requirements.txt` для установки. Папка `python_embeded` обычно находится на одном уровне с папкой `ComfyUI`.
4. Если у вас возникли проблемы с конфигурацией окружения, вы можете попробовать использовать зависимости из файла `requirements_fixed.txt`.
## Конфигурация
* В `config.ini` можно настроить язык, в настоящее время доступны только китайский (zh_CN) и английский (en_US), по умолчанию устанавливается язык вашей системы.
* В `config.ini` вы можете настроить, нужно ли включить быструю установку. Параметр `fast_installed` по умолчанию установлен на `False`, и если вам не нужна модель GGUF, его можно установить на `True`.
* Для настройки APIKEY можно использовать один из следующих методов.
### Метод 1:
1. Откройте файл `config.ini`, находящийся в папке проекта `comfyui_LLM_party`.
2. Введите ваш `openai_api_key` и `base_url` в `config.ini`.
3. Если вы используете модель ollama, введите `http://127.0.0.1:11434/v1/` в `base_url`, `ollama` в `openai_api_key`, а в `model_name` укажите название вашей модели, например: llama3.
4. Если вы хотите использовать инструменты поиска Google или Bing, введите ваш `google_api_key`, `cse_id` или `bing_api_key` в `config.ini`.
5. Если вы хотите использовать ввод изображений в LLM, рекомендуется использовать хостинг изображений imgbb, введите ваш `imgbb_api` в `config.ini`.
6. Каждая модель может быть настроена отдельно в файле `config.ini`, вы можете обратиться к файлу `config.ini.example` для справки. После настройки вам нужно просто ввести `model_name` на узле.

### Метод 2:
1. Откройте интерфейс comfyui.
2. Создайте узел большого языкового моделирования (LLM), введите ваш `openai_api_key` и `base_url` непосредственно в узле.
3. Если вы используете модель ollama, используйте узел LLM_api, введите `http://127.0.0.1:11434/v1/` в `base_url`, `ollama` в `api_key`, а в `model_name` укажите название вашей модели, например: llama3.
4. Если вы хотите использовать ввод изображений в LLM, рекомендуется использовать хостинг изображений imgbb, введите ваш `imgbb_api_key` на узле.

## Журнал обновлений
**[Click here](change_log.md)**

## Следующий план:
1. Больше адаптаций моделей;
2. Больше способов создания агентов;
3. Больше функций автоматизации;
4. Больше функций управления базой знаний;
5. Больше инструментов, больше персон.

## Еще один полезный проект с открытым исходным кодом:
[super-agent-party](https://github.com/heshengtao/super-agent-party) — это 3D-приложение с безграничными возможностями, ваш AI-компаньон на рабочем столе! Уже поддерживает RAG, поиск в интернете, долговременную память, интерпретатор кода, MCP, A2A, Comfyui, QQ-бота и множество других функций!
![image](img/vrmbot.jpeg)

## Отказ от ответственности:
Данный открытый проект и его содержание (далее именуемые "проект") предназначены только для справочных целей и не подразумевают никаких явных или подразумеваемых гарантий. Участники проекта не несут никакой ответственности за полноту, точность, надежность или применимость проекта. Любые действия, основанные на содержании проекта, осуществляются на ваш собственный риск. В любых случаях участники проекта не несут ответственности за любые косвенные, специальные или побочные убытки или повреждения, возникшие в результате использования содержания проекта.

## Особая благодарность
<a href="https://github.com/bigcat88">
  <img src="https://avatars.githubusercontent.com/u/13381981?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://github.com/guobalove">
  <img src="https://avatars.githubusercontent.com/u/171540731?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://github.com/SpenserCai">
  <img src="https://avatars.githubusercontent.com/u/25168945?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>

## Список заимствований
Некоторые узлы в этом проекте заимствованы из следующих проектов, благодарим их за вклад в сообщество с открытым исходным кодом!
1. [pythongosssss/ComfyUI-Custom-Scripts](https://github.com/pythongosssss/ComfyUI-Custom-Scripts)
2. [lllyasviel/Omost](https://github.com/lllyasviel/Omost)

## Поддержка:

### Присоединяйтесь к сообществу
Если у вас возникли проблемы с плагином или есть другие вопросы, приглашаем вас присоединиться к нашему сообществу.

1. QQ группа: `931057213`
<div style="display: flex; justify-content: center;">
    <img src="img/Q群.jpg" style="width: 48%;" />
</div>

2. 微信群：`we_glm`（添加小助手微信后进群）

3. discord:[дискорд-ссылка](https://discord.gg/f2dsAKKr2V)

### Следите за нами
1. Если вы хотите оставаться в курсе последних функций этого проекта, пожалуйста, подпишитесь на аккаунт B站: [派酱](https://space.bilibili.com/26978344)
2. [youtube@LLM-party](https://www.youtube.com/@LLM-party)

## История звёзд

[![График истории звёзд](https://api.star-history.com/svg?repos=heshengtao/comfyui_LLM_party&type=Date)](https://star-history.com/#heshengtao/comfyui_LLM_party&Date)
