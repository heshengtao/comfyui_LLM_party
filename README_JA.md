![画像](img/封面.png)

<div align="center">
  <a href="https://space.bilibili.com/26978344">ビデオチュートリアル</a> ·
  <a href="how_to_use_nodes_ZH.md">テキストチュートリアル</a> ·
  <a href="workflow_tutorial/">ワークフローチュートリアル</a> ·
  <a href="https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu">百度リンク</a> ·
  <a href="img/Q群.jpg">QQグループ</a> ·
  <a href="https://discord.gg/gxrQAYy6">ディスコード</a> ·
  <a href="https://dcnsxxvm4zeq.feishu.cn/wiki/IyUowXNj9iH0vzk68cpcLnZXnYf">私たちについて</a>
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

Comfyui_llm_partyは、[comfyui](https://github.com/comfyanonymous/ComfyUI)という非常にシンプルなUIインターフェースを基に、LLMワークフロー構築のための完全なノードライブラリを開発することを目指しています。これにより、ユーザーは自身のLLMワークフローをより便利かつ迅速に構築でき、自身の画像ワークフローに接続することも容易になります。

## 効果の展示
https://github.com/user-attachments/assets/945493c0-92b3-4244-ba8f-0c4b2ad4eba6

## プロジェクト概要
ComfyUI LLM Partyは、最も基本的なLLMの多ツール呼び出しやキャラクター設定によって、専属のAIアシスタントを迅速に構築することから、業界に適用可能な単語ベクトルRAG、GraphRAGを用いた知識ベースのローカル管理までを行います。単一のエージェントパイプラインから、複雑なエージェント間の放射状および環状の相互作用モードの構築まで、個人ユーザーのためのSNSアプリ（QQ、Feishu、Discord）への接続から、ストリーミングメディアの作業者が必要とするワンストップLLM+TTS+ComfyUIワークフローまで、普通の学生が必要とする最初のLLMアプリケーションの簡単な導入から、研究者が一般的に使用するさまざまなパラメータ調整インターフェースやモデル適応に至るまで、これらすべての答えはComfyUI LLM Partyの中にあります。

## 最新の更新
1. comfyui LLMパーティーで、chatgpt-o1シリーズモデルのストロベリーシステムが再現され、[Llamaberry](https://huggingface.co/spaces/martinbowling/Llamaberry/blob/main/app.py)のプロンプトを参照しました。例のワークフロー：[ストロベリーシステムとo1の比較](workflow\草莓系统与o1对比.json)。
2. 新しいGPT-sovitsノードが追加され、GPT-sovitsモデルを呼び出して、参照オーディオに基づいてテキストを音声に変換できるようになりました。また、微調整されたモデルのパスを入力することもできます（入力しない場合はベースモデルが推論に使用されます）任意の音声を取得できます。使用するには、[GPT-sovits](https://github.com/RVC-Boss/GPT-SoVITS)プロジェクトと対応するベースモデルをローカルにダウンロードし、GPT-sovitsプロジェクトフォルダーで`runtime\python.exe api_v2.py`を使用してAPIサービスを開始する必要があります。さらに、chatTTSノードは[comfyui LLM mafia](https://github.com/heshengtao/comfyui_LLM_mafia)に移動されました。理由は、chatTTSには多くの依存関係があり、PyPiのライセンスはCC BY-NC 4.0であり、これは非商用ライセンスです。chatTTSのGitHubプロジェクトがAGPLライセンスの下にあるにもかかわらず、不要なトラブルを避けるためにchatTTSノードをcomfyui LLM mafiaに移動しました。皆さんの理解をお願いします！
3. 最新のOpenAIモデル、o1シリーズをサポートしました！
4. 指定したフォルダ内のファイルを制御できるローカルファイル制御ツールを追加しました。読み取り、書き込み、追加、削除、名前変更、移動、コピーなどが可能です。このノードの潜在的な危険性のため、[comfyui LLM mafia](https://github.com/heshengtao/comfyui_LLM_mafia)に含まれています。
5. 新しいSQLツールにより、LLMがSQLデータベースをクエリできます。
6. READMEの多言語バージョンを更新しました。READMEドキュメントを翻訳するためのワークフロー：[translate_readme](workflow/文档自动翻译机.json)
7. 4つのイテレーターノード（テキストイテレーター、画像イテレーター、表イテレーター、JSONイテレーター）が更新され、イテレーターのモードとして順次、ランダム、無限の3種類が追加されました。順次は順番に出力を行い、インデックスの上限を超えると自動的にプロセスを中止し、インデックス値を0にリセットします。ランダムはランダムなインデックスを選択して出力し、無限は無限に出力を繰り返します。
8. Gemini APIローダーノードが新たに追加され、Gemini公式APIとの互換性が確保されました！国内ネットワーク環境でAPI地域制限の問題が発生した場合は、ノードをアメリカに切り替え、TUNモードを使用してください。Geminiはツール呼び出し時に、戻りパラメータに中文文字が含まれると、500のエラーコードが返されるため、特定のツールノードが使用できない場合があります。サンプルワークフロー：[start_with_gemini](workflow/start_with_gemini.json)
9. lore bookノードが新たに追加され、LLMとの対話時に背景設定を挿入することができます。サンプルワークフロー：[lorebook](workflow/lorebook.json)
10. FLUXプロンプト生成器マスクノードが新たに追加され、ハースストーンカード、遊戯王カード、ポスター、漫画などのさまざまなスタイルのプロンプトを生成でき、FLUXモデルを直接出力できます。参考ワークフロー：[FLUXプロンプト](https://openart.ai/workflows/comfyui_llm_party/flux-by-llm-party/sjME541i68Kfw6Ib0EAD)

## 使用説明
1. ノードの使用説明については、以下を参照してください：[ノードの使用方法](how_to_use_nodes.md)

2. プラグインに問題がある場合や他に疑問がある場合は、ぜひQQ群にご参加ください：[931057213](img/Q群.jpg)
3. ワークフローのチュートリアルについては、[ワークフローのチュートリアル](workflow_tutorial/)をご参照ください。貢献してくださった[HuangYuChuh](https://github.com/HuangYuChuh)に感謝いたします。

4. 高度なワークフローのアカウント：[openart](https://openart.ai/workflows/profile/comfyui_llm_party?sort=latest&tab=creation)

4. さらに多くのワークフローは[workflow](workflow)フォルダーをご覧ください。

## 動画チュートリアル
1. [手取り足取り、ブロック型エージェントの構築方法を教えます（超簡単！）](https://www.bilibili.com/video/BV1JZ421v7Tw/?vd_source=f229e378448918b84afab7c430c6a75b)

2. [GPT-4oをcomfyuiに接続する方法 | ワークフローが別のワークフローを呼び出す | LLMをツールにする](https://www.bilibili.com/video/BV1JJ4m1A789/?spm_id_from=333.999.0.0&vd_source=f229e378448918b84afab7c430c6a75b)

3. [あなたのワークフローをGPTに偽装し、WeChatに接続 | Omost互換！自分のdalle3を柔軟に創造する](https://www.bilibili.com/video/BV1DT421a7KY/?spm_id_from=333.999.0.0)

4. [comfyuiでインタラクティブノベルゲームを楽しむ方法](https://www.bilibili.com/video/BV15y411q78L/?spm_id_from=333.999.0.0&vd_source=f229e378448918b84afab7c430c6a75b)

5. [AI彼女、そしてあなたの形 | comfyui上でgraphRAGを実現し、neoa4jと連携 | comfyuiワークフローをstreamlitフロントエンドに接続する](https://www.bilibili.com/video/BV1dS421R7Au/?spm_id_from=333.999.0.0&vd_source=f229e378448918b84afab7c430c6a75b)
## モデルサポート
1. 画像内のテキストと位置を認識するためのEasyOCRノードを追加しました。対応するマスクを生成し、LLMが表示するためのJSON文字列を返すことができます。標準版とプレミアム版が選択可能です！
2. すべてのOpenAI形式のAPI呼び出しをサポートしています（[oneapi](https://github.com/songquanpeng/one-api)を組み合わせることで、ほぼすべてのLLM APIを呼び出すことができ、中継APIもサポートしています）。base_urlの選択は[config.ini.example](config.ini.example)を参考にしてください。現在、テスト済みのものは以下の通りです：
* [openai](https://platform.openai.com/docs/api-reference/chat/create)（すべてのOpenAIモデルに完全に対応しており、4oおよびo1シリーズを含みます！）
* [ollama](https://github.com/ollama/ollama)（おすすめ！ローカルで呼び出す場合は、ollama方式を使用してローカルモデルをホストすることを強くお勧めします！）
* [llama.cpp](https://github.com/ggerganov/llama.cpp?tab=readme-ov-file#web-server)（おすすめ！ローカルgguf形式のモデルを使用したい場合は、llama.cppプロジェクトのAPIを使用してこのプロジェクトにアクセスできます！）
* [通義千问/qwen](https://help.aliyun.com/zh/dashscope/developer-reference/compatibility-of-openai-with-dashscope/?spm=a2c4g.11186623.0.0.7b576019xkArPq)
* [智谱清言/glm](https://open.bigmodel.cn/dev/api#http_auth)
* [deepseek](https://platform.deepseek.com/api-docs/zh-cn/)
* [kimi/moonshot](https://platform.moonshot.cn/docs/api/chat#%E5%9F%BA%E6%9C%AC%E4%BF%A1%E6%81%AF)
* [豆包](https://www.volcengine.com/docs/82379/1263482)

2. Gemini形式のAPI呼び出しをサポートしています：
* [Gemini](https://aistudio.google.com/app/prompts/new_chat)
3. transformerライブラリのAutoModelForCausalLMクラスがサポートするほとんどのローカルモデルと互換性があります（ローカルモデルノードでmodel typeがわからない場合はllamaを選択すると高確率で適合します）。現在テスト済みのモデルは以下の通りです：
* [ClosedCharacter/Peach-9B-8k-Roleplay](https://huggingface.co/ClosedCharacter/Peach-9B-8k-Roleplay)(推奨！ロールプレイモデル)
* [omost-llama-3-8b-4bits](https://huggingface.co/lllyasviel/omost-llama-3-8b-4bits)(推奨！豊富なプロンプトモデル)
* [meta-llama/Llama-2-7b-chat-hf](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)
* [Qwen/Qwen2-7B-Instruct](https://huggingface.co/Qwen/Qwen2-7B-Instruct)
* [xtuner/llava-llama-3-8b-v1_1-gguf](https://huggingface.co/xtuner/llava-llama-3-8b-v1_1-gguf)（開発者はすべてのgguf形式の大規模モデルの呼び出しを維持できないため、llama.cpp方式を使用してgguf形式のローカルモデルを呼び出すことをお勧めします！）
* [THUDM/chatglm3-6b](https://huggingface.co/THUDM/chatglm3-6b)（GLM4の新しい呼び出し形式のため、開発者はすべてのローカル大規模モデルの呼び出しを維持できないため、ollama方式を使用してローカル呼び出しを行うことをお勧めします！）

4. モデルのダウンロード：
* [百度云アドレス](https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu)、抽出コード：qyhu

## ダウンロード
以下のいずれかの方法でインストールしてください。
### 方法1：
1. [comfyuiマネージャー](https://github.com/ltdrdata/ComfyUI-Manager)で`comfyui_LLM_party`を検索し、一回のクリックでインストールします。
2. comfyuiを再起動します。
### 方法二：
1. ComfyUIのルートフォルダー内の`custom_nodes`サブフォルダーに移動します。
2. このリポジトリをクローンします。`git clone https://github.com/heshengtao/comfyui_LLM_party.git`

### 方法三：
1. 右上の`CODE`をクリックします。
2. `download zip`をクリックします。
3. ダウンロードした圧縮ファイルをComfyUIのルートフォルダー内の`custom_nodes`サブフォルダーに解凍します。

## 環境デプロイ
1. `comfyui_LLM_party`のプロジェクトフォルダーに移動します。
2. ターミナルで`pip install -r requirements.txt`を入力し、本プロジェクトに必要なサードパーティライブラリをcomfyuiの環境にデプロイします。comfyuiの環境でインストールしているかどうかに注意し、ターミナルの`pip`エラーにも留意してください。
3. comfyuiランチャーを使用している場合は、ターミナルに`ランチャー設定のパス\python_embeded\python.exe -m pip install -r requirements.txt`を入力してインストールを行ってください。`python_embeded`フォルダーは通常`ComfyUI`フォルダーと同じ階層にあります。
4. 環境設定に関する問題が発生した場合は、`requirements_fixed.txt`内の依存関係を使用することを検討してください。
## 設定
* `config.ini`において言語を設定できます。現在は中国語（zh_CN）と英語（en_US）の2種類があり、デフォルトはシステム言語です。
* 以下のいずれかの方法でAPIKEYを設定できます。
### 方法一：
1. `comfyui_LLM_party`のプロジェクトフォルダ内の`config.ini`ファイルを開きます。
2. `config.ini`にあなたの`openai_api_key`、`base_url`を入力します。
3. ollamaモデルを使用する場合は、`base_url`に`http://127.0.0.1:11434/v1/`を入力し、`openai_api_key`に`ollama`を、`model_name`にはあなたのモデル名（例：llama3）を入力します。
4. Google検索またはBing検索ツールを使用する場合は、`config.ini`にあなたの`google_api_key`、`cse_id`または`bing_api_key`を入力します。
5. 画像入力LLMを使用する場合は、画像ホスティングサービスのimgbbを推奨し、`config.ini`にあなたの`imgbb_api`を入力します。
6. 各モデルは`config.ini`ファイル内で個別に設定でき、`config.ini.example`ファイルを参考に記入できます。設定が完了したら、ノードに`model_name`を入力するだけで済みます。

### 方法二：
1. comfyuiインターフェースを開きます。
2. 大規模言語モデル（LLM）ノードを新規作成し、ノード内に直接あなたの`openai_api_key`、`base_url`を入力します。
3. ollamaモデルを使用する場合は、LLM_apiノードを使用し、ノードの`base_url`に`http://127.0.0.1:11434/v1/`を入力し、`api_key`に`ollama`を、`model_name`にはあなたのモデル名（例：llama3）を入力します。
4. 画像入力LLMを使用する場合は、画像ホスティングサービスのimgbbを推奨し、ノードにあなたの`imgbb_api_key`を入力します。
## 更新ログ
1. comfyuiのインターフェースで右クリックし、右クリックメニューの`llm`を選択すると、本プロジェクトのノードを見つけることができます。[ノードの使い方](how_to_use_nodes_ZH.md)
2. API接続またはローカル大モデル接続をサポートします。モジュール化されたツール呼び出し機能を実現しています。base_urlを入力する際は、`/v1/`で終わるURLを入力してください。[ollama](https://github.com/ollama/ollama)を使用してモデルを管理し、base_urlに`http://127.0.0.1:11434/v1/`を入力し、api_keyにollamaを、model_nameにモデル名を入力してください。例: llama3。
- API接続のワークフロー例：[start_with_LLM_api](workflow/start_with_LLM_api.json)
- ローカルモデル接続のワークフロー例：[start_with_LLM_local](workflow/start_with_LLM_local.json)
- ollama接続のワークフロー例：[ollama](workflow/ollama.json)
3. ローカル知識ベース接続をサポートし、RAGを実現しています。ワークフロー例：[知識ベースRAG検索.json](workflow/知识库RAG搜索.json)
4. コードインタープリターを呼び出すことができます。
5. インターネット検索が可能で、Google検索をサポートしています。ワークフロー例：[映画検索ワークフロー](workflow/电影查询工作流.json)
6. comfyuiで条件文を実現でき、ユーザーからの質問を分類した後に特定の応答ができます。ワークフロー例：[スマートカスタマーサービス](workflow/智能客服.json)
7. 大モデルのループリンクをサポートし、2つの大モデルによる討論会を実現できます。ワークフロー例：[電車のジレンマ討論会](workflow/电车难题辩论赛.json)
8. 任意の人格マスクを接続でき、プロンプトテンプレートをカスタマイズできます。
9. 様々なツール呼び出しをサポートし、現在、天気確認、時間確認、知識ベース、コード実行、インターネット検索、単一のウェブページ検索などの機能を開発しています。
10. LLMをツールノードとして使用することができます。ワークフロー例：[LLM入れ子](workflow/LLM套娃.json)
11. API+streamlitを使用して、自分のWebアプリケーションを迅速に開発することができます。
12. 危険な万能インタープリターノードが新たに追加され、大モデルにあらゆることをさせることができます。
13. 右クリックメニューの関数（function）サブディレクトリ内の表示テキスト（show_text）ノードをLLMノードの出力表示として使用することをお勧めします。
14. GPT-4Oの視覚機能をサポートしました！サンプルワークフロー：[GPT-4o](workflow/GPT-4o.json)  
15. 他のワークフローを呼び出すことができるワークフロートランスファーを追加しました！サンプルワークフロー：[別のワークフローを呼び出す](workflow/调用另一个工作流.json)  
16. openaiインターフェースに類似したすべてのモデルに対応しました。例：通義千問/qwen、智谱清言/GLM、deepseek、kimi/moonshot。これらのモデルのbase_url、api_key、model_nameをLLMノードに入力して呼び出してください。  
17. LVMローダーを新たに追加し、ローカルでLVMモデルを呼び出すことができるようになりました。[llava-llama-3-8b-v1_1-gguf](https://huggingface.co/xtuner/llava-llama-3-8b-v1_1-gguf)モデルをサポートしており、他のLVMモデルもGGUF形式であれば理論上は動作するはずです。サンプルワークフローはこちら: [start_with_LVM.json](workflow/start_with_LVM.json).  
18. `fastapi.py`ファイルを作成しました。このファイルを直接実行すれば、`http://127.0.0.1:8817/v1/`においてopenaiインターフェースを取得でき、GPTを呼び出すことができるアプリケーションがあなたのcomfyuiワークフローを呼び出すことが可能です！具体的な操作方法については、チュートリアルを作成してご紹介いたします~  
19. LLMローダーとLLMチェーンを分け、モデルの読み込みと設定を分離しました。これにより、異なるLLMノード間でモデルを共有できるようになりました！  
20. 現在、macOSおよびmpsデバイスをサポートしています！[bigcat88](https://github.com/bigcat88)の貢献に感謝いたします！  
21. ユーザーの選択に基づいて異なる結末に進むインタラクティブな小説ゲームを構築できるようになりました！サンプルワークフローの参考：[インタラクティブ小説](workflow/互动小说.json)  
22. openaiのwhisperおよびtts機能に対応し、音声入力と出力を実現しました。サンプルワークフローの参考：[音声入力+音声出力](workflow/语音输入+语音输出.json)  
23. [Omost](https://github.com/lllyasviel/Omost)に対応しました！！！ぜひ[omost-llama-3-8b-4bits](https://huggingface.co/lllyasviel/omost-llama-3-8b-4bits)をダウンロードして、今すぐ体験してください！サンプルワークフローはこちら：[start_with_OMOST](workflow/start_with_OMOST.json)をご参照ください。
24. 企業微信、钉钉、飛書にメッセージを送信するLLMツールと、呼び出し可能な外部関数を追加しました。
25. テキストイテレータを新たに追加しました。これは、各回ごとに一部分の文字だけを出力し、改行記号とチャンクサイズに基づいてテキストを安全に分割します。テキストの途中で分割することはありません。chunk_overlapは、分割されたテキストの重複文字数を示します。これにより、超長テキストを一括入力でき、無心でクリックするか、comfyuiのループ実行を開始するだけで、自動的に完了します。is_locked属性を有効にすると、入力終了時にワークフローが自動的にロックされ、実行が続行されなくなります。サンプルワークフロー：[テキストイテレータ入力](workflow/文本迭代输入.json)をご覧ください。
26. ローカルLLMローダーおよびローカルllavaローダーにmodel name属性を追加しました。空の場合は、ノード内の各種ローカルパスを使用してロードします。空でない場合は、`config.ini`に自分で記入したパスパラメータを使用してロードします。空でなく、`config.ini`に存在しない場合は、huggingfaceからダウンロードするか、huggingfaceのモデル保存ディレクトリからロードします。huggingfaceからダウンロードしたい場合は、例えば`THUDM/glm-4-9b-chat`の形式でmodel name属性を記入してください。注意！この方法でロードされるモデルは、transformerライブラリに適合している必要があります。
27. JSONファイル解析ノードとJSON値取得ノードを追加しました。これにより、ファイルまたはテキストから特定のキーの値を取得できるようになります。[guobalove](https://github.com/guobalove)の貢献に感謝します！
28. ツール呼び出しのコードを改善しました。これにより、ツール呼び出し機能を持たないLLMでもis_tools_in_sys_prompt属性を有効にできるようになりました（ローカルLLMはデフォルトで有効にする必要がなく、自動的に適応します）。有効にすると、ツール情報がシステムプロンプトに追加され、LLMはツールを呼び出すことができるようになります。実現原理に関する論文：[Achieving Tool Calling Functionality in LLMs Using Only Prompt Engineering Without Fine-Tuning](https://arxiv.org/abs/2407.04997)

29. カスタムツールのコードを保存するためのcustom_toolフォルダーを新設しました。custom_toolフォルダー内のコードを参考にして、カスタムツールのコードをcustom_toolフォルダーに配置することで、LLM内でカスタムツールを呼び出すことができます。

30. 知識グラフツールを新たに追加し、LLMと知識グラフが完璧に相互作用できるようになりました。LLMはあなたの入力に基づいて知識グラフを修正でき、知識グラフ上で推論を行い、必要な答えを得ることができます。サンプルワークフローの参考：[graphRAG_neo4j](workflow/graphRAG_neo4j.json)

31. パーソナリティAI機能を追加し、0コードで自分の彼女AIまたは彼氏AIを開発できます。無限の対話、永続的な記憶、キャラクター設定の安定性があります。サンプルワークフローの参考：[麦洛薇人格AI](workflow/麦洛薇人格AI.json)

32. このLLMツール製造機を使用してLLMツールを自動生成できます。生成したツールコードをPythonファイルとして保存し、そのコードをcustom_toolフォルダーにコピーすることで、新しいノードを創造したことになります。サンプルワークフロー：[LLM工具生成器](workflow/LLM工具制造机.json)。

33. duckduckgo検索をサポートしましたが、大きな制限があります。どうやら英語のキーワードしか入力できず、キーワードに複数の概念を含めることはできません。ただし、APIキーの制限がないという利点があります。

34. 複数の知識ベースを分けて呼び出す機能をサポートし、プロンプト内でどの知識ベースの知識を使用して質問に回答するかを明確に示すことができます。サンプルワークフロー：[多知识库分别调用](workflow/多知识库分别调用.json)。

35. LLMに追加のパラメータを入力することをサポートし、json outなどの高度なパラメータを含めることができます。サンプルワークフロー：[LLM入力额外参数](workflow/LLM额外参数eg_JSON_OUT.json)。[用json_out分离提示词](workflow/用json_out分离提示词.json)。
36. Discordへのエージェント接続機能を新たに追加しました。（現在テスト中です）
37. Feishuへのエージェント接続機能を新たに追加しました。特に[guobalove](https://github.com/guobalove)の貢献に感謝いたします！参考ワークフローは[飛書ロボット](workflow/飞书机器人.json)です。
38. 汎用API呼び出しノードと多数の補助ノードを新たに追加し、リクエストボディの構築とレスポンスからの情報取得を支援します。
39. モデルをクリアするノードを新たに追加し、任意の位置でLLMをメモリからアンロードできます！
40. [chatTTS](https://github.com/2noise/ChatTTS)ノードを追加しました。特に[guobalove](https://github.com/guobalove)の貢献に感謝いたします！`model_path`パラメータは空にすることができます！HFモードでモデルをロードすることをお勧めします。モデルは自動的にHugging Faceからダウンロードされ、手動でのダウンロードは不要です。ローカルでロードする場合は、モデルの`asset`と`config`フォルダーをルートディレクトリに置いてください。[百度云地址](https://pan.baidu.com/share/init?surl=T4aEB4HumdJ7iVbvsv1vzA&pwd=qyhu)、抽出コード：qyhu；`custom`モードでロードする場合は、モデルの`asset`と`config`フォルダーを`model_path`下に置いてください。
## 次のステップ計画：
1. さらなるモデルの適応を進め、少なくとも主流の大規模モデルAPIインターフェースおよび主流のオープンソースモデルのローカル呼び出しをカバーし、さらに多くのLVMモデルの適応を行います。現時点では、GPT-4の視覚機能の呼び出しのみを適応しました。
2. さらなるインテリジェントエージェントの構築方法を模索しています。現在、この分野での取り組みとして、LLMを別のLLMにツールとして導入し、放射状にLLMワークフローを構築し、一つのワークフローを別のワークフローのノードとして導入することに成功しました。今後、さらにクールな機能を実現する予定です。
3. より多くの自動化機能を導入する予定です。将来的には、画像、テキスト、動画、音声を他のアプリケーションに自動的に送信するノードを追加し、主流のソーシャルメディアやフォーラムに自動返信する機能を持つリスニングノードも提供する予定です。
4. より多くの知識ベース管理機能を実装します。現在、本プロジェクトはローカルファイル検索とウェブ検索をサポートしていますが、今後は知識グラフ検索や長期記憶検索を導入し、インテリジェントエージェントが論理的に専門知識を考え、ユーザーとの対話の際に特定の重要情報を永続的に記憶できる機能を提供します。
5. より多くのツールと多様な人格マスクを開発します。この分野は最も容易に実現できる部分ですが、同時に最も蓄積が必要な部分でもあります。将来的には、このプロジェクトがcomfyuiのように多くのカスタマイズノードを持つことを目指し、多くのツールと人格マスクを揃えられることを期待しています。

## 免責事項：
本オープンソースプロジェクトおよびその内容（以下「プロジェクト」といいます）は、参考用に提供されるものであり、明示または暗示の保証を意味するものではありません。プロジェクトの貢献者は、プロジェクトの完全性、正確性、信頼性または適用性に対して一切の責任を負いません。プロジェクトの内容に依存する行為は、すべて自己の責任において行うものとします。いかなる場合においても、プロジェクトの貢献者は、プロジェクトの内容の使用に起因して生じた間接的、特別または付随的な損失または損害について、一切の責任を負いません。
## 特別な感謝
<a href="https://github.com/bigcat88">
  <img src="https://avatars.githubusercontent.com/u/13381981?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://github.com/guobalove">
  <img src="https://avatars.githubusercontent.com/u/171540731?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://github.com/HuangYuChuh">
  <img src="https://avatars.githubusercontent.com/u/167663109?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>

## 参考文献
本プロジェクトのいくつかのノードは以下のプロジェクトを参考にしており、オープンソースコミュニティへの貢献に感謝します！
1. [pythongosssss/ComfyUI-Custom-Scripts](https://github.com/pythongosssss/ComfyUI-Custom-Scripts)
2. [lllyasviel/Omost](https://github.com/lllyasviel/Omost)

## サポート：

### コミュニティに参加
プラグインに問題がある場合や他の質問がある場合は、ぜひ私たちのコミュニティに参加してください。

1. QQグループ：`931057213`
<div style="display: flex; justify-content: center;">
    <img src="img/Q群.jpg" style="width: 48%;" />
</div>

2. WeChatグループ：`Choo-Yong`（小助手のWeChatを追加した後にグループに参加してください）

3. discord:[discordリンク](https://discord.gg/gxrQAYy6)

### 私たちをフォローする
1. このプロジェクトの最新機能を継続的にフォローしたい方は、Bilibiliアカウントをフォローしてください：[派对主持BB机](https://space.bilibili.com/26978344)
2. OpenArtアカウントは、最も便利なパーティーのワークフローを継続的に更新しています：[openart](https://openart.ai/workflows/profile/comfyui_llm_party?sort=latest&tab=creation)

### 寄付のサポート
私の仕事があなたに価値をもたらしたなら、ぜひ私にコーヒーをおごってください！あなたのサポートはプロジェクトに活力を与えるだけでなく、クリエイターの心を温めます。☕💖 一杯一杯が意義深いです！
<div style="display:flex; justify-content:space-between;">
    <img src="img/zhifubao.jpg" style="width: 48%;" />
    <img src="img/wechat.jpg" style="width: 48%;" />
</div>

## スター履歴

[![Star History Chart](https://api.star-history.com/svg?repos=heshengtao/comfyui_LLM_party&type=Date)](https://star-history.com/#heshengtao/comfyui_LLM_party&Date)
