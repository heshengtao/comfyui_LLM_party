from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info
import torch

# 加载模型和处理器
model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
    "D:\AI\mychat\model\Qwen2.5-VL-3B-Instruct", 
    torch_dtype="auto", 
    device_map="auto"
)
processor = AutoProcessor.from_pretrained("D:\AI\mychat\model\Qwen2.5-VL-3B-Instruct")

def process_image_and_text(image, text_prompt):
    if image is None:
           # 构建消息格式
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": text_prompt if text_prompt else "Describe this image."},
                ],
            }
        ]
    else:
        # 构建消息格式
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "image": image,  
                    },
                    {"type": "text", "text": text_prompt if text_prompt else "Describe this image."},
                ],
            }
        ]
    
    try:
        # 准备推理输入
        text = processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        image_inputs, video_inputs = process_vision_info(messages)
        inputs = processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        )
        inputs = inputs.to(model.device)

        # 生成输出
        with torch.no_grad():
            generated_ids = model.generate(**inputs, max_new_tokens=128)
            generated_ids_trimmed = [
                out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
            ]
            output_text = processor.batch_decode(
                generated_ids_trimmed, 
                skip_special_tokens=True, 
                clean_up_tokenization_spaces=False
            )
        
        return output_text[0]
    
    except Exception as e:
        return f"处理过程中出现错误: {str(e)}"

if __name__ == "__main__":
    print(process_image_and_text(None, "你好哇"))