![이미지](img/封面.png)

<div align="center">
  <a href="https://space.bilibili.com/26978344">bilibili</a> ·
  <a href="https://www.youtube.com/@comfyui-LLM-party">youtube</a> ·
  <a href="https://github.com/heshengtao/Let-LLM-party">텍스트 튜토리얼</a> ·
  <a href="workflow_tutorial/">작업 흐름 튜토리얼</a> ·
  <a href="https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu">바이두 링크</a> ·
  <a href="img/Q群.jpg">QQ 그룹</a> ·
  <a href="https://discord.gg/f2dsAKKr2V">디스코드</a> ·
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

## 빠른 시작
0. 만약 당신이 comfyu를 사용해 본 적이 없고, comfyui에서 LLM 파티를 설치할 때 의존성 문제가 발생했다면, [여기를 클릭](https://drive.google.com/file/d/1NJSpwEL3FqroKVv5UsrVY3YbCG-9YWmt/view?usp=sharing) 하여 LLM 파티가 포함된 comfyui **windows** 휴대용 패키지를 다운로드하십시오. 주의하십시오! 이 휴대용 패키지에는 party와 관리자라는 두 개의 플러그인만 포함되어 있으며, 오직 windows 시스템에만 적합합니다.(기존의 comfyui에 LLM party를 설치해야 하는 경우, 이 단계를 건너뛸 수 있습니다.)
1. 다음 워크플로를 comfyui에 드래그한 다음 [comfyui-Manager](https://github.com/ltdrdata/ComfyUI-Manager)를 사용하여 누락된 노드를 설치합니다.
  - API를 사용하여 LLM 호출: [start_with_LLM_api](workflow/start_with_LLM_api.json)
  - ollama를 사용하여 로컬 LLM 관리: [start_with_Ollama](workflow/ollama.json)
  - 분산 형식의 로컬 LLM 사용: [start_with_LLM_local](workflow/start_with_LLM_local.json)
  - GGUF 형식의 로컬 LLM 사용: [start_with_LLM_GGUF](workflow/start_with_GGUF.json)
  - 분산 형식의 로컬 VLM 사용: [start_with_VLM_local](https://github.com/heshengtao/comfyui_LLM_party/blob/main/workflow_tutorial/LLM_Party%20for%20Llama3.2%20-Vision%EF%BC%88%E5%B8%A6%E8%AE%B0%E5%BF%86%EF%BC%89.json) (테스트 중, 현재는 [Llama-3.2-Vision-Instruct](https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct)만 지원)
  - GGUF 형식의 로컬 VLM 사용: [start_with_VLM_GGUF](workflow/start_with_llava.json)
2. API를 사용하는 경우, API LLM 로더 노드에 `base_url`(릴레이 API일 수 있으며, 끝이 `/v1/`로 끝나는지 확인)과 `api_key`를 입력합니다. 예: `https://api.openai.com/v1/`
3. ollama를 사용하는 경우, API LLM 로더 노드에서 `is_ollama` 옵션을 켜고 `base_url` 및 `api_key`를 입력할 필요가 없습니다.
4. 로컬 모델을 사용하는 경우, 로컬 모델 로더 노드에 모델 경로를 입력합니다. 예: `E:\model\Llama-3.2-1B-Instruct`. 또한 로컬 모델 로더 노드에 Huggingface 모델 repo id를 입력할 수도 있습니다. 예: `lllyasviel/omost-llama-3-8b-4bits`
5. 이 프로젝트는 사용 임계값이 높기 때문에 빠른 시작을 선택하더라도 프로젝트 홈페이지를 꼼꼼히 읽어주시기 바랍니다.

## 최신 업데이트
1. 로컬 파일 읽기 도구가 추가되었습니다. 이전의 comfyui LLM mafia에 있는 로컬 파일 제어 도구와 비교했을 때, 이 도구는 파일이나 특정 폴더 내의 파일 트리만 읽을 수 있어 훨씬 더 안전합니다.
1. [chatgpt-on-wechat](https://github.com/zhayujie/chatgpt-on-wechat)을 포크하여 새로운 저장소 [party-on-wechat](https://github.com/heshengtao/party-on-wechat)를 만들었습니다. 설치 및 사용 방법은 원래 프로젝트와 동일하며, 설정이 필요하지 않고 party의 FastAPI만 실행하면 됩니다. 기본적으로 wx_api 워크플로를 호출하고 이미지 출력을 지원합니다. 점진적으로 업데이트되어 WeChat에서 party를 부드럽게 사용할 수 있도록 보장됩니다.
2. 일관된 [In-Context-LoRA](https://github.com/ali-vilab/In-Context-LoRA/tree/main) 프롬프트를 생성하기 위해 In-Context-LoRA 마스크 노드를 추가했습니다.
1. 자동 모델 이름 목록 노드는 제거되었으며 config.ini 파일의 구성에서 모델 이름 목록을 자동으로 가져오는 간단한 API LLM 로더 노드로 대체되었습니다. 모델을 로드하려면 이름을 선택하기만 하면 됩니다. 또한 간단한 LLM 로더, 간단한 LLM-GGUF 로더, 간단한 VLM 로더, 간단한 VLM-GGUF 로더, 간단한 LLM lora 로더 노드가 업데이트되었습니다. 이들은 모두 파티 폴더 내의 모델 폴더에서 모델 경로를 자동으로 읽어 다양한 로컬 모델을 더 쉽게 로드할 수 있습니다.
1. 이제 LLM은 SD 및 FLUX처럼 동적으로 lora를 로드할 수 있습니다. 동일한 LLM에 더 많은 lora를 로드하기 위해 여러 lora를 연결할 수 있습니다. 예제 워크플로: [start_with_LLM_LORA](workflow/LLM_lora.json).
2. [searxng](https://github.com/searxng/searxng) 도구가 추가되어 전체 웹의 검색을 집계할 수 있습니다. Perplexica도 이 집계된 검색 도구에 의존하므로 파티에서 Perplexica를 설정할 수 있습니다. Docker에서 공개 이미지 searxng/searxng를 배포한 다음 명령 `docker run -d -p 8080:8080 searxng/searxng`을 사용하여 시작한 다음 `http://localhost:8080`을 사용하여 액세스할 수 있습니다. URL `http://localhost:8080`을 party의 searxng 도구에 입력하면 searxng이 LLM의 도구로 사용될 수 있습니다.
1. **중대한 업데이트!!!** 이제 모든 ComfyUI 워크플로를 LLM 도구 노드로 캡슐화할 수 있습니다. LLM이 여러 ComfyUI 워크플로를 동시에 제어할 수 있습니다. 작업을 완료하고 싶을 때, 프롬프트에 따라 적절한 ComfyUI 워크플로를 선택하여 작업을 완료하고 결과를 반환할 수 있습니다. 예제 워크플로: [comfyui_workflows_tool](workflow/把任意workflow当作LLM_tool.json). 구체적인 단계는 다음과 같습니다:
   - 먼저, 도구로 캡슐화할 워크플로의 텍스트 입력 인터페이스를 "워크플로 시작" 노드의 "user_prompt" 출력에 연결합니다. 이는 LLM이 도구를 호출할 때 프롬프트가 전달되는 위치입니다.
   - 텍스트와 이미지를 출력하려는 위치를 "워크플로 종료" 노드의 해당 입력 위치에 연결합니다.
   - 이 워크플로를 API로 저장합니다(설정에서 개발자 모드를 활성화해야 이 버튼을 볼 수 있습니다).
   - 이 워크플로를 프로젝트의 workflow_api 폴더에 저장합니다.
   - ComfyUI를 다시 시작하고 간단한 LLM 워크플로를 만듭니다. 예: [start_with_LLM_api](workflow/start_with_LLM_api.json).
   - 이 LLM 노드에 "워크플로 도구" 노드를 추가하고 LLM 노드의 도구 입력에 연결합니다.
   - "워크플로 도구" 노드에서 호출하려는 워크플로 파일 이름을 첫 번째 입력 상자에 작성합니다. 예: draw.json. 여러 워크플로 파일 이름을 작성할 수 있습니다. 두 번째 입력 상자에 각 워크플로의 기능을 작성합니다. 이를 통해 LLM이 이러한 워크플로를 사용하는 방법을 이해할 수 있습니다.
   - 실행하여 LLM이 캡슐화된 워크플로를 호출하고 결과를 반환하는 것을 확인합니다. 결과가 이미지인 경우, LLM 노드의 이미지 출력에 "이미지 미리보기" 노드를 연결하여 생성된 이미지를 확인합니다. 주의! 이 방법은 8190 포트에서 새로운 ComfyUI를 호출합니다. 이 포트를 점유하지 마십시오. Windows 및 Mac 시스템에서는 새로운 터미널이 열립니다. 닫지 마십시오. Linux 시스템에서는 screen 프로세스를 사용하여 이를 구현합니다. 사용하지 않을 경우 이 screen 프로세스를 닫으십시오. 그렇지 않으면 포트가 항상 점유됩니다.

![workflow_tool](img/workflowtool.png)

## 사용 설명
1. 노드 사용 설명서는 다음을 참고하십시오: [노드 사용 방법](https://github.com/heshengtao/Let-LLM-party)

2. 플러그인에 문제가 있거나 다른 질문이 있으시면 QQ 그룹에 참여해 주십시오: [931057213](img/Q群.jpg) |discord：[discord](https://discord.gg/f2dsAKKr2V).
3. 워크플로우 튜토리얼은 다음을 참조하시기 바랍니다: [워크플로우 튜토리얼](workflow_tutorial/), [HuangYuChuh](https://github.com/HuangYuChuh)님의 기여에 감사드립니다!

4. 고급 워크플로우 플레이 계정: [openart](https://openart.ai/workflows/profile/comfyui_llm_party?sort=latest&tab=creation)

4. 더 많은 워크플로우는 [workflow](workflow) 폴더를 참조하시기 바랍니다.

## 비디오 튜토리얼
<a href="https://space.bilibili.com/26978344">
  <img src="img/B.png" width="100" height="100" style="border-radius: 80%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://www.youtube.com/@comfyui-LLM-party">
  <img src="img/YT.png" width="100" height="100" style="border-radius: 80%; overflow: hidden;" alt="octocat"/>
</a>

## 모델 지원
1. 이미지에서 텍스트와 위치를 인식하기 위한 EasyOCR 노드를 추가했습니다. 해당 마스크를 생성하고 LLM이 볼 수 있도록 JSON 문자열을 반환할 수 있습니다. 표준 버전과 프리미엄 버전이 모두 제공됩니다!
2. 모든 OpenAI 형식의 API 호출을 지원합니다( [oneapi](https://github.com/songquanpeng/one-api)와 결합하면 거의 모든 LLM API를 호출할 수 있으며, 모든 중계 API도 지원합니다). base_url 선택은 [config.ini.example](config.ini.example)을 참조하시기 바랍니다. 현재 테스트된 항목은 다음과 같습니다:
* [openai](https://platform.openai.com/docs/api-reference/chat/create) (모든 OpenAI 모델과 완벽하게 호환되며, 4o 및 o1 시리즈를 포함합니다!)
* [ollama](https://github.com/ollama/ollama) (추천! 로컬에서 호출하는 경우, 로컬 모델을 호스팅하기 위해 ollama 방법을 사용하는 것이 강력히 권장됩니다!)
* [Azure OpenAI](https://azure.microsoft.com/zh-cn/products/ai-services/openai-service/)
* [llama.cpp](https://github.com/ggerganov/llama.cpp?tab=readme-ov-file#web-server) (추천! 로컬 gguf 형식 모델을 사용하려면 llama.cpp 프로젝트의 API를 사용하여 이 프로젝트에 액세스할 수 있습니다!)
* [Grok](https://x.ai/api)
* [통의천문/qwen](https://help.aliyun.com/zh/dashscope/developer-reference/compatibility-of-openai-with-dashscope/?spm=a2c4g.11186623.0.0.7b576019xkArPq)
* [지푸청언/glm](https://open.bigmodel.cn/dev/api#http_auth)
* [deepseek](https://platform.deepseek.com/api-docs/zh-cn/)
* [kimi/moonshot](https://platform.moonshot.cn/docs/api/chat#%E5%9F%BA%E6%9C%AC%E4%BF%A1%E6%81%AF)
* [doubao](https://www.volcengine.com/docs/82379/1263482)
* [讯飞星火/spark](https://xinghuo.xfyun.cn/sparkapi?scr=price)

2. Gemini 형식의 API 호출을 지원합니다:
* [Gemini](https://aistudio.google.com/app/prompts/new_chat)

3. transformer 라이브러리의 대부분의 로컬 모델과 호환됩니다 (로컬 LLM 모델 체인 노드의 모델 유형이 LLM, VLM-GGUF 및 LLM-GGUF로 변경되어 LLM 모델을 직접 로드하고, VLM 모델을 로드하고, GGUF 형식의 LLM 모델을 로드할 수 있습니다). VLM 또는 GGUF 형식의 LLM 모델에서 오류가 발생하면 [llama-cpp-python](https://github.com/abetlen/llama-cpp-python/releases)에서 최신 버전의 llama-cpp-python을 다운로드하십시오. 현재 테스트된 모델에는 다음이 포함됩니다:
* [ClosedCharacter/Peach-9B-8k-Roleplay](https://huggingface.co/ClosedCharacter/Peach-9B-8k-Roleplay) (추천! 역할극 모델)
* [lllyasviel/omost-llama-3-8b-4bits](https://huggingface.co/lllyasviel/omost-llama-3-8b-4bits) (추천! 풍부한 프롬프트 모델)
* [meta-llama/Llama-2-7b-chat-hf](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)
* [Qwen/Qwen2-7B-Instruct](https://huggingface.co/Qwen/Qwen2-7B-Instruct)
* [openbmb/MiniCPM-V-2_6-gguf](https://huggingface.co/openbmb/MiniCPM-V-2_6-gguf/tree/main)
* [lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF](https://huggingface.co/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/tree/main)
* [meta-llama/Llama-3.2-11B-Vision-Instruct](https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct)

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
1. comfyui 인터페이스에서 마우스 오른쪽 버튼을 클릭한 후, 오른쪽 클릭 메뉴의 `llm`을 선택하면 본 프로젝트의 노드를 찾을 수 있습니다. [노드 사용 방법](https://github.com/heshengtao/Let-LLM-party)
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
2. 일련의 변환 노드를 업데이트했습니다: markdown에서 HTML, svg에서 이미지, HTML에서 이미지, mermaid에서 이미지, markdown에서 Excel.
1. llama3.2 vision 모델과 호환되며, 다중 회차 대화 및 시각 기능을 지원합니다. 모델 주소: [meta-llama/Llama-3.2-11B-Vision-Instruct](https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct). 예제 워크플로우: [llama3.2_vision](https://github.com/heshengtao/comfyui_LLM_party/blob/main/workflow_tutorial/LLM_Party%20for%20Llama3.2%20-Vision%EF%BC%88%E5%B8%A6%E8%AE%B0%E5%BF%86%EF%BC%89.json).
1. GOT-OCR2를 적용하여 형식화된 출력 결과를 지원하고 위치 상자와 색상을 사용하여 텍스트를 정밀하게 인식합니다. 모델 주소: [GOT-OCR2](https://huggingface.co/stepfun-ai/GOT-OCR2_0). 예제 워크플로우는 웹페이지의 스크린샷을 HTML 코드로 변환한 다음 브라우저를 열어 이 웹페이지를 표시합니다: [img2web](workflow/图片转网页.json).
2. 로컬 LLM 로더 노드가 크게 조정되어 모델 유형을 직접 선택할 필요가 없습니다. llava 로더 노드와 GGUF 로더 노드가 다시 추가되었습니다. 로컬 LLM 모델 체인 노드의 모델 유형이 LLM, VLM-GGUF 및 LLM-GGUF로 변경되어 LLM 모델을 직접 로드하고, VLM 모델을 로드하고, GGUF 형식의 LLM 모델을 로드할 수 있습니다. 이제 VLM 모델과 GGUF 형식의 LLM 모델이 다시 지원됩니다. 로컬 호출은 이제 더 많은 모델과 호환될 수 있습니다! 예제 워크플로우: [LLM_local](workflow/start_with_LLM_local.json), [llava](workflow/start_with_llava.json), [GGUF](workflow/start_with_GGUF.json)
2. easyOCR 노드가 추가되어 이미지 내 텍스트와 위치를 인식할 수 있습니다. 해당 마스크를 생성할 수 있으며, LLM이 볼 수 있는 JSON 문자열을 반환할 수 있습니다. 일반 버전과 고급 버전이 제공됩니다!
2. comfyui LLM 파티에서 chatgpt-o1 시리즈 모델의 딸기 시스템을 재현했습니다. [Llamaberry](https://huggingface.co/spaces/martinbowling/Llamaberry/blob/main/app.py)의 프롬프트를 참고했습니다. 예제 워크플로우: [Strawberry system compared to o1](workflow/草莓系统与o1对比.json).
2. 새로운 GPT-sovits 노드가 추가되어 GPT-sovits 모델을 호출하여 참조 오디오를 기반으로 텍스트를 음성으로 변환할 수 있습니다. 또한 미세 조정된 모델 경로를 입력할 수도 있습니다(입력하지 않으면 기본 모델이 추론에 사용됨) 원하는 음성을 얻을 수 있습니다. 사용하려면 [GPT-sovits](https://github.com/RVC-Boss/GPT-SoVITS) 프로젝트와 해당 기본 모델을 로컬에 다운로드한 다음 GPT-sovits 프로젝트 폴더에서 `runtime\python.exe api_v2.py`를 사용하여 API 서비스를 시작해야 합니다. 또한 chatTTS 노드는 [comfyui LLM mafia](https://github.com/heshengtao/comfyui_LLM_mafia)로 이동되었습니다. 이유는 chatTTS에 많은 종속성이 있으며 PyPi의 라이선스가 CC BY-NC 4.0으로 비상업적 라이선스이기 때문입니다. chatTTS의 GitHub 프로젝트가 AGPL 라이선스 하에 있음에도 불구하고 불필요한 문제를 피하기 위해 chatTTS 노드를 comfyui LLM mafia로 이동했습니다. 모두의 이해를 바랍니다!
3. 이제 OpenAI의 최신 모델인 o1 시리즈를 지원합니다!
4. 지정한 폴더의 파일을 제어할 수 있는 로컬 파일 제어 도구가 추가되었습니다. 읽기, 쓰기, 추가, 삭제, 이름 변경, 이동, 복사 등이 가능합니다.이 노드의 잠재적인 위험성 때문에 [comfyui LLM mafia](https://github.com/heshengtao/comfyui_LLM_mafia)에 포함되어 있습니다.
5. 새로운 SQL 도구로 LLM이 SQL 데이터베이스를 쿼리할 수 있습니다.
6. README의 다국어 버전을 업데이트했습니다. README 문서를 번역하는 워크플로우: [translate_readme](workflow/文档自动翻译机.json)
7. 4개의 반복기 노드(텍스트 반복기, 이미지 반복기, 표 반복기, json 반복기)가 업데이트되었습니다. 반복기 모드는 순차, 무작위 및 무한의 세 가지 모드가 있습니다. 순차 모드는 순서대로 출력을 하며, 인덱스 한계를 초과하면 자동으로 프로세스가 중단되고 인덱스 값이 0으로 재설정됩니다. 무작위 모드는 무작위 인덱스를 선택하여 출력을 하며, 무한 모드는 무한 반복 출력을 진행합니다.
8. Gemini API 로더 노드가 추가되어 이제 Gemini 공식 API와 호환됩니다! 국내 네트워크 환경에서 API 지역 제한 문제가 발생하면 노드를 미국으로 전환하고 TUN 모드를 사용해 주십시오. Gemini에서 도구 호출 시 반환된 파라미터에 중국어 문자가 포함되면 반환 코드 500 오류가 발생할 수 있어 일부 도구 노드가 사용 불가능합니다. 예시 워크플로우: [start_with_gemini](workflow/start_with_gemini.json)
9. LLM과 대화할 때 배경 설정을 삽입할 수 있는 lore book 노드가 추가되었습니다. 예시 워크플로우: [lorebook](workflow/lorebook.json)
10. FLUX 프롬프트 생성기 마스크 노드가 추가되어 하스스톤 카드, 유희왕 카드, 포스터, 만화 등 다양한 스타일의 프롬프트를 생성할 수 있으며, FLUX 모델이 직접 출력할 수 있게 해줍니다. 참고 워크플로우: [FLUX 프롬프트](https://openart.ai/workflows/comfyui_llm_party/flux-by-llm-party/sjME541i68Kfw6Ib0EAD)

## 다음 단계 계획:
1. 더 많은 모델 적응;
2. 더 많은 에이전트 구축 방법;
3. 더 많은 자동화 기능;
4. 더 많은 지식 베이스 관리 기능;
5. 더 많은 도구, 더 많은 페르소나.

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
<a href="https://github.com/SpenserCai">
  <img src="https://avatars.githubusercontent.com/u/25168945?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
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

3. 디스코드:[discord 링크](https://discord.gg/f2dsAKKr2V)

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
