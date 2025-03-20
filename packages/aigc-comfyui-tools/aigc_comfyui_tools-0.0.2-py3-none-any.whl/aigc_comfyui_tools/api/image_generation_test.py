from aigc_comfyui_tools.api.image_generation import *


################################################################################
# ImageGeneration()
# ComfyUI图像生成, 这是一个基础工作流, 用SD1.5进行文生图。
################################################################################
# server="http://localhost:8188"
server="http://10.1.1.29:8180"
prompt = "masterpiece best quality girl, with a cat."
api_json_path = "./data/jsonfile/image_generation.json"
save_images_dir = "./tmp/"

tex2image = ImageGeneration(server)
tex2image(api_json_path, prompt, save_images_dir)
