import base64
import uuid
import os

from dotenv import load_dotenv
import pyautogui
import pynput
import requests

# Load environment variables from .env file
load_dotenv(verbose=True)
dotenvPath = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenvPath)

# .env file should contain the following variables
# Azure OpenAI Service Constants
# Documents: https://learn.microsoft.com/ja-jp/azure/ai-services/openai/overview
RESOURCE_NAME = os.environ.get("RESOURCE_NAME")
DEPLOYMENT_NAME = os.environ.get("DEPLOYMENT_NAME")
API_VERSION = os.environ.get("API_VERSION")
API_KEY = os.environ.get("API_KEY")


class ClickListener():
    def __init__(self) -> None:
        self.region = [0, 0, 0, 0]
        self.numOfClicks = 0

    def on_click(self, x, y, button, pressed) -> bool:
        # Listen to the mouse click event
        if pressed:
            if self.numOfClicks == 0:
                pass
            elif self.numOfClicks == 1:
                self.region[0] = x
                self.region[1] = y
                print(f"upper left : ({x:4d}, {y:4d})")
            elif self.numOfClicks == 2:
                self.region[2] = x
                self.region[3] = y
                print(f"lower right: ({x:4d}, {y:4d})")
                self.numOfClicks = 0
                return False
            self.numOfClicks += 1
        return True

    def listen(self) -> tuple:
        # Listen to the mouse click event and return the region of the screenshot
        with pynput.mouse.Listener(on_click=self.on_click) as listener:
            listener.join()
        return tuple(self.region)


def takeScreenshot(path: str, region: tuple = None):
    # Take a screenshot of the specified region and save it to the specified path
    if region:
        return pyautogui.screenshot(path, region=region)
    return pyautogui.screenshot(path)


def convBase64(path: str) -> str:
    # Convert the image file to base64
    with open(path, "rb") as img:
        imBase64 = base64.b64encode(img.read())
    return imBase64.decode("utf-8")


def requestGPT4o(prompt: str, imPath: str = ""):
    # Request to the Azure OpenAI Service
    endpoint = f"https://{RESOURCE_NAME}.openai.azure.com/deployments/{
        DEPLOYMENT_NAME}/chat/completions?api-version={API_VERSION}"
    requestJson = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            f"data:image/png;base64,{convBase64(imPath)}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 800,
    }
    try:
        resp = requests.post(endpoint, json=requestJson, headers={
            "Content-Type": "application/json", "api-key": API_KEY})
    except Exception as e:
        print(e.__class__, e)
        return None
    return resp


if __name__ == "__main__":
    cl = ClickListener()
    os.makedirs("tmp", exist_ok=True)
    while True:
        region = cl.listen()
        imPath = f"tmp/{uuid.uuid4()}.png"
        takeScreenshot(imPath, region)
        prompt = input("Enter prompt: ")
        resp = requestGPT4o(prompt, imPath)
        if resp is None:
            exit(1)
        print("Status code:", resp.status_code)
        if resp.status_code != 200:
            continue
        print("Response:")
        print(resp.json()["choices"][0]["message"]["content"])
