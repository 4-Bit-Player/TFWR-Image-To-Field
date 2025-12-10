import math, cv2
import numpy as np
from PIL import Image
from img_encoder import run_length_encode, get_game_decoder_string

def convert_gif(gif_path:str, result_file_name:str="result_gif.txt") -> None:
    ### Converting a video
    if gif_path.endswith(".mp4"):
        video:list[list[int]] = get_video(gif_path) # If you want to convert a video you have to uncomment this and comment out the get_gif function.
    ###
    ### Converting a gif
    else:
        video:list[list[int]] = get_gif(gif_path)
    ###

    out_vid:list[list[str]] = []

    for frame in video:
        normalize_img(frame)
        out_vid.append(convert_to_str(frame))

    tmp_list = run_length_encode(mix_lists(out_vid)) # [run_length_encode(x) for x in mix_lists(out_vid)]

    to_save = []
    for i in range(len(tmp_list)):
        to_save.append(nested_list_to_str([tmp_list[i]]))
    save_list(to_save, result_file_name)


def convert_and_rotate_image(image_path:str, result_file_name:str="result_img_rotated.txt") -> None:
    imgs:list[list[str]] = []
    # Rotating backwards. You can change it to range(0, 360, 10) to make it rotate the other way.
    for rotation in range(360, 0, -10):
        img = get_img(image_path, rotation)
        normalize_img(img)
        str_arr = convert_to_str(img)
        imgs.append(str_arr)

    tmp_list = run_length_encode(mix_lists(imgs))
    to_save:list[str] = []

    for i in range(len(tmp_list)):
        to_save.append(nested_list_to_str([tmp_list[i]]))

    save_list(to_save, result_file_name)



def convert_image(image_path:str, result_file_name:str="result_img1.txt") -> None:
    img = get_img(image_path)
    normalize_img(img)

    str_arr = convert_to_str(img)
    str_arr = run_length_encode(str_arr)



    save_list(str_arr, result_file_name)



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
            # removing every second frame to save a bit of space.
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
    decoder = get_game_decoder_string()
    func_beginning = decoder + "def get_img():\n    return "
    data = "[" + ",\n".join(to_save) + "]"

    if add_func_prefix:
        data = func_beginning + data

    with open(img_name, "w", encoding="utf-8") as file:
        file.write(data)


def nested_list_to_str(nested_list:list) -> str:
    return ",\n".join(nested_list)


def mix_lists(base_list:list[list[str]])->list[list[str]]:
    out:list[list[str]] = []

    for i in range(len(base_list[0])):
        line:list[str] = []
        for ii in range(len(base_list)):
            line.append(base_list[ii][i])
        out.append(line)

    ac_out = []

    for i in range(len(out)):
        arr = out[i]

        tmp = []
        for str_line in arr:
            tmp.append(str_line.replace('"', ""))
            continue

        if i % 2 == 1:
            tmp.reverse()
        ac_out.append('"'+"".join(tmp) + '"')

    return ac_out