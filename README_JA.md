![画像](img/封面.png)

<div align="center">
  <a href="https://space.bilibili.com/26978344">bilibili</a> ·
  <a href="https://www.youtube.com/@comfyui-LLM-party">youtube</a> ·
  <a href="https://github.com/heshengtao/Let-LLM-party">テキストチュートリアル</a> ·
  <a href="https://pan.quark.cn/s/190b41f3bbdb">クラウドディスクのアドレス</a> ·
  <a href="img/Q群.jpg">QQグループ</a> ·
  <a href="https://discord.gg/f2dsAKKr2V">ディスコード</a> ·
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

## クイックスタート
0. もしあなたがcomfyuiを使用したことがなく、comfyuiでLLMパーティをインストールする際に依存関係の問題が発生した場合は、[こちらをクリック](https://drive.google.com/file/d/1T9C7gEbd-w_zf9GqZO1VeI3z8ek8clpX/view?usp=sharing)して、LLMパーティを含むcomfyui **windows** ポータブルパッケージをダウンロードしてください。ご注意ください！このポータブルパッケージにはpartyと管理者の2つのプラグインのみが含まれており、windowsシステム専用となっています。（既にcomfyuiがインストールされている場合、LLM partyのインストール手順は省略できます。）
1. 以下のワークフローをcomfyuiにドラッグし、[comfyui-Manager](https://github.com/ltdrdata/ComfyUI-Manager)を使用して不足しているノードをインストールします。
  - APIを使用してLLMを呼び出す：[start_with_LLM_api](workflow/start_with_LLM_api.json)
  - aisuiteを使用してLLMを呼び出します：[start_with_aisuite](workflow/start_with_aisuite.json)
  - ollamaを使用してローカルLLMを管理する：[start_with_Ollama](workflow/ollama.json)
  - 分散形式のローカルLLMを使用する：[start_with_LLM_local](workflow/start_with_LLM_local.json)
  - GGUF形式のローカルLLMを使用する：[start_with_LLM_GGUF](workflow/start_with_GGUF.json)
  - 分散形式のローカルVLMを使用する：[start_with_VLM_local](workflow/start_with_VLM_local.json)（現在は[Llama-3.2-Vision](https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct)/[Qwen/Qwen2.5-VL](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct)/[deepseek-ai/Janus-Pro](https://huggingface.co/deepseek-ai/Janus-Pro-1B)をサポートしています。   ）
  - GGUF形式のローカルVLMを使用する：[start_with_VLM_GGUF](workflow/start_with_llava.json)
  - APIを使用してLLMにSDプロンプトを生成させ、画像を生成する：[start_with_VLM_API_for_SD](workflow/start_with_VLM_API_for_SD.json)
  - ollamaを使用してminicpmにSDプロンプトを生成させ、画像を生成する：[start_with_ollama_minicpm_for_SD](workflow/start_with_ollama_minicpm_for_SD.json)
  - ローカルのqwen-vlを使用してSDプロンプトを生成させ、画像を生成する：[start_with_qwen_vl_local_for_SD](workflow/start_with_qwen_vl_local_for_SD.json) 
2. APIを使用する場合、API LLMローダーノードに`base_url`（リレーAPIでも可、末尾は`/v1/`であることを確認）と`api_key`を入力します。例：`https://api.openai.com/v1/`
3. ollamaを使用する場合、API LLMローダーノードで`is_ollama`オプションをオンにし、`base_url`と`api_key`を入力する必要はありません。
4. ローカルモデルを使用する場合、ローカルモデルローダーノードにモデルパスを入力します。例：`E:\model\Llama-3.2-1B-Instruct`。また、ローカルモデルローダーノードにHuggingfaceのモデルrepo idを入力することもできます。例：`lllyasviel/omost-llama-3-8b-4bits`
5. このプロジェクトは使用の敷居が高いため、クイックスタートを選択した場合でも、プロジェクトのホームページをじっくり読んでいただけると幸いです。

## 最新の更新
1. LLM APIノードはストリーミング出力モードをサポートするようになり、コントロールパネルでAPIが返すテキストをリアルタイムでストリーム表示することが可能になりました。これにより、リクエストが完了するのを待つ必要なく、APIの出力を即座に確認できます。
2. LLM APIノードにreasoning_content出力が追加され、R1モデルのreasoningとresponseを自動的に分離することができます。
3. only_apiというリポジトリのブランチが新たに追加され、このブランチにはAPI呼び出しの部分のみが含まれており、API呼び出しのみを必要とするユーザーに便利です。`comfyui`の`custom tool`フォルダで、次のコマンドを使用して`git clone -b only_api https://github.com/heshengtao/comfyui_LLM_party.git`を実行してください。そして、本プロジェクトのホームページに従って環境を構築すれば、このブランチを使用できます。注意！`custom tool`フォルダ内に`comfyui_LLM_party`という名前の他のフォルダが存在しないことを確認する必要があります。
1. VLMローカルロードノードはすでに[deepseek-ai/Janus-Pro](https://huggingface.co/deepseek-ai/Janus-Pro-1B)をサポートしています。サンプルワークフロー：[Janus-Pro](workflow/deepseek-janus-pro.json)  
1. VLMローカルローダーノードは既に[Qwen/Qwen2.5-VL-3B-Instruct](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct)をサポートしていますが、transformerを最新バージョンに更新する必要があります（```pip install -U transformers```）。サンプルワークフロー：[qwen-vl](workflow/qwen-vl.json)  
1. 新しい画像ホスティングノードが追加されました。現在、https://sm.ms の画像ホスティング（中国のドメインは https://smms.app）および https://imgbb.com の画像ホスティングをサポートしています。将来的には、より多くの画像ホスティングをサポートする予定です。サンプルワークフロー：[画像ホスティング](workflow/图床.json)
1. ~~partyがデフォルトで互換性のあるimgbbの画像ホスティングは[imgbb](https://imgbb.io)というドメインに更新されましたが、以前の画像ホスティングは中国本土のユーザーに対してあまり親切ではなかったため、変更されました。~~ 大変申し訳ございませんが、 https://imgbb.io の画像ホスティングAPIサービスは停止しているようですので、コードは元の https://imgbb.com にロールバックされました。皆様のご理解に感謝いたします。今後、より多くの画像ホスティングをサポートするノードを更新する予定です。 
1. 更新された[MCP](https://modelcontextprotocol.io/introduction)ツールでは、partyプロジェクトフォルダ内の'[mcp_config.json](mcp_config.json)'ファイルの設定を変更することで、接続するMCPサーバーを調整できます。さまざまなMCPサーバーの設定パラメーターは、こちらでご確認いただけます：[modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)。本プロジェクトでは、デフォルト設定としてEverythingサーバーが用意されており、MCPサーバーが正常に機能するかのテストに使用されます。ワークフローの参照：[start_with_MCP](workflow/start_with_MCP.json)。開発者向けの注意：MCPツールノードは、設定済みのMCPサーバーに接続でき、その後サーバー内のtoolsをLLMが直接使用可能なツールに変換します。異なるローカルサーバーやクラウドサーバーを設定することで、世界中のすべてのLLMツールを体験することができます。

## 使用説明
1. ノードの使用説明については、以下を参照してください：[ノードの使用方法](https://github.com/heshengtao/Let-LLM-party)

2. プラグインに問題がある場合や他に疑問がある場合は、ぜひQQ群にご参加ください：[931057213](img/Q群.jpg) |discord：[discord](https://discord.gg/f2dsAKKr2V).

4. さらに多くのワークフローは[workflow](workflow)フォルダーをご覧ください。

## 動画チュートリアル
<a href="https://space.bilibili.com/26978344">
  <img src="img/B.png" width="100" height="100" style="border-radius: 80%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://www.youtube.com/@comfyui-LLM-party">
  <img src="img/YT.png" width="100" height="100" style="border-radius: 80%; overflow: hidden;" alt="octocat"/>
</a>

## モデルサポート
1. 画像内のテキストと位置を認識するためのEasyOCRノードを追加しました。対応するマスクを生成し、LLMが表示するためのJSON文字列を返すことができます。標準版とプレミアム版が選択可能です！
2. すべてのOpenAI形式のAPI呼び出しをサポートしています（[oneapi](https://github.com/songquanpeng/one-api)を組み合わせることで、ほぼすべてのLLM APIを呼び出すことができ、中継APIもサポートしています）。base_urlの選択は[config.ini.example](config.ini.example)を参考にしてください。現在、テスト済みのものは以下の通りです：
* [openai](https://platform.openai.com/docs/api-reference/chat/create)（すべてのOpenAIモデルに完全に対応しており、4oおよびo1シリーズを含みます！）
* [ollama](https://github.com/ollama/ollama)（おすすめ！ローカルで呼び出す場合は、ollama方式を使用してローカルモデルをホストすることを強くお勧めします！）
* [Azure OpenAI](https://azure.microsoft.com/zh-cn/products/ai-services/openai-service/)
* [llama.cpp](https://github.com/ggerganov/llama.cpp?tab=readme-ov-file#web-server)（おすすめ！ローカルgguf形式のモデルを使用したい場合は、llama.cppプロジェクトのAPIを使用してこのプロジェクトにアクセスできます！）
* [Grok](https://x.ai/api)
* [通義千问/qwen](https://help.aliyun.com/zh/dashscope/developer-reference/compatibility-of-openai-with-dashscope/?spm=a2c4g.11186623.0.0.7b576019xkArPq)
* [智谱清言/glm](https://open.bigmodel.cn/dev/api#http_auth)
* [deepseek](https://platform.deepseek.com/api-docs/zh-cn/)
* [kimi/moonshot](https://platform.moonshot.cn/docs/api/chat#%E5%9F%BA%E6%9C%AC%E4%BF%A1%E6%81%AF)
* [doubao](https://www.volcengine.com/docs/82379/1263482)
* [讯飞星火/spark](https://xinghuo.xfyun.cn/sparkapi?scr=price)
* [Gemini](https://developers.googleblog.com/zh-hans/gemini-is-now-accessible-from-the-openai-library/)(従来のGemini API LLM ローダーノードは新しいバージョンで廃止されましたので、LLM APIローダーノードをご利用ください。base_urlは以下を選択してください：https://generativelanguage.googleapis.com/v1beta/openai/)

2. [aisuite](https://github.com/andrewyng/aisuite)互換のすべてのAPI呼び出しをサポート：
* [anthropic/claude](https://www.anthropic.com/)  
* [aws](https://docs.aws.amazon.com/solutions/latest/generative-ai-application-builder-on-aws/api-reference.html)
* [vertex](https://cloud.google.com/vertex-ai/docs/reference/rest)
* [huggingface](https://huggingface.co/) 

3. トランスフォーマーライブラリのほとんどのローカルモデルと互換性があります（ローカルLLMモデルチェーンノードのモデルタイプは、LLM、VLM-GGUF、およびLLM-GGUFに変更され、LLMモデルの直接ロード、VLMモデルのロード、およびGGUF形式のLLMモデルのロードに対応します）。VLMまたはGGUF形式のLLMモデルでエラーが発生した場合は、[llama-cpp-python](https://github.com/abetlen/llama-cpp-python/releases)から最新バージョンのllama-cpp-pythonをダウンロードしてください。現在テストされているモデルには次のものが含まれます：
* [ClosedCharacter/Peach-9B-8k-Roleplay](https://huggingface.co/ClosedCharacter/Peach-9B-8k-Roleplay)(推奨！ロールプレイモデル)
* [lllyasviel/omost-llama-3-8b-4bits](https://huggingface.co/lllyasviel/omost-llama-3-8b-4bits)(推奨！豊富なプロンプトモデル)
* [meta-llama/Llama-2-7b-chat-hf](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)
* [Qwen/Qwen2-7B-Instruct](https://huggingface.co/Qwen/Qwen2-7B-Instruct)
* [openbmb/MiniCPM-V-2_6-gguf](https://huggingface.co/openbmb/MiniCPM-V-2_6-gguf/tree/main)
* [lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF](https://huggingface.co/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/tree/main)
* [meta-llama/Llama-3.2-11B-Vision-Instruct](https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct)
* [Qwen/Qwen2.5-VL-3B-Instruct](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct)
* [deepseek-ai/Janus-Pro](https://huggingface.co/deepseek-ai/Janus-Pro-1B)

4. モデルのダウンロード：
* [クォーククラウドアドレス](https://pan.quark.cn/s/190b41f3bbdb)
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
* `config.ini`に言語を設定することが可能です。現在は中国語（zh_CN）と英語（en_US）の2種類のみがサポートされています。デフォルトはお使いのシステム言語です。
* `config.ini`に迅速インストールの設定が可能です。`fast_installed`のデフォルトは`False`であり、GGUFモデルを使用しない場合は`True`に設定できます。
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
**[Click here](change_log.md)**

## 次のステップ計画：
1. さらなるモデル適応;
2. さらなるエージェント構築方法;
3. さらなる自動化機能;
4. さらなるナレッジベース管理機能;
5. さらなるツール、さらなるペルソナ。

## 免責事項：
本オープンソースプロジェクトおよびその内容（以下「プロジェクト」といいます）は、参考用に提供されるものであり、明示または暗示の保証を意味するものではありません。プロジェクトの貢献者は、プロジェクトの完全性、正確性、信頼性または適用性に対して一切の責任を負いません。プロジェクトの内容に依存する行為は、すべて自己の責任において行うものとします。いかなる場合においても、プロジェクトの貢献者は、プロジェクトの内容の使用に起因して生じた間接的、特別または付随的な損失または損害について、一切の責任を負いません。
## 特別な感謝
<a href="https://github.com/bigcat88">
  <img src="https://avatars.githubusercontent.com/u/13381981?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://github.com/guobalove">
  <img src="https://avatars.githubusercontent.com/u/171540731?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
</a>
<a href="https://github.com/SpenserCai">
  <img src="https://avatars.githubusercontent.com/u/25168945?v=4" width="50" height="50" style="border-radius: 50%; overflow: hidden;" alt="octocat"/>
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

2. WeChatグループ：`we_glm`（小助手のWeChatを追加した後にグループに参加してください）

3. discord:[discordリンク](https://discord.gg/f2dsAKKr2V)

### 私たちをフォローする
1. このプロジェクトの最新機能を継続的にフォローしたい方は、Bilibiliアカウントをフォローしてください：[派酱](https://space.bilibili.com/26978344)
2. [youtube@comfyui-LLM-party](https://www.youtube.com/@comfyui-LLM-party)

### 寄付のサポート
私の仕事があなたに価値をもたらしたなら、ぜひ私にコーヒーをおごってください！あなたのサポートはプロジェクトに活力を与えるだけでなく、クリエイターの心を温めます。☕💖 一杯一杯が意義深いです！
<div style="display:flex; justify-content:space-between;">
    <img src="img/zhifubao.jpg" style="width: 48%;" />
    <img src="img/wechat.jpg" style="width: 48%;" />
</div>

## スター履歴

[![Star History Chart](https://api.star-history.com/svg?repos=heshengtao/comfyui_LLM_party&type=Date)](https://star-history.com/#heshengtao/comfyui_LLM_party&Date)
