![صورة](img/封面.png)

<div align="center">
  <a href="https://space.bilibili.com/26978344">دليل الفيديو</a> ·
  <a href="how_to_use_nodes_ZH.md">دليل النص</a> ·
  <a href="workflow_tutorial/">دليل سير العمل</a> ·
  <a href="https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu">رابط دودة</a> ·
  <a href="img/Q群.jpg">مجموعة QQ</a> ·
  <a href="https://discord.gg/gxrQAYy6">ديسكورد</a> ·
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
https://github.com/user-attachments/assets/9e627204-4626-479e-8806-cb06cd6157a6
## نظرة عامة على المشروع
ComfyUI LLM Party، من أبسط استدعاءات أدوات LLM المتعددة، وإعداد الشخصيات لبناء مساعد AI الخاص بك بسرعة، إلى RAG وGraphRAG القابلة للتطبيق في الصناعة لإدارة قواعد المعرفة المحلية؛ من خط أنابيب وكيل واحد إلى بناء أنماط تفاعل معقدة بين الوكلاء وأنماط تفاعل دائرية؛ من الحاجة الفردية للمستخدمين للوصول إلى تطبيقات التواصل الاجتماعي الخاصة بهم (QQ، Feishu، Discord)، إلى تدفقات العمل الشاملة التي يحتاجها العاملون في وسائل الإعلام LLM+TTS+ComfyUI؛ من بدء استخدام تطبيق LLM الأول للطلاب العاديين، إلى واجهات ضبط المعلمات التي يستخدمها الباحثون. كل هذا يمكنك العثور على إجابات له في ComfyUI LLM Party.

