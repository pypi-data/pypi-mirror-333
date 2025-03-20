import io
import json
import pathlib
import time
import uuid
import urllib.request
import urllib.parse
import websocket

from PIL import Image
                

class ImageGeneration(object):
    """This is an example that uses the websockets api to know when a prompt 
       execution is done. Once the prompt execution is done it downloads the 
       images using the /history endpoint
    Paramaters:
        server(str): ComfyUI Server Address, such as: http://localhost:8188
    Note:
        websocket-client (https://github.com/websocket-client/websocket-client)
    """

    def __init__(self, server="http://localhost:8188"):
        self.server = server.rstrip("/")
        if self.server.startswith("http://"):
            self.ws = "ws://" + self.server[len("http://"):]
        elif self.server.startswith("https://"):
            self.ws = "wss://" + self.server[len("https://"):]
        else:
            raise ValueError(f"Invalid URL: {server}") 

    def read_api_prompt(self, api_json_path):
        """读取ComfyUI API请求文件。
        Args:
            api_json_path(str): 在ComfyUI页面的API选项中导出你需要的工作流.json文件。
        Returns:
            返回json字典, 这是API请求中的prompt内容, 你的API生图设置都在这里。包括工作
            流结构, 用到的模型, 提示词等选择。
        """
        with open(api_json_path, 'r', encoding='utf-8') as f:
            api_prompt = json.load(f)
        return api_prompt

    def set_prompt(self, api_prompt, text="masterpiece best quality girl, with a cat.", seed=5):
        """设置参数, 要求和json里面的key相对应。这里我演示了两个key: 随机数和prompt。
        """
        api_prompt["3"]["inputs"]["seed"] = seed
        api_prompt["6"]["inputs"]["text"] = text
        return api_prompt

    def queue_prompt(self, prompt, client_id, server):
        """发起apt请求。
        Args:
            prompt(dict): API json工作流文件数据。
            client_id(str): API发起生图请求后, Server通过websocket将结果发送给前端的标识。
            server(str): server地址。
        Returns:
            返回json字典, 这是API请求中的prompt内容, 你的API生图设置都在这里。包括工作
            流结构, 用到的模型, 提示词等选择。
        """
        api_json = {"prompt": prompt, "client_id": client_id}
        data = json.dumps(api_json).encode('utf-8')
        req = urllib.request.Request("{}/prompt".format(server), data=data)
        return json.loads(urllib.request.urlopen(req).read())

    def get_image(self, filename, subfolder, folder_type, server):
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        with urllib.request.urlopen("{}/view?{}".format(server, url_values)) as response:
            return response.read()

    def get_history(self, server, prompt_id):
        with urllib.request.urlopen("{}/history/{}".format(server, prompt_id)) as response:
            return json.loads(response.read())

    def get_images(self, ws, api_prompt, client_id, server):
        prompt_id = self.queue_prompt(api_prompt, client_id, server)['prompt_id']
        output_images = {}
        while True:
            out = ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                if message['type'] == 'executing':
                    data = message['data']
                    if data['node'] is None and data['prompt_id'] == prompt_id:
                        break  # Execution is done
            else:
                # If you want to be able to decode the binary stream for latent previews, here is how you can do it:
                # bytesIO = BytesIO(out[8:])
                # preview_image = Image.open(bytesIO) # This is your preview in PIL image format, store it in a global
                continue  # previews are binary data

        history = self.get_history(server, prompt_id)[prompt_id]
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            images_output = []
            if 'images' in node_output:
                for image in node_output['images']:
                    image_data = self.get_image(image['filename'], image['subfolder'], image['type'], server)
                    images_output.append(image_data)
            output_images[node_id] = images_output

        return output_images
    
    def save_images(self, images, dst_dir):
        dst_dir = pathlib.Path(dst_dir)
        if not dst_dir.exists():
            dst_dir.mkdir(parents=True)

        for node_id in images:
            for image_data in images[node_id]:
                image = Image.open(io.BytesIO(image_data))
                name = str(int(time.time() * 1e6)).zfill(16)
                dst_path = dst_dir / "img{}.png".format(name)
                image.save(str(dst_path))
    
    def __call__(self, api_json_path, text, dst_dir):
        api_prompt = self.read_api_prompt(api_json_path)
        api_prompt = self.set_prompt(api_prompt, text)
        client_id = str(uuid.uuid4())
        ws = websocket.WebSocket()
        ws.connect("{}/ws?clientId={}".format(self.ws, client_id))
        images = self.get_images(ws, api_prompt, client_id, self.server)
        # for in case this example is used in an environment where it will be 
        # repeatedly called, like in a Gradio app. otherwise, you'll randomly receive connection timeouts
        ws.close()
        self.save_images(images, dst_dir)
        