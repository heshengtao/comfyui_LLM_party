import locale
import easyocr
import cv2
import json
import numpy as np
import torch
from PIL import Image

class EasyOCR_advance:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "gpu": ("BOOLEAN", {"default": True}),
                "language_name": ("STRING", {"default": "ch_sim,en"}),
                "decoder": ("STRING", {"default": "greedy"}),
                "beamWidth": ("INT", {"default": 5}),
                "batch_size": ("INT", {"default": 1}),
                "workers": ("INT", {"default": 0}),
                "allowlist": ("STRING", {"default": ""}),
                "blocklist": ("STRING", {"default": ""}),
                "paragraph": ("BOOLEAN", {"default": False}),
                "min_size": ("INT", {"default": 20}),
                "contrast_ths": ("FLOAT", {"default": 0.1}),
                "adjust_contrast": ("FLOAT", {"default": 0.5}),
                "text_threshold": ("FLOAT", {"default": 0.7}),
                "low_text": ("FLOAT", {"default": 0.4}),
                "link_threshold": ("FLOAT", {"default": 0.4}),
                "canvas_size": ("INT", {"default": 2560}),
                "mag_ratio": ("FLOAT", {"default": 1.0}),
                "slope_ths": ("FLOAT", {"default": 0.1}),
                "ycenter_ths": ("FLOAT", {"default": 0.5}),
                "height_ths": ("FLOAT", {"default": 0.5}),
                "width_ths": ("FLOAT", {"default": 0.5}),
                "add_margin": ("INT", {"default": 0}),
                "is_enable": ("BOOLEAN", {"default": True}),
            },
        }

    CATEGORY = "大模型派对（llm_party）/函数（function）"
    FUNCTION = "OCR"
    RETURN_TYPES = ("IMAGE", "MASK", "STRING",)
    RETURN_NAMES = ("images", "masks", "json_str",)

    def OCR(self, image, gpu, language_name, decoder="greedy", beamWidth=5, batch_size=1, workers=0, allowlist="", blocklist="", paragraph=False, min_size=20, contrast_ths=0.1, adjust_contrast=0.5, text_threshold=0.7, low_text=0.4, link_threshold=0.4, canvas_size=2560, mag_ratio=1.0, slope_ths=0.1, ycenter_ths=0.5, height_ths=0.5, width_ths=0.5, add_margin=0,is_enable=True):
        if not is_enable:
            return (None,)
        out_images = []
        out_masks = []
        out_json = []

        for item in image:
            image_pil = Image.fromarray(np.clip(255.0 * item.cpu().numpy(), 0, 255).astype(np.uint8)).convert("RGB")

            languages = language_name.split(",")

            reader = easyocr.Reader(languages, gpu=gpu)
            result = reader.readtext(
                np.array(image_pil), 
                detail=1, 
                decoder=decoder, 
                beamWidth=beamWidth, 
                batch_size=batch_size, 
                workers=workers, 
                allowlist=allowlist, 
                blocklist=blocklist, 
                paragraph=paragraph, 
                min_size=min_size, 
                contrast_ths=contrast_ths, 
                adjust_contrast=adjust_contrast, 
                text_threshold=text_threshold, 
                low_text=low_text, 
                link_threshold=link_threshold, 
                canvas_size=canvas_size, 
                mag_ratio=mag_ratio, 
                slope_ths=slope_ths, 
                ycenter_ths=ycenter_ths, 
                height_ths=height_ths, 
                width_ths=width_ths, 
                add_margin=add_margin
            )

            W, H = image_pil.size
            mask = np.zeros((H, W, 1), dtype=np.uint8)
            image_with_boxes = np.array(image_pil)

            parsed_result = []
            for (bbox, text, prob) in result:
                top_left = tuple(map(int, bbox[0]))
                bottom_right = tuple(map(int, bbox[2]))

                cv2.rectangle(image_with_boxes, top_left, bottom_right, (0, 0, 255), 2)
                cv2.putText(image_with_boxes, text, top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
                cv2.rectangle(mask, top_left, bottom_right, (255, 255, 255), -1)

                parsed_result.append({
                    "bounding_box": {
                        "top_left": [int(coord) for coord in bbox[0]],
                        "top_right": [int(coord) for coord in bbox[1]],
                        "bottom_right": [int(coord) for coord in bbox[2]],
                        "bottom_left": [int(coord) for coord in bbox[3]]
                    },
                    "text": text,
                    "confidence": float(prob)
                })

            out_images.append(torch.from_numpy(image_with_boxes.astype(np.float32) / 255.0).unsqueeze(0))
            out_masks.append(torch.from_numpy(mask.astype(np.float32) / 255.0).permute(2, 0, 1).unsqueeze(0))
            out_json.append(parsed_result)

        json_result = json.dumps(out_json, ensure_ascii=False, indent=4)
        return (torch.cat(out_images, dim=0), torch.cat(out_masks, dim=0), json_result,)


lang_list = {
    "English": "en",
    "简体中文": "ch_sim",
    "繁體中文": "ch_tra",
    "العربية": "ar",
    "Azərbaycan": "az",
    "Euskal": "eu",
    "Bosanski": "bs",
    "Български": "bg",
    "Català": "ca",
    "Hrvatski": "hr",
    "Čeština": "cs",
    "Dansk": "da",
    "Nederlands": "nl",
    "Eesti": "et",
    "Suomi": "fi",
    "Français": "fr",
    "Galego": "gl",
    "Deutsch": "de",
    "Ελληνικά": "el",
    "עברית": "he",
    "हिन्दी": "hi",
    "Magyar": "hu",
    "Íslenska": "is",
    "Indonesia": "id",
    "Italiano": "it",
    "日本語": "ja",
    "한국어": "ko",
    "Latviešu": "lv",
    "Lietuvių": "lt",
    "Македонски": "mk",
    "Norsk": "no",
    "Polski": "pl",
    "Português": "pt",
    "Română": "ro",
    "Русский": "ru",
    "Српски": "sr",
    "Slovenčina": "sk",
    "Slovenščina": "sl",
    "Español": "es",
    "Svenska": "sv",
    "ไทย": "th",
    "Türkçe": "tr",
    "Українська": "uk",
    "Tiếng Việt": "vi",
}


def get_lang_list():
    result = []
    for key, value in lang_list.items():
        result.append(key)
    return result

class EasyOCR_choose:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "gpu": ("BOOLEAN", {"default": True}),
                "language_list": (get_lang_list(), {"default": "English"}),
                "is_enable": ("BOOLEAN", {"default": True}),
            },
        }

    CATEGORY = "大模型派对（llm_party）/函数（function）"
    FUNCTION = "OCR"
    RETURN_TYPES = ("IMAGE", "MASK", "STRING",)
    RETURN_NAMES = ("images", "masks", "json_str",)

    def OCR(self, image, gpu, language_list, is_enable=True):
        if not is_enable:
            return (None,)
        out_images = []
        out_masks = []
        out_json = []

        for item in image:
            image_pil = Image.fromarray(np.clip(255.0 * item.cpu().numpy(), 0, 255).astype(np.uint8)).convert("RGB")

            languages = [lang_list[language_list]]

            reader = easyocr.Reader(languages, gpu=gpu)
            result = reader.readtext(np.array(image_pil), detail=1)

            W, H = image_pil.size
            mask = np.zeros((H, W, 1), dtype=np.uint8)
            image_with_boxes = np.array(image_pil)

            parsed_result = []
            for (bbox, text, prob) in result:
                top_left = tuple(map(int, bbox[0]))
                bottom_right = tuple(map(int, bbox[2]))

                cv2.rectangle(image_with_boxes, top_left, bottom_right, (0, 0, 255), 2)
                cv2.putText(image_with_boxes, text, top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
                cv2.rectangle(mask, top_left, bottom_right, (255, 255, 255), -1)

                parsed_result.append({
                    "bounding_box": {
                        "top_left": [int(coord) for coord in bbox[0]],
                        "top_right": [int(coord) for coord in bbox[1]],
                        "bottom_right": [int(coord) for coord in bbox[2]],
                        "bottom_left": [int(coord) for coord in bbox[3]]
                    },
                    "text": text,
                    "confidence": float(prob)
                })

            out_images.append(torch.from_numpy(image_with_boxes.astype(np.float32) / 255.0).unsqueeze(0))
            out_masks.append(torch.from_numpy(mask.astype(np.float32) / 255.0).permute(2, 0, 1).unsqueeze(0))
            out_json.append(parsed_result)

        json_result = json.dumps(out_json, ensure_ascii=False, indent=4)
        return (torch.cat(out_images, dim=0), torch.cat(out_masks, dim=0), json_result,)


NODE_CLASS_MAPPINGS = {
    "EasyOCR_advance": EasyOCR_advance,
    "EasyOCR_choose":EasyOCR_choose,
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
        "EasyOCR_advance": "EasyOCR高级",
        "EasyOCR_choose": "EasyOCR",
        }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "EasyOCR_advance": "EasyOCR advance",
        "EasyOCR_choose": "EasyOCR",
        }