## التحديثات الأخيرة
1. تم تحديث النسخة متعددة اللغات من README. سير العمل لترجمة وثيقة README: [translate_readme](workflow/文档自动翻译机.json)
2. تم تحديث أربعة عقد متكررة (عقدة النص، عقدة الصورة، عقدة الجدول، عقدة json)، أنماط المتكررات هي: تسلسلي، عشوائي ولا نهائي. التسلسلي سيخرج بالتتابع حتى يتجاوز الحد الأقصى للفهرس ويتوقف تلقائيًا، مما يعيد تعيين قيمة الفهرس إلى 0، والعشوائي سيختار فهرسًا عشوائيًا للإخراج، واللانهائي سيخرج باستمرار.
3. تمت إضافة عقدة محمل Gemini API، وهي الآن متوافقة مع API الرسمي لـ Gemini! إذا كنت في بيئة شبكة محلية، وإذا ظهرت مشكلة تقييد المنطقة مع API، يرجى تحويل العقدة إلى الولايات المتحدة واستخدام وضع TUN. نظرًا لأن Gemini في استدعاء الأدوات، إذا كان هناك أحرف صينية في المعلمات المعادة، فستظهر رسالة خطأ برمز 500، لذا فإن بعض عقد الأدوات غير متاحة. تدفق العمل النموذجي: [start_with_gemini](workflow/start_with_gemini.json)
4. تمت إضافة عقدة lore book، يمكنك من خلالها إدخال إعدادات الخلفية الخاصة بك أثناء الدردشة مع LLM، تدفق العمل النموذجي: [lorebook](workflow/lorebook.json)
5. تمت إضافة عقدة مولد الكلمات المفتاحية FLUX، يمكنها إنشاء كلمات مفتاحية بأنماط متعددة مثل بطاقات Hearthstone، بطاقات Yu-Gi-Oh، الملصقات، والقصص المصورة، مما يسمح لنموذج FLUX بالإنتاج المباشر. تدفق العمل المرجعي: [FLUX提示词](https://openart.ai/workflows/comfyui_llm_party/flux-by-llm-party/sjME541i68Kfw6Ib0EAD)

## تعليمات الاستخدام
1. يرجى الرجوع إلى تعليمات استخدام العقدة: [怎么使用节点](how_to_use_nodes.md)

2. إذا كانت هناك مشاكل في المكون الإضافي أو إذا كان لديك أي استفسارات أخرى، فنحن نرحب بك للانضمام إلى مجموعة QQ: [931057213](img/Q群.jpg)
3. يُرجى الرجوع إلى [دليل سير العمل](workflow_tutorial/) ، شكرًا لمساهمة [HuangYuChuh](https://github.com/HuangYuChuh)！

4. حساب لعب سير العمل المتقدم: [openart](https://openart.ai/workflows/profile/comfyui_llm_party?sort=latest&tab=creation)

4. يمكن الاطلاع على المزيد من سير العمل في مجلد [workflow](workflow)

## دروس الفيديو
1. [دليل خطوة بخطوة لبناء وكيل ذكي بطريقة الكتل (سهل جدًا！)](https://www.bilibili.com/video/BV1JZ421v7Tw/?vd_source=f229e378448918b84afab7c430c6a75b)

2. [كيفية توصيل GPT-4o بـ comfyui | جعل سير العمل يستدعي سير عمل آخر | تحويل LLM إلى أداة](https://www.bilibili.com/video/BV1JJ4m1A789/?spm_id_from=333.999.0.0&vd_source=f229e378448918b84afab7c430c6a75b)

3. [تخفي سير عملك كـ GPT لتوصيله بـ WeChat | متوافق مع Omost！ أنشئ Dalle3 الخاص بك بمرونة](https://www.bilibili.com/video/BV1DT421a7KY/?spm_id_from=333.999.0.0)

4. [كيفية اللعب بألعاب الروايات التفاعلية في comfyui](https://www.bilibili.com/video/BV15y411q78L/?spm_id_from=333.999.0.0&vd_source=f229e378448918b84afab7c430c6a75b)

5. [صديقة AI ، وهي على شكل شخصيتك | تنفيذ graphRAG على comfyui ، والتفاعل مع neoa4j | توصيل سير عمل comfyui بـ streamlit](https://www.bilibili.com/video/BV1dS421R7Au/?spm_id_from=333.999.0.0&vd_source=f229e378448918b84afab7c430c6a75b)
## دعم النموذج
1. يدعم جميع استدعاءات واجهة برمجة التطبيقات بتنسيق openai (بالاشتراك مع [oneapi](https://github.com/songquanpeng/one-api) يمكن استدعاء تقريبًا جميع واجهات برمجة التطبيقات LLM، كما يدعم جميع واجهات البرمجة الوسيطة)، يرجى الرجوع إلى اختيار base_url في [config.ini.example](config.ini.example)، وقد تم اختبار ما يلي حتى الآن:
* [ollama](https://github.com/ollama/ollama) (موصى به! إذا كنت تستخدم استدعاء محلي، يُوصى بشدة باستخدام طريقة ollama لاستضافة نموذجك المحلي!)
* [通义千问/qwen](https://help.aliyun.com/zh/dashscope/developer-reference/compatibility-of-openai-with-dashscope/?spm=a2c4g.11186623.0.0.7b576019xkArPq)
* [智谱清言/glm](https://open.bigmodel.cn/dev/api#http_auth)
* [deepseek](https://platform.deepseek.com/api-docs/zh-cn/)
* [kimi/moonshot](https://platform.moonshot.cn/docs/api/chat#%E5%9F%BA%E6%9C%AC%E4%BF%A1%E6%81%AF)
* [豆包](https://www.volcengine.com/docs/82379/1263482)

2. يدعم استدعاءات واجهة برمجة التطبيقات بتنسيق Gemini:
* [Gemini](https://aistudio.google.com/app/prompts/new_chat)
3. متوافق مع معظم النماذج المحلية المدعومة من فئة AutoModelForCausalLM في مكتبة transformer (إذا لم تكن متأكدًا من اختيار نوع النموذج على عقدة النموذج المحلي، يمكنك اختيار llama، من المحتمل أن يكون متوافقًا)، وقد تم اختبار ما يلي:
* [ClosedCharacter/Peach-9B-8k-Roleplay](https://huggingface.co/ClosedCharacter/Peach-9B-8k-Roleplay) (موصى به! نموذج لعب الأدوار)
* [omost-llama-3-8b-4bits](https://huggingface.co/lllyasviel/omost-llama-3-8b-4bits) (موصى به! نموذج غني بالكلمات الرئيسية)
* [meta-llama/Llama-2-7b-chat-hf](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)
* [Qwen/Qwen2-7B-Instruct](https://huggingface.co/Qwen/Qwen2-7B-Instruct)
* [xtuner/llava-llama-3-8b-v1_1-gguf](https://huggingface.co/xtuner/llava-llama-3-8b-v1_1-gguf)
* [THUDM/chatglm3-6b](https://huggingface.co/THUDM/chatglm3-6b) (نظرًا لأن GLM4 قد غيرت تنسيق الاستدعاء الجديد، فإن المطورين غير قادرين على الحفاظ على استدعاء جميع النماذج الكبيرة المحلية، لذلك يُوصى للجميع باستخدام طريقة ollama للاستدعاء المحلي!)

4. تحميل النموذج:
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
* يمكنك تكوين اللغة في `config.ini`، حالياً يتوفر فقط اللغتين الصينية (zh_CN) والإنجليزية (en_US)، والافتراضي هو لغة نظامك.
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
1. يمكنك النقر بزر الماوس الأيمن في واجهة **comfyui** واختيار `llm` من قائمة السياق، للعثور على عقدة هذا المشروع. [كيفية استخدام العقد](how_to_use_nodes_ZH.md)
2. يدعم الاتصال عبر API أو الاتصال بالنموذج الكبير المحلي. تم تنفيذ وظيفة استدعاء الأدوات بشكل وحدوي. عند إدخال **base_url**، يرجى إدخال عنوان URL الذي ينتهي بـ `/v1/`. يمكنك استخدام [ollama](https://github.com/ollama/ollama) لإدارة نماذجك، ثم أدخل `http://127.0.0.1:11434/v1/` في **base_url**، وأدخل **ollama** في **api_key**، وأدخل اسم نموذجك في **model_name**، على سبيل المثال: **llama3**.
- مثال على سير العمل مع API: [start_with_LLM_api](workflow/start_with_LLM_api.json)
- مثال على سير العمل مع النموذج المحلي: [start_with_LLM_local](workflow/start_with_LLM_local.json)
- مثال على سير العمل مع **ollama**: [ollama](workflow/ollama.json)
3. دعم الاتصال بمكتبة المعرفة المحلية، يدعم **RAG**. مثال على سير العمل: [知识库RAG搜索.json](workflow/知识库RAG搜索.json)
4. يمكن استدعاء مفسر الأكواد.
5. يمكن البحث عبر الإنترنت، يدعم بحث Google. مثال على سير العمل: [电影查询工作流](workflow/电影查询工作流.json)
6. يمكنك تنفيذ عبارات الشرط في **comfyui**، ويمكنك تصنيف أسئلة المستخدم قبل الرد بشكل مستهدف. مثال على سير العمل: [智能客服](workflow/智能客服.json)
7. يدعم الارتباط الدائري للنماذج الكبيرة، مما يسمح لنموذجين كبيرين بالجدال. مثال على سير العمل: [电车难题辩论赛](workflow/电车难题辩论赛.json)
8. يدعم توصيل أي قناع شخصية، يمكنك تخصيص قوالب النصوص.
9. يدعم استدعاء أدوات متعددة، وقد تم تطوير وظائف مثل التحقق من الطقس، والتحقق من الوقت، ومكتبة المعرفة، وتنفيذ الأكواد، والبحث عبر الإنترنت، والبحث في صفحة ويب واحدة.
10. يدعم استخدام **LLM** كعقدة أداة. مثال على سير العمل: [LLM套娃](workflow/LLM套娃.json)
11. يدعم تطوير تطبيقات الويب الخاصة بك بسرعة من خلال **API + streamlit**.
12. تم إضافة عقدة المفسر الشامل الخطير، مما يسمح للنموذج الكبير بفعل أي شيء.
13. يوصى باستخدام الوظائف الموجودة في دليل النصوص (show_text) في قائمة السياق كإخراج لعقدة **LLM**.
14. تم دعم ميزة الرؤية في GPT-4O! مثال على سير العمل: [GPT-4o](workflow/GPT-4o.json)
15. تم إضافة محول سير العمل، مما يتيح لسير العمل الخاص بك استدعاء سير عمل آخر! مثال على سير العمل: [استدعاء سير عمل آخر](workflow/调用另一个工作流.json)
16. تم التوافق مع جميع النماذج التي تحتوي على واجهة مشابهة لـ openai، مثل: 通义千问/qwen، 智谱清言/GLM، deepseek، kimi/moonshot. يرجى ملء base_url و api_key و model_name لهذه النماذج في عقدة LLM لاستدعائها.
17. تم إضافة محمل LVM جديد، يمكنك الآن استدعاء نموذج LVM محليًا، ويدعم نموذج [llava-llama-3-8b-v1_1-gguf](https://huggingface.co/xtuner/llava-llama-3-8b-v1_1-gguf)، يجب أن تكون النماذج الأخرى من نوع LVM إذا كانت بتنسيق GGUF قادرة على العمل أيضًا. مثال على سير العمل هنا: [start_with_LVM.json](workflow/start_with_LVM.json).
18. كتبت ملف `fastapi.py`، إذا قمت بتشغيله مباشرة، ستحصل على واجهة openai على `http://127.0.0.1:8817/v1/`، يمكن لأي تطبيق قادر على استدعاء GPT استدعاء سير العمل الخاص بك في comfyui الآن! سأقوم بإصدار برنامج تعليمي لتوضيح كيفية القيام بذلك~
19. تم فصل محمل LLM وسلسلة LLM، مما أدى إلى فصل تحميل النموذج وإعداد النموذج، بحيث يمكن مشاركة النموذج بين عقد LLM المختلفة!
20. تم دعم macOS وأجهزة mps حاليًا! شكرًا لـ [bigcat88](https://github.com/bigcat88) على هذه المساهمة!
21. يمكنك الآن إنشاء لعبة رواية تفاعلية خاصة بك، حيث تتبع الرواية نهايات مختلفة بناءً على اختيارات المستخدم! يرجى الرجوع إلى مثال سير العمل: [رواية تفاعلية](workflow/互动小说.json)
22. تم توافق ميزة whisper وtts من openai، مما يتيح إدخال وإخراج الصوت. يرجى الرجوع إلى مثال سير العمل: [إدخال صوتي + إخراج صوتي](workflow/语音输入+语音输出.json)
23. متوافق مع [Omost](https://github.com/lllyasviel/Omost)!!! يرجى تحميل [omost-llama-3-8b-4bits](https://huggingface.co/lllyasviel/omost-llama-3-8b-4bits) لتجربته على الفور! نموذج سير العمل المرجعي: [start_with_OMOST](workflow/start_with_OMOST.json)
24. تمت إضافة أدوات LLM لإرسال الرسائل إلى WeChat Enterprise و DingTalk و Feishu بالإضافة إلى وظائف خارجية يمكن استدعاؤها.
25. تمت إضافة مُكرر نصي يمكنه إخراج جزء من الأحرف في كل مرة، حيث يتم تقسيم النص بأمان بناءً على أحرف العودة وحجم الكتلة، دون تقسيم النص من المنتصف. تشير الكتلة المتداخلة إلى عدد الأحرف التي تتداخل في النص المقسم. يمكنك إدخال نصوص طويلة بشكل جماعي، فقط اضغط بلا تفكير، أو قم بتمكين التنفيذ المتكرر في ComfyUI، وسيتم التنفيذ تلقائيًا. تذكر تمكين خاصية is_locked، حيث يمكنها قفل سير العمل تلقائيًا عند انتهاء الإدخال، ولن يستمر في التنفيذ. نموذج سير العمل: [نص تكراري إدخال](workflow/文本迭代输入.json)
26. تمت إضافة خاصية model name إلى محمل LLM المحلي ومحمل llava المحلي، وإذا كانت فارغة، فسيتم تحميلها من مسارات محلية مختلفة في العقدة. إذا لم تكن فارغة، فسيتم تحميلها باستخدام معلمات المسار التي قمت بإدخالها في `config.ini`. إذا لم تكن فارغة ولم تكن موجودة في `config.ini`، فسيتم تنزيلها من Hugging Face أو تحميلها من دليل حفظ النماذج في Hugging Face. إذا كنت ترغب في تنزيلها من Hugging Face، يرجى ملء خاصية model name بتنسيق مثل: `THUDM/glm-4-9b-chat`. ملاحظة! يجب أن تكون النماذج المحملة بهذه الطريقة متوافقة مع مكتبة Transformer.
27. تمت إضافة عقدة تحليل ملفات JSON وعقدة استخراج قيم JSON، مما يتيح لك الحصول على قيمة مفتاح معين من ملف أو نص. شكرًا لمساهمة [guobalove](https://github.com/guobalove)!
28. تم تحسين كود استدعاء الأدوات، والآن يمكن أن يتم تفعيل خاصية is_tools_in_sys_prompt حتى في نماذج اللغة الكبيرة (LLM) التي لا تحتوي على وظيفة استدعاء الأدوات (يتم تفعيلها بشكل افتراضي في LLM المحلية تلقائيًا). بعد التفعيل، ستضاف معلومات الأدوات إلى نص النظام، مما يتيح للـ LLM استدعاء الأدوات. يتعلق مبدأ التنفيذ بالورقة البحثية التالية: [Achieving Tool Calling Functionality in LLMs Using Only Prompt Engineering Without Fine-Tuning](https://arxiv.org/abs/2407.04997)
29. تم إنشاء مجلد custom_tool لتخزين كود الأدوات المخصصة، يمكنك الرجوع إلى كود المجلد [custom_tool](custom_tool) لوضع كود الأداة المخصصة في مجلد custom_tool، مما يتيح لك استدعاء الأداة المخصصة في LLM.
30. تمت إضافة أداة الرسم البياني المعرفي، مما يتيح لـ LLM التفاعل المثالي مع الرسم البياني المعرفي، حيث يمكن لـ LLM تعديل الرسم البياني المعرفي بناءً على مدخلاتك، ويمكنه الاستنتاج من الرسم البياني للحصول على الإجابات التي تحتاجها. يمكنك الاطلاع على سير العمل كمثال: [graphRAG_neo4j](workflow/graphRAG_neo4j.json)
31. تمت إضافة وظيفة AI الشخصية، مما يتيح لك تطوير صديقك الافتراضي (فتاة أو شاب) بدون الحاجة إلى كتابة أي كود، مع محادثات غير محدودة، وذاكرة دائمة، وثبات الشخصية. يمكنك الاطلاع على سير العمل كمثال: [麦洛薇人格AI](workflow/麦洛薇人格AI.json)
32. يمكنك استخدام هذه الأداة لإنشاء أدوات LLM تلقائيًا، حيث يتم حفظ كود الأداة التي قمت بإنشائها كملف بايثون، ثم انسخ الكود إلى مجلد custom_tool، وبالتالي تكون قد أنشأت عقدة جديدة. سير العمل كمثال: [LLM工具生成器](workflow/LLM工具制造机.json).
33. تمت إضافة دعم بحث duckduckgo، ولكن هناك قيود كبيرة، يبدو أنه يمكن إدخال كلمات رئيسية باللغة الإنجليزية فقط، كما لا يمكن أن تحتوي الكلمات الرئيسية على مفاهيم متعددة، وتكمن الميزة في عدم وجود قيود على مفتاح API.
34. تمت إضافة دعم لاستدعاء عدة قواعد معرفية بشكل منفصل، مما يتيح لك تحديد أي قاعدة معرفية تستخدمها للإجابة على الأسئلة داخل نص التوجيه. سير العمل كمثال: [多知识库分别调用](workflow/多知识库分别调用.json).
35. يدعم LLM إدخال معلمات إضافية، بما في ذلك json out وغيرها من المعلمات المتقدمة. سير العمل كمثال: [LLM输入额外参数](workflow/LLM额外参数eg_JSON_OUT.json). [用json_out分离提示词](workflow/用json_out分离提示词.json).
36. تم إضافة ميزة ربط الوكيل بـ Discord. (لا يزال في مرحلة الاختبار)
37. تم إضافة ميزة ربط الوكيل بـ Fei Shu، شكرًا جزيلًا لمساهمة [guobalove](https://github.com/guobalove)! راجع سير العمل [روبوت Fei Shu](workflow/飞书机器人.json).
38. تم إضافة عقدة استدعاء API العالمية وعدد كبير من العقد المساعدة، لبناء جسم الطلب واستخراج المعلومات من الاستجابة.
39. تم إضافة عقدة لمسح النموذج، مما يتيح لك إلغاء تحميل LLM من الذاكرة في أي مكان!
40. تم إضافة عقدة [chatTTS](https://github.com/2noise/ChatTTS)، شكرًا جزيلًا لمساهمة [guobalove](https://github.com/guobalove)! يمكن أن يكون معامل `model_path` فارغًا! يُوصى باستخدام وضع HF لتحميل النموذج، حيث سيتم تنزيل النموذج تلقائيًا من Hugging Face، دون الحاجة للتنزيل يدويًا؛ إذا كنت تستخدم التحميل المحلي، يرجى وضع مجلدات `asset` و`config` في الدليل الجذر. [عنوان Baidu Cloud](https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu)، رمز الاستخراج: qyhu؛ إذا كنت تستخدم وضع `custom` للتحميل، يرجى وضع مجلدات `asset` و`config` تحت `model_path`.
## الخطط المستقبلية:
1. المزيد من التكيفات للنماذج، بحيث تغطي على الأقل واجهات برمجة التطبيقات للنماذج الكبيرة الشائعة واستدعاء النماذج مفتوحة المصدر المحلية، بالإضافة إلى المزيد من التكيفات لنماذج LVM، حيث أنني حتى الآن قد قمت بتكييف وظيفة الرؤية لـ GPT4 فقط؛
2. المزيد من طرق بناء الوكالات الذكية، حيث أنني قد أكملت في هذا المجال العمل على استيراد LLM كأداة إلى LLM آخر، لتحقيق بناء تدفق عمل LLM شعاعي، واستيراد تدفق عمل واحد كنقطة إلى تدفق عمل آخر، وفي المستقبل قد أبتكر بعض الوظائف الأكثر روعة في هذا المجال.
3. المزيد من الوظائف الآلية، حيث سأقوم في المستقبل بإطلاق المزيد من النقاط التي تقوم تلقائيًا بإرسال الصور والنصوص والفيديوهات والصوتيات إلى تطبيقات أخرى، وسأقدم أيضًا نقاط مراقبة لتحقيق الرد التلقائي على برامج التواصل الاجتماعي والمنتديات الرئيسية.
4. المزيد من وظائف إدارة قواعد المعرفة، حيث يدعم هذا المشروع حاليًا البحث في الملفات المحلية والبحث عبر الإنترنت، وفي المستقبل سأطلق بحثًا في خرائط المعرفة وبحثًا في الذاكرة الطويلة. ليتمكن الوكلاء من التفكير المنطقي في المعرفة المتخصصة، وتذكر بعض المعلومات الرئيسية عند الحوار مع المستخدم.
5. المزيد من الأدوات، والمزيد من أقنعة الشخصيات، حيث أن هذه النقطة هي الأسهل في التنفيذ لكنها تحتاج إلى تراكم، وآمل في المستقبل أن أتمكن من جعل هذا المشروع يمتلك العديد من الأدوات وأقنعة الشخصيات مثل comfyui.

## إخلاء المسؤولية:
هذا المشروع المفتوح المصدر ومحتواه (المشار إليه فيما يلي بـ "المشروع") هو لأغراض مرجعية فقط، ولا يعني أي ضمانات صريحة أو ضمنية. لا يتحمل المساهمون في المشروع أي مسؤولية عن كمال المشروع أو دقته أو موثوقيته أو ملاءمته. أي تصرف يعتمد على محتوى المشروع يجب أن يتحمل المخاطر بنفسه. في أي حالة من الأحوال، لا يتحمل المساهمون في المشروع أي مسؤولية عن أي خسائر أو أضرار غير مباشرة أو خاصة أو تبعية ناتجة عن استخدام محتوى المشروع.
## شكر خاص
<a href="https://github.com/bigcat88">
  <img src="https://avatars.githubusercontent.com/u/13381981?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://github.com/guobalove">
  <img src="https://avatars.githubusercontent.com/u/171540731?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://github.com/HuangYuChuh">
  <img src="https://avatars.githubusercontent.com/u/167663109?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>

## قائمة الاقتراض
بعض العقد في هذا المشروع مستوحاة من المشاريع التالية، نشكرهم على مساهماتهم في مجتمع المصادر المفتوحة!
1. [pythongosssss/ComfyUI-Custom-Scripts](https://github.com/pythongosssss/ComfyUI-Custom-Scripts)
2. [lllyasviel/Omost](https://github.com/lllyasviel/Omost)
3. [2noise/ChatTTS](https://github.com/2noise/ChatTTS)

## الدعم:

### انضم إلى المجتمع
إذا كانت هناك مشكلات في الملحق أو كانت لديك أي استفسارات أخرى، فلا تتردد في الانضمام إلى مجتمعنا.

1. مجموعة QQ: `931057213`
<div style="display: flex; justify-content: center;">
    <img src="img/Q群.jpg" style="width: 48%;" />
</div>

2. مجموعة وي شات：`Choo-Yong`（أضف مساعدنا إلى وي شات ثم انضم إلى المجموعة）

3. ديسكورد: [رابط الديسكورد](https://discord.gg/gxrQAYy6)

### تابعونا
1. إذا كنت ترغب في متابعة أحدث ميزات هذا المشروع، ندعوك لمتابعة حسابنا على بلي بلي: [派对主持BB机](https://space.bilibili.com/26978344)
2. حساب OpenArt يقوم بتحديث أكثر سير العمل المفيدة للحفلات: [openart](https://openart.ai/workflows/profile/comfyui_llm_party?sort=latest&tab=creation)

### دعم التبرعات
إذا كانت أعمالي قد جلبت لك قيمة، يرجى التفكير في دعوتي لتناول فنجان من القهوة! دعمك لا ينعش المشروع فحسب، بل يدفئ قلب المبدع أيضًا.☕💖 كل فنجان له معنى!
<div style="display:flex; justify-content:space-between;">
    <img src="img/zhifubao.jpg" style="width: 48%;" />
    <img src="img/wechat.jpg" style="width: 48%;" />
</div>

## تاريخ النجوم

[![Star History Chart](https://api.star-history.com/svg?repos=heshengtao/comfyui_LLM_party&type=Date)](https://star-history.com/#heshengtao/comfyui_LLM_party&Date)
