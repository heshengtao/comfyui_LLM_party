import configparser
import io
import json
import locale
import os
import requests
from PIL import Image
import numpy as np
import openai
import base64
from langchain_text_splitters import RecursiveCharacterTextSplitter
# 当前脚本目录的上级目录
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir, "config.ini")

class AnyType(str):
    """A special class that is always equal in not equal comparisons. Credit to pythongosssss"""

    def __ne__(self, __value: object) -> bool:
        return False


any_type = AnyType("*")
def load_api_keys(config_file):
    config = configparser.ConfigParser()
    config.read(config_file, encoding="utf-8")

    api_keys = {}
    if "API_KEYS" in config:
        api_keys = config["API_KEYS"]

    return api_keys


class mini_party:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_str": ("STRING", {"forceInput": True}),
                "prompt": ("STRING", {"default": "input function here","multiline": True}),
                "model_name": ("STRING", {"default": "gpt-4o-mini",}),
            },
            "optional": {
                "base_url": (
                    "STRING",
                    {
                        "default": "https://api.openai.com/v1/",
                    },
                ),
                "api_key": (
                    "STRING",
                    {
                        "default": "sk-XXXXX",
                    },
                ),
                "is_enable": ("BOOLEAN", {"default": True,}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_str",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/迷你派对（mini-party）"

    def file(
        self,
        input_str,
        prompt,
        model_name,
        base_url=None,
        api_key=None,
        is_enable=True,
    ):
        if not is_enable:
            return (None,)
        api_keys = load_api_keys(config_path)
        if api_key:
            openai.api_key = api_key
        elif api_keys.get("openai_api_key"):
            openai.api_key = api_keys.get("openai_api_key")
        else:
            openai.api_key = os.environ.get("OPENAI_API_KEY")

        if base_url:
            openai.base_url = base_url.rstrip("/") + "/"
        elif api_keys.get("base_url"):
            openai.base_url = api_keys.get("base_url")
        else:
            openai.base_url = os.environ.get("OPENAI_API_BASE")

        if not openai.api_key:
            return ("请输入API_KEY",)
        history= [
            {"role": "system", "content": prompt},
            {"role": "user", "content": input_str}
        ]
        response = openai.chat.completions.create(
                            model=model_name,
                            messages=history,
                        )
        output = response.choices[0].message.content
        return (output,)
    

class mini_translate:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_str": ("STRING", {"forceInput": True}),
                "target_language": ("STRING", {"default": "English"}),
                "tone": ("STRING", {"default": "正式"}),
                "degree": ("INT", {"default": 5, " min": 0, "max": 10}),
                "model_name": ("STRING", {"default": "gpt-4o-mini",}),
            },
            "optional": {
                "base_url": (
                    "STRING",
                    {
                        "default": "https://api.openai.com/v1/",
                    },
                ),
                "api_key": (
                    "STRING",
                    {
                        "default": "sk-XXXXX",
                    },
                ),
                "is_enable": ("BOOLEAN", {"default": True,}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_str",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/迷你派对（mini-party）"

    def file(
        self,
        input_str,
        target_language, 
        degree=5, 
        tone="正式",
        model_name="gpt-4o-mini",
        base_url=None,
        api_key=None,
        is_enable=True,
    ):
        if not is_enable:
            return (None,)
        api_keys = load_api_keys(config_path)
        if api_key:
            openai.api_key = api_key
        elif api_keys.get("openai_api_key"):
            openai.api_key = api_keys.get("openai_api_key")
        else:
            openai.api_key = os.environ.get("OPENAI_API_KEY")

        if base_url:
            openai.base_url = base_url.rstrip("/") + "/"
        elif api_keys.get("base_url"):
            openai.base_url = api_keys.get("base_url")
        else:
            openai.base_url = os.environ.get("OPENAI_API_BASE")

        if not openai.api_key:
            return ("请输入API_KEY",)
        sys_prompt = f"""你是一个翻译专家，请将我的输入翻译成{target_language}，语气为{tone}，语气程度为{str(degree)}。
语气程度最大为10，最小为0，数字越大语气越{tone}。当语气程度为0时，几乎不改变原文的语气，当语气程度为10时，语气会非常{tone}。
即使我的输入的语言和{target_language}相同，也请注意语气的调整，而不是返回原内容。
翻译时不要复述原文以及其他无关内容，直接返回翻译后的内容即可。注意！如果我输入的内容带有格式（例如markdown格式），请保留原格式。

如果是markdown格式的文字，有以下要求：
1. 请保留原格式，不要改变markdown格式。
2. 请不要改变markdown格式中的超链接中的()部分，但[]中的内容必须翻译。如果改变了()部分，可能会导致超链接失效。
3. HTML格式的文字，请保留原格式，不要改变HTML格式,其中会被显示在前端的文字需要翻译，而链接部分不能翻译。

从现在开始，请将以下内容翻译成{target_language}。
        """

        # 将file_content用RecursiveCharacterTextSplitter分割
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000, chunk_overlap=0
        )
        output=""
        for chunk in text_splitter.split_text(input_str):   
            history= [
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": chunk}
            ]
            response = openai.chat.completions.create(
                                model=model_name,
                                messages=history,
                            )
            output += response.choices[0].message.content
        return (output,)

class mini_error_correction:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_str": ("STRING", {"forceInput": True}),
                "model_name": ("STRING", {"default": "gpt-4o-mini",}),
            },
            "optional": {
                "base_url": (
                    "STRING",
                    {
                        "default": "https://api.openai.com/v1/",
                    },
                ),
                "api_key": (
                    "STRING",
                    {
                        "default": "sk-XXXXX",
                    },
                ),
                "is_enable": ("BOOLEAN", {"default": True,}),
            },
        }

    RETURN_TYPES = ("STRING","STRING","STRING",)
    RETURN_NAMES = ("input_text","output_text","error",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/迷你派对（mini-party）"

    def file(
        self,
        input_str,
        model_name="gpt-4o-mini",
        base_url=None,
        api_key=None,
        is_enable=True,
    ):
        if not is_enable:
            return (None,)
        api_keys = load_api_keys(config_path)
        if api_key:
            openai.api_key = api_key
        elif api_keys.get("openai_api_key"):
            openai.api_key = api_keys.get("openai_api_key")
        else:
            openai.api_key = os.environ.get("OPENAI_API_KEY")

        if base_url:
            openai.base_url = base_url.rstrip("/") + "/"
        elif api_keys.get("base_url"):
            openai.base_url = api_keys.get("base_url")
        else:
            openai.base_url = os.environ.get("OPENAI_API_BASE")

        if not openai.api_key:
            return ("请输入API_KEY",)
        sys_prompt = f"""你是一个文档纠错大师，你会纠正我输入的文字中的包括但不限于错别字、语法错误、病句、拼写错误等一系列文档错误，并给出修改后的内容以及错误的位置。
输出格式为json，格式如下：
{{
    "input_str": "输入的文字，用** **将错误的地方括起来",
    "output_str": "修改后的文字，保留原格式",
    "error":"你修改的部分，如果没有错误则为空字符串。如果有错误，则用无序列表的形式列出错误",
}}

示例：
{{
    "input_str": "三年中，这个县的粮食产量以平均每年递增20%的速度大踏步地**向前发展**。他主动为这个系工程力学专业的两届船舶结构力学学习班**挑起**了薄壳力学、船舶结构力学等课程的主讲任务。",
    "output_str": "三年中，这个县的粮食产量以平均每年递增20%的速度大踏步地提高。他主动为这个系工程力学专业的两届船舶结构力学学习班承担了薄壳力学、船舶结构力学等课程的主讲任务。",
    "error":"- 向前发展 -> 提高\n- 挑起 -> 承担\n",
}}

从现在开始，请对我的输入进行纠错。
        """

        # 将file_content用RecursiveCharacterTextSplitter分割
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000, chunk_overlap=0
        )
        input_text=""
        output_text=""
        error=""
        for chunk in text_splitter.split_text(input_str):   
            history= [
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": chunk}
            ]
            response = openai.chat.completions.create(
                                model=model_name,
                                messages=history,
                                response_format={"type": "json_object"},
                            )
            output = response.choices[0].message.content
            output = json.loads(output)
            input_text += output["input_str"]
            output_text += output["output_str"]
            error += output["error"]
        return (input_text,output_text,error,)


