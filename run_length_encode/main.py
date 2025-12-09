from img_funcs import convert_image, convert_and_rotate_image, convert_gif


if __name__ == '__main__':
    image_path = "Ying_yang_sign.jpg"
    #result_file_name = "../Saves/Save3/img_data.py"
    result_file_name = "img_data.py"
    # Comment this line out and uncomment the lines below to convert different things. :)
    # convert_image(image_path, result_file_name)

    # If you want to "animate" the image by rotating it you can use these functions.
    # result_file_name = "result_rotated.txt"
    # convert_and_rotate_image(image_path, result_file_name)


    # For gifs/videos you can use this part.
    gif_path = "bad_apple.mp4"
    # result_file_name = "result_gif.txt"
    convert_gif(gif_path, result_file_name)