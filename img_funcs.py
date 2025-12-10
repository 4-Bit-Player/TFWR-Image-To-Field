import math
import numpy as np
from PIL import Image
import cv2



def get_video(path:str) -> list[list[int]]:
    frames = []
    video = cv2.VideoCapture(path)
    success = True
    while success:
        success, frame = video.read()
        if success:
            img = Image.fromarray(frame)

            frame = img.convert("L").resize((32,32), resample=Image.Resampling.LANCZOS)
            frames.append(np.array(frame).tolist())
            video.read()

    return frames


def get_gif(path:str):
    frames = []
    with Image.open(path) as img:
        try:
            while True:
                frame = img.convert("L").resize((32,32))

                frames.append(np.array(frame).tolist())
                img.seek(img.tell()+1)
        except EOFError:
            pass
    return frames




def get_img(path:str, rotation:float=0.0) -> list[list[int]]:
    if rotation != 0:
        img = Image.open(path).rotate(rotation, fillcolor=255).convert("L").resize((32, 32))
    else:
        img = Image.open(path).convert("L").resize((32, 32))
    arr = np.array(img)
    return arr.tolist()


def normalize_img(arr:np.ndarray|list[list[int]]) -> None:
    for row in range(len(arr)):
        for i in range(len(arr[row])):
            arr[row][i] = int(arr[row][i] / math.ceil(255/8))



def convert_to_str(arr:list[list[int]]) -> list[str]:
    out = []
    for row in arr:
        out.append("\"" + "".join([str(x) for x in row]) + "\"")
    return out


def save_list(to_save:list[str], img_name:str="result_img2.txt", add_func_prefix=True) -> None:

    func_beginning = "def get_img():\n    return "
    data = "[" + ",\n".join(to_save) + "]"

    if add_func_prefix:
        data = func_beginning + data

    with open(img_name, "w", encoding="utf-8") as file:
        file.write(data)


def nested_list_to_str(nested_list:list) -> str:
    return "[" + ",\n".join(nested_list) + "]"



def mix_lists(base_list:list[list[str]])->list[list[str]]:
    out:list[list[str]] = []

    for i in range(len(base_list[0])):
        line:list[str] = []
        for ii in range(len(base_list)):
            line.append(base_list[ii][i])
        out.append(line)

    return out