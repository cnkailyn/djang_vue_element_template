from PIL import Image
import os


current_path = os.getcwd()
print(current_path)
for file_ in os.listdir():
    file_full_path = os.path.join(current_path, file_)

    if file_.split(".")[-1].lower() in ["png", "jpg", "jpeg", "bmp"]:
        if file_.startswith("【已处理】"):
            os.remove(file_full_path)
        im = Image.open(file_full_path)
        box = (0, 0, im.width, im.height*0.97)
        im_crop = im.crop(box)
        im_crop.save(os.path.join(current_path, f"【已处理】{file_}"))
