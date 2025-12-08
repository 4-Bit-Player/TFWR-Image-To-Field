from img_funcs import get_img, normalize_img, convert_to_str, mix_lists, nested_list_to_str, save_list, get_gif, get_video


def convert_and_rotate_image(image_path:str, result_file_name:str="result_img_rotated.txt") -> None:
    imgs:list[list[str]] = []
    # Rotating backwards. You can change it to (0, 360, 10) to make it rotate the other way.
    for rotation in range(360, 0, -10):
        img = get_img(image_path, rotation)
        normalize_img(img)
        str_arr = convert_to_str(img)
        imgs.append(str_arr)

    tmp_list = mix_lists(imgs)
    to_save:list[str] = []

    for i in range(len(tmp_list)):
        to_save.append(nested_list_to_str(tmp_list[i]))

    save_list(to_save, result_file_name)



def convert_image(image_path:str, result_file_name:str="result_img1.txt") -> None:
    img = get_img(image_path)
    normalize_img(img)

    str_arr = convert_to_str(img)

    nested = ["[" + x + "]" for x in str_arr]


    save_list(nested, result_file_name)


def convert_gif(gif_path:str, result_file_name:str="result_gif.txt") -> None:
    ### Converting a video
    #video:list[list[int]] = get_video(image_path) # If you want to convert a video you have to uncomment this and comment out the get_gif function.
    ###
    ### Converting a gif
    video:list[list[int]] = get_gif(gif_path)
    ###

    out_vid:list[list[str]] = []

    for frame in video:
        normalize_img(frame)
        out_vid.append(convert_to_str(frame))

    tmp_list = mix_lists(out_vid)

    to_save = []
    for i in range(len(tmp_list)):
        to_save.append(nested_list_to_str(tmp_list[i]))
    save_list(to_save, result_file_name)







if __name__ == '__main__':
    image_path = "Ying_yang_sign.jpg"
    result_file_name = "result_img.txt"
    # Comment this line out and uncomment the lines below to convert different things. :)
    convert_image(image_path, result_file_name)

    # If you want to "animate" the image by rotating it you can use these functions.
    # result_file_name = "result_rotated.txt"
    # convert_and_rotate_image(image_path, result_file_name)


    # For gifs/videos you can use this part.
    # gif_path = "rickroll-roll.gif"
    # result_file_name = "result_gif.txt"
    # convert_gif(gif_path, result_file_name)