import click
import pathlib
try:
    from importlib.resources import files  #  python3.10之后的版本
except Exception:
    from importlib_resources import files  #  python3.10之前的版本

from aigc_comfyui_tools.api.image_generation import ImageGeneration


@click.command('image_generation')
@click.option('--server', "-s", default="http://localhost:8188", help='SSL要用https, 本地用http')
@click.option('--api_json_path', "-p", default="", help='API JSON File')
@click.option('--text', "-t", default="masterpiece best quality girl, with a cat.", help='提示词')
@click.option('--dst_dir', "-d", default="./tmp", help='生成的图片保存目录')

def cli(server, api_json_path, text, dst_dir, *args, **kwargs):
    """文件重命名。
    aigc_comfyui_tools image_generation -s "http://10.1.1.29:8180" -p "./data/jsonfile/image_generation.json"
    """
    if not api_json_path:
        api_json_path = pathlib.Path("data/jsonfile/image_generation.json")
        if not api_json_path.exists():
            # 调试模式的话，要：pip install -e . --config-settings editable_mode=compat
            # 不然files()会抛出异常。
            api_json_path = files("aigc_comfyui_tools") / api_json_path
            if not api_json_path.exists():
                raise FileExistsError(f"Not Exists: data/jsonfile/image_generation.json and {api_json_path}")
        
    print("ComfyUI Server: {}".format(server))
    print("api_json_path: {}".format(api_json_path))
    print("prompt text: {}".format(text))
    tex2image = ImageGeneration(server)
    tex2image(api_json_path, text, dst_dir, *args, **kwargs)
    print("Images saved: {}".format(dst_dir))