class mini_sd_prompt:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": ("STRING", {"default": "a girl","multiline": True}),
                "model_name": ("STRING", {"default": "gpt-4o-mini",}),
            },
            "optional": {
                "base_url": (
                    "STRING",
                    {
                        "default": "https://api.openai.com/v1/",
                    },
                ),
                "api_key": (
                    "STRING",
                    {
                        "default": "sk-XXXXX",
                    },
                ),
                "is_enable": ("BOOLEAN", {"default": True,}),
            },
        }

    RETURN_TYPES = ("STRING","STRING",)
    RETURN_NAMES = ("positive_prompt","negative_prompt",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/迷你派对（mini-party）"

    def file(
        self,
        prompt,
        model_name="gpt-4o-mini",
        base_url=None,
        api_key=None,
        is_enable=True,
    ):
        if not is_enable:
            return (None,)
        api_keys = load_api_keys(config_path)
        if api_key:
            openai.api_key = api_key
        elif api_keys.get("openai_api_key"):
            openai.api_key = api_keys.get("openai_api_key")
        else:
            openai.api_key = os.environ.get("OPENAI_API_KEY")

        if base_url:
            openai.base_url = base_url.rstrip("/") + "/"
        elif api_keys.get("base_url"):
            openai.base_url = api_keys.get("base_url")
        else:
            openai.base_url = os.environ.get("OPENAI_API_BASE")

        if not openai.api_key:
            return ("请输入API_KEY",)
        sys_prompt = f'''# Stable Diffusion prompt 助理

你来充当一位有艺术气息的Stable Diffusion prompt 助理。

## 任务

我用自然语言告诉你要生成的prompt的主题，你的任务是根据这个主题想象一幅完整的画面，然后转化成一份详细的、高质量的prompt，让Stable Diffusion可以生成高质量的图像。

## 背景介绍

Stable Diffusion是一款利用深度学习的文生图模型，支持通过使用 prompt 来产生新的图像，描述要包含或省略的元素。

## prompt 概念

- 完整的prompt包含“**Positive Prompt:**”和"**Negative Prompt:**"两部分。
- Positive prompt 用来描述图像，由普通常见的单词构成，使用英文半角","做为分隔符。
- negative prompt用来描述你不想在生成的图像中出现的内容。
- 以","分隔的每个单词或词组称为 tag。所以prompt和negative prompt是由系列由","分隔的tag组成的。

## () 和 [] 语法

调整关键字强度的等效方法是使用 () 和 []。 (keyword) 将tag的强度增加 1.1 倍，与 (keyword:1.1) 相同，最多可加三层。 [keyword] 将强度降低 0.9 倍，与 (keyword:0.9) 相同。

## Prompt 格式要求

你需要用以下json格式输出：
{{
"positive":"",
"negative":""
}}

下面我将说明 prompt 的生成步骤，这里的 prompt 可用于描述人物、风景、物体或抽象数字艺术图画。你可以根据需要添加合理的、但不少于5处的画面细节。

### 1. positive prompt 要求

- 你输出的 Stable Diffusion prompt 放入json字典的"positive"对应的值中。
- Positive prompt 内容包含画面主体、材质、附加细节、图像质量、艺术风格、色彩色调、灯光等部分，但你输出的 prompt 不能分段，例如类似"medium:"这样的分段描述是不需要的，也不能包含":"和"."。
- 画面主体：不简短的英文描述画面主体, 如 A girl in a garden，主体细节概括（主体可以是人、事、物、景）画面核心内容。这部分根据我每次给你的主题来生成。你可以添加更多主题相关的合理的细节。
- 对于人物主题，你必须描述人物的眼睛、鼻子、嘴唇，例如'beautiful detailed eyes,beautiful detailed lips,extremely detailed eyes and face,longeyelashes'，以免Stable Diffusion随机生成变形的面部五官，这点非常重要。你还可以描述人物的外表、情绪、衣服、姿势、视角、动作、背景等。人物属性中，1girl表示一个女孩，2girls表示两个女孩。
- 材质：用来制作艺术品的材料。 例如：插图、油画、3D 渲染和摄影。 Medium 有很强的效果，因为一个关键字就可以极大地改变风格。
- 附加细节：画面场景细节，或人物细节，描述画面细节内容，让图像看起来更充实和合理。这部分是可选的，要注意画面的整体和谐，不能与主题冲突。
- 图像质量：这部分内容开头永远要加上“(best quality,4k,8k,highres,masterpiece:1.2),ultra-detailed,(realistic,photorealistic,photo-realistic:1.37)”， 这是高质量的标志。其它常用的提高质量的tag还有，你可以根据主题的需求添加：HDR,UHD,studio lighting,ultra-fine painting,sharp focus,physically-based rendering,extreme detail description,professional,vivid colors,bokeh。
- 艺术风格：这部分描述图像的风格。加入恰当的艺术风格，能提升生成的图像效果。常用的艺术风格例如：portraits,landscape,horror,anime,sci-fi,photography,concept artists等。
- 色彩色调：颜色，通过添加颜色来控制画面的整体颜色。
- 灯光：整体画面的光线效果。

### 2. negative prompt 要求
- negative prompt部分放入json字典的"negative"对应的值中。你想要避免出现在图像中的内容都可以添加到"**Negative Prompt:**"后面。
- 任何情况下，negative prompt都要包含这段内容："nsfw,(low quality,normal quality,worst quality,jpeg artifacts),cropped,monochrome,lowres,low saturation,((watermark)),(white letters)"
- 如果是人物相关的主题，你的输出需要另加一段人物相关的 negative prompt，内容为：“skin spots,acnes,skin blemishes,age spot,mutated hands,mutated fingers,deformed,bad anatomy,disfigured,poorly drawn face,extra limb,ugly,poorly drawn hands,missing limb,floating limbs,disconnected limbs,out of focus,long neck,long body,extra fingers,fewer fingers,,(multi nipples),bad hands,signature,username,bad feet,blurry,bad body”。

### 3. 限制：
- tag 内容用英语单词或短语来描述，并不局限于我给你的单词。注意只能包含关键词或词组。
- 注意不要输出句子，不要有任何解释。
- tag数量限制40个以内，单词数量限制在60个以内。
- tag不要带引号("")。
- 使用英文半角","做分隔符。
- tag 按重要性从高到低的顺序排列。
- 我给你的主题可能是用中文描述，你给出的Positive prompt和negative prompt只用英文。
'''
        history= [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ]
        response = openai.chat.completions.create(
                            model=model_name,
                            messages=history,
                            response_format={"type": "json_object"},
                        )
        output = response.choices[0].message.content
        output = json.loads(output)
        positive_prompt= output["positive"]
        negative_prompt=output["negative"]
        return (positive_prompt,negative_prompt,)

class mini_flux_prompt:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": ("STRING", {"default": "a girl","multiline": True}),
                "model_name": ("STRING", {"default": "gpt-4o-mini",}),
            },
            "optional": {
                "base_url": (
                    "STRING",
                    {
                        "default": "https://api.openai.com/v1/",
                    },
                ),
                "api_key": (
                    "STRING",
                    {
                        "default": "sk-XXXXX",
                    },
                ),
                "is_enable": ("BOOLEAN", {"default": True,}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("flux_prompt",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/迷你派对（mini-party）"

    def file(
        self,
        prompt,
        model_name="gpt-4o-mini",
        base_url=None,
        api_key=None,
        is_enable=True,
    ):
        if not is_enable:
            return (None,)
        api_keys = load_api_keys(config_path)
        if api_key:
            openai.api_key = api_key
        elif api_keys.get("openai_api_key"):
            openai.api_key = api_keys.get("openai_api_key")
        else:
            openai.api_key = os.environ.get("OPENAI_API_KEY")

        if base_url:
            openai.base_url = base_url.rstrip("/") + "/"
        elif api_keys.get("base_url"):
            openai.base_url = api_keys.get("base_url")
        else:
            openai.base_url = os.environ.get("OPENAI_API_BASE")

        if not openai.api_key:
            return ("请输入API_KEY",)
        sys_prompt = f'''# FLUX prompt 助理

你来充当一位有艺术气息的FLUX prompt 助理。

## 任务

我用自然语言告诉你要生成的prompt的主题，你的任务是根据这个主题想象一幅完整的画面，然后生成详细的prompt，包含具体的描述、场景、情感和风格等元素，让FLUX可以生成高质量的图像。

## 背景介绍

FLUX是一款利用深度学习的文生图模型，支持通过使用 自然语言 prompt 来产生新的图像，描述要包含或省略的元素。

## Prompt 格式要求

下面我将说明 prompt 的生成步骤，这里的 prompt 可用于描述人物、风景、物体或抽象数字艺术图画。你可以根据需要添加合理的、但不少于5处的画面细节。

**示例：**

- **输入主题**：A dragon soaring above a mountain range.
  - **生成提示词**：A majestic, emerald-scaled dragon with glowing amber eyes, wings outstretched, soars through a breathtaking vista of snow-capped mountains. The dragon's powerful form dominates the scene, casting a long shadow over the imposing peaks. Below, a cascading waterfall plunges into a deep valley, its spray catching the sunlight in a dazzling array of colors. The dragon's scales shimmer with iridescent hues, reflecting the surrounding natural beauty. The sky is a vibrant blue, dotted with fluffy white clouds, creating a sense of awe and wonder. This dynamic and visually stunning depiction captures the majesty of both the dragon and the mountainous landscape.

- **输入主题**：Explain the process of making a cup of tea.
  - **生成提示词**：A detailed infographic depicting the step-by-step process of making a cup of tea. The infographic should be visually appealing with clear illustrations and concise text. It should start with a kettle filled with water and end with a steaming cup of tea, highlighting steps like heating the water, selecting tea leaves, brewing the tea, and enjoying the final product. The infographic should be designed to be informative and engaging, with a color scheme that complements the theme of tea. The text should be legible and informative, explaining each step in the process clearly and concisely.

**指导**：

1. **描述细节**：尽量提供具体的细节，如颜色、形状、位置等。
2. **情感和氛围**：描述场景的情感和氛围，如温暖、神秘、宁静等。
3. **风格和背景**：说明场景的风格和背景，如卡通风格、未来主义、复古等。

### 3. 限制：
- 我给你的主题可能是用中文描述，你给出的prompt只用英文。
- 不要解释你的prompt，直接输出prompt。
- 不要输出其他任何非prompt字符，只输出prompt，也不要包含 **生成提示词**： 等类似的字符。
'''
        history= [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ]
        response = openai.chat.completions.create(
                            model=model_name,
                            messages=history,
                        )
        flux_prompt = response.choices[0].message.content
        return (flux_prompt,)

class mini_sd_tag:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE", {}),
                "model_name": ("STRING", {"default": "gpt-4o-mini",}),
            },
            "optional": {
                "base_url": (
                    "STRING",
                    {
                        "default": "https://api.openai.com/v1/",
                    },
                ),
                "api_key": (
                    "STRING",
                    {
                        "default": "sk-XXXXX",
                    },
                ),
                "imgbb_api_key":(
                    "STRING",
                    {
                        "default": "",
                    }
                ),
                "is_enable": ("BOOLEAN", {"default": True,}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tags",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/迷你派对（mini-party）"

    def file(
        self,
        image,
        model_name="gpt-4o-mini",
        base_url=None,
        api_key=None,
        is_enable=True,
        imgbb_api_key=None,
    ):
        if not is_enable:
            return (None,)
        api_keys = load_api_keys(config_path)
        if api_key:
            openai.api_key = api_key
        elif api_keys.get("openai_api_key"):
            openai.api_key = api_keys.get("openai_api_key")
        else:
            openai.api_key = os.environ.get("OPENAI_API_KEY")

        if base_url:
            openai.base_url = base_url.rstrip("/") + "/"
        elif api_keys.get("base_url"):
            openai.base_url = api_keys.get("base_url")
        else:
            openai.base_url = os.environ.get("OPENAI_API_BASE")

        if not openai.api_key:
            return ("请输入API_KEY",)
        sys_prompt = f'''# Stable Diffusion prompt 助理

你来充当一位图片反推prompt助理。

## 任务

我会发给你一张图片，你要根据这张图片生成的prompt，你的任务是根据这张图片反推成一份详细的、高质量的prompt，可以让Stable Diffusion重现这张图片。

## 背景介绍

Stable Diffusion是一款利用深度学习的文生图模型，支持通过使用 prompt 来产生新的图像，描述要包含或省略的元素。

## prompt 概念

- 以","分隔的每个单词或词组称为 tag。所以prompt是由系列由","分隔的tag组成的。

## Prompt 格式要求

你必须尽可能的和我会发给你的图片保持一致。不多不少的描述完整张图片的所有tag。

### 示例：
a girl, beautiful detailed eyes, stars in the eyes, messy floating hair, colored inner hair, Starry sky adorns hair, depth of field


### 3. 限制：
- tag 内容用英语单词或短语来描述，并不局限于我给你的单词。注意只能包含关键词或词组。
- 注意不要输出句子，不要有任何解释。
- tag数量限制40个以内，单词数量限制在60个以内。
- tag不要带引号("")。
- 使用英文半角","做分隔符。
- tag 按重要性从高到低的顺序排列。
- 我给你的主题可能是用中文描述，你给出的prompt只用英文。
'''
        if imgbb_api_key == "" or imgbb_api_key is None:
            imgbb_api_key = api_keys.get("imgbb_api")
        if imgbb_api_key == "" or imgbb_api_key is None:
            i = 255.0 * image[0].cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            # 将图片保存到缓冲区
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            # 将图片编码为base64
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            img_json = [
                {"type": "text", "text": "请生成这张图片的prompt"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{img_str}"},
                },
            ]
        else:
            i = 255.0 * image[0].cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            # 将图片保存到缓冲区
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            # 将图片编码为base64
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            url = "https://api.imgbb.com/1/upload"
            payload = {"key": imgbb_api_key, "image": img_str}
            # 向API发送POST请求
            response = requests.post(url, data=payload)
            # 检查请求是否成功
            if response.status_code == 200:
                # 解析响应以获取图片URL
                result = response.json()
                img_url = result["data"]["url"]
                print(img_url)
            else:
                return "Error: " + response.text
            img_json = [
                {"type": "text", "text": "请生成这张图片的prompt"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": img_url,
                    },
                },
            ]
        history= [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": img_json}
        ]
        response = openai.chat.completions.create(
                            model=model_name,
                            messages=history,
                        )
        tags = response.choices[0].message.content
        return (tags,)

class mini_flux_tag:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE", {}),
                "model_name": ("STRING", {"default": "gpt-4o-mini",}),
            },
            "optional": {
                "base_url": (
                    "STRING",
                    {
                        "default": "https://api.openai.com/v1/",
                    },
                ),
                "api_key": (
                    "STRING",
                    {
                        "default": "sk-XXXXX",
                    },
                ),
                "imgbb_api_key":(
                    "STRING",
                    {
                        "default": "",
                    }
                ),
                "is_enable": ("BOOLEAN", {"default": True,}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tags",)

    FUNCTION = "file"

    # OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/迷你派对（mini-party）"

    def file(
        self,
        image,
        model_name="gpt-4o-mini",
        base_url=None,
        api_key=None,
        is_enable=True,
        imgbb_api_key=None,
    ):
        if not is_enable:
            return (None,)
        api_keys = load_api_keys(config_path)
        if api_key:
            openai.api_key = api_key
        elif api_keys.get("openai_api_key"):
            openai.api_key = api_keys.get("openai_api_key")
        else:
            openai.api_key = os.environ.get("OPENAI_API_KEY")

        if base_url:
            openai.base_url = base_url.rstrip("/") + "/"
        elif api_keys.get("base_url"):
            openai.base_url = api_keys.get("base_url")
        else:
            openai.base_url = os.environ.get("OPENAI_API_BASE")

        if not openai.api_key:
            return ("请输入API_KEY",)
        sys_prompt = f'''# FLUX prompt 助理

你来充当一位图片反推prompt助理。

## 任务

我会发给你一张图片，你要根据这张图片生成的prompt，你的任务是根据这张图片反推成一份详细的、高质量的prompt，可以让FLUX重现这张图片。

## 背景介绍

FLUX是一款利用深度学习的文生图模型，支持通过使用 自然语言 prompt 来产生新的图像，描述要包含或省略的元素。

## Prompt 格式要求

你必须尽可能的和我会发给你的图片保持一致。不多不少的描述完整张图片的所有细节。

**示例：**

A majestic, emerald-scaled dragon with glowing amber eyes, wings outstretched, soars through a breathtaking vista of snow-capped mountains. The dragon's powerful form dominates the scene, casting a long shadow over the imposing peaks. Below, a cascading waterfall plunges into a deep valley, its spray catching the sunlight in a dazzling array of colors. The dragon's scales shimmer with iridescent hues, reflecting the surrounding natural beauty. The sky is a vibrant blue, dotted with fluffy white clouds, creating a sense of awe and wonder. This dynamic and visually stunning depiction captures the majesty of both the dragon and the mountainous landscape.

**指导**：

1. **描述细节**：尽量提供具体的细节，如颜色、形状、位置等。
2. **情感和氛围**：描述场景的情感和氛围，如温暖、神秘、宁静等。
3. **风格和背景**：说明场景的风格和背景，如卡通风格、未来主义、复古等。

### 3. 限制：
- 你给出的prompt只用英文。
- 不要解释你的prompt，直接输出prompt。
- 不要输出其他任何非prompt字符，只输出prompt，也不要包含 **生成提示词**： 等类似的字符。
'''
        if imgbb_api_key == "" or imgbb_api_key is None:
            imgbb_api_key = api_keys.get("imgbb_api")
        if imgbb_api_key == "" or imgbb_api_key is None:
            i = 255.0 * image[0].cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            # 将图片保存到缓冲区
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            # 将图片编码为base64
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            img_json = [
                {"type": "text", "text": "请生成这张图片的prompt"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{img_str}"},
                },
            ]
        else:
            i = 255.0 * image[0].cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            # 将图片保存到缓冲区
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            # 将图片编码为base64
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            url = "https://api.imgbb.com/1/upload"
            payload = {"key": imgbb_api_key, "image": img_str}
            # 向API发送POST请求
            response = requests.post(url, data=payload)
            # 检查请求是否成功
            if response.status_code == 200:
                # 解析响应以获取图片URL
                result = response.json()
                img_url = result["data"]["url"]
                print(img_url)
            else:
                return "Error: " + response.text
            img_json = [
                {"type": "text", "text": "请生成这张图片的prompt"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": img_url,
                    },
                },
            ]
        history= [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": img_json}
        ]
        response = openai.chat.completions.create(
                            model=model_name,
                            messages=history,
                        )
        tags = response.choices[0].message.content
        return (tags,)


NODE_CLASS_MAPPINGS = {
    "mini_party": mini_party,
    "mini_translate": mini_translate,
    "mini_sd_prompt": mini_sd_prompt,
    "mini_flux_prompt":mini_flux_prompt,
    "mini_sd_tag":mini_sd_tag,
    "mini_flux_tag":mini_flux_tag,
    "mini_error_correction":mini_error_correction,
    }
# 获取系统语言
lang = locale.getdefaultlocale()[0]
import os
import sys
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(current_dir, "config.ini")
import configparser
config = configparser.ConfigParser()
config.read(config_path)
try:
    language = config.get("API_KEYS", "language")
except:
    language = ""
if language == "zh_CN" or language=="en_US":
    lang=language
if lang == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {
        "mini_party": "迷你派对",
        "mini_translate": "迷你翻译机",
        "mini_sd_prompt": "迷你SD提示词生成器",
        "mini_flux_prompt": "迷你FLUX提示词生成器",
        "mini_sd_tag": "迷你SD图片提示词反推器",
        "mini_flux_tag": "迷你FLUX图片提示词反推器",
        "mini_error_correction": "迷你文档纠错器",
        }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "mini_party": "Mini Party",
        "mini_translate": "Mini Translator",
        "mini_sd_prompt": "Mini SD Prompt Generator",
        "mini_flux_prompt": "Mini FLUX Prompt Generator",
        "mini_sd_tag": "Mini SD image prompt retractor",
        "mini_flux_tag": "Mini FLUX image prompt retractor",
        "mini_error_correction": "Mini file Error Corrector",
        }