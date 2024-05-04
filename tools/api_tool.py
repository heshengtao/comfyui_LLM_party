import json
import requests
class api_box:
    def __init__(self,id,url) -> None:
        self.id=id
        self.url=url
    def request_api(self,**parameter):
        response = requests.get(self.url, params=parameter, timeout=10)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return response.text
        else:
            return "API请求失败"
        
api_boxes = {}

def use_api_tool(id,**parameter):
    global api_boxes
    if str(id).strip() in api_boxes:
        return api_boxes[str(id).strip()].request_api(**parameter)
    else:
        return "API ID不存在"


class api_tool:
    def __init__(self) -> None:
        #哈希值给到ID
        self.id=hash(self)

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "is_enable": (["enable", "disable"],{
                    "default":"enable"
                }),      
                "url": ("STRING",{
                    "default":"被请求的网址"
                }),
                "description":("STRING",{
                    "multiline": True,
                    "default":"用来查天气的工具"
                }),
                "parameters":("STRING",{
                    "multiline": True,
                    "default":"""
                    {
"city": "用户询问的目标区域，例如：长沙市",
"extensions": "可选值：base/all base:返回实况天气 all:返回预报天气，默认为all"
}
"""
                }),
            },
            "optional": {

            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tool",)

    FUNCTION = "read_web"

    #OUTPUT_NODE = False

    CATEGORY = "大模型派对（llm_party）/工具（tools）"



    def read_web(self,url,description,parameters,is_enable="enable"):   
        if is_enable=="disable":
            return (None,)
        global api_boxes
        api_boxes[str(self.id).strip()]=api_box(self.id,url)

        if parameters:
            try:
                parameters=json.loads(parameters)
            except:
                return ("参数格式错误，请检查",)
        parameter={"id":{"type": "string", "description": "API ID="+str(self.id).strip()}}
        required=["id"]
        for key in parameters:
            parameter[key]={"type": "string", "description":parameters[key]}
            required.append(key)
        output = [{
    "type": "function",
    "function": {
        "name": "use_api_tool",
        "description": description,
        "parameters": {
            "type": "object",
            "properties": parameter,
            "required": required
        }
    }
}]
        

        out=json.dumps(output, ensure_ascii=False)
        return (out,)