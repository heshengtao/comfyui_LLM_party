![Imagen](img/封面.png)

<div align="center">
  <a href="https://space.bilibili.com/26978344">bilibili</a> ·
  <a href="https://www.youtube.com/@comfyui-LLM-party">youtube</a> ·
  <a href="https://github.com/heshengtao/Let-LLM-party">Tutorial escrito</a> ·
  <a href="workflow_tutorial/">Tutorial de flujo de trabajo</a> ·
  <a href="https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu">Enlace de Baidu</a> ·
  <a href="img/Q群.jpg">Grupo QQ</a> ·
  <a href="https://discord.gg/f2dsAKKr2V">Discord</a> ·
  <a href="https://dcnsxxvm4zeq.feishu.cn/wiki/IyUowXNj9iH0vzk68cpcLnZXnYf">Sobre nosotros</a>
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

Comfyui_llm_party tiene la intención de desarrollar una biblioteca completa de nodos para la construcción de flujos de trabajo de LLM, basada en la interfaz de usuario extremadamente simple de [comfyui](https://github.com/comfyanonymous/ComfyUI) como frontend. Esto permitirá a los usuarios construir sus flujos de trabajo de LLM de manera más rápida y conveniente, además de facilitar la integración de sus flujos de trabajo de imágenes.

## Demostración de resultados
https://github.com/user-attachments/assets/945493c0-92b3-4244-ba8f-0c4b2ad4eba6

## Resumen del Proyecto
ComfyUI LLM Party permite desde la llamada a múltiples herramientas LLM desde la base, la rápida configuración de un asistente AI personalizado, hasta la implementación de vectores de palabras RAG y GraphRAG para la gestión local de bases de datos de conocimiento en la industria; desde una simple línea de agentes inteligentes hasta la construcción de complejos modos de interacción radial entre agentes inteligentes y modos de interacción en círculo; desde la integración de aplicaciones sociales (QQ, Feishu, Discord) para usuarios individuales, hasta un flujo de trabajo integral de LLM+TTS+ComfyUI para trabajadores de streaming; desde el inicio sencillo que necesita un estudiante común con su primera aplicación LLM, hasta las diversas interfaces de ajuste de parámetros frecuentemente utilizadas por investigadores. Todo esto lo puedes encontrar en ComfyUI LLM Party.

## Inicio rápido
0. Si nunca has utilizado ComfyUI y al instalar LLM party en ComfyUI has encontrado algunos problemas de dependencia, haz clic [aquí](https://drive.google.com/file/d/1NJSpwEL3FqroKVv5UsrVY3YbCG-9YWmt/view?usp=sharing) para descargar el paquete portátil de ComfyUI **windows** que incluye LLM party. ¡Atención! Este paquete portátil contiene únicamente los dos plugins: party y manager, y es exclusivamente para sistemas Windows.(En caso de que necesite instalar LLM party en un comfyui existente, este paso se puede omitir.)  
1. Arrastra los siguientes flujos de trabajo a tu comfyui, luego usa [comfyui-Manager](https://github.com/ltdrdata/ComfyUI-Manager) para instalar los nodos faltantes.
  - Usa la API para llamar a LLM: [start_with_LLM_api](workflow/start_with_LLM_api.json)
  - Llamando a LLM con aisuite: [iniciar_con_aisuite](workflow/start_with_aisuite.json)
  - Gestiona LLM local con ollama: [start_with_Ollama](workflow/ollama.json)
  - Usa LLM local en formato distribuido: [start_with_LLM_local](workflow/start_with_LLM_local.json)
  - Usa LLM local en formato GGUF: [start_with_LLM_GGUF](workflow/start_with_GGUF.json)
  - Usa VLM local en formato distribuido: [start_with_VLM_local](https://github.com/heshengtao/comfyui_LLM_party/blob/main/workflow_tutorial/LLM_Party%20for%20Llama3.2%20-Vision%EF%BC%88%E5%B8%A6%E8%AE%B0%E5%BF%86%EF%BC%89.json) (en prueba, actualmente solo admite [Llama-3.2-Vision-Instruct](https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct))
  - Usa VLM local en formato GGUF: [start_with_VLM_GGUF](workflow/start_with_llava.json)
2. Si estás usando la API, completa tu `base_url` (puede ser una API de retransmisión, asegúrate de que termine con `/v1/`) y `api_key` en el nodo de carga de API LLM. Ejemplo: `https://api.openai.com/v1/`
3. Si estás usando ollama, activa la opción `is_ollama` en el nodo de carga de API LLM, no es necesario completar `base_url` y `api_key`.
4. Si estás usando un modelo local, completa la ruta de tu modelo en el nodo de carga del modelo local, por ejemplo: `E:\model\Llama-3.2-1B-Instruct`. También puedes completar el ID del repositorio del modelo en Huggingface en el nodo de carga del modelo local, por ejemplo: `lllyasviel/omost-llama-3-8b-4bits`.
5. Debido al alto umbral de uso de este proyecto, incluso si eliges el inicio rápido, espero que puedas leer pacientemente la página principal del proyecto.

## Últimas Actualizaciones
1. Se ha añadido un nodo de cargador de aisuite, lo que hace compatible aisuite con todas las API que puede manejar, incluyendo: ["openai","anthropic","aws","azure","vertex","huggingface"], flujo de trabajo de ejemplo: [iniciar_con_aisuite](workflow/start_with_aisuite.json). 
1. Se ha añadido una nueva categoría, "nodos de memoria", que puede ser utilizada para gestionar el historial de conversaciones de tu LLM. Los nodos de memoria actualmente soportan tres modos para gestionar tu historial de conversaciones: archivo json local, Redis y SQL. Al desacoplar el historial de conversaciones del LLM, puedes utilizar modelos de incrustación de palabras para comprimir y organizar tu historial de conversaciones, ahorrando así tokens y ventana de contexto del LLM. Ejemplo de flujo de trabajo: [Memoria externa](workflow/外置记忆.json).
1. Se ha añadido una herramienta de lectura de archivos locales, a diferencia de la herramienta de control de archivos locales anterior en comfyui LLM mafia, esta herramienta solo puede leer archivos o el árbol de archivos dentro de una carpeta específica, por lo que es mucho más segura.
1. He bifurcado [chatgpt-on-wechat](https://github.com/zhayujie/chatgpt-on-wechat) y creado un nuevo repositorio [party-on-wechat](https://github.com/heshengtao/party-on-wechat). Los métodos de instalación y uso son los mismos que en el proyecto original, no se requiere configuración, solo necesita iniciar el FastAPI de party. Por defecto, llama al flujo de trabajo wx_api y admite la salida de imágenes. Se actualizará gradualmente para garantizar una experiencia suave de party en WeChat.
2. Se ha agregado un nodo de máscara In-Context-LoRA, utilizado para generar indicaciones [In-Context-LoRA](https://github.com/ali-vilab/In-Context-LoRA/tree/main) coherentes.
1. Hemos añadido un componente frontend cuyas funciones se disponen de izquierda a derecha como sigue:
  - Guarda tu clave API y la URL Base en el archivo `config.ini`. Cuando usas la función `fix node` en el nodo cargador de API LLM, lee automáticamente la clave API y la URL Base que hayas modificado en el archivo `config.ini`.
  - Inicia un servicio FastAPI que puede usarse para llamar a tus flujos de trabajo de ComfyUI. Si lo ejecutas directamente, obtienes una interfaz OpenAI en `http://127.0.0.1:8817/v1/`. Debes conectar el inicio y el final de tu flujo de trabajo con los nodos 'Inicio del flujo de trabajo' y 'Fin del flujo de trabajo', luego guardar en formato API en la carpeta `workflow_api`. Luego, en cualquier frontend que pueda llamar a la interfaz OpenAI, introduce `model name=<nombre de tu flujo de trabajo sin la extensión .json>`, `Base URL=http://127.0.0.1:8817/v1/`, y la clave API puede ser cualquier valor.
  - Inicia una aplicación Streamlit; el proceso de guardado del flujo de trabajo es el mismo que el anterior. Puedes seleccionar tu flujo de trabajo guardado en la 'Configuración' de la aplicación Streamlit e interactuar con tu agente de flujo de trabajo en el 'Chat'.
  - 'Acerca de nosotros', que presenta este proyecto.
2. El nodo de lista de nombres de modelos automáticos ha sido eliminado y reemplazado con un nodo de cargador de API LLM simple, que obtiene automáticamente la lista de nombres de modelos de la configuración en su archivo config.ini. Solo necesita seleccionar un nombre para cargar el modelo. Además, se han actualizado los nodos de cargador LLM simple, cargador LLM-GGUF simple, cargador VLM simple, cargador VLM-GGUF simple y cargador LLM lora simple. Todos ellos leen automáticamente las rutas de los modelos desde la carpeta model dentro de la carpeta party, lo que facilita la carga de varios modelos locales.
1. Los LLMs ahora pueden cargar lora dinámicamente como SD y FLUX. Puedes encadenar múltiples loras para cargar más loras en el mismo LLM. Ejemplo de flujo de trabajo: [start_with_LLM_LORA](workflow/LLM_lora.json).
2. Se agregó la herramienta [searxng](https://github.com/searxng/searxng), que puede agregar búsquedas en toda la web. Perplexica también depende de esta herramienta de búsqueda agregada, lo que significa que puedes configurar un Perplexica en una fiesta. Puedes desplegar la imagen pública searxng/searxng en Docker, luego usar el comando `docker run -d -p 8080:8080 searxng/searxng` para iniciarlo, y luego usar `http://localhost:8080` para acceder a él. Puedes ingresar la URL `http://localhost:8080` en la herramienta searxng en party, y luego searxng puede usarse como una herramienta para LLM.
1. **¡Actualización importante!!!** Ahora puedes encapsular cualquier flujo de trabajo de ComfyUI en un nodo de herramienta LLM. Puedes hacer que tu LLM controle múltiples flujos de trabajo de ComfyUI simultáneamente. Cuando quieras que complete algunas tareas, puede elegir el flujo de trabajo de ComfyUI adecuado según tu solicitud, completar tu tarea y devolverte el resultado. Ejemplo de flujo de trabajo: [comfyui_workflows_tool](workflow/把任意workflow当作LLM_tool.json). Los pasos específicos son los siguientes:
   - Primero, conecta la interfaz de entrada de texto del flujo de trabajo que deseas encapsular como herramienta a la salida "user_prompt" del nodo "Iniciar flujo de trabajo". Este es el lugar donde se pasa la solicitud cuando el LLM llama a la herramienta.
   - Conecta las posiciones donde deseas sacar texto e imágenes a las posiciones de entrada correspondientes del nodo "Finalizar flujo de trabajo".
   - Guarda este flujo de trabajo como una API (necesitas habilitar el modo desarrollador en la configuración para ver este botón).
   - Guarda este flujo de trabajo en la carpeta workflow_api de este proyecto.
   - Reinicia ComfyUI y crea un flujo de trabajo LLM simple, como: [start_with_LLM_api](workflow/start_with_LLM_api.json).
   - Añade un nodo "Herramienta de flujo de trabajo" a este nodo LLM y conéctalo a la entrada de herramienta del nodo LLM.
   - En el nodo "Herramienta de flujo de trabajo", escribe el nombre del archivo de flujo de trabajo que deseas llamar en el primer cuadro de entrada, por ejemplo: draw.json. Puedes escribir varios nombres de archivos de flujo de trabajo. En el segundo cuadro de entrada, escribe la función de cada flujo de trabajo para que el LLM entienda cómo usar estos flujos de trabajo.
   - Ejecútalo para ver cómo el LLM llama a tu flujo de trabajo encapsulado y te devuelve el resultado. Si el resultado es una imagen, conecta el nodo "Vista previa de imagen" a la salida de imagen del nodo LLM para ver la imagen generada. ¡Atención! Este método llama a un nuevo ComfyUI en tu puerto 8190, por favor no ocupes este puerto. Se abrirá una nueva terminal en los sistemas Windows y Mac, por favor no la cierres. El sistema Linux utiliza el proceso screen para lograr esto, cuando no lo necesites, cierra este proceso screen, de lo contrario, siempre ocupará tu puerto.

![workflow_tool](img/workflowtool.png)

## Instrucciones de Uso
1. Para las instrucciones de uso de los nodos, consulta: [怎么使用节点](https://github.com/heshengtao/Let-LLM-party)

2. Si hay problemas con el plugin o tienes otras dudas, no dudes en unirte a nuestro grupo de QQ: [931057213](img/Q群.jpg) | discord：[discord](https://discord.gg/f2dsAKKr2V).
3. Para el tutorial de flujos de trabajo, consulte: [工作流教程](workflow_tutorial/)，agradecemos la contribución de [HuangYuChuh](https://github.com/HuangYuChuh).

4. Cuenta para funciones avanzadas de flujos de trabajo: [openart](https://openart.ai/workflows/profile/comfyui_llm_party?sort=latest&tab=creation)

4. Para más flujos de trabajo, puede consultar la carpeta [workflow](workflow).

## Tutoriales en video
<a href="https://space.bilibili.com/26978344">
  <img src="img/B.png" width="100" height="100" style="border-radius: 80%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://www.youtube.com/@comfyui-LLM-party">
  <img src="img/YT.png" width="100" height="100" style="border-radius: 80%; overflow: hidden;" alt="octocat"/>
</a>

## Soporte de Modelos
1. Se admiten todas las llamadas a la API en formato OpenAI (en combinación con [oneapi](https://github.com/songquanpeng/one-api) se pueden realizar llamadas a casi todas las API de LLM, también se admiten todas las API de retransmisión), para la elección de base_url, consulte [config.ini.example](config.ini.example). Actualmente se han probado las siguientes:
* [openai](https://platform.openai.com/docs/api-reference/chat/create) (¡Perfectamente compatible con todos los modelos de OpenAI, incluidas las series 4o y o1!)
* [ollama](https://github.com/ollama/ollama) (¡Recomendado! Si estás llamando localmente, se recomienda encarecidamente utilizar el método ollama para alojar tu modelo local!)
* [Azure OpenAI](https://azure.microsoft.com/zh-cn/products/ai-services/openai-service/)
* [llama.cpp](https://github.com/ggerganov/llama.cpp?tab=readme-ov-file#web-server) (¡Recomendado! Si deseas utilizar el modelo en formato gguf local, puedes utilizar la API del proyecto llama.cpp para acceder a este proyecto!)
* [Grok](https://x.ai/api)
* [通义千问/qwen](https://help.aliyun.com/zh/dashscope/developer-reference/compatibility-of-openai-with-dashscope/?spm=a2c4g.11186623.0.0.7b576019xkArPq)
* [智谱清言/glm](https://open.bigmodel.cn/dev/api#http_auth)
* [deepseek](https://platform.deepseek.com/api-docs/zh-cn/)
* [kimi/moonshot](https://platform.moonshot.cn/docs/api/chat#%E5%9F%BA%E6%9C%AC%E4%BF%A1%E6%81%AF)
* [doubao](https://www.volcengine.com/docs/82379/1263482)
* [讯飞星火/spark](https://xinghuo.xfyun.cn/sparkapi?scr=price)

2. Se admiten llamadas a la API en formato Gemini:
* [Gemini](https://aistudio.google.com/app/prompts/new_chat)

3. Soporte para todas las llamadas API compatibles con [aisuite](https://github.com/andrewyng/aisuite):
* [antropico](https://www.anthropic.com/)
* [aws](https://docs.aws.amazon.com/solutions/latest/generative-ai-application-builder-on-aws/api-reference.html)
* [vértice](https://cloud.google.com/vertex-ai/docs/reference/rest)
* [huggingface](https://huggingface.co/)

3. Compatible con la mayoría de los modelos locales en la biblioteca transformer (el tipo de modelo en el nodo de la cadena de modelos LLM local se ha cambiado a LLM, VLM-GGUF y LLM-GGUF, lo que corresponde a cargar directamente modelos LLM, cargar modelos VLM y cargar modelos LLM en formato GGUF). Si tu modelo LLM en formato VLM o GGUF informa un error, descarga la última versión de llama-cpp-python desde [llama-cpp-python](https://github.com/abetlen/llama-cpp-python/releases). Los modelos actualmente probados incluyen:
* [ClosedCharacter/Peach-9B-8k-Roleplay](https://huggingface.co/ClosedCharacter/Peach-9B-8k-Roleplay) (¡Recomendado! Modelo de rol)
* [lllyasviel/omost-llama-3-8b-4bits](https://huggingface.co/lllyasviel/omost-llama-3-8b-4bits) (¡Recomendado! Modelo de palabras clave ricas)
* [meta-llama/Llama-2-7b-chat-hf](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)
* [Qwen/Qwen2-7B-Instruct](https://huggingface.co/Qwen/Qwen2-7B-Instruct)
* [openbmb/MiniCPM-V-2_6-gguf](https://huggingface.co/openbmb/MiniCPM-V-2_6-gguf/tree/main)
* [lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF](https://huggingface.co/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/tree/main)
* [meta-llama/Llama-3.2-11B-Vision-Instruct](https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct)

4. Descarga del modelo:
* [Dirección de Baidu Cloud](https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu), código de extracción: qyhu

## Descarga
Instale utilizando uno de los siguientes métodos:
### Método Uno:
1. Busque `comfyui_LLM_party` en [el administrador de ComfyUI](https://github.com/ltdrdata/ComfyUI-Manager) e instálelo con un solo clic.
2. Reinicie ComfyUI.
### Método dos:
1. Navegue hasta la subcarpeta `custom_nodes` en la carpeta raíz de ComfyUI.
2. Clone este repositorio. `git clone https://github.com/heshengtao/comfyui_LLM_party.git`

### Método tres:
1. Haga clic en `CODE` en la esquina superior derecha.
2. Haga clic en `download zip`.
3. Extraiga el archivo comprimido descargado en la subcarpeta `custom_nodes` de la carpeta raíz de ComfyUI.

## Implementación del entorno
1. Navegue hasta la carpeta del proyecto `comfyui_LLM_party`.
2. En la terminal, ingrese `pip install -r requirements.txt` para implementar las bibliotecas de terceros necesarias para este proyecto en el entorno de comfyui. Tenga en cuenta si está instalando en el entorno de comfyui y preste atención a los errores de `pip` en la terminal.
3. Si está utilizando el lanzador de comfyui, deberá ingresar en la terminal `ruta en la configuración del lanzador\python_embeded\python.exe -m pip install -r requirements.txt` para realizar la instalación. La carpeta `python_embeded` generalmente está al mismo nivel que su carpeta `ComfyUI`.
4. Si encuentra problemas con la configuración del entorno, puede intentar usar las dependencias del archivo `requirements_fixed.txt`.
## Configuración
* Puede configurar el idioma en `config.ini`, actualmente solo hay dos opciones: chino (zh_CN) e inglés (en_US), siendo el predeterminado el idioma de su sistema.
* Puede utilizar uno de los siguientes métodos para configurar el APIKEY.
### Método uno:
1. Abra el archivo `config.ini` en la carpeta del proyecto `comfyui_LLM_party`.
2. Ingrese su `openai_api_key` y `base_url` en `config.ini`.
3. Si utiliza el modelo ollama, ingrese `http://127.0.0.1:11434/v1/` en `base_url`, `ollama` en `openai_api_key`, y el nombre de su modelo en `model_name`, por ejemplo: llama3.
4. Si desea utilizar herramientas de búsqueda de Google o Bing, ingrese su `google_api_key`, `cse_id` o `bing_api_key` en `config.ini`.
5. Si desea utilizar entrada de imágenes para LLM, se recomienda usar el servicio de alojamiento de imágenes imgbb, ingresando su `imgbb_api` en `config.ini`.
6. Cada modelo se puede configurar individualmente en el archivo `config.ini`, y puede consultar el archivo `config.ini.example` para completar la configuración. Una vez que esté configurado, solo necesita ingresar `model_name` en el nodo.

### Método dos:
1. Abra la interfaz de comfyui.
2. Cree un nuevo nodo de modelo de lenguaje grande (LLM), ingresando directamente su `openai_api_key` y `base_url` en el nodo.
3. Si utiliza el modelo ollama, utilice el nodo LLM_api, ingresando `http://127.0.0.1:11434/v1/` en `base_url`, `ollama` en `api_key`, y el nombre de su modelo en `model_name`, por ejemplo: llama3.
4. Si desea utilizar entrada de imágenes para LLM, se recomienda usar el servicio de alojamiento de imágenes imgbb, ingresando su `imgbb_api_key` en el nodo.
## Registro de Actualizaciones
1. Puede hacer clic derecho en la interfaz de comfyui, seleccionar `llm` en el menú contextual y así encontrará el nodo de este proyecto. [Cómo usar nodos](https://github.com/heshengtao/Let-LLM-party)
2. Se admite la integración de API o la conexión de modelos grandes locales. Se ha implementado de manera modular la funcionalidad de llamada de herramientas. Al ingresar el base_url, debe ser una URL que termine en `/v1/`. Puede utilizar [ollama](https://github.com/ollama/ollama) para gestionar sus modelos; en base_url ingrese `http://127.0.0.1:11434/v1/`, en api_key ingrese ollama, y en model_name ingrese el nombre de su modelo, por ejemplo: llama3.
   - Ejemplo de flujo de trabajo de integración de API: [start_with_LLM_api](workflow/start_with_LLM_api.json)
   - Ejemplo de flujo de trabajo de integración de modelo local: [start_with_LLM_local](workflow/start_with_LLM_local.json)
   - Ejemplo de flujo de trabajo de integración de ollama: [ollama](workflow/ollama.json)
3. Integración de repositorios de conocimiento local, soporte para RAG. Ejemplo de flujo de trabajo: [Búsqueda RAG en Repositorio](workflow/知识库RAG搜索.json)
4. Se puede invocar un intérprete de código.
5. Se permite la consulta en línea, con soporte para búsqueda en Google. Ejemplo de flujo de trabajo: [Flujo de Trabajo de Consulta de Películas](workflow/电影查询工作流.json)
6. Es posible implementar declaraciones condicionales en comfyui, permitiendo clasificar preguntas de los usuarios y responder de manera específica. Ejemplo de flujo de trabajo: [Servicio al Cliente Inteligente](workflow/智能客服.json)
7. Soporte para enlaces de retroalimentación de modelos grandes, lo que permite que dos modelos grandes participen en un debate. Ejemplo de flujo de trabajo: [Debate sobre el Dilema del Tranvía](workflow/电车难题辩论赛.json)
8. Se admite la conexión de cualquier máscara de personalidad, permitiendo personalizar plantillas de indicaciones.
9. Soporte para diversas llamadas de herramientas, actualmente se han desarrollado funciones como consulta del clima, hora, repositorio de conocimiento, ejecución de código, búsqueda en línea y búsqueda en una única página web.
10. Se admite el uso de LLM como un nodo de herramienta. Ejemplo de flujo de trabajo: [LLM Matryoshka](workflow/LLM套娃.json)
11. Se admite el desarrollo rápido de aplicaciones web propias mediante API + streamlit.
12. Se ha añadido un nodo de intérprete universal peligroso, que permite a los modelos grandes hacer cualquier cosa.
13. Se recomienda utilizar el nodo de mostrar texto (show_text) en el subdirectorio de funciones (function) del menú contextual como salida del nodo LLM.
14. ¡Se ha habilitado la función visual de GPT-4O! Flujo de trabajo de ejemplo: [GPT-4o](workflow/GPT-4o.json)  
15. Se ha añadido un conector de flujo de trabajo, que permite que tu flujo de trabajo llame a otros flujos de trabajo. Flujo de trabajo de ejemplo: [Llamar a otro flujo de trabajo](workflow/调用另一个工作流.json)  
16. Se han adaptado todos los modelos que tienen interfaces similares a openai, como: Tongyi Qianwen/qwen, Zhipu Qingyan/GLM, deepseek, kimi/moonshot. Por favor, completa los campos base_url, api_key y model_name de los nodos LLM para poder llamarlos.  
17. Se ha añadido un cargador LVM, ahora puedes llamar a modelos LVM localmente, soportando el modelo [llava-llama-3-8b-v1_1-gguf](https://huggingface.co/xtuner/llava-llama-3-8b-v1_1-gguf); otros modelos LVM en formato GGUF teóricamente también deberían funcionar. El flujo de trabajo de ejemplo está aquí: [start_with_LVM.json](workflow/start_with_LVM.json).  
18. Se ha escrito un archivo `fastapi.py`, si lo ejecutas directamente, obtendrás una interfaz openai en `http://127.0.0.1:8817/v1/`, cualquier aplicación que pueda llamar a GPT podrá invocar tu flujo de trabajo de comfyui. Detallaré cómo hacerlo en un tutorial próximo.  
19. Se ha separado el cargador LLM y la cadena LLM, dividiendo la carga del modelo y la configuración del modelo, lo que permite compartir modelos entre diferentes nodos LLM.  
20. Actualmente se admite macOS y dispositivos mps. ¡Gracias a [bigcat88](https://github.com/bigcat88) por esta contribución!  
21. Ahora puedes crear tu propio juego de novela interactiva, donde las decisiones del usuario conducen a diferentes finales. Flujo de trabajo de ejemplo: [Novela interactiva](workflow/互动小说.json)  
22. Se han adaptado las funciones de whisper y tts de openai, permitiendo la entrada y salida de voz. Flujo de trabajo de ejemplo: [Entrada de voz + Salida de voz](workflow/语音输入+语音输出.json)
23. ¡Compatibilidad con [Omost](https://github.com/lllyasviel/Omost) ya disponible! Descargue [omost-llama-3-8b-4bits](https://huggingface.co/lllyasviel/omost-llama-3-8b-4bits) y comience a experimentar de inmediato. Referencia de flujo de trabajo: [start_with_OMOST](workflow/start_with_OMOST.json)  
24. Se han añadido herramientas LLM para enviar mensajes a WeChat empresarial, DingTalk y Feishu, así como funciones externas que se pueden invocar.  
25. Se ha añadido un iterador de texto que puede emitir solo una parte de los caracteres cada vez. Este iterador divide el texto de manera segura según el símbolo de retorno de carro y el tamaño del fragmento, sin dividir el texto a la mitad. El parámetro chunk_overlap indica cuántos caracteres se superponen en el texto dividido. Esto permite la entrada masiva de textos extremadamente largos; solo es necesario hacer clic sin pensar o activar la ejecución cíclica en ComfyUI para completarlo automáticamente. Recuerde activar la propiedad is_locked para que, al finalizar la entrada, el flujo de trabajo se bloquee automáticamente y no continúe ejecutándose. Ejemplo de flujo de trabajo: [文本迭代输入](workflow/文本迭代输入.json)  
26. Se ha añadido el atributo model name en el cargador local de LLM y el cargador local de llava. Si está vacío, se utilizarán las diversas rutas locales en el nodo. Si no está vacío, se cargará utilizando el parámetro de ruta que usted mismo haya especificado en `config.ini`. Si no está vacío y no se encuentra en `config.ini`, se descargará desde Hugging Face o se cargará desde el directorio de modelos guardados de Hugging Face. Si desea descargar desde Hugging Face, complete el atributo model name en el formato: `THUDM/glm-4-9b-chat`. ¡Atención! Los modelos cargados de esta manera deben ser compatibles con la biblioteca transformer.  
27. Se han añadido nodos de análisis de archivos JSON y nodos de obtención de valores JSON, que permiten obtener el valor de una clave específica de un archivo o texto. ¡Agradecimientos a [guobalove](https://github.com/guobalove) por su contribución!
28. Se ha mejorado el código para la invocación de herramientas, de modo que ahora los LLM sin función de llamada a herramientas también pueden activar el atributo is_tools_in_sys_prompt (por defecto, no es necesario activarlo en LLM locales, se adapta automáticamente). Una vez activado, la información de las herramientas se añadirá al mensaje del sistema, permitiendo así que el LLM invoque herramientas. Artículo relacionado sobre el principio de implementación: [Achieving Tool Calling Functionality in LLMs Using Only Prompt Engineering Without Fine-Tuning](https://arxiv.org/abs/2407.04997).

29. Se ha creado la carpeta custom_tool para almacenar el código de las herramientas personalizadas. Puede hacer referencia al código en la carpeta [custom_tool](custom_tool) y colocar el código de su herramienta personalizada en la carpeta custom_tool para que pueda ser invocada en el LLM.

30. Se ha añadido una herramienta de gráfico de conocimiento que permite una interacción perfecta entre el LLM y el gráfico de conocimiento. El LLM puede modificar el gráfico de conocimiento según su entrada y razonar sobre él para obtener las respuestas que necesita. Flujo de trabajo de ejemplo: [graphRAG_neo4j](workflow/graphRAG_neo4j.json).

31. Se ha incorporado la función de IA de personalidad, permitiendo desarrollar su propia IA de novia o novio sin necesidad de código, con conversaciones ilimitadas, memoria permanente y una personalidad estable. Flujo de trabajo de ejemplo: [麦洛薇人格AI](workflow/麦洛薇人格AI.json).

32. Puede utilizar esta máquina generadora de herramientas LLM para crear automáticamente herramientas LLM. Guarde el código de las herramientas generadas como un archivo python, luego copie el código en la carpeta custom_tool y habrá creado un nuevo nodo. Flujo de trabajo de ejemplo: [LLM工具生成器](workflow/LLM工具制造机.json).

33. Se ha habilitado la búsqueda en duckduckgo, aunque con importantes limitaciones; parece que solo se pueden ingresar palabras clave en inglés y no se pueden incluir múltiples conceptos. La ventaja es que no hay restricciones de API key.

34. Se ha añadido la función de invocación separada de múltiples bases de conocimiento, permitiendo especificar en el mensaje cuál base de conocimiento se utilizará para responder a las preguntas. Flujo de trabajo de ejemplo: [多知识库分别调用](workflow/多知识库分别调用.json).

35. Se admite la entrada de parámetros adicionales en el LLM, incluidos parámetros avanzados como json out. Flujo de trabajo de ejemplo: [LLM输入额外参数](workflow/LLM额外参数eg_JSON_OUT.json). [用json_out分离提示词](workflow/用json_out分离提示词.json).
36. Se ha añadido la función de conectar el agente a Discord. (Aún en fase de prueba)  
37. Se ha añadido la función de conectar el agente a Feishu. Agradecemos enormemente la contribución de [guobalove](https://github.com/guobalove). Consulte el flujo de trabajo [Robot de Feishu](workflow/飞书机器人.json).  
38. Se ha añadido un nodo de llamada a API universal y numerosos nodos auxiliares para construir el cuerpo de la solicitud y extraer información de la respuesta.  
39. Se ha añadido un nodo para limpiar el modelo, que permite descargar el LLM de la memoria en cualquier momento.  
40. Se ha añadido el nodo [chatTTS](https://github.com/2noise/ChatTTS). Agradecemos enormemente la contribución de [guobalove](https://github.com/guobalove). El parámetro `model_path` puede dejarse vacío. Se recomienda utilizar el modo HF para cargar el modelo, el cual se descargará automáticamente desde Hugging Face, sin necesidad de descarga manual; si se utiliza la carga local, coloque las carpetas `asset` y `config` del modelo en el directorio raíz. [Dirección de Baidu Cloud](https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu), código de extracción: qyhu; si se utiliza el modo `custom` para cargar, coloque las carpetas `asset` y `config` del modelo en el directorio `model_path`.
2. Se ha actualizado una serie de nodos de conversión: markdown a HTML, svg a imagen, HTML a imagen, mermaid a imagen, markdown a Excel.
1. Compatible con el modelo llama3.2 vision, admite diálogos de múltiples turnos, funciones visuales. Dirección del modelo: [meta-llama/Llama-3.2-11B-Vision-Instruct](https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct). Ejemplo de flujo de trabajo: [llama3.2_vision](https://github.com/heshengtao/comfyui_LLM_party/blob/main/workflow_tutorial/LLM_Party%20for%20Llama3.2%20-Vision%EF%BC%88%E5%B8%A6%E8%AE%B0%E5%BF%86%EF%BC%89.json).
1. Adaptado GOT-OCR2, admite resultados de salida formateados, admite el reconocimiento fino de texto utilizando cuadros de posición y colores. Dirección del modelo: [GOT-OCR2](https://huggingface.co/stepfun-ai/GOT-OCR2_0). El flujo de trabajo de ejemplo convierte una captura de pantalla de una página web en código HTML y luego abre el navegador para mostrar esta página web: [img2web](workflow/图片转网页.json).
2. Se han ajustado significativamente los nodos de carga de LLM locales, por lo que ya no necesitas elegir el tipo de modelo tú mismo. Se han vuelto a agregar el nodo de carga de llava y el nodo de carga de GGUF. El tipo de modelo en el nodo de la cadena de modelos LLM local se ha cambiado a LLM, VLM-GGUF y LLM-GGUF, lo que corresponde a cargar directamente modelos LLM, cargar modelos VLM y cargar modelos LLM en formato GGUF. Ahora se vuelven a admitir modelos VLM y modelos LLM en formato GGUF. ¡Las llamadas locales ahora pueden ser compatibles con más modelos! Ejemplos de flujos de trabajo: [LLM_local](workflow/start_with_LLM_local.json), [llava](workflow/start_with_llava.json), [GGUF](workflow/start_with_GGUF.json)
2. Se ha añadido el nodo EasyOCR para reconocer texto y posiciones en imágenes. Puede generar máscaras correspondientes y devolver una cadena JSON para que LLM la vea. ¡Hay versiones estándar y premium disponibles para todos!
2. En la fiesta comfyui LLM, se reprodujo el sistema de fresas del modelo de la serie chatgpt-o1, haciendo referencia a las indicaciones de [Llamaberry](https://huggingface.co/spaces/martinbowling/Llamaberry/blob/main/app.py). Ejemplo de flujo de trabajo: [Sistema de fresas comparado con o1](workflow/草莓系统与o1对比.json).
2. Se ha añadido un nuevo nodo GPT-sovits, que permite llamar al modelo GPT-sovits para convertir texto en voz basado en tu audio de referencia. También puedes rellenar la ruta de tu modelo afinado (si no se rellena, se utilizará el modelo base para la inferencia) para obtener cualquier voz deseada. Para usarlo, necesitas descargar el proyecto [GPT-sovits](https://github.com/RVC-Boss/GPT-SoVITS) y el modelo base correspondiente localmente, luego iniciar el servicio API con `runtime\python.exe api_v2.py` en la carpeta del proyecto GPT-sovits. Además, el nodo chatTTS se ha movido a [comfyui LLM mafia](https://github.com/heshengtao/comfyui_LLM_mafia). La razón es que chatTTS tiene muchas dependencias, y su licencia en PyPi es CC BY-NC 4.0, que es una licencia no comercial. Aunque el proyecto chatTTS en GitHub está bajo la licencia AGPL, movimos el nodo chatTTS a comfyui LLM mafia para evitar problemas innecesarios. ¡Esperamos que todos lo entiendan!
3. ¡Ahora admite el último modelo de OpenAI, la serie o1!
4. Se ha añadido una herramienta de control de archivos locales que permite al LLM controlar los archivos en la carpeta especificada, como leer, escribir, añadir, eliminar, renombrar, mover y copiar archivos.Debido al peligro potencial de este nodo, está incluido en [comfyui LLM mafia](https://github.com/heshengtao/comfyui_LLM_mafia).
5. Las nuevas herramientas SQL permiten a LLM consultar bases de datos SQL.
6. Actualizada la versión multilingüe del README. Flujo de trabajo para traducir el documento README: [translate_readme](workflow/文档自动翻译机.json)
7. Se han actualizado cuatro nodos iteradores (iterador de texto, iterador de imágenes, iterador de tablas, iterador json), con tres modos de iteración: secuencial, aleatorio e infinito. El modo secuencial emitirá los resultados en orden, deteniéndose automáticamente al superar el límite de índice y reiniciando el valor del índice a 0; el modo aleatorio elegirá un índice al azar para emitir; el modo infinito emitirá indefinidamente en bucle.
8. Se ha añadido un nodo cargador de API Gemini, ahora compatible con la API oficial de Gemini. Si estás en un entorno de red nacional y enfrentas problemas de restricción regional de la API, cambia el nodo a Estados Unidos y utiliza el modo TUN. Debido a que Gemini presenta un error con código de retorno 500 si los parámetros devueltos contienen caracteres en chino, algunos nodos de herramientas pueden no estar disponibles. Flujo de trabajo de ejemplo: [start_with_gemini](workflow/start_with_gemini.json)
9. Se ha añadido el nodo lore book, que permite insertar tus configuraciones de fondo al dialogar con el LLM. Flujo de trabajo de ejemplo: [lorebook](workflow/lorebook.json)
10. Se ha añadido el nodo generador de palabras clave FLUX, que puede generar palabras clave en varios estilos como cartas de Hearthstone, cartas de Yu-Gi-Oh, carteles, cómics, entre otros, permitiendo que el modelo FLUX genere directamente. Flujo de trabajo de referencia: [FLUX提示词](https://openart.ai/workflows/comfyui_llm_party/flux-by-llm-party/sjME541i68Kfw6Ib0EAD)

## Plan de acción siguiente:
1. Más adaptaciones de modelos;
2. Más formas de construir agentes;
3. Más funciones de automatización;
4. Más funciones de gestión de bases de conocimiento;
5. Más herramientas, más personajes.

## Aviso legal:
Este proyecto de código abierto y su contenido (en adelante, "el proyecto") son solo para fines de referencia y no implican ninguna garantía expresa o implícita. Los contribuyentes del proyecto no asumen ninguna responsabilidad por la integridad, precisión, fiabilidad o aplicabilidad del proyecto. Cualquier acción que dependa del contenido del proyecto debe asumir el riesgo por su cuenta. En ningún caso, los contribuyentes del proyecto serán responsables de cualquier pérdida o daño indirecto, especial o incidental que surja del uso del contenido del proyecto.
## Agradecimientos especiales
<a href="https://github.com/bigcat88">
  <img src="https://avatars.githubusercontent.com/u/13381981?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://github.com/guobalove">
  <img src="https://avatars.githubusercontent.com/u/171540731?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://github.com/HuangYuChuh">
  <img src="https://avatars.githubusercontent.com/u/167663109?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://github.com/SpenserCai">
  <img src="https://avatars.githubusercontent.com/u/25168945?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>

## Lista de proyectos referenciados
Algunos nodos en este proyecto se han inspirado en los siguientes proyectos. ¡Agradecemos su contribución a la comunidad de código abierto!
1. [pythongosssss/ComfyUI-Custom-Scripts](https://github.com/pythongosssss/ComfyUI-Custom-Scripts)
2. [lllyasviel/Omost](https://github.com/lllyasviel/Omost)

## Soporte:

### Únete a la comunidad
Si hay problemas con el complemento o si tiene alguna otra pregunta, le damos la bienvenida a unirse a nuestra comunidad.

1. Grupo de QQ: `931057213`
<div style="display: flex; justify-content: center;">
    <img src="img/Q群.jpg" style="width: 48%;" />
</div>

2. Grupo de WeChat: `Choo-Yong` (una vez que añada a la asistente de WeChat, podrá unirse al grupo)

3. Discord: [enlace de discord](https://discord.gg/f2dsAKKr2V)

### Síguenos
1. Si desea mantenerse informado sobre las últimas funciones de este proyecto, le invitamos a seguir nuestra cuenta de Bilibili: [主持BB机](https://space.bilibili.com/26978344)
2. La cuenta de OpenArt se actualiza continuamente con los flujos de trabajo de fiesta más útiles: [openart](https://openart.ai/workflows/profile/comfyui_llm_party?sort=latest&tab=creation)

### Apoyo a donaciones
Si mi trabajo le ha aportado valor, ¡considere invitarme a un café! Su apoyo no solo revitaliza el proyecto, sino que también calienta el corazón del creador.☕💖 ¡Cada taza cuenta!
<div style="display:flex; justify-content:space-between;">
    <img src="img/zhifubao.jpg" style="width: 48%;" />
    <img src="img/wechat.jpg" style="width: 48%;" />
</div>

## Historial de estrellas

[![Gráfico de Historial de Estrellas](https://api.star-history.com/svg?repos=heshengtao/comfyui_LLM_party&type=Date)](https://star-history.com/#heshengtao/comfyui_LLM_party&Date)
