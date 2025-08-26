![صورة](img/封面.png)

<div align="center">
  <a href="https://space.bilibili.com/26978344">bilibili</a> ·
  <a href="https://www.youtube.com/@LLM-party">youtube</a> ·
  <a href="https://github.com/heshengtao/Let-LLM-party">دليل النص</a> ·
  <a href="https://pan.quark.cn/s/190b41f3bbdb">عنوان القرص السحابي</a> ·
  <a href="img/Q群.jpg">مجموعة QQ</a> ·
  <a href="https://discord.gg/f2dsAKKr2V">ديسكورد</a> ·
  <a href="https://dcnsxxvm4zeq.feishu.cn/wiki/IyUowXNj9iH0vzk68cpcLnZXnYf">معلومات عنا</a>
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

تسعى Comfyui_llm_party إلى تطوير مكتبة كاملة من العقد لبناء سير العمل لـ LLM، مستندةً إلى واجهة المستخدم البسيطة [comfyui](https://github.com/comfyanonymous/ComfyUI) كواجهة أمامية. مما يتيح للمستخدمين بناء سير العمل الخاص بهم بشكل أسرع وأسهل، ويسهل دمج ذلك في سير العمل الخاص بالصور.

## عرض النتائج
https://github.com/user-attachments/assets/945493c0-92b3-4244-ba8f-0c4b2ad4eba6

## نظرة عامة على المشروع
ComfyUI LLM Party، من أبسط استدعاءات أدوات LLM المتعددة، وإعداد الشخصيات لبناء مساعد AI الخاص بك بسرعة، إلى RAG وGraphRAG القابلة للتطبيق في الصناعة لإدارة قواعد المعرفة المحلية؛ من خط أنابيب وكيل واحد إلى بناء أنماط تفاعل معقدة بين الوكلاء وأنماط تفاعل دائرية؛ من الحاجة الفردية للمستخدمين للوصول إلى تطبيقات التواصل الاجتماعي الخاصة بهم (QQ، Feishu، Discord)، إلى تدفقات العمل الشاملة التي يحتاجها العاملون في وسائل الإعلام LLM+TTS+ComfyUI؛ من بدء استخدام تطبيق LLM الأول للطلاب العاديين، إلى واجهات ضبط المعلمات التي يستخدمها الباحثون. كل هذا يمكنك العثور على إجابات له في ComfyUI LLM Party.

## بدء سريع
0. إذا لم تقم باستخدام comfyui من قبل، وواجهت بعض مشاكل الاعتماد عند تثبيت LLM party في comfyui، يرجى النقر على [هنا](https://drive.google.com/file/d/1T9C7gEbd-w_zf9GqZO1VeI3z8ek8clpX/view?usp=sharing) لتحميل حزمة comfyui **windows** المحمولة التي تحتوي على LLM party. ملاحظة! تحتوي هذه الحزمة المحمولة فقط على المكونين الإضافيين party و manager، وهي مناسبة فقط لنظام تشغيل ويندوز.(إذا كنت بحاجة لتثبيت LLM party على comfyui القائم، يمكن تخطي هذه الخطوة.)
1. اسحب سير العمل التالي إلى comfyui الخاص بك، ثم استخدم [comfyui-Manager](https://github.com/ltdrdata/ComfyUI-Manager) لتثبيت العقد المفقودة.
  - استخدم API لاستدعاء LLM: [start_with_LLM_api](workflow/start_with_LLM_api.json)
  - استخدام aisuite لاستدعاء LLM: [بدء_باستخدام_aisuite](workflow/start_with_aisuite.json)
  - إدارة LLM المحلي باستخدام ollama: [start_with_Ollama](workflow/ollama.json)
  - استخدم LLM المحلي بتنسيق موزع: [start_with_LLM_local](workflow/start_with_LLM_local.json)
  - استخدم LLM المحلي بتنسيق GGUF: [start_with_LLM_GGUF](workflow/start_with_GGUF.json)
  - استخدم VLM المحلي بتنسيق موزع: [start_with_VLM_local](workflow/start_with_VLM_local.json) (تدعم حاليًا [Llama-3.2-Vision](https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct)/[Qwen/Qwen2.5-VL](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct)/[deepseek-ai/Janus-Pro](https://huggingface.co/deepseek-ai/Janus-Pro-1B))
  - استخدم VLM المحلي بتنسيق GGUF: [start_with_VLM_GGUF](workflow/start_with_llava.json)
  - استخدام واجهة برمجة التطبيقات لاستدعاء LLM لتوليد كلمات مفتاحية لـ SD وتوليد الصورة: [start_with_VLM_API_for_SD](workflow/start_with_VLM_API_for_SD.json)
  - استخدام ollama لاستدعاء minicpm لتوليد كلمات مفتاحية لـ SD وتوليد الصورة: [start_with_ollama_minicpm_for_SD](workflow/start_with_ollama_minicpm_for_SD.json)
  - استخدام qwen-vl المحلي لتوليد كلمات مفتاحية لـ SD وتوليد الصورة: [start_with_qwen_vl_local_for_SD](workflow/start_with_qwen_vl_local_for_SD.json)
2. إذا كنت تستخدم API، فاملأ `base_url` (يمكن أن يكون API وسيط، تأكد من أنه ينتهي بـ `/v1/`) و`api_key` في عقدة تحميل API LLM. مثال: `https://api.openai.com/v1/`
3. إذا كنت تستخدم ollama، فقم بتشغيل خيار `is_ollama` في عقدة تحميل API LLM، ولا حاجة لملء `base_url` و`api_key`.
4. إذا كنت تستخدم نموذجًا محليًا، فاملأ مسار النموذج الخاص بك في عقدة تحميل النموذج المحلي، على سبيل المثال: `E:\model\Llama-3.2-1B-Instruct`. يمكنك أيضًا ملء معرف مستودع النموذج في Huggingface في عقدة تحميل النموذج المحلي، على سبيل المثال: `lllyasviel/omost-llama-3-8b-4bits`.
5. نظرًا للعتبة العالية لاستخدام هذا المشروع، حتى إذا اخترت البدء السريع، آمل أن تتمكن من قراءة الصفحة الرئيسية للمشروع بصبر.

## التحديثات الأخيرة
1. تم تمكين وضع الإخراج المتدفق لواجهة LLM API، وسيتم عرض نصوص الإخراج من واجهة برمجة التطبيقات في وحدة التحكم بشكل متدفق، مما يتيح لك رؤية المخرجات من واجهة برمجة التطبيقات في الوقت الفعلي، دون الحاجة إلى انتظار اكتمال الطلب بالكامل.
2. أضافت واجهة LLM API ميزة إخراج reasoning_content، التي تستطيع فصل reasoning واستجابة نموذج R1 تلقائيًا.
3. تمت إضافة فرع مستودع only_api، والذي يتضمن فقط الأجزاء الخاصة بالاستدعاء API، لتسهيل الأمر على المستخدمين الذين يحتاجون فقط إلى استدعاء API. يمكن للمستخدمين ببساطة استخدام سطر الأوامر في مجلد `custom node` الخاص بـ `comfyui` بتنفيذ الأمر `git clone -b only_api https://github.com/heshengtao/comfyui_LLM_party.git`، ثم اتباع خطة نشر البيئة المذكورة في الصفحة الرئيسية لهذا المشروع لاستخدام هذا الفرع. ملاحظة! إذا كنت بحاجة إلى ضمان عدم وجود مجلد آخر يسمى `comfyui_LLM_party` في مجلد `custom node`.
1. لقد دعم العقدة المحلية لمحمّل VLM [deepseek-ai/Janus-Pro](https://huggingface.co/deepseek-ai/Janus-Pro-1B)، مثال على سير العمل: [Janus-Pro](workflow/deepseek-janus-pro.json)
1. لقد دعم عقدة المحمل المحلي لـ VLM [Qwen/Qwen2.5-VL-3B-Instruct](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct)، ولكن يجب عليك تحديث مكتبة transformer إلى أحدث إصدار (```pip install -U transformers```)، سير العمل النموذجي: [qwen-vl](workflow/qwen-vl.json)
1. لقد تم إضافة نقطة استضافة صور جديدة تمامًا، والتي تدعم حاليًا خدمة استضافة الصور https://sm.ms (النطاق في مناطق الصين هو https://smms.app) بالإضافة إلى خدمة استضافة الصور https://imgbb.com، وسيتم دعم المزيد من خدمات استضافة الصور في المستقبل. نموذج سير العمل: [استضافة الصور](workflow/图床.json)
1. ~~لقد تم تحديث خدمة استضافة الصور الافتراضية المستخدمة في party إلى [imgbb](https://imgbb.io) على هذا النطاق، حيث كانت الخدمة السابقة غير مرحب بها لمستخدمي البر الرئيسي الصيني، لذا تم تغييرها.~~ أعتذر بشدة، يبدو أن خدمة واجهة برمجة التطبيقات لاستضافة الصور على https://imgbb.io قد توقفت، لذلك تم الرجوع إلى https://imgbb.com. أشكر الجميع على تفهمهم. سأقوم في المستقبل بتحديث خادم يدعم المزيد من خدمات استضافة الصور.
1. تم تحديث أداة [MCP](https://modelcontextprotocol.io/introduction) ، يمكنك تعديل الإعدادات في ملف '[mcp_config.json](mcp_config.json)' الموجود ضمن مجلد مشروع party لتغيير إعدادات اتصالك بخادم MCP. يمكنك العثور هنا على مجموعة متنوعة من معلمات تكوين خوادم MCP التي ترغب في إضافتها: [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers). في هذا المشروع، الإعداد الافتراضي هو خادم Everything، وهو خادم يُستخدم لاختبار ما إذا كان خادم MCP يعمل بشكل صحيح. مرجع سير العمل: [start_with_MCP](workflow/start_with_MCP.json). ملاحظة للمطورين: يمكن لعقدة أداة MCP الاتصال بخادم MCP الذي قمت بتكوينه، ثم تحويل الأدوات الموجودة في الخادم إلى أدوات يمكن استخدامها مباشرة بواسطة LLM. من خلال تكوين خوادم محلية أو سحابية مختلفة، يمكنك تجربة جميع أدوات LLM المتاحة في هذا العالم.

## تعليمات الاستخدام
1. يرجى الرجوع إلى تعليمات استخدام العقدة: [怎么使用节点](https://github.com/heshengtao/Let-LLM-party)

2. إذا كانت هناك مشاكل في المكون الإضافي أو إذا كان لديك أي استفسارات أخرى، فنحن نرحب بك للانضمام إلى مجموعة QQ: [931057213](img/Q群.jpg) | discord：[discord](https://discord.gg/f2dsAKKr2V).

4. يمكن الاطلاع على المزيد من سير العمل في مجلد [workflow](workflow)

## دروس الفيديو
<a href="https://space.bilibili.com/26978344">
  <img src="img/B.png" width="100" height="100" style="border-radius: 80%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://www.youtube.com/@LLM-party">
  <img src="img/YT.png" width="100" height="100" style="border-radius: 80%; overflow: hidden;" alt="octocat"/>
</a>

## دعم النموذج
1. يدعم جميع استدعاءات واجهة برمجة التطبيقات بتنسيق openai (بالاشتراك مع [oneapi](https://github.com/songquanpeng/one-api) يمكن استدعاء تقريبًا جميع واجهات برمجة التطبيقات LLM، كما يدعم جميع واجهات البرمجة الوسيطة)، يرجى الرجوع إلى اختيار base_url في [config.ini.example](config.ini.example)، وقد تم اختبار ما يلي حتى الآن:
* [openai](https://platform.openai.com/docs/api-reference/chat/create) (متوافق تمامًا مع جميع نماذج OpenAI، بما في ذلك السلسلتين 4o و o1!)
* [ollama](https://github.com/ollama/ollama) (موصى به! إذا كنت تتصل محليًا، فمن المستحسن بشدة استخدام طريقة ollama لاستضافة النموذج المحلي الخاص بك!)
* [Azure OpenAI](https://azure.microsoft.com/zh-cn/products/ai-services/openai-service/)
* [llama.cpp](https://github.com/ggerganov/llama.cpp?tab=readme-ov-file#web-server) (موصى به! إذا كنت ترغب في استخدام نموذج تنسيق gguf المحلي، يمكنك استخدام واجهة برمجة تطبيقات مشروع llama.cpp للوصول إلى هذا المشروع!)
* [Grok](https://x.ai/api)
* [通义千问/qwen](https://help.aliyun.com/zh/dashscope/developer-reference/compatibility-of-openai-with-dashscope/?spm=a2c4g.11186623.0.0.7b576019xkArPq)
* [智谱清言/glm](https://open.bigmodel.cn/dev/api#http_auth)
* [deepseek](https://platform.deepseek.com/api-docs/zh-cn/)
* [kimi/moonshot](https://platform.moonshot.cn/docs/api/chat#%E5%9F%BA%E6%9C%AC%E4%BF%A1%E6%81%AF)
* [doubao](https://www.volcengine.com/docs/82379/1263482)
* [讯飞星火/spark](https://xinghuo.xfyun.cn/sparkapi?scr=price)
* [جيميناي](https://developers.googleblog.com/zh-hans/gemini-is-now-accessible-from-the-openai-library/)(تم إهمال عقدة محمل API LLM الأصلية لجيميناي في الإصدار الجديد، يرجى استخدام عقدة محمل LLM API، واختر base_url ليكون: https://generativelanguage.googleapis.com/v1beta/openai/)

2. دعم جميع استدعاءات واجهة برمجة التطبيقات المتوافقة مع [aisuite](https://github.com/andrewyng/aisuite):
* [anthropic/claude](https://www.anthropic.com/)
* [aws](https://docs.aws.amazon.com/solutions/latest/generative-ai-application-builder-on-aws/api-reference.html)
* [vertex](https://cloud.google.com/vertex-ai/docs/reference/rest)
* [huggingface](https://huggingface.co/)

3. متوافق مع معظم النماذج المحلية في مكتبة transformer (تم تغيير نوع النموذج على عقدة سلسلة نماذج LLM المحلية إلى LLM وVLM-GGUF وLLM-GGUF، مما يتوافق مع تحميل نماذج LLM مباشرة، وتحميل نماذج VLM، وتحميل نماذج LLM بتنسيق GGUF). إذا أبلغ نموذج LLM بتنسيق VLM أو GGUF عن خطأ، فيرجى تنزيل أحدث إصدار من llama-cpp-python من [llama-cpp-python](https://github.com/abetlen/llama-cpp-python/releases). النماذج التي تم اختبارها حاليًا تشمل:
* [ClosedCharacter/Peach-9B-8k-Roleplay](https://huggingface.co/ClosedCharacter/Peach-9B-8k-Roleplay) (موصى به! نموذج لعب الأدوار)
* [lllyasviel/omost-llama-3-8b-4bits](https://huggingface.co/lllyasviel/omost-llama-3-8b-4bits) (موصى به! نموذج غني بالكلمات الرئيسية)
* [meta-llama/Llama-2-7b-chat-hf](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)
* [Qwen/Qwen2-7B-Instruct](https://huggingface.co/Qwen/Qwen2-7B-Instruct)
* [openbmb/MiniCPM-V-2_6-gguf](https://huggingface.co/openbmb/MiniCPM-V-2_6-gguf/tree/main)
* [lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF](https://huggingface.co/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/tree/main)
* [meta-llama/Llama-3.2-11B-Vision-Instruct](https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct)
* [Qwen/Qwen2.5-VL-3B-Instruct](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct)
* [deepseek-ai/Janus-Pro](https://huggingface.co/deepseek-ai/Janus-Pro-1B)

4. تحميل النموذج:
* [عنوان سحابة كوارك](https://pan.quark.cn/s/190b41f3bbdb)
* [رابط بايدو السحابي](https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu)، رمز الاستخراج: qyhu

## تحميل
استخدم إحدى الطرق التالية للتثبيت
### الطريقة الأولى:
1. ابحث عن `comfyui_LLM_party` في [مدير comfyui](https://github.com/ltdrdata/ComfyUI-Manager) وقم بالتثبيت بنقرة واحدة
2. أعد تشغيل comfyui
### الطريقة الثانية:
1. انتقل إلى المجلد الجذري لـ ComfyUI ثم إلى المجلد الفرعي `custom_nodes`
2. استخدم أمر استنساخ هذا المستودع. `git clone https://github.com/heshengtao/comfyui_LLM_party.git`

### الطريقة الثالثة:
1. انقر على الزر `CODE` في الزاوية العلوية اليمنى
2. انقر على `download zip`
3. قم بفك ضغط الملف المضغوط الذي تم تنزيله في المجلد الفرعي `custom_nodes` داخل المجلد الجذري لـ ComfyUI

## نشر البيئة
1. انتقل إلى مجلد المشروع الخاص بـ `comfyui_LLM_party`
2. في الطرفية، أدخل `pip install -r requirements.txt` لتثبيت المكتبات الخارجية اللازمة لهذا المشروع في بيئة comfyui. يرجى التأكد من أنك تقوم بالتثبيت في بيئة comfyui، وراقب أي أخطاء تظهر في الطرفية المتعلقة بـ `pip`
3. إذا كنت تستخدم مشغل comfyui، يجب عليك إدخال الأمر `مسار التكوين في المشغل\python_embeded\python.exe -m pip install -r requirements.txt` للتثبيت. عادةً ما يكون مجلد `python_embeded` في نفس مستوى مجلد `ComfyUI`.
4. إذا واجهت بعض مشاكل تكوين البيئة، يمكنك محاولة استخدام الاعتماديات الموجودة في `requirements_fixed.txt`.
## الإعداد
* يمكنك تكوين اللغة في `config.ini`، حاليًا لا توجد سوى لغتين، هما الصينية (zh_CN) والإنجليزية (en_US)، والإعداد الافتراضي هو لغة النظام الخاص بك.
* يمكنك تكوين ما إذا كنت ترغب في التثبيت السريع في `config.ini`، حيث أن `fast_installed` هو `False` افتراضيًا، إذا كنت لا تحتاج إلى استخدام نموذج GGUF، يمكنك ضبطه على `True`.
* يمكنك استخدام واحدة من الطرق التالية لتكوين APIKEY
### الطريقة الأولى:
1. افتح ملف `config.ini` في مجلد مشروع `comfyui_LLM_party`.
2. في `config.ini`، أدخل `openai_api_key` و `base_url` الخاصين بك.
3. إذا كنت تستخدم نموذج ollama، أدخل في `base_url` `http://127.0.0.1:11434/v1/`، وفي `openai_api_key` أدخل `ollama`، وفي `model_name` أدخل اسم نموذجك، مثل: llama3.
4. إذا كنت ترغب في استخدام أدوات بحث جوجل أو بينغ، أدخل `google_api_key` و `cse_id` أو `bing_api_key` في `config.ini`.
5. إذا كنت ترغب في استخدام إدخال الصور في LLM، يُوصى باستخدام خدمة imgBB، أدخل `imgbb_api` الخاص بك في `config.ini`.
6. يمكن تكوين كل نموذج بشكل منفصل في ملف `config.ini`، يمكنك الرجوع إلى ملف `config.ini.example` للملء. بعد تكوينك، تحتاج فقط إلى إدخال `model_name` في العقدة.

### الطريقة الثانية:
1. افتح واجهة comfyui.
2. أنشئ عقدة نموذج لغة كبيرة (LLM)، وأدخل مباشرة `openai_api_key` و `base_url` الخاصين بك في العقدة.
3. إذا كنت تستخدم نموذج ollama، يرجى استخدام عقدة LLM_api، أدخل في `base_url` `http://127.0.0.1:11434/v1/`، وفي `api_key` أدخل `ollama`، وفي `model_name` أدخل اسم نموذجك، مثل: llama3.
4. إذا كنت ترغب في استخدام إدخال الصور في LLM، يُوصى باستخدام خدمة imgBB، أدخل `imgbb_api_key` الخاص بك في العقدة.

## سجل التحديثات
**[Click here](change_log.md)**

## الخطوات التالية:
1. المزيد من تكييف النماذج;
2. المزيد من طرق بناء الوكلاء;
3. المزيد من ميزات الأتمتة;
4. المزيد من ميزات إدارة قاعدة المعرفة;
5. المزيد من الأدوات، المزيد من الشخصيات.

## مشروع آخر مفتوح المصدر من مشاريعي:
[super-agent-party](https://github.com/heshengtao/super-agent-party) هو تطبيق رفيق سطح مكتب ثلاثي الأبعاد ذكي بلا حدود! يدعم بالفعل ميزات مثل RAG، البحث على الإنترنت، الذاكرة طويلة المدى، مفسر الأكواد، MCP، A2A، Comfyui، روبوت QQ والمزيد!
![image](img/vrmbot.jpeg)

## إخلاء المسؤولية:
هذا المشروع المفتوح المصدر ومحتواه (المشار إليه فيما يلي بـ "المشروع") هو لأغراض مرجعية فقط، ولا يعني أي ضمانات صريحة أو ضمنية. لا يتحمل المساهمون في المشروع أي مسؤولية عن كمال المشروع أو دقته أو موثوقيته أو ملاءمته. أي تصرف يعتمد على محتوى المشروع يجب أن يتحمل المخاطر بنفسه. في أي حالة من الأحوال، لا يتحمل المساهمون في المشروع أي مسؤولية عن أي خسائر أو أضرار غير مباشرة أو خاصة أو تبعية ناتجة عن استخدام محتوى المشروع.

## شكر خاص
<a href="https://github.com/bigcat88">
  <img src="https://avatars.githubusercontent.com/u/13381981?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://github.com/guobalove">
  <img src="https://avatars.githubusercontent.com/u/171540731?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://github.com/SpenserCai">
  <img src="https://avatars.githubusercontent.com/u/25168945?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>

## قائمة الاقتراض
بعض العقد في هذا المشروع مستوحاة من المشاريع التالية، نشكرهم على مساهماتهم في مجتمع المصادر المفتوحة!
1. [pythongosssss/ComfyUI-Custom-Scripts](https://github.com/pythongosssss/ComfyUI-Custom-Scripts)
2. [lllyasviel/Omost](https://github.com/lllyasviel/Omost)

## الدعم:

### انضم إلى المجتمع
إذا كانت هناك مشكلات في الملحق أو كانت لديك أي استفسارات أخرى، فلا تتردد في الانضمام إلى مجتمعنا.

1. مجموعة QQ: `931057213`
<div style="display: flex; justify-content: center;">
    <img src="img/Q群.jpg" style="width: 48%;" />
</div>

2. مجموعة وي شات：`we_glm`（أضف مساعدنا إلى وي شات ثم انضم إلى المجموعة）

3. ديسكورد: [رابط الديسكورد](https://discord.gg/f2dsAKKr2V)

### تابعونا
1. إذا كنت ترغب في متابعة أحدث ميزات هذا المشروع، ندعوك لمتابعة حسابنا على بلي بلي: [派酱](https://space.bilibili.com/26978344)
2. [youtube@LLM-party](https://www.youtube.com/@LLM-party)

## تاريخ النجوم

[![Star History Chart](https://api.star-history.com/svg?repos=heshengtao/comfyui_LLM_party&type=Date)](https://star-history.com/#heshengtao/comfyui_LLM_party&Date)
