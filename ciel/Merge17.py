import os
import math


def merge(dir: str, filename: str, width: int, height: int, dv: int):
  files = os.listdir(dir)
  cnt = len(files)
  try:
    from PIL import Image
    col = min(cnt, dv)
    row = math.ceil(cnt / dv)
    img_width = width * col
    img_height = height * row

    res_img = Image.new("RGBA", (img_width, img_height))
    for i in range(cnt):
      y = i // col
      x = i % col
      path = os.path.join(dir, files[i])
      print("Merge " + path)
      img = Image.open(path)
      res_img.paste(img, (x * width, y * height))

    path = os.path.join(dir, filename)
    print("Save to " + path)
    res_img.save(path)

  except Exception as e:
    print(e)
    pass
