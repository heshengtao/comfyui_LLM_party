import json
import os

import folder_paths
import numpy as np
from comfy.cli_args import args
from PIL import Image, ImageOps, ImageSequence
from PIL.PngImagePlugin import PngInfo


class end_workflow:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 4

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {"filename_prefix": ("STRING", {"default": "ComfyUI"})},
            "optional": {
                "images": ("IMAGE",),
                "text": ("STRING", {"forceInput": True}),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    RETURN_TYPES = ()
    FUNCTION = "save_all"

    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/工作流（workflow）"

    def save_all(self, images=None, text=None, filename_prefix="ComfyUI", prompt=None, extra_pnginfo=None):
        results = list()
        all_results = {}
        if images is not None and len(images) > 0:
            filename_prefix += self.prefix_append
            full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(
                filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0]
            )
            for batch_number, image in enumerate(images):
                i = 255.0 * image.cpu().numpy()
                img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
                metadata = None
                if not args.disable_metadata:
                    metadata = PngInfo()
                    if prompt is not None:
                        metadata.add_text("prompt", json.dumps(prompt))
                    if extra_pnginfo is not None:
                        for x in extra_pnginfo:
                            metadata.add_text(x, json.dumps(extra_pnginfo[x]))

                filename_with_batch_num = filename.replace("%batch_num%", str(batch_number))
                file = f"{filename_with_batch_num}_{counter:05}_.png"
                img.save(os.path.join(full_output_folder, file), pnginfo=metadata, compress_level=self.compress_level)
                results.append({"filename": file, "subfolder": subfolder, "type": self.type})
                counter += 1
            # 给 all_results添加images元素
            all_results["images"] = results
        text_results = list()
        # 文件命名
        if text is not None:
            # 对保存的文件命名，和图片同名
            file = f"{filename_prefix}_.txt"
            # 保存文本
            with open(os.path.join(self.output_dir, file), "w", encoding="utf-8") as f:
                f.write(text)
            text_results.append({"content": text})
            # 给 all_results添加response元素
            all_results["response"] = text_results
        return {"ui": all_results}


class img2path:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 4

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {"filename_prefix": ("STRING", {"default": "ComfyUI"})},
            "optional": {
                "images": ("IMAGE",),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("path",)
    FUNCTION = "save_all"

    OUTPUT_NODE = True

    CATEGORY = "大模型派对（llm_party）/图片（image）"

    def save_all(self, images=None, filename_prefix="ComfyUI", prompt=None, extra_pnginfo=None):
        if images is None or len(images) == 0:
            return (None,)
        results = list()
        all_results = {}
        if images is not None:
            filename_prefix += self.prefix_append
            full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(
                filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0]
            )
            for batch_number, image in enumerate(images):
                i = 255.0 * image.cpu().numpy()
                img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
                metadata = None
                if not args.disable_metadata:
                    metadata = PngInfo()
                    if prompt is not None:
                        metadata.add_text("prompt", json.dumps(prompt))
                    if extra_pnginfo is not None:
                        for x in extra_pnginfo:
                            metadata.add_text(x, json.dumps(extra_pnginfo[x]))

                filename_with_batch_num = filename.replace("%batch_num%", str(batch_number))
                file = f"{filename_with_batch_num}_{counter:05}_.png"
                img.save(os.path.join(full_output_folder, file), pnginfo=metadata, compress_level=self.compress_level)
                results.append({"filename": file, "subfolder": subfolder, "type": self.type})
                counter += 1
                if batch_number == 0:
                    # 获得第一张图片的绝对路径
                    path = os.path.join(full_output_folder, file)
        return (path,)
