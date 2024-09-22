![이미지](img/封面.png)

<div align="center">
  <a href="https://space.bilibili.com/26978344">비디오 튜토리얼</a> ·
  <a href="how_to_use_nodes_ZH.md">텍스트 튜토리얼</a> ·
  <a href="workflow_tutorial/">작업 흐름 튜토리얼</a> ·
  <a href="https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu">바이두 링크</a> ·
  <a href="img/Q群.jpg">QQ 그룹</a> ·
  <a href="https://discord.gg/gxrQAYy6">디스코드</a> ·
  <a href="https://dcnsxxvm4zeq.feishu.cn/wiki/IyUowXNj9iH0vzk68cpcLnZXnYf">우리에 관하여</a>
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

Comfyui_llm_party는 [comfyui](https://github.com/comfyanonymous/ComfyUI)라는 매우 간단한 UI 인터페이스를 기반으로 LLM 작업 흐름 구축을 위한 완전한 노드 라이브러리를 개발하고자 합니다. 이를 통해 사용자는 자신의 LLM 작업 흐름을 더 편리하고 신속하게 구축할 수 있으며, 자신의 이미지 작업 흐름에 더 쉽게 통합할 수 있습니다.

## 효과 시연
https://github.com/user-attachments/assets/945493c0-92b3-4244-ba8f-0c4b2ad4eba6

## 프로젝트 개요
ComfyUI LLM Party는 가장 기본적인 LLM 다중 도구 호출, 역할 설정을 통해 나만의 AI 도우미를 신속하게 구축하고, 산업에 적용 가능한 단어 벡터 RAG, GraphRAG를 통해 산업 내 지식 관리 시스템을 로컬화합니다. 단일 지능체 파이프라인에서 복잡한 지능체 간의 방사형 상호작용 모드, 순환 상호작용 모드를 구성하는 것까지; 개인 사용자가 자신의 사회적 APP(QQ, Feishu, Discord)에 접속할 필요가 있는 것부터, 스트리밍 작업자가 필요로 하는 원스톱 LLM+TTS+ComfyUI 워크플로우까지; 일반 학생들이 필요로 하는 첫 번째 LLM 응용 프로그램의 간단한 시작부터, 연구자들이 자주 사용하는 다양한 파라미터 조정 인터페이스, 모델 적응까지. 이 모든 것을 ComfyUI LLM Party에서 확인할 수 있습니다.

## 최신 업데이트
1. 
2. 새로운 GPT-sovits 노드가 추가되어 GPT-sovits 모델을 호출하여 참조 오디오를 기반으로 텍스트를 음성으로 변환할 수 있습니다. 또한 미세 조정된 모델 경로를 입력할 수도 있습니다(입력하지 않으면 기본 모델이 추론에 사용됨) 원하는 음성을 얻을 수 있습니다. 사용하려면 [GPT-sovits](https://github.com/RVC-Boss/GPT-SoVITS) 프로젝트와 해당 기본 모델을 로컬에 다운로드한 다음 GPT-sovits 프로젝트 폴더에서 `runtime\python.exe api_v2.py`를 사용하여 API 서비스를 시작해야 합니다. 또한 chatTTS 노드는 [comfyui LLM mafia](https://github.com/heshengtao/comfyui_LLM_mafia)로 이동되었습니다. 이유는 chatTTS에 많은 종속성이 있으며 PyPi의 라이선스가 CC BY-NC 4.0으로 비상업적 라이선스이기 때문입니다. chatTTS의 GitHub 프로젝트가 AGPL 라이선스 하에 있음에도 불구하고 불필요한 문제를 피하기 위해 chatTTS 노드를 comfyui LLM mafia로 이동했습니다. 모두의 이해를 바랍니다!
3. 이제 OpenAI의 최신 모델인 o1 시리즈를 지원합니다!
4. 지정한 폴더의 파일을 제어할 수 있는 로컬 파일 제어 도구가 추가되었습니다. 읽기, 쓰기, 추가, 삭제, 이름 변경, 이동, 복사 등이 가능합니다.이 노드의 잠재적인 위험성 때문에 [comfyui LLM mafia](https://github.com/heshengtao/comfyui_LLM_mafia)에 포함되어 있습니다.
5. 새로운 SQL 도구로 LLM이 SQL 데이터베이스를 쿼리할 수 있습니다.
6. README의 다국어 버전을 업데이트했습니다. README 문서를 번역하는 워크플로우: [translate_readme](workflow/文档自动翻译机.json)
7. 4개의 반복기 노드(텍스트 반복기, 이미지 반복기, 표 반복기, json 반복기)가 업데이트되었습니다. 반복기 모드는 순차, 무작위 및 무한의 세 가지 모드가 있습니다. 순차 모드는 순서대로 출력을 하며, 인덱스 한계를 초과하면 자동으로 프로세스가 중단되고 인덱스 값이 0으로 재설정됩니다. 무작위 모드는 무작위 인덱스를 선택하여 출력을 하며, 무한 모드는 무한 반복 출력을 진행합니다.
8. Gemini API 로더 노드가 추가되어 이제 Gemini 공식 API와 호환됩니다! 국내 네트워크 환경에서 API 지역 제한 문제가 발생하면 노드를 미국으로 전환하고 TUN 모드를 사용해 주십시오. Gemini에서 도구 호출 시 반환된 파라미터에 중국어 문자가 포함되면 반환 코드 500 오류가 발생할 수 있어 일부 도구 노드가 사용 불가능합니다. 예시 워크플로우: [start_with_gemini](workflow/start_with_gemini.json)
9. LLM과 대화할 때 배경 설정을 삽입할 수 있는 lore book 노드가 추가되었습니다. 예시 워크플로우: [lorebook](workflow/lorebook.json)
10. FLUX 프롬프트 생성기 마스크 노드가 추가되어 하스스톤 카드, 유희왕 카드, 포스터, 만화 등 다양한 스타일의 프롬프트를 생성할 수 있으며, FLUX 모델이 직접 출력할 수 있게 해줍니다. 참고 워크플로우: [FLUX 프롬프트](https://openart.ai/workflows/comfyui_llm_party/flux-by-llm-party/sjME541i68Kfw6Ib0EAD)

## 사용 설명
1. 노드 사용 설명서는 다음을 참고하십시오: [노드 사용 방법](how_to_use_nodes.md)

2. 플러그인에 문제가 있거나 다른 질문이 있으시면 QQ 그룹에 참여해 주십시오: [931057213](img/Q群.jpg)
3. 워크플로우 튜토리얼은 다음을 참조하시기 바랍니다: [워크플로우 튜토리얼](workflow_tutorial/), [HuangYuChuh](https://github.com/HuangYuChuh)님의 기여에 감사드립니다!

4. 고급 워크플로우 플레이 계정: [openart](https://openart.ai/workflows/profile/comfyui_llm_party?sort=latest&tab=creation)

4. 더 많은 워크플로우는 [workflow](workflow) 폴더를 참조하시기 바랍니다.

## 비디오 튜토리얼
1. [손쉽게 블록형 지능형 에이전트를 구축하는 방법](https://www.bilibili.com/video/BV1JZ421v7Tw/?vd_source=f229e378448918b84afab7c430c6a75b)

2. [GPT-4o를 comfyui에 연결하는 방법 | 워크플로우가 다른 워크플로우를 호출하게 하기 | LLM을 하나의 도구로 만드는 방법](https://www.bilibili.com/video/BV1JJ4m1A789/?spm_id_from=333.999.0.0&vd_source=f229e378448918b84afab7c430c6a75b)

3. [당신의 워크플로우를 GPT로 위장하여 WeChat에 접속하는 방법 | Omost 호환! 자신만의 dalle3을 유연하게 창조하기](https://www.bilibili.com/video/BV1DT421a7KY/?spm_id_from=333.999.0.0)

4. [comfyui에서 인터랙티브 소설 게임을 즐기는 방법](https://www.bilibili.com/video/BV15y411q78L/?spm_id_from=333.999.0.0&vd_source=f229e378448918b84afab7c430c6a75b)

5. [AI 여자친구, 그리고 당신의 형태 | comfyui에서 graphRAG 구현, neoa4j 연동 | comfyui 워크플로우를 streamlit 프론트엔드에 접속하기](https://www.bilibili.com/video/BV1dS421R7Au/?spm_id_from=333.999.0.0&vd_source=f229e378448918b84afab7c430c6a75b)
## 모델 지원
1. 이미지에서 텍스트와 위치를 인식하기 위한 EasyOCR 노드를 추가했습니다. 해당 마스크를 생성하고 LLM이 볼 수 있도록 JSON 문자열을 반환할 수 있습니다. 표준 버전과 프리미엄 버전이 모두 제공됩니다!
2. 모든 OpenAI 형식의 API 호출을 지원합니다( [oneapi](https://github.com/songquanpeng/one-api)와 결합하면 거의 모든 LLM API를 호출할 수 있으며, 모든 중계 API도 지원합니다). base_url 선택은 [config.ini.example](config.ini.example)을 참조하시기 바랍니다. 현재 테스트된 항목은 다음과 같습니다:
* [openai](https://platform.openai.com/docs/api-reference/chat/create) (모든 OpenAI 모델과 완벽하게 호환되며, 4o 및 o1 시리즈를 포함합니다!)
* [ollama](https://github.com/ollama/ollama) (추천! 로컬에서 호출하는 경우, 로컬 모델을 호스팅하기 위해 ollama 방법을 사용하는 것이 강력히 권장됩니다!)
* [llama.cpp](https://github.com/ggerganov/llama.cpp?tab=readme-ov-file#web-server) (추천! 로컬 gguf 형식 모델을 사용하려면 llama.cpp 프로젝트의 API를 사용하여 이 프로젝트에 액세스할 수 있습니다!)
* [통의천문/qwen](https://help.aliyun.com/zh/dashscope/developer-reference/compatibility-of-openai-with-dashscope/?spm=a2c4g.11186623.0.0.7b576019xkArPq)
* [지푸청언/glm](https://open.bigmodel.cn/dev/api#http_auth)
* [deepseek](https://platform.deepseek.com/api-docs/zh-cn/)
* [kimi/moonshot](https://platform.moonshot.cn/docs/api/chat#%E5%9F%BA%E6%9C%AC%E4%BF%A1%E6%81%AF)
* [두부](https://www.volcengine.com/docs/82379/1263482)

2. Gemini 형식의 API 호출을 지원합니다:
* [Gemini](https://aistudio.google.com/app/prompts/new_chat)
3. transformer 라이브러리의 AutoModelForCausalLM 클래스가 지원하는 대부분의 로컬 모델과 호환됩니다(로컬 모델 노드에서 model type을 무엇으로 선택해야 할지 모를 경우 llama를 선택하면 대체로 적합합니다). 현재 테스트된 모델은 다음과 같습니다:
* [ClosedCharacter/Peach-9B-8k-Roleplay](https://huggingface.co/ClosedCharacter/Peach-9B-8k-Roleplay) (추천! 역할극 모델)
* [omost-llama-3-8b-4bits](https://huggingface.co/lllyasviel/omost-llama-3-8b-4bits) (추천! 풍부한 프롬프트 모델)
* [meta-llama/Llama-2-7b-chat-hf](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)
* [Qwen/Qwen2-7B-Instruct](https://huggingface.co/Qwen/Qwen2-7B-Instruct)
* [xtuner/llava-llama-3-8b-v1_1-gguf](https://huggingface.co/xtuner/llava-llama-3-8b-v1_1-gguf) (개발자는 모든 gguf 형식의 대형 모델 호출을 유지할 수 없으므로 gguf 형식의 로컬 모델을 호출하기 위해 llama.cpp 방법을 사용하는 것이 좋습니다!)
* [THUDM/chatglm3-6b](https://huggingface.co/THUDM/chatglm3-6b) (GLM4의 새로운 호출 형식으로 인해 개발자는 모든 로컬 대형 모델 호출을 유지할 수 없으므로 로컬 호출을 위해 ollama 방법을 사용하는 것이 좋습니다!)

4. 모델 다운로드:
* [百度云地址](https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu)，提取码：qyhu

## 다운로드
다음 방법 중 하나를 사용하여 설치하세요.
### 방법 1:
1. [comfyui 관리자](https://github.com/ltdrdata/ComfyUI-Manager)에서 `comfyui_LLM_party`를 검색하여 한 번의 클릭으로 설치합니다.
2. comfyui를 재시작합니다.
### 방법 이:
1. ComfyUI 루트 폴더 아래의 `custom_nodes` 하위 폴더로 이동합니다.
2. 이 저장소를 클론합니다. `git clone https://github.com/heshengtao/comfyui_LLM_party.git`

### 방법 삼:
1. 오른쪽 상단의 `CODE`를 클릭합니다.
2. `download zip`을 클릭합니다.
3. 다운로드한 압축 파일을 ComfyUI 루트 폴더 아래의 `custom_nodes` 하위 폴더에 압축 해제합니다.

## 환경 배포
1. `comfyui_LLM_party` 프로젝트 폴더로 이동합니다.
2. 터미널에 `pip install -r requirements.txt`를 입력하여 본 프로젝트에 필요한 서드파티 라이브러리를 comfyui 환경에 배포합니다. 설치 시 comfyui 환경에 있는지 확인하고, 터미널의 `pip` 오류를 주의 깊게 살펴보시기 바랍니다.
3. comfyui 실행기를 사용하는 경우, 터미널에 `실행기 구성의 경로\python_embeded\python.exe -m pip install -r requirements.txt`를 입력하여 설치합니다. `python_embeded` 폴더는 일반적으로 `ComfyUI` 폴더와 같은 수준에 있습니다.
4. 환경 구성 문제 발생 시, `requirements_fixed.txt`에 있는 의존성을 사용해 볼 수 있습니다.
## 구성
* 언어는 `config.ini`에서 설정할 수 있으며, 현재 중국어(zh_CN)와 영어(en_US) 두 가지가 지원되며, 기본값은 시스템 언어입니다.
* 다음 방법 중 하나로 APIKEY를 설정할 수 있습니다.
### 방법 1:
1. `comfyui_LLM_party` 프로젝트 폴더 내의 `config.ini` 파일을 엽니다.
2. `config.ini`에 `openai_api_key`와 `base_url`을 입력합니다.
3. ollama 모델을 사용하는 경우, `base_url`에 `http://127.0.0.1:11434/v1/`를 입력하고, `openai_api_key`에 `ollama`를 입력하며, `model_name`에 모델 이름(예: llama3)을 입력합니다.
4. 구글 검색 또는 빙 검색 도구를 사용하려면 `config.ini`에 `google_api_key`, `cse_id` 또는 `bing_api_key`를 입력합니다.
5. 이미지 입력 LLM을 사용하려면, 이미지 호스팅 서비스인 imgbb를 추천하며, `config.ini`에 `imgbb_api`를 입력합니다.
6. 각 모델은 `config.ini` 파일에서 개별적으로 설정할 수 있으며, `config.ini.example` 파일을 참조하여 작성할 수 있습니다. 설정이 완료되면, 노드에서 `model_name`을 입력하기만 하면 됩니다.

### 방법 2:
1. comfyui 인터페이스를 엽니다.
2. 대형 언어 모델(LLM) 노드를 새로 생성하고, 노드 내에 `openai_api_key`와 `base_url`을 직접 입력합니다.
3. ollama 모델을 사용하는 경우, LLM_api 노드를 사용하고, 노드의 `base_url`에 `http://127.0.0.1:11434/v1/`를 입력하며, `api_key`에 `ollama`를 입력하고, `model_name`에 모델 이름(예: llama3)을 입력합니다.
4. 이미지 입력 LLM을 사용하려면, 이미지 호스팅 서비스인 imgbb를 추천하며, 노드에 `imgbb_api_key`를 입력합니다.
## 업데이트 로그
1. comfyui 인터페이스에서 마우스 오른쪽 버튼을 클릭한 후, 오른쪽 클릭 메뉴의 `llm`을 선택하면 본 프로젝트의 노드를 찾을 수 있습니다. [노드 사용 방법](how_to_use_nodes_ZH.md)
2. API 접속 또는 로컬 대모델 접속을 지원합니다. 모듈화된 방식으로 도구 호출 기능을 구현하였습니다. base_url을 입력할 때는 `/v1/`로 끝나는 URL을 입력해야 합니다. [ollama](https://github.com/ollama/ollama)를 사용하여 모델을 관리한 후, base_url에 `http://127.0.0.1:11434/v1/`를 입력하고, api_key에 ollama를, model_name에 모델 이름을 입력하십시오. 예: llama3.
   - API 접속 예시 워크플로우: [start_with_LLM_api](workflow/start_with_LLM_api.json)
   - 로컬 모델 접속 예시 워크플로우: [start_with_LLM_local](workflow/start_with_LLM_local.json)
   - ollama 접속 예시 워크플로우: [ollama](workflow/ollama.json)
3. 로컬 지식베이스 접속을 지원하며, RAG를 지원합니다. 예시 워크플로우: [지식베이스 RAG 검색.json](workflow/知识库RAG搜索.json)
4. 코드 해석기를 호출할 수 있습니다.
5. 인터넷 검색이 가능하며, 구글 검색을 지원합니다. 예시 워크플로우: [영화 조회 워크플로우](workflow/电影查询工作流.json)
6. comfyui에서 조건문을 구현할 수 있으며, 사용자 질문을 분류한 후에 맞춤형으로 응답할 수 있습니다. 예시 워크플로우: [스마트 고객 서비스](workflow/智能客服.json)
7. 대모델의 회전 링크를 지원하며, 두 개의 대모델이 토론 대회를 개최할 수 있습니다. 예시 워크플로우: [전기차 난제 토론 대회](workflow/电车难题辩论赛.json)
8. 임의의 인격 마스크를 연결할 수 있으며, 프롬프트 템플릿을 사용자 정의할 수 있습니다.
9. 다양한 도구 호출을 지원하며, 현재 날씨 조회, 시간 조회, 지식베이스, 코드 실행, 인터넷 검색, 단일 웹페이지 검색 등의 기능이 개발되었습니다.
10. LLM을 도구 노드로 사용할 수 있습니다. 예시 워크플로우: [LLM 중첩](workflow/LLM套娃.json)
11. API + streamlit를 통해 빠르게 웹 애플리케이션을 개발할 수 있습니다.
12. 위험한 만능 해석기 노드를 추가하여 대모델이 다양한 작업을 수행할 수 있게 하였습니다.
13. LLM 노드의 출력으로 사용하기 위해 오른쪽 클릭 메뉴의 함수(function) 하위 디렉토리에 있는 텍스트 표시(show_text) 노드를 사용하는 것을 추천합니다.
14. GPT-4O의 시각적 기능을 지원합니다! 예시 워크플로우: [GPT-4o](workflow/GPT-4o.json)  
15. 다른 워크플로우를 호출할 수 있는 워크플로우 중계기가 추가되었습니다! 예시 워크플로우: [다른 워크플로우 호출](workflow/调用另一个工作流.json)  
16. 통의천문/qwen, 지표청언/GLM, deepseek, kimi/moonshot와 같은 유사한 openai 인터페이스를 가진 모든 모델에 적합합니다. 이 모델의 base_url, api_key, model_name을 LLM 노드에 입력하여 호출하시기 바랍니다.  
17. LVM 로더가 추가되어 이제 로컬에서 LVM 모델을 호출할 수 있으며, [llava-llama-3-8b-v1_1-gguf](https://huggingface.co/xtuner/llava-llama-3-8b-v1_1-gguf) 모델을 지원합니다. 다른 LVM 모델이 GGUF 형식인 경우 이론적으로도 실행 가능해야 합니다. 예시 워크플로우는 여기에 있습니다: [start_with_LVM.json](workflow/start_with_LVM.json).  
18. `fastapi.py` 파일을 작성하였습니다. 이를 직접 실행하면 `http://127.0.0.1:8817/v1/`에서 openai 인터페이스를 얻을 수 있으며, GPT를 호출할 수 있는 모든 애플리케이션이 귀하의 comfyui 워크플로우를 호출할 수 있습니다! 자세한 조작 방법은 별도의 튜토리얼을 통해 시연할 예정입니다~  
19. LLM 로더와 LLM 체인을 분리하였으며, 모델 로드와 모델 설정을 분리하여 서로 다른 LLM 노드 간에 모델을 공유할 수 있게 되었습니다!  
20. 현재 macOS 및 mps 장치를 지원합니다! 이에 대한 기여에 감사드립니다, [bigcat88](https://github.com/bigcat88)!  
21. 사용자 선택에 따라 다양한 결말로 진행되는 인터랙티브 소설 게임을 구축할 수 있습니다! 예시 워크플로우 참고: [인터랙티브 소설](workflow/互动小说.json)  
22. openai의 whisper 및 tts 기능에 적합하여 음성 입력 및 출력을 구현할 수 있습니다. 예시 워크플로우 참고: [음성 입력+음성 출력](workflow/语音输入+语音输出.json)  
23. [Omost](https://github.com/lllyasviel/Omost)와 호환됩니다!!! [omost-llama-3-8b-4bits](https://huggingface.co/lllyasviel/omost-llama-3-8b-4bits)를 다운로드하여 즉시 체험해 보세요! 예시 워크플로우 참조: [start_with_OMOST](workflow/start_with_OMOST.json)  
24. 기업 WeChat, DingTalk 및 Feishu로 메시지를 전송하는 LLM 도구와 호출 가능한 외부 함수가 추가되었습니다.  
25. 텍스트 반복기를 새롭게 추가하였습니다. 이 반복기는 매번 일부 문자만 출력하며, 줄 바꿈 기호와 청크 크기를 기준으로 안전하게 텍스트를 분할합니다. 텍스트 중간에서 분할되지 않습니다. chunk_overlap은 분할된 텍스트가 얼마나 많은 문자를 겹치는지를 나타냅니다. 이를 통해 긴 텍스트를 일괄 입력할 수 있으며, 단순히 클릭하거나 comfyui의 루프 실행을 활성화하기만 하면 자동으로 실행됩니다. is_locked 속성을 활성화하는 것을 잊지 마세요. 입력이 끝날 때 워크플로우가 자동으로 잠기게 되어 계속 실행되지 않습니다. 예시 워크플로우: [텍스트 반복 입력](workflow/文本迭代输入.json)  
26. 로컬 LLM 로더 및 로컬 llava 로더에 model name 속성을 추가하였습니다. 비어 있을 경우, 노드 내의 다양한 로컬 경로를 사용하여 로드합니다. 비어 있지 않을 경우, `config.ini`에서 입력한 경로 매개변수를 사용하여 로드합니다. 비어 있지 않지만 `config.ini`에 없다면, huggingface에서 다운로드하거나 huggingface의 모델 저장 디렉토리에서 로드합니다. huggingface에서 다운로드하려면, 예를 들어 `THUDM/glm-4-9b-chat` 형식으로 model name 속성을 입력하세요. 주의! 이렇게 로드된 모델은 transformer 라이브러리와 호환되어야 합니다.  
27. JSON 파일 파싱 노드와 JSON 값 추출 노드를 새롭게 추가하여, 파일이나 텍스트에서 특정 키의 값을 가져올 수 있게 하였습니다. [guobalove](https://github.com/guobalove)의 기여에 감사드립니다!
28. 도구 호출 코드를 개선하여 이제 도구 호출 기능이 없는 LLM도 is_tools_in_sys_prompt 속성을 활성화할 수 있습니다(로컬 LLM은 기본적으로 활성화할 필요가 없으며 자동으로 조정됩니다). 활성화 후, 도구 정보가 시스템 프롬프트에 추가되어 LLM이 도구를 호출할 수 있게 됩니다. 구현 원리에 대한 관련 논문: [Achieving Tool Calling Functionality in LLMs Using Only Prompt Engineering Without Fine-Tuning](https://arxiv.org/abs/2407.04997)
29. 사용자 정의 도구 코드를 저장할 수 있는 custom_tool 폴더를 새로 만들었습니다. [custom_tool](custom_tool) 폴더의 코드를 참고하여 사용자 정의 도구 코드를 custom_tool 폴더에 넣으면 LLM에서 사용자 정의 도구를 호출할 수 있습니다.
30. 지식 그래프 도구를 추가하여 LLM과 지식 그래프가 완벽하게 상호작용할 수 있게 하였습니다. LLM은 사용자의 입력에 따라 지식 그래프를 수정할 수 있으며, 지식 그래프를 통해 필요한 답변을 추론할 수 있습니다. 예제 워크플로우는 다음을 참조하십시오: [graphRAG_neo4j](workflow/graphRAG_neo4j.json)
31. 인격 AI 기능을 추가하여 0 코드로 자신의 여자친구 AI 또는 남자친구 AI를 개발할 수 있으며, 무한 대화와 영구 기억, 안정된 캐릭터 설정을 제공합니다. 예제 워크플로우는 다음을 참조하십시오: [麦洛薇人格AI](workflow/麦洛薇人格AI.json)
32. 이 LLM 도구 생성기를 사용하여 LLM 도구를 자동으로 생성하고, 생성된 도구 코드를 Python 파일로 저장한 후, 코드를 custom_tool 폴더에 복사하면 새로운 노드를 생성할 수 있습니다. 예제 워크플로우: [LLM工具生成器](workflow/LLM工具制造机.json)。
33. duckduckgo 검색을 지원하지만 큰 제한이 있으며, 영어 키워드만 입력할 수 있는 것 같습니다. 키워드에 여러 개념이 포함될 수 없으며, 장점은 API 키의 제한이 없다는 점입니다.
34. 여러 지식베이스를 개별적으로 호출할 수 있는 기능을 지원하며, 프롬프트 내에서 어떤 지식베이스의 지식을 사용하여 질문에 답변할 것인지 명확히 할 수 있습니다. 예제 워크플로우: [多知识库分别调用](workflow/多知识库分别调用.json)。
35. LLM에 추가 매개변수를 입력할 수 있는 기능을 지원하며, json out 등 고급 매개변수를 포함합니다. 예제 워크플로우: [LLM输入额外参数](workflow/LLM额外参数eg_JSON_OUT.json)。[用json_out分离提示词](workflow/用json_out分离提示词.json)。
36. Discord에 에이전트를 연결하는 기능이 추가되었습니다. (아직 테스트 중입니다.)
37. Feishu에 에이전트를 연결하는 기능이 추가되었습니다. [guobalove](https://github.com/guobalove)의 기여에 진심으로 감사드립니다! 작업 흐름 참조: [飞书机器人](workflow/飞书机器人.json).
38. 요청 본체를 구성하고 응답에서 정보를 가져오기 위한 만능 API 호출 노드 및 다수의 보조 노드가 추가되었습니다.
39. 모델을 비워주는 노드가 추가되어, 원하는 위치에서 LLM을 메모리에서 언로드할 수 있습니다!
40. [chatTTS](https://github.com/2noise/ChatTTS) 노드가 추가되었습니다. [guobalove](https://github.com/guobalove)의 기여에 진심으로 감사드립니다! `model_path` 매개변수는 비워둘 수 있습니다! HF 모드로 모델을 로드하는 것을 추천하며, 모델은 자동으로 hugging face에서 다운로드되므로 수동 다운로드가 필요하지 않습니다; 로컬 로드를 사용할 경우, 모델의 `asset` 및 `config` 폴더를 루트 디렉토리에 놓아야 합니다. [百度云地址](https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu), 추출 코드: qyhu; `custom` 모드로 로드를 사용할 경우, 모델의 `asset` 및 `config` 폴더를 `model_path` 아래에 놓아야 합니다.
## 다음 단계 계획:
1. 더 많은 모델 적응, 최소한 주류 대형 모델 API 인터페이스와 주류 오픈 소스 모델의 로컬 호출을 포함하며, 더 많은 LVM 모델의 적응도 진행할 예정입니다. 현재 저는 GPT-4의 시각 기능 호출만 적응한 상태입니다;
2. 더 많은 지능체 구축 방식, 현재 이 분야에서 제가 완료한 작업은 LLM을 도구로 사용하여 다른 LLM에 도입하고, 방사형으로 LLM 워크플로우를 구축하며, 하나의 워크플로우를 노드로 하여 다른 워크플로우에 도입하는 것입니다. 향후 이 부분에서 좀 더 멋진 기능을 개발할 계획입니다;
3. 더 많은 자동화 기능, 앞으로 이미지, 텍스트, 비디오, 오디오를 다른 애플리케이션으로 자동 전송하는 노드를 더 많이 출시할 예정이며, 주류 소셜 소프트웨어 및 포럼에 자동으로 응답하는 기능을 구현하는 리스닝 노드도 선보일 것입니다;
4. 더 많은 지식 관리 기능, 현재 본 프로젝트는 로컬 파일 검색과 웹 검색을 지원하며, 앞으로 지식 그래프 검색과 장기 기억 검색 기능을 출시할 예정입니다. 이를 통해 지능체는 논리적으로 전문 지식을 사고하고, 사용자와 대화할 때 특정 핵심 정보를 영구히 기억할 수 있는 기능을 갖출 것입니다;
5. 더 많은 도구와 더 많은 인격 마스크, 이 부분은 가장 쉽게 구현할 수 있지만, 또한 가장 많은 축적이 필요한 부분입니다. 앞으로 이 프로젝트도 comfyui처럼 다양한 사용자 정의 노드를 갖추고, 많은 도구와 인격 마스크를 가질 수 있기를 희망합니다.

## 면책 조항:
본 오픈 소스 프로젝트 및 그 내용(이하 "프로젝트")은 참고용으로만 제공되며, 어떠한 명시적 또는 암시적 보증을 의미하지 않습니다. 프로젝트 기여자는 프로젝트의 완전성, 정확성, 신뢰성 또는 적합성에 대해 어떤 책임도 지지 않습니다. 프로젝트 내용에 의존하는 모든 행위는 본인 스스로 위험을 감수해야 합니다. 어떤 경우에도 프로젝트 기여자는 프로젝트 내용을 사용하여 발생하는 간접적, 특별한 또는 부수적인 손실이나 피해에 대해 책임을 지지 않습니다.
## 특별 감사
<a href="https://github.com/bigcat88">
  <img src="https://avatars.githubusercontent.com/u/13381981?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://github.com/guobalove">
  <img src="https://avatars.githubusercontent.com/u/171540731?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://github.com/HuangYuChuh">
  <img src="https://avatars.githubusercontent.com/u/167663109?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>

## 참고 목록
본 프로젝트의 일부 노드는 아래 프로젝트를 참고하였으며, 오픈소스 커뮤니티에 대한 그들의 기여에 감사드립니다!
1. [pythongosssss/ComfyUI-Custom-Scripts](https://github.com/pythongosssss/ComfyUI-Custom-Scripts)
2. [lllyasviel/Omost](https://github.com/lllyasviel/Omost)

## 지원:

### 커뮤니티 가입
플러그인에 문제가 있거나 다른 질문이 있으신 경우, 저희 커뮤니티에 가입해 주시기 바랍니다.

1. QQ 그룹: `931057213`
<div style="display: flex; justify-content: center;">
    <img src="img/Q群.jpg" style="width: 48%;" />
</div>

2. 웨이신 그룹：`Choo-Yong`（소助手의 웨이신을 추가한 후 그룹에 가입하세요）

3. 디스코드:[discord 링크](https://discord.gg/gxrQAYy6)

### 저희를 팔로우하세요
1. 본 프로젝트의 최신 기능을 지속적으로 관심 가져주시길 원하신다면, B站 계정에 팔로우해 주세요：[파티 호스트 BB기](https://space.bilibili.com/26978344)
2. OpenArt 계정은 가장 유용한 파티 워크플로우를 지속적으로 업데이트합니다：[openart](https://openart.ai/workflows/profile/comfyui_llm_party?sort=latest&tab=creation)

### 기부 지원
저의 작업이 여러분께 가치를 드렸다면, 커피 한 잔을 사주시는 것을 고려해 주세요! 여러분의 지원은 프로젝트에 활력을 불어넣을 뿐만 아니라 창작자에게도 따뜻함을 전해줍니다.☕💖 모든 한 잔이 의미가 있습니다!
<div style="display:flex; justify-content:space-between;">
    <img src="img/zhifubao.jpg" style="width: 48%;" />
    <img src="img/wechat.jpg" style="width: 48%;" />
</div>

## 스타 기록

[![Star History Chart](https://api.star-history.com/svg?repos=heshengtao/comfyui_LLM_party&type=Date)](https://star-history.com/#heshengtao/comfyui_LLM_party&Date)
