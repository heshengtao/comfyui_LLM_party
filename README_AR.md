![صورة](img/封面.png)

<div align="center">
  <a href="https://space.bilibili.com/26978344">bilibili</a> ·
  <a href="https://www.youtube.com/@comfyui-LLM-party">youtube</a> ·
  <a href="https://github.com/heshengtao/Let-LLM-party">دليل النص</a> ·
  <a href="workflow_tutorial/">دليل سير العمل</a> ·
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
0. إذا لم تقم باستخدام comfyui من قبل، وواجهت بعض مشاكل الاعتماد عند تثبيت LLM party في comfyui، يرجى النقر على [هنا](https://drive.google.com/file/d/1NJSpwEL3FqroKVv5UsrVY3YbCG-9YWmt/view?usp=sharing) لتحميل حزمة comfyui **windows** المحمولة التي تحتوي على LLM party. ملاحظة! تحتوي هذه الحزمة المحمولة فقط على المكونين الإضافيين party و manager، وهي مناسبة فقط لنظام تشغيل ويندوز.(إذا كنت بحاجة لتثبيت LLM party على comfyui القائم، يمكن تخطي هذه الخطوة.)
1. اسحب سير العمل التالي إلى comfyui الخاص بك، ثم استخدم [comfyui-Manager](https://github.com/ltdrdata/ComfyUI-Manager) لتثبيت العقد المفقودة.
  - استخدم API لاستدعاء LLM: [start_with_LLM_api](workflow/start_with_LLM_api.json)
  - استخدام aisuite لاستدعاء LLM: [بدء_باستخدام_aisuite](workflow/start_with_aisuite.json)
  - إدارة LLM المحلي باستخدام ollama: [start_with_Ollama](workflow/ollama.json)
  - استخدم LLM المحلي بتنسيق موزع: [start_with_LLM_local](workflow/start_with_LLM_local.json)
  - استخدم LLM المحلي بتنسيق GGUF: [start_with_LLM_GGUF](workflow/start_with_GGUF.json)
  - استخدم VLM المحلي بتنسيق موزع: [start_with_VLM_local](https://github.com/heshengtao/comfyui_LLM_party/blob/main/workflow_tutorial/LLM_Party%20for%20Llama3.2%20-Vision%EF%BC%88%E5%B8%A6%E8%AE%B0%E5%BF%86%EF%BC%89.json) (تحت الاختبار، يدعم حاليًا فقط [Llama-3.2-Vision-Instruct](https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct))
  - استخدم VLM المحلي بتنسيق GGUF: [start_with_VLM_GGUF](workflow/start_with_llava.json)
2. إذا كنت تستخدم API، فاملأ `base_url` (يمكن أن يكون API وسيط، تأكد من أنه ينتهي بـ `/v1/`) و`api_key` في عقدة تحميل API LLM. مثال: `https://api.openai.com/v1/`
3. إذا كنت تستخدم ollama، فقم بتشغيل خيار `is_ollama` في عقدة تحميل API LLM، ولا حاجة لملء `base_url` و`api_key`.
4. إذا كنت تستخدم نموذجًا محليًا، فاملأ مسار النموذج الخاص بك في عقدة تحميل النموذج المحلي، على سبيل المثال: `E:\model\Llama-3.2-1B-Instruct`. يمكنك أيضًا ملء معرف مستودع النموذج في Huggingface في عقدة تحميل النموذج المحلي، على سبيل المثال: `lllyasviel/omost-llama-3-8b-4bits`.
5. نظرًا للعتبة العالية لاستخدام هذا المشروع، حتى إذا اخترت البدء السريع، آمل أن تتمكن من قراءة الصفحة الرئيسية للمشروع بصبر.

## التحديثات الأخيرة
1. تم تطوير أداة جديدة لمتصفح عبر [browser-use](https://github.com/gregpr07/browser-use) ، والتي تتيح لـ LLM تنفيذ المهام التي تنشرها في المتصفح بشكل تلقائي.
1. تم ترقية تحميل الملفات، تحميل المجلدات، تحميل محتوى الويب وجميع العقد ذات الصلة بالتضمينات اللفظية، حيث إن محتوى ملفك الآن يحتوي دائمًا على اسم الملف وفهرس الفقرات. يمكن فرز عقد تحميل المجلدات من خلال `related_characters` لاختيار الملفات التي ترغب في تحميلها.
1. تم إضافة أداة نموذج تحويل الصوت إلى نص محلي، وفي النظرية، فإن جميع نماذج ASR الموجودة على HF متوافقة مع هذه العقدة. على سبيل المثال: [openai/whisper-small](https://huggingface.co/openai/whisper-small)، [nyrahealth/CrisperWhisper](https://huggingface.co/nyrahealth/CrisperWhisper) وغيرها.
1. تم إضافة عقد ASR و TTS لـ [صوت السمك](https://docs.fish.audio/introduction)، يرجى الرجوع إلى وثائق واجهة برمجة التطبيقات الخاصة بـ صوت السمك للاستخدام.
1. تمت إضافة عقدة محمل aisuite، التي تتوافق مع جميع واجهات البرمجة المتاحة لـ aisuite، بما في ذلك: ["openai","anthropic","aws","azure","vertex","huggingface"]، نموذج سير العمل: [بدء_باستخدام_aisuite](workflow/start_with_aisuite.json).
1. تم إضافة فئة جديدة تُعرف بـ "نقاط الذاكرة"، والتي يمكن استخدامها لإدارة تاريخ محادثاتك مع نموذج اللغة الكبير (LLM). تدعم نقاط الذاكرة حاليًا ثلاثة أوضاع لإدارة تاريخ المحادثات، وهي الملفات المحلية بتنسيق JSON وRedis وSQL. بعد فصل تاريخ محادثات LLM عن النموذج، يمكنك استخدام نماذج تضمين الكلمات لتنظيم وضغط تاريخ محادثاتك، مما يوفر لك Tokens وسياقات لنموذج اللغة الكبير. نموذج سير العمل: [ذاكرة خارجية](workflow/外置记忆.json).
1. تم إضافة أداة لقراءة الملفات المحلية، مقارنةً بالأداة السابقة للتحكم في الملفات المحلية في comfyui LLM mafia، فإن هذه الأداة تستطيع فقط قراءة الملفات أو شجرة الملفات داخل مجلد معين، مما يوفر مستوى أعلى من الأمان.
1. قمت بنسخ [chatgpt-on-wechat](https://github.com/zhayujie/chatgpt-on-wechat)، وأنشأت مستودعًا جديدًا [party-on-wechat](https://github.com/heshengtao/party-on-wechat). طرق التثبيت والاستخدام متطابقة مع المشروع الأصلي، ولا يتطلب الأمر أي تكوين، فقط قم بتشغيل FastAPI لـ party. بشكل افتراضي، يتم استدعاء سير العمل wx_api ويدعم إخراج الصور. سيتم تحديثه تدريجيًا لضمان استخدام سلس لـ party على WeChat.
2. أضفت عقدة قناع In-Context-LoRA، والتي تُستخدم لإنشاء تعليمات [In-Context-LoRA](https://github.com/ali-vilab/In-Context-LoRA/tree/main) متسقة.
1. لقد أضفنا مكونًا أماميًا، وظائفه مرتبة من اليسار إلى اليمين كما يلي:
  - يحفظ مفتاح API و Base URL في ملف `config.ini`. عند استخدامك لخيار `fix node` على عقدة загрузчик API LLM، سيقوم بقراءة المفتاح API و Base URL التي قمت بتحديثها تلقائيًا من ملف `config.ini`.
  - يبدأ خدمة FastAPI يمكن استخدامها للاتصال بأعمالك في ComfyUI. إذا قمت بتشغيله مباشرةً، ستحصل على واجهة OpenAI على `http://127.0.0.1:8817/v1/`. عليك ربط بداية ونهاية عملية العمل بالعقد `بدء عملية العمل` و`نهاية عملية العمل`، ثم حفظها في تنسيق API في مجلد `workflow_api`. ثم، في أي واجدة أمامية يمكنها الاتصال بواجهة OpenAI، أدخل `model name=<اسم عملية العمل بدون ملحق .json>`, `Base URL=http://127.0.0.1:8817/v1/`، والمفتاح API يمكن أن يكون أي قيمة.
  - يبدأ تطبيق Streamlit؛ عملية حفظ عملية العمل مشابهة لما سبق. يمكنك اختيار عملية العمل المحفوظة في الإعدادات في تطبيق Streamlit والتواصل مع وكيل عملية العمل في الدردشة.
  - "معلومات عنا"، حيث يتم تقديم المشروع.
2. تمت إزالة عقدة قائمة أسماء النماذج التلقائية واستبدالها بعقدة محمل API LLM البسيطة، التي تقوم تلقائيًا باستخراج قائمة أسماء النماذج من التكوين في ملف config.ini الخاص بك. كل ما عليك فعله هو اختيار اسم لتحميل النموذج. بالإضافة إلى ذلك، تم تحديث عقد محمل LLM البسيطة، محمل LLM-GGUF البسيطة، محمل VLM البسيطة، محمل VLM-GGUF البسيطة وعقد محمل LLM lora البسيطة. جميعهم يقومون بقراءة مسارات النموذج تلقائيًا من مجلد النموذج داخل مجلد الحزب، مما يسهل على الجميع تحميل النماذج المحلية المختلفة.
1. يمكن لـ LLM الآن تحميل lora ديناميكيًا مثل SD و FLUX. يمكنك ربط عدة lora لتحميل المزيد من lora على نفس LLM. مثال على سير العمل: [start_with_LLM_LORA](workflow/LLM_lora.json).
2. تمت إضافة أداة [searxng](https://github.com/searxng/searxng) التي يمكنها تجميع عمليات البحث عبر الإنترنت بالكامل. يعتمد Perplexica أيضًا على أداة البحث المجمعة هذه، مما يعني أنه يمكنك إعداد Perplexica في حفلة. يمكنك نشر الصورة العامة searxng/searxng في Docker، ثم استخدام الأمر `docker run -d -p 8080:8080 searxng/searxng` لبدء تشغيله، ثم استخدام `http://localhost:8080` للوصول إليه. يمكنك إدخال عنوان URL `http://localhost:8080` في أداة searxng في party، ثم يمكن استخدام searxng كأداة لـ LLM.
1. **تحديث ضخم!!!** الآن يمكنك تغليف أي سير عمل ComfyUI في عقدة أداة LLM. يمكنك جعل LLM الخاص بك يتحكم في سير عمل ComfyUI متعدد في نفس الوقت. عندما تريد إكمال بعض المهام، يمكنه اختيار سير العمل المناسب لـ ComfyUI بناءً على طلبك، وإكمال مهمتك، وإرجاع النتيجة لك. مثال على سير العمل: [comfyui_workflows_tool](workflow/把任意workflow当作LLM_tool.json). الخطوات المحددة هي كما يلي:
   - أولاً، قم بتوصيل واجهة إدخال النص لسير العمل الذي تريد تغليفه كأداة بمخرج "user_prompt" لعقدة "بدء سير العمل". هذا هو المكان الذي يتم فيه تمرير الطلب عند استدعاء الأداة بواسطة LLM.
   - قم بتوصيل الأماكن التي تريد إخراج النص والصور فيها بالمواقع المدخلة المقابلة لعقدة "إنهاء سير العمل".
   - احفظ سير العمل هذا كـ API (تحتاج إلى تمكين وضع المطور في الإعدادات لرؤية هذا الزر).
   - احفظ سير العمل هذا في مجلد workflow_api لهذا المشروع.
   - أعد تشغيل ComfyUI وأنشئ سير عمل LLM بسيط، مثل: [start_with_LLM_api](workflow/start_with_LLM_api.json).
   - أضف عقدة "أداة سير العمل" إلى هذه العقدة LLM وقم بتوصيلها بمدخل الأداة لعقدة LLM.
   - في عقدة "أداة سير العمل"، اكتب اسم ملف سير العمل الذي تريد استدعاءه في مربع الإدخال الأول، على سبيل المثال: draw.json. يمكنك كتابة أسماء ملفات سير العمل المتعددة. في مربع الإدخال الثاني، اكتب وظيفة كل سير عمل حتى يفهم LLM كيفية استخدام هذه سير العمل.
   - قم بتشغيله لرؤية LLM يستدعي سير العمل المغلف الخاص بك ويعيد النتيجة لك. إذا كانت النتيجة صورة، قم بتوصيل عقدة "معاينة الصورة" بمخرج الصورة لعقدة LLM لعرض الصورة المولدة. ملاحظة! هذه الطريقة تستدعي ComfyUI جديد على منفذ 8190 الخاص بك، يرجى عدم شغل هذا المنفذ. سيتم فتح محطة جديدة على أنظمة Windows وMac، يرجى عدم إغلاقها. يستخدم نظام Linux عملية screen لتحقيق ذلك، عند عدم الحاجة إلى استخدامها، أغلق عملية screen هذه، وإلا ستظل المنفذ مشغولًا دائمًا.

![workflow_tool](img/workflowtool.png)

## تعليمات الاستخدام
1. يرجى الرجوع إلى تعليمات استخدام العقدة: [怎么使用节点](https://github.com/heshengtao/Let-LLM-party)

2. إذا كانت هناك مشاكل في المكون الإضافي أو إذا كان لديك أي استفسارات أخرى، فنحن نرحب بك للانضمام إلى مجموعة QQ: [931057213](img/Q群.jpg) | discord：[discord](https://discord.gg/f2dsAKKr2V).
3. يُرجى الرجوع إلى [دليل سير العمل](workflow_tutorial/) ، شكرًا لمساهمة [HuangYuChuh](https://github.com/HuangYuChuh)！

4. حساب لعب سير العمل المتقدم: [openart](https://openart.ai/workflows/profile/comfyui_llm_party?sort=latest&tab=creation)

4. يمكن الاطلاع على المزيد من سير العمل في مجلد [workflow](workflow)

## دروس الفيديو
<a href="https://space.bilibili.com/26978344">
  <img src="img/B.png" width="100" height="100" style="border-radius: 80%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://www.youtube.com/@comfyui-LLM-party">
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
* [جيميناي](https://developers.googleblog.com/zh-hans/gemini-is-now-accessible-from-the-openai-library/)(تم إهمال عقدة محمل API LLM الأصلية لجيميناي في الإصدار الجديد، يرجى استخدام عقدة محمل LLM API، واختر base_url ليكون: https://generativelanguage.googleapis.com/v1beta/)

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
1. يمكنك النقر بزر الماوس الأيمن في واجهة **comfyui** واختيار `llm` من قائمة السياق، للعثور على عقدة هذا المشروع. [كيفية استخدام العقد](https://github.com/heshengtao/Let-LLM-party)
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
2. تم تحديث سلسلة من عقد التحويل: markdown إلى HTML، svg إلى صورة، HTML إلى صورة، mermaid إلى صورة، markdown إلى Excel.
1. متوافق مع نموذج llama3.2 vision، يدعم الحوار متعدد الأدوار، والوظائف البصرية. عنوان النموذج: [meta-llama/Llama-3.2-11B-Vision-Instruct](https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct). مثال على سير العمل: [llama3.2_vision](https://github.com/heshengtao/comfyui_LLM_party/blob/main/workflow_tutorial/LLM_Party%20for%20Llama3.2%20-Vision%EF%BC%88%E5%B8%A6%E8%AE%B0%E5%BF%86%EF%BC%89.json).
1. تم تكييف GOT-OCR2، يدعم نتائج الإخراج المنسقة، يدعم التعرف الدقيق على النصوص باستخدام مربعات الموضع والألوان. عنوان النموذج: [GOT-OCR2](https://huggingface.co/stepfun-ai/GOT-OCR2_0). مثال على سير العمل يحول لقطة شاشة لصفحة ويب إلى كود HTML ثم يفتح المتصفح لعرض هذه الصفحة: [img2web](workflow/图片转网页.json).
2. تم تعديل عقد تحميل LLM المحلية بشكل كبير، لذلك لم تعد بحاجة إلى اختيار نوع النموذج بنفسك. تم إعادة إضافة عقدة تحميل llava وعقدة تحميل GGUF. تم تغيير نوع النموذج على عقدة سلسلة نماذج LLM المحلية إلى LLM وVLM-GGUF وLLM-GGUF، مما يتوافق مع تحميل نماذج LLM مباشرة، وتحميل نماذج VLM، وتحميل نماذج LLM بتنسيق GGUF. الآن يتم دعم نماذج VLM ونماذج LLM بتنسيق GGUF مرة أخرى. يمكن الآن أن تكون المكالمات المحلية متوافقة مع المزيد من النماذج! أمثلة على سير العمل: [LLM_local](workflow/start_with_LLM_local.json), [llava](workflow/start_with_llava.json), [GGUF](workflow/start_with_GGUF.json)
2. تمت إضافة عقدة EasyOCR للتعرف على النصوص والمواقع في الصور. يمكنه إنشاء الأقنعة المقابلة وإرجاع سلسلة JSON لعرضها بواسطة LLM. تتوفر إصدارات عادية ومميزة للاختيار من بينها!
2. في حفلة comfyui LLM، تم إعادة إنتاج نظام الفراولة لنموذج سلسلة chatgpt-o1، بالإشارة إلى مطالبات [Llamaberry](https://huggingface.co/spaces/martinbowling/Llamaberry/blob/main/app.py). مثال على سير العمل: [نظام الفراولة مقارنة بـ o1](workflow/草莓系统与o1对比.json).
2. تمت إضافة عقدة GPT-sovits جديدة، مما يتيح لك استدعاء نموذج GPT-sovits لتحويل النص إلى كلام بناءً على الصوت المرجعي الخاص بك. يمكنك أيضًا ملء مسار النموذج المحسن الخاص بك (إذا لم يتم ملؤه، سيتم استخدام النموذج الأساسي للاستدلال) للحصول على أي صوت تريده. لاستخدامه، تحتاج إلى تنزيل مشروع [GPT-sovits](https://github.com/RVC-Boss/GPT-SoVITS) والنموذج الأساسي المقابل محليًا، ثم بدء خدمة API باستخدام `runtime\python.exe api_v2.py` في مجلد مشروع GPT-sovits. بالإضافة إلى ذلك، تم نقل عقدة chatTTS إلى [comfyui LLM mafia](https://github.com/heshengtao/comfyui_LLM_mafia). السبب هو أن chatTTS يحتوي على العديد من التبعيات، ورخصته على PyPi هي CC BY-NC 4.0، وهي رخصة غير تجارية. على الرغم من أن مشروع chatTTS على GitHub تحت رخصة AGPL، فقد نقلنا عقدة chatTTS إلى comfyui LLM mafia لتجنب المشاكل غير الضرورية. نأمل أن يفهم الجميع!
3. يدعم الآن أحدث نموذج من OpenAI، سلسلة o1!
4. تمت إضافة أداة للتحكم في الملفات المحلية تتيح لـ LLM التحكم في الملفات في المجلد المحدد، مثل القراءة والكتابة والإضافة والحذف وإعادة التسمية والنقل والنسخ.نظرًا للخطر المحتمل لهذه العقدة، تم تضمينها في [comfyui LLM mafia](https://github.com/heshengtao/comfyui_LLM_mafia).
5. أدوات SQL الجديدة تتيح لـ LLM استعلام قواعد بيانات SQL.
6. تم تحديث النسخة متعددة اللغات من README. سير العمل لترجمة وثيقة README: [translate_readme](workflow/文档自动翻译机.json)
7. تم تحديث أربعة عقد متكررة (عقدة النص، عقدة الصورة، عقدة الجدول، عقدة json)، أنماط المتكررات هي: تسلسلي، عشوائي ولا نهائي. التسلسلي سيخرج بالتتابع حتى يتجاوز الحد الأقصى للفهرس ويتوقف تلقائيًا، مما يعيد تعيين قيمة الفهرس إلى 0، والعشوائي سيختار فهرسًا عشوائيًا للإخراج، واللانهائي سيخرج باستمرار.
8. تمت إضافة عقدة محمل Gemini API، وهي الآن متوافقة مع API الرسمي لـ Gemini! إذا كنت في بيئة شبكة محلية، وإذا ظهرت مشكلة تقييد المنطقة مع API، يرجى تحويل العقدة إلى الولايات المتحدة واستخدام وضع TUN. نظرًا لأن Gemini في استدعاء الأدوات، إذا كان هناك أحرف صينية في المعلمات المعادة، فستظهر رسالة خطأ برمز 500، لذا فإن بعض عقد الأدوات غير متاحة. تدفق العمل النموذجي: [start_with_gemini](workflow/start_with_gemini.json)
9. تمت إضافة عقدة lore book، يمكنك من خلالها إدخال إعدادات الخلفية الخاصة بك أثناء الدردشة مع LLM، تدفق العمل النموذجي: [lorebook](workflow/lorebook.json)
10. تمت إضافة عقدة مولد الكلمات المفتاحية FLUX، يمكنها إنشاء كلمات مفتاحية بأنماط متعددة مثل بطاقات Hearthstone، بطاقات Yu-Gi-Oh، الملصقات، والقصص المصورة، مما يسمح لنموذج FLUX بالإنتاج المباشر. تدفق العمل المرجعي: [FLUX提示词](https://openart.ai/workflows/comfyui_llm_party/flux-by-llm-party/sjME541i68Kfw6Ib0EAD)

## الخطوات التالية:
1. المزيد من تكييف النماذج;
2. المزيد من طرق بناء الوكلاء;
3. المزيد من ميزات الأتمتة;
4. المزيد من ميزات إدارة قاعدة المعرفة;
5. المزيد من الأدوات، المزيد من الشخصيات.

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

2. مجموعة وي شات：`Choo-Yong`（أضف مساعدنا إلى وي شات ثم انضم إلى المجموعة）

3. ديسكورد: [رابط الديسكورد](https://discord.gg/f2dsAKKr2V)

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
