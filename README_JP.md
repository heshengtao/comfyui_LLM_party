![画像](img/封面.png)

<div align="center">
  <a href="https://space.bilibili.com/26978344">ビデオチュートリアル</a> ·
  <a href="how_to_use_nodes.md">テキストチュートリアル</a> ·
  <a href="workflow_tutorial/">ワークフローチュートリアル</a> ·
  <a href="https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu">Baiduクラウド</a> ·
  <a href="img/Q群.jpg">QQグループ</a> ·
  <a href="https://discord.gg/gxrQAYy6">ディスコード</a> ·
  <a href="https://dcnsxxvm4zeq.feishu.cn/wiki/IyUowXNj9iH0vzk68cpcLnZXnYf">私たちについて</a>
</div>

####

<div align="center">
  <a href="./README.md"><img src="https://img.shields.io/badge/English-d9d9d9"></a>
  <a href="./README_ZH.md"><img src="https://img.shields.io/badge/简体中文-d9d9d9"></a>
  <a href="./README_JP.md"><img src="https://img.shields.io/badge/日本語-d9d9d9"></a>
</div>

####

C‌‌﻿​﻿‎﻿​﻿‎‏​﻿‍‎​﻿‎﻿​﻿‎‏​﻿‌‎​﻿‎‍​﻿‍‏​‍﻿‌​﻿‌‏omfyui_llm_partyは、[comfyui](https://github.com/comfyanonymous/ComfyUI)をフロントエンドとして、LLMワークフロー構築のための完全なノードセットを開発することを目的としています。これにより、ユーザーは自分のLLMワークフローを迅速かつ便利に構築し、既存の画像ワークフローに簡単に統合することができます。

## 効果の表示
https://github.com/user-attachments/assets/945493c0-92b3-4244-ba8f-0c4b2ad4eba6

## プロジェクト概要

ComfyUI LLM Partyは、最も基本的なLLMマルチツール呼び出し、役割設定から独自のAIアシスタントを迅速に構築することから、業界固有の単語ベクトルRAGおよびGraphRAGを使用して業界知識ベースのローカライズ管理まで、単一のエージェントパイプラインから複雑なエージェント間の放射状相互作用モードおよびリング相互作用モードの構築まで、個々のユーザーが必要とする自分のソーシャルAPP（QQ、Feishu、Discord）へのアクセスから、ストリーミングメディアワーカーが必要とするワンストップLLM + TTS + ComfyUIワークフローまで、普通の学生が必要とする最初のLLMアプリケーションの簡単なスタートから、科学研究者がよく使用するさまざまなパラメータデバッグインターフェース、モデル適応まで、すべての答えをComfyUI LLM Partyで見つけることができます。

## 最新の更新
1. Gemini APIローダーノードを追加し、Gemini公式APIと互換性があります！Geminiがツール呼び出し中に返されたパラメータに中国語の文字が含まれている場合、エラーコード500が生成されるため、一部のツールノードは使用できません。例：ワークフロー：[start_with_gemini](workflow/start_with_gemini.json)
2. ロアブックノードを追加し、LLMとの対話中に背景設定を挿入できます。例：ワークフロー：[lorebook](workflow/lorebook.json)
3. FLUXプロンプトワードジェネレーターマスクノードを追加し、ハースストーンカード、ゲームキングカード、ポスター、漫画などのスタイルのプロンプトワードを生成できます。これにより、FLUXモデルが直接出力できます。参考ワークフロー：[FLUXプロンプトワード](https://openart.ai/workflows/comfyui_llm_party/flux-by-llm-party/sjME541i68Kfw6Ib0EAD)
4. このLLMツールメーカーを使用してLLMツールを自動生成し、生成されたツールコードをpythonファイルとして保存し、コードをcustom_toolフォルダーにコピーすると、新しいノードが作成されます。例：ワークフロー：[LLMツールジェネレーター](workflow/LLM工具制造机.json)。
5. duckduckgo検索をサポートしていますが、重大な制限があります。英語のキーワードのみを入力でき、キーワードに複数の概念を含めることはできません。利点は、APIkeyの制限がないことです。
6. 複数の知識ベースを個別に呼び出す機能をサポートしており、プロンプトワード内でどの知識ベースを使用して質問に回答するかを指定できます。例：ワークフロー：[複数の知識ベースを個別に呼び出す](workflow/多知识库分别调用.json)。
7. LLM入力の追加パラメータをサポートし、json outなどの高度なパラメータを含みます。例：ワークフロー：[LLM入力の追加パラメータ](workflow/LLM额外参数eg_JSON_OUT.json)。[json_outでプロンプトワードを分離](workflow/用json_out分离提示词.json)。
8. エージェントをdiscordに接続する機能を追加しました。（まだテスト中）
9. エージェントをFeishuに接続する機能を追加しました。貢献してくれた[guobalove](https://github.com/guobalove)に感謝します！参考ワークフロー：[Feishuロボット](workflow/飞书机器人.json)。
10. 汎用API呼び出しノードと、リクエストボディを構築し、レスポンス内の情報を取得するための多数の補助ノードを追加しました。
11. 任意の場所でLLMをビデオメモリからアンインストールできる空のモデルノードを追加しました！
12. [chatTTS](https://github.com/2noise/ChatTTS)ノードが追加されました。貢献してくれた[guobalove](https://github.com/guobalove)に感謝します！ `model_path`パラメータは空にすることができます！ `HF`モードを使用してモデルをロードすることをお勧めします。モデルはhugging faceから自動的にダウンロードされ、手動でダウンロードする必要はありません。 `local`ロードを使用する場合は、モデルの`asset`および`config`フォルダーをルートディレクトリに配置してください。[Baiduクラウドアドレス](https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu)、抽出コード：qyhu; `custom`モードを使用してロードする場合は、モデルの`asset`および`config`フォルダーを`model_path`に配置してください。

## ユーザーガイド
1. ノードの使用方法については、[ノードの使用方法](how_to_use_nodes.md)を参照してください。

2. プラグインに問題がある場合や他の質問がある場合は、QQグループに参加してください：[931057213](img/Q群.jpg)。

3. ワークフローチュートリアルについては、[ワークフローチュートリアル](workflow_tutorial/)を参照してください。貢献してくれた[HuangYuChuh](https://github.com/HuangYuChuh)に感謝します！

4. 高度なワークフローのプレイアカウント：[openart](https://openart.ai/workflows/profile/comfyui_llm_party?sort=latest&tab=creation)

5. 詳細なワークフローについては、[workflow](workflow)フォルダーを参照してください。

## ビデオチュートリアル
1. [ComfyUI×LLMでモジュラーAIを構築する：ステップバイステップチュートリアル（超簡単！）](https://www.bilibili.com/video/BV1JZ421v7Tw/?vd_source=f229e378448918b84afab7c430c6a75b)

2. [GPT-4oをcomfyuiに接続する方法 | ワークフローを別のワークフローに呼び出す | LLMをツールにする](https://www.bilibili.com/video/BV1JJ4m1A789/?spm_id_from=333.999.0.0&vd_source=f229e378448918b84afab7c430c6a75b)

3. [ワークフローをGPTに偽装してWeChatに接続する方法 | Omost互換！柔軟に自分のdalle3を作成する](https://www.bilibili.com/video/BV1DT421a7KY/?spm_id_from=333.999.0.0)

4. [comfyuiでインタラクティブフィクションゲームをプレイする方法](https://www.bilibili.com/video/BV15y411q78L/?spm_id_from=333.999.0.0&vd_source=f229e378448918b84afab7c430c6a75b)

5. [AIガールフレンド、そしてあなたの形 | comfyuiでgraphRAGを実装し、neoa4jと連携 | comfyuiワークフローをstreamlitフロントエンドに接続](https://www.bilibili.com/video/BV1dS421R7Au/?spm_id_from=333.999.0.0&vd_source=f229e378448918b84afab7c430c6a75b)

## モデルサポート
1. openai形式のすべてのAPI呼び出しをサポートします（[oneapi](https://github.com/songquanpeng/one-api)と組み合わせることで、ほぼすべてのLLM APIを呼び出すことができ、すべてのトランジットAPIもサポートします）。base_urlの選択は[config.ini.example](config.ini.example)を参照してください。これまでにテストされたものは次のとおりです：
* [ollama](https://github.com/ollama/ollama)（推奨！ローカルで呼び出す場合は、ollamaを使用してローカルモデルをホストすることを強くお勧めします！）
* [Tongyi Qianwen /qwen](https://help.aliyun.com/zh/dashscope/developer-reference/compatibility-of-openai-with-dashscope/?spm=a2c4g.11186623.0.0.7b576019xkArPq)
* [zhipu qingyan/glm](https://open.bigmodel.cn/dev/api#http_auth)
* [deepseek](https://platform.deepseek.com/api-docs/zh-cn/)
* [kimi/moonshot](https://platform.moonshot.cn/docs/api/chat#%E5%9F%BA%E6%9C%AC%E4%BF%A1%E6%81%AF)
* [doubao](https://www.volcengine.com/docs/82379/1263482)

2. transformerライブラリAutoModelForCausalLMクラスがサポートするほとんどのローカルモデル（ローカルモデルノードのモデルタイプが何を選択するかわからない場合は、llamaを選択してください。高確率で適応できます）。これまでにテストされたものは次のとおりです：
* [ClosedCharacter/Peach-9B-8k-Roleplay](https://huggingface.co/ClosedCharacter/Peach-9B-8k-Roleplay)（推奨！ロールプレイングモデル）
* [omost-llama-3-8b-4bits](https://huggingface.co/lllyasviel/omost-llama-3-8b-4bits)（推奨！リッチプロンプトモデル）
* [meta-llama/llama-2-7b-chat-hf](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)
* [Qwen/Qwen2-7B-Instruct](https://huggingface.co/Qwen/Qwen2-7B-Instruct)
* [xtuner/llava-llama-3-8b-v1_1-gguf](https://huggingface.co/xtuner/llava-llama-3-8b-v1_1-gguf)
* [THUDM/chatglm3-6b](https://huggingface.co/THUDM/chatglm3-6b)（GLM4の新しい呼び出し形式のため、開発者はすべてのローカル大規模モデルの呼び出しを維持できないため、ollamaを使用してローカルで呼び出すことをお勧めします！）

3. モデルのダウンロード：
* [Baiduクラウドアドレス](https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu)、抽出コード：qyhu

## ダウンロード
* `config.ini`で言語を設定できます。現在、言語は中国語（zh_CN）と英語（en_US）のみで、デフォルトはシステム言語です。
* 次の方法のいずれかを使用してインストールします：
### 方法1：
1. [comfyuiマネージャー](https://github.com/ltdrdata/ComfyUI-Manager)でcomfyui_LLM_partyを検索し、ワンクリックでインストールします。
2. comfyuiを再起動します。

### 方法2：
1. ComfyUIルートフォルダーの`custom_nodes`サブフォルダーに移動します。
2. `git clone https://github.com/heshengtao/comfyui_LLM_party.git`でこのリポジトリをクローンします。

### 方法3：
1. 右上の`CODE`をクリックします。
2. `download zip`をクリックします。
3. ダウンロードしたパッケージをComfyUIルートフォルダーの`custom_nodes`サブフォルダーに解凍します。

## 環境の展開
1. `comfyui_LLM_party`プロジェクトフォルダーに移動します。
2. ターミナルで`pip install -r requirements.txt`を入力して、プロジェクトに必要なサードパーティライブラリをcomfyui環境にデプロイします。comfyui環境内でインストールしていることを確認し、ターミナルの`pip`エラーに注意してください。
3. comfyuiランチャーを使用している場合は、ターミナルで`path_in_launcher_configuration\python_embeded\python.exe -m pip install -r requirements.txt`を入力してインストールする必要があります。 `python_embeded`フォルダーは通常、`ComfyUI`フォルダーと同じレベルにあります。
4. 環境構成に問題がある場合は、`requirements_fixed.txt`の依存関係を使用してみてください。

## 設定
APIKEYは次の方法のいずれかを使用して設定できます
### 方法1：
1. `comfyui_LLM_party`のプロジェクトフォルダー内の`config.ini`ファイルを開きます。
2. `config.ini`にopenai_api_key、base_urlを入力します。
3. ollamaモデルを使用している場合は、`base_url`に`http://127.0.0.1:11434/v1/`を入力し、`openai_api_key`に`ollama`を入力し、`model_name`にモデル名を入力します。例：`llama3`。
4. Google検索またはBing検索ツールを使用する場合は、`config.ini`に`google_api_key`、`cse_id`または`bing_api_key`を入力します。
5. 画像入力LLMを使用する場合は、画像ベッドimgbbを使用することをお勧めし、`config.ini`にimgbb_apiを入力します。
6. 各モデルは`config.ini`ファイルで個別に設定できます。`config.ini.example`ファイルを参照して記入してください。設定が完了したら、ノードに`model_name`を入力するだけです。

### 方法2：
1. comfyuiインターフェースを開きます。
2. 大規模言語モデル（LLM）ノードを作成し、ノードにopenai_api_keyとbase_urlを直接入力します。
3. ollamaモデルを使用する場合は、LLM_apiノードを使用し、ノードの`base_url`に`http://127.0.0.1:11434/v1/`を入力し、`api_key`に`ollama`を入力し、`model_name`にモデル名を入力します。例：`llama3`。
4. 画像入力LLMを使用する場合は、画像ベッドimgbbを使用することをお勧めし、ノードにimgbb_api_keyを入力します。

## 変更履歴
1. comfyuiインターフェースで右クリックし、コンテキストメニューから`llm`を選択すると、このプロジェクトのノードが表示されます。[ノードの使用方法](how_to_use_nodes.md)
2. API統合またはローカル大規模モデル統合をサポートします。ツール呼び出しのモジュール化を実現します。base_urlを入力する際は、`/v1/`で終わるURLを使用してください。モデルを管理するために[ollama](https://github.com/ollama/ollama)を使用できます。その場合、base_urlに`http://127.0.0.1:11434/v1/`、api_keyにollama、model_nameにモデル名を入力します。例：llama3。
- APIアクセスのサンプルワークフロー：[start_with_LLM_api](workflow/start_with_LLM_api)
- ローカルモデルアクセスのサンプルワークフロー：[start_with_LLM_local](workflow/start_with_LLM_local)
- ollamaアクセスのサンプルワークフロー：[ollama](workflow/ollama.json)
3. RAGサポートを備えたローカル知識ベースの統合。サンプルワークフロー：[Knowledge Base RAG Search](workflow/知识库RAG搜索.json)
4. コードインタープリターの呼び出し機能。
5. オンラインクエリを有効にし、Google検索をサポートします。サンプルワークフロー：[movie query workflow](workflow/电影查询工作流.json)
6. ComfyUI内で条件文を実装し、ユーザーのクエリを分類してターゲット応答を提供します。サンプルワークフロー：[intelligent customer service](workflow/智能客服.json)
7. 大規模モデルのループリンクをサポートし、2つの大規模モデルがディベートを行うことができます。サンプルワークフロー：[Tram Challenge Debate](workflow/电车难题辩论赛.json)
8. 任意のペルソナマスクを添付し、プロンプトテンプレートをカスタマイズします。
9. 天気検索、時間検索、知識ベース、コード実行、ウェブ検索、単一ページ検索など、さまざまなツール呼び出しをサポートします。
10. LLMをツールノードとして使用します。サンプルワークフロー：[LLM Matryoshka dolls](workflow/LLM套娃.json)
11. API + Streamlitを使用して独自のWebアプリケーションを迅速に開発します。
12. 大規模モデルが任意のタスクを実行できる危険な万能インタープリターノードを追加しました。
13. LLMノードの表示出力として、右クリックメニューの`function`サブメニューの`show_text`ノードを使用することをお勧めします。
14. GPT-4Oの視覚機能をサポートしました！サンプルワークフロー：[GPT-4o](workflow/GPT-4o.json)
15. 新しいワークフロー中継器を追加し、ワークフローが他のワークフローを呼び出すことができます！サンプルワークフロー：[Invoke another workflow](workflow/调用另一个工作流.json)
16. OpenAIに似たインターフェースを持つすべてのモデルに適応しました。例：Tongyi Qianwen/QWEN、Zhigu Qingyan/GLM、DeepSeek、Kimi/Moonshot。これらのモデルのbase_url、api_key、model_nameをLLMノードに入力して呼び出します。
17. LVMローダーを追加し、LVMモデルをローカルで呼び出すことができるようになりました。サポートされているモデル：[lava-llama-3-8b-v1_1-gguf](https://huggingface.co/xtuner/llava-llama-3-8b-v1_1-gguf)。他のLVMモデルはGGUF形式であれば理論的に実行できるはずです。サンプルワークフローはここにあります：[start_with_LVM.json](workflow/start_with_LVM.json)。
18. `fastapi.py`ファイルを書きました。これを直接実行すると、`http://127.0.0.1:8817/v1/`にOpenAIインターフェースが表示されます。GPTを呼び出すことができるアプリケーションは、comfyuiワークフローを呼び出すことができます！詳細な操作方法については、チュートリアルを作成してデモンストレーションします。
19. LLMローダーとLLMチェーンを分離し、モデルのロードとモデルの設定を分けました。これにより、異なるLLMノード間でモデルを共有できます！
20. macOSおよびmpsデバイスがサポートされました！貢献してくれた[bigcat88](https://github.com/bigcat88)に感謝します！
21. インタラクティブな小説ゲームを構築でき、ユーザーの選択に応じて異なるエンディングに進むことができます！サンプルワークフローの参考：[interactive_novel](workflow/互动小说.json)
22. OpenAIのwhisperおよびtts機能に適応し、音声入力および出力を実現できます。サンプルワークフローの参考：[voice_input&voice_output](workflow/语音输入+语音输出.json)
23. [Omost](https://github.com/lllyasviel/Omost)と互換性があります!!! [omost-llama-3-8b-4bits](https://huggingface.co/lllyasviel/omost-llama-3-8b-4bits)をダウンロードしてすぐに体験してください！サンプルワークフローの参考：[start_with_OMOST](workflow/start_with_OMOST)
24. WeCom、DingTalk、Feishuにメッセージを送信するLLMツールと、呼び出すための外部関数を追加しました。
25. 新しいテキストイテレータを追加し、文字の一部だけを出力できます。キャリッジリターンとチャンクサイズに基づいてテキストを安全に分割し、テキストの途中から分割されることはありません。チャンクオーバーラップは、分割されたテキストがどれだけ重なるかを指します。このようにして、超長テキストをバッチで入力できます。無脳でクリックするだけで、またはcomfyuiでループ実行を開始すると、自動的に実行されます。入力の終わりにワークフローを自動的にロックし、実行を続けないようにするis_lockedプロパティをオンにすることを忘れないでください。サンプルワークフロー：[text iteration input](workflow/文本迭代输入.json)
26. ローカルLLMローダー、ローカルllavaローダーにモデル名属性を追加しました。空の場合、ノード内のさまざまなローカルパスを使用してロードされます。空でない場合、`config.ini`に自分で入力したパスパラメータを使用してロードされます。空でなく、`config.ini`にない場合、huggingfaceからダウンロードされるか、huggingfaceのモデル保存ディレクトリからロードされます。huggingfaceからダウンロードする場合は、例：`THUDM/glm-4-9b-chat`の形式でモデル名属性を入力してください。注意！この方法でロードされるモデルは、transformerライブラリに適応する必要があります。
27. [CosyVoice](https://github.com/FunAudioLLM/CosyVoice)に適応し、モデルやAPIキーをダウンロードせずにTTS機能を直接使用できるようになりました。現在、このインターフェースは中国語にのみ適応しています。
28. JSONファイル解析ノードとJSON値ノードを追加し、ファイルやテキストからキーの値を取得できます。貢献してくれた[guobalove](https://github.com/guobalove)に感謝します！
29. ツール呼び出しのコードを改善しました。現在、ツール呼び出し機能を持たないLLMもis_tools_in_sys_prompt属性を開くことができます（ローカルLLMはデフォルトで開く必要はなく、自動適応します）。開くと、ツール情報がシステムプロンプトワードに追加され、LLMがツールを呼び出すことができます。実装原理に関する関連論文：[Achieving Tool Calling Functionality in LLMs Using Only Prompt Engineering Without Fine-Tuning](https://arxiv.org/abs/2407.04997)
30. カスタムツールのコードを保存するための新しいcustom_toolフォルダーを作成しました。カスタムツールのコードをcustom_toolフォルダーに配置することで、LLMでカスタムツールを呼び出すことができます。
31. 知識グラフツールを追加し、LLMと知識グラフが完全に相互作用できるようにしました。LLMは入力に基づいて知識グラフを変更し、知識グラフ上で推論して必要な回答を得ることができます。サンプルワークフローの参考：[graphRAG_neo4j](workflow/graphRAG_neo4j.json)
32. パーソナリティAI機能を追加し、0コードで独自のガールフレンドAIまたはボーイフレンドAIを開発し、無限の対話、永続的な記憶、安定したパーソナリティを実現します。サンプルワークフローの参考：[Mylover Personality AI](workflow/麦洛薇人格AI.json)

## 次のステップの計画：
1. さらに多くのモデル適応、少なくとも主流の大規模モデルAPIインターフェースと主流のオープンソースモデルのローカル呼び出しをカバーし、さらに多くのLVMモデルの適応を行います。現在、GPT-4の視覚機能の呼び出しのみを適応しています。
2. さらに多くのエージェント構築方法。これまでに完了した作業には、LLMをツールとして別のLLMにインポートし、放射状のLLMワークフローを構築し、1つのワークフローを別のワークフローにノードとしてインポートすることが含まれます。将来的には、この分野でさらにクールな機能を開発するかもしれません。
3. さらに多くの自動化機能。将来的には、画像、テキスト、ビデオ、オーディオを他のアプリケーションに自動的にプッシュするノードや、主流のソーシャルソフトウェアやフォーラムに自動返信する機能を実装するリスニングノードを導入します。
4. さらに多くの知識ベース管理機能。現在、このプロジェクトはローカルファイル検索とウェブ検索をサポートしています。将来的には、知識グラフ検索と長期記憶検索を導入します。これにより、エージェントは専門知識を論理的に考え、ユーザーとの対話中に特定の重要な情報を常に記憶することができます。
5. さらに多くのツール、さらに多くのペルソナ。この部分は最も簡単に実行できますが、最も多くの蓄積が必要です。将来的には、このプロジェクトがcomfyuiのように多数のカスタムノードを持ち、多数のツールとペルソナを持つことを願っています。

## 免責事項：
このオープンソースプロジェクトおよびその内容（以下「プロジェクト」）は、参考目的で提供されており、明示的または黙示的な保証を意味するものではありません。プロジェクトの貢献者は、プロジェクトの完全性、正確性、信頼性、または適用性について一切の責任を負いません。プロジェクトの内容に依存する行為はすべて自己責任で行ってください。いかなる場合においても、プロジェクトの貢献者は、プロジェクトの内容の使用に起因する間接的、特別、または付随的な損害または損失について一切の責任を負いません。

## 特別な感謝：
<a href="https://github.com/bigcat88">
  <img src="https://avatars.githubusercontent.com/u/13381981?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://github.com/guobalove">
  <img src="https://avatars.githubusercontent.com/u/171540731?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://github.com/HuangYuChuh">
  <img src="https://avatars.githubusercontent.com/u/167663109?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>

## 借用リスト
このプロジェクトの一部のノードは、以下のプロジェクトから借用されています。オープンソースコミュニティへの貢献に感謝します！
1. [ComfyUI-Custom-Scripts](https://github.com/pythongosssss/ComfyUI-Custom-Scripts)
2. [omost](https://github.com/lllyasviel/Omost)
3. [chatTTS](https://github.com/2noise/ChatTTS)
4. [CosyVoice](https://github.com/FunAudioLLM/CosyVoice)

## サポート：

### コミュニティに参加する
プラグインに問題がある場合や他の質問がある場合は、コミュニティに参加してください。

1. discord：[discordリンク](https://discord.gg/gxrQAYy6)
2. QQグループ：`931057213`

<div style="display: flex; justify-content: center;">
    <img src="img/Q群.jpg" style="width: 48%;" />
</div>

3. WeChatグループ：`Choo-Yong`（小助手WeChatを追加してからグループに参加）

### フォローする
1. このプロジェクトの最新機能に引き続き関心を持ちたい場合は、Bilibiliアカウントをフォローしてください：[Party host BB machine](https://space.bilibili.com/26978344)
2. OpenArtアカウントは、最も役立つパーティーワークフローを継続的に更新します：[openart](https://openart.ai/workflows/profile/comfyui_llm_party?sort=latest&tab=creation)

### 寄付のサポート
私の仕事があなたの日常に価値をもたらした場合は、コーヒーで燃料を補給することを検討してください！あなたのサポートはプロジェクトにエネルギーを与えるだけでなく、クリエイターの心を温めます。☕💖 すべてのカップが違いを生みます！
<div style="display:flex; justify-content:space-between;">
    <img src="img/zhifubao.jpg" style="width: 48%;" />
    <img src="img/wechat.jpg" style="width: 48%;" />
</div>

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=heshengtao/comfyui_LLM_party&type=Date)](https://star-history.com/#heshengtao/comfyui_LLM_party&Date)
