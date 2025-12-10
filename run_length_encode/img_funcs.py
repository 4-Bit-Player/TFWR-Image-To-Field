import math, cv2
import numpy as np
from PIL import Image


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


default_decoder = {}
dynamic_decoder = {}

def run_length_encode(line_arr:list[str]) -> list[str]:
    default_encoder = {1:"a",2:"b",3:"c",4:"d",5:"e",6:"f",7:"g",8:"h",9:"i",10:"j",11:"k",12:"l",13:"m",14:"n",15:"o",16:"p",17:"q",18:"r",19:"s",20:"t",21:"u",22:"v",23:"w",24:"x",25:"y",26:"z",27:"A",28:"B",29:"C",30:"D",31:"E",32:"F",33:"G",34:"H",35:"I",36:"J",37:"K",38:"L",39:"M",40:"N",41:"O",42:"P",43:"Q",44:"R",45:"S",46:"T",47:"U",48:"V",49:"W",50:"X",51:"Y",52:"Z",53:"0",54:"1",55:"2",56:"3",57:"4",58:"5",59:"6",60:"7",61:"8",62:"9",63:"ö",64:"ä",65:"ü",66:"#",67:"$",68:"%",69:"&",70:"'",71:"(",72:")",73:"*",74:"+",75:",",76:"-",77:".",78:"/",79:":",80:";",81:"<",82:"=",83:">",84:"?",85:"@",86:"[",87:"Ö",88:"]",89:"^",90:"_",91:"`",92:"{",93:"|",94:"}",95:"~",96:"!",}
    out:list[str]=[]

    for line in line_arr:
        new_line:list[str] = []
        char = line[0]
        count = 0
        for i in range(len(line)):
            if line[i] == '"':
                continue
            if line[i] == char:
                count += 1
                if count == len(default_encoder):
                    new_line.append(f"{default_encoder[count]}{char}")
                    count = 0
                continue
            if count != 0:
                new_line.append(f"{default_encoder[count]}{char}")
            char = line[i]
            count = 1
        if count != 0:
            new_line.append(f"{default_encoder[count]}{char}")
        out.append('"'+ "".join(new_line) + '"')
    return out


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