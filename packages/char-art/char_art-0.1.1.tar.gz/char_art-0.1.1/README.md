# char_art

方便地制作字符画与字符视频 ~

---

## 0. 引言

制作字符画和字符视频的脚本很多人都写过, 而我写该库的目的主要是为了:

1. 让制作字符画与字符视频更方便, 只需一行命令即可完成从生成到保存的全部过程
2. 做了许多优化, 让生成字符画和字符视频更加高效

---

## 1. 安装

使用以下命令安装该库, 使用该库的基本功能:

  ```commandline
  pip install char_art
  ```

若需要保存生成的字符画和字符视频, 则需要额外安装 **pygame** 库, 或者可以直接用以下命令进行安装

  ```commandline
  pip install char_art[save]
  ```

---

## 2. 快速开始

- 生成一张图片的字符画
  ```commandline
  python -m char_art display 'my_image.jpg' -s 120 37
  ```

- 生成一段视频的字符视频
  ```commandline
  python -m char_art display 'my_video.mp4' -v -s 80 30
  ```

- 保存生成的字符画 (需要 pygame 库)
  ```commandline
  python -m char_art save 'my_image.jpg' 'save_file.jpg' -s 120 37
  ```

- 保存生成的字符视频 (需要 pygame 库)
  ```commandline
  python -m char_art save 'my_video.mp4' 'save_file.mp4' -v -s 80 30
  ```

---

## 3. 使用帮助

```commandline
usage: python -m char_art [-h] [-v] {display,save} ...

positional arguments:
  {display,save}
    display       展示字符画或字符视频
    save          保存字符画为图像文件 / 字符视频为视频文件

options:
  -h, --help      show this help message and exit
  -v, --version   show program's version number and exit
```

```commandline
usage: python -m char_art display [-h] [-v] -s WIDTH HEIGHT [-c CHARS] [-l] file

positional arguments:
  file                  图像或视频的文件路径

options:
  -h, --help            show this help message and exit
  -v, --video           展示字符视频, 若不设置则为字符画
  -s, --size WIDTH HEIGHT
                        字符画或字符视频的尺寸, 按字符数量计
  -c, --chars CHARS     使用的字符序列 (默认为 ' .-+{#')
  -l, --load            在展示字符视频前加载并缓存所有字符帧, 使得播放时更流畅
```

```commandline
usage: python -m char_art save [-h] [-v] -s WIDTH HEIGHT [-c CHARS] [--font FONT] [--font-size FONT_SIZE] [--spacing SPACING] [--fill FILL] [--bg BG] [--scale SCALE] [--fourcc FOURCC]
                               file save_file

positional arguments:
  file                  图像或视频的文件路径
  save_file             生成的图像或视频的保存路径

options:
  -h, --help            show this help message and exit
  -v, --video           保存字符视频, 若不设置则为字符画
  -s, --size WIDTH HEIGHT
                        字符画或字符视频的尺寸, 按字符数量计
  -c, --chars CHARS     使用的字符序列 (默认为 ' .-+{#')
  --font FONT           字体文件路径, **需要等宽字体** (默认为系统字体 Courier New)
  --font-size FONT_SIZE
                        字体大小 (默认为 15)
  --spacing SPACING     行间距 (默认为 0)
  --fill FILL           字符前景色 (默认为白色 '#FFFFFF')
  --bg BG               背景色 (默认为黑色 '#000000')
  --scale SCALE         按比例缩放生成的图像或视频尺寸 (默认不缩放)
  --fourcc FOURCC       视频编码器 (默认为 'mp4v')
```
