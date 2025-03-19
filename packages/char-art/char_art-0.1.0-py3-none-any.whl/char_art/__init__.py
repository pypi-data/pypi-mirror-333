# 方便地制作字符画与字符视频 ~
# 作者↓ (不是鬼图) **需要等宽字体才能正常显示**
#
# {{{{{{{{{{{{{{{{{{{{{{{{{{{{{{##############+{.      -..---... .   .-+{+.
# {{{{{{{{{{{{{{{{{{{{{{{{{{{{{+---+++----++++--.      ---{{{{+---. .-+{++-.  .##
# {{{{{{{{{{{{{{{{{{{{{+++....      ....    .----...   .--{{{{{{{{-.-+{#{{{+++{##{
# {{{{{{{{{{{{{{{{{+----. ......  ...     ..-.    .-..    ...-++{{+.--{{{{{{{{{{{{
# {{{{{{{{{{{{{{{+.-...-. ..                          .        ..-...-{{+--    --
# {{{{{{{{{{#{+-...                                      .           .++--.
# {{{{{{{{#{-..                                                       .----
# {{{{{{##+.                         .....                              .--.  .+-
# {{{{{{{-                         .-------++.                            ... +#{
# {{{{{{.                    .    .-+++++{{{{{-.                         .++++{##+
# {{{{{+                ...--..-...-+{{{{#{{{{{+-                            .....
# {{{{{-         .-.--.-++{{{+{{{{+{{{{########{{-.
# {{{{{-        .-+-----+++{{{{{###########{{++-...          ..
# {{{{{-        +-....        ..-{{#####{+-.     .....        ..          .
# {{{{{{-      ++-+{{{{{{{{+++--++{{{{{{{+---+++{{{{+++---..  ..         --
# {{{{{#{+-    ---+++++----------++{{{{+--..----..  . ....              -##{{{++++
# {{{{#####{-   .+++-...-......--+. ...  .--{++------...... .-----.   .-##########
# {{{{{{{{{{{.-+-#{{+++{{{{++++{{+ .{{{+   -++{{{{{+++++++-.------.  ..{##########
# +++++++++++-.#++{#####{{{{{{{{+.+###{{+.  .-+{{{{{{{+++---+----..  ..+##########
# -------------###{{{{+{++++++---{####{{+-....-+++++++++++++++---..  ..-##########
# ---+++++++++-{##########{{+++########{{++++-.+{########{{{+++--..  .-{##########
# ---------...-{#########{+++{##{{{###{+-------++{######{{{{+++--.. ..+{##########
# {+---+{{+++{{{#######{{{{{###{{{{{{{++---.---+++{{#{{{{{{{++++-......{{#########
# +--------..-+#########{#{{###{{{{{{{{{+++++++---+{{{{{{{{+++++-....-.+{#########
# .............+##########{{++----------.........-+{{{{{{{++++++-....-..{{{#######
# .............-##########{{{##{{{{+++++-------+++{{#{{{+++++++-..-..-. +{########
# ...........-+{{######{{{{########{{+++{{{{{{{{{{{{+++++++++++--.....- -{{{{{####
# ....-+-+{{{##########{{{{##########{{{{{{{{{{+++++++++++++{#####{+---.-{{#######
# {{{####################{#########{{{{{{{{{{{+++++++++----+{###########{{########
# #####################{########{{{{{{{{++++++++++---------. +{{{#################
# #####################{######{{+----------.---------------.+##{{{{{##############
# #####################{{#######{{++++---...---------+++--.+####{{################
# ####################################{{{++++++++-++++---+########################
# #####################################{{{{{++++------+{##########################
# ##########################+{#########{{{{{{++-+++{{###############{{############

import sys
import time

import cv2
import numpy as np

# python >= 3.6.0

__version__ = '0.1.0'

__all__ = ['CharImage', 'CharVideo']

default_chars = ' .-+{#'  # 默认使用的字符序列


class Base:
    """内部类, 字符画和字符视频的基类"""

    def __init__(self, size, chars):
        self._size = self._validate_size(size)  # 内部参数, 字符画的尺寸
        self._chars, self._char_lut = self._validate_chars(chars)  # 内部参数, 字符画使用的字符序列, 以及像素点亮度到字符的查找表
        self._char_img = None  # 内部参数, 字符画或字符视频字符帧缓存, 懒加载

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        size0 = self._size
        self._size = self._validate_size(value)
        # 参数发生变动后清空字符画缓存
        if self._char_img is not None:
            if self._size != size0:
                self._char_img = None

    @property
    def chars(self):
        return self._chars

    @chars.setter
    def chars(self, value):
        chars0 = self._chars
        self._chars, self._char_lut = self._validate_chars(value)
        # 参数发生变动后清空字符画缓存
        if self._char_img is not None:
            if self._chars != chars0:
                self._char_img = None

    @staticmethod
    def _validate_size(size):
        """内部函数, 验证 size 参数"""
        size = tuple(size)
        w, h = size
        if not isinstance(w, int) or not isinstance(h, int):
            raise TypeError('width and height must be a integer')
        if w <= 0 or h <= 0:
            raise ValueError('width and height must be > 0')
        return size

    @staticmethod
    def _validate_chars(chars):
        """内部函数, 验证 chars 参数, 并给出亮度到字符的查找表"""
        if not isinstance(chars, str):
            chars = ''.join(chars)
        if len(chars) <= 1:
            raise ValueError('length of chars must be > 1')
        chars_array = np.fromiter(chars, dtype='<U1')
        char_lut = np.arange(0, 256 * chars_array.size, chars_array.size)
        char_lut >>= 8
        char_lut = chars_array[char_lut]
        return chars, char_lut

    @staticmethod
    def _gray2char_img(img, size, char_lut):
        """内部函数, 将灰度图 (numpy.ndarray) 转化为字符画"""
        img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
        char_pixel = char_lut[img]
        char_img = '\n'.join(char_pixel.view(f'<U{size[0]}').ravel())
        return char_img

    @staticmethod
    def _char2img(font, char_img, spacing, fill, bg, scale, size):
        """内部函数, 将字符画渲染为图像 (numpy.ndarray)"""
        from ._pygame import render

        img = render(font, char_img, fill=fill, bg=bg, spacing=spacing)
        img = cv2.transpose(img)  # pygame 是 (width, height, 3), opencv 是 (height, width, 3)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # pygame 是 RGB, opencv 是 BGR

        if scale is not None:
            if scale != 1.0:
                img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

        elif size is not None:
            height, width, _ = img.shape
            if (width, height) != size:
                img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)

        return img


class CharImage(Base):
    """字符画"""
    __slots__ = ('_size', '_chars', '_char_lut', '_img', '_char_img')

    def __init__(self, img_fp, size, chars=default_chars):
        """
        初始化方法
        :param img_fp: 图像的文件路径
        :param size: 字符画的尺寸, 按字符数量计
        :param chars: 字符画使用的字符序列，索引越往右字符的视觉亮度应当越大, 默认为 ' .-+{#'
        """
        super().__init__(size, chars)
        self._img = cv2.imread(img_fp, cv2.IMREAD_GRAYSCALE)  # 内部参数, 灰度图像
        if self._img is None:
            raise RuntimeError(f'can not open image file: {img_fp}')

    def __str__(self):
        if self._char_img is None:
            self._char_img = self._gray2char_img(self._img, self.size, self._char_lut)
        return self._char_img

    def display(self):
        """展示字符画"""
        print(self)

    def save(self, save_file, *, font=None, font_size=15, spacing=0, fill='#FFFFFF', bg='#000000', scale=None):
        """
        保存字符画为图像文件
        :param save_file: 图像的保存路径
        :param font: 字体文件路径, **需要等宽字体**, 默认为系统字体 'Courier New'
        :param font_size: 字体大小, 默认为 15
        :param spacing: 行间距, 默认为 0
        :param fill: 字符前景色, 默认为白色 '#FFFFFF'
        :param bg: 图像背景色, 默认为黑色 '#000000'
        :param scale: 按比例缩放生成的图像尺寸, 默认不缩放
        """
        from ._pygame import get_font

        font = get_font(font, font_size)
        img = self._char2img(font, str(self), spacing=spacing, fill=fill, bg=bg, scale=scale, size=None)
        cv2.imwrite(save_file, img)


class CharVideo(Base):
    """字符视频"""
    __slots__ = ('_size', '_chars', '_char_lut', '_cap', '_fps', '_frames', '_char_img')

    def __init__(self, video_fp, size, chars=default_chars):
        """
        初始化方法
        :param video_fp: 视频的文件路径或摄像头索引
        :param size: 字符视频的尺寸, 按字符数量计
        :param chars: 字符视频使用的字符序列，索引越往右字符的视觉亮度应当越大, 默认为 ' .-+{#'
        """
        super().__init__(size, chars)
        self._cap = cv2.VideoCapture(video_fp)  # 内部参数, 视频对象
        if not self._cap.isOpened():
            self._cap.release()
            raise RuntimeError(f'can not open video file or camera: {video_fp}')
        self._fps = self._cap.get(cv2.CAP_PROP_FPS)  # 内部参数, 视频帧率
        self._frames = None  # 内部参数, 每帧灰度图像缓存, 懒加载

    def __del__(self):
        # 删除对象时释放视频资源
        if hasattr(self, '_cap'):
            self._cap.release()

    def load(self):
        """一次性加载并缓存视频的所有帧, 以及对应的字符画"""
        if self._frames is None:
            self._frames = list(self._get_frames())
            self._cap.release()

        if self._char_img is None:
            self._char_img = [self._gray2char_img(frame, self._size, self._char_lut) for frame in self._frames]

    def get_frame(self, index):
        """
        按帧索引获得某一帧的字符画
        :param index: 帧索引
        :return: CharImage 对象
        """
        if not isinstance(index, int):
            raise TypeError('index must be a integer')
        if index < 0:
            raise IndexError('index must be >= 0')

        if self._frames is not None:
            if index >= len(self._frames):
                return
            frame = self._frames[index]
        else:
            frame = next(self._get_frames(index), None)
            if frame is None:
                return

        if self._char_img is not None:
            if index >= len(self._char_img):
                return
            char_img = self._char_img[index]
        else:
            char_img = None

        char_frame = object.__new__(CharImage)
        char_frame._size = self.size
        char_frame._chars = self.chars
        char_frame._char_lut = self._char_lut.copy()
        char_frame._img = frame.copy()
        char_frame._char_img = char_img
        return char_frame

    def display(self):
        """
        直接在默认输出终端(sys.stdout)播放(打印)字符视频
        需要支持 ANSI 转义代码的终端才能正常播放, 并且若字符视频的尺寸超过输出终端的尺寸则播放时可能会有问题
        若遇到不正常播放情况, 建议保存视频后再播放
        """
        char_imgs = self._iter_char_imgs()

        write = sys.stdout.write
        flush = sys.stdout.flush
        perf_counter = time.perf_counter
        sleep = time.sleep

        d = 1 / self._fps
        cursor_reset = '\x1b[H'

        write('\x1b[?25l\n\x1b[2J')  # 隐藏光标, 换行, 清屏
        try:
            tic = perf_counter()
            for char_img in char_imgs:
                write(cursor_reset)  # 移动光标到起始位置
                write(char_img)
                flush()
                tic += d
                toc = perf_counter()
                if toc < tic:
                    sleep(tic - toc)
                else:
                    tic = toc
        finally:
            write('\n\x1b[?25h')  # 换行, 显示光标

    def save(self, save_file, *, font=None, font_size=15, spacing=0, fill='#FFFFFF', bg='#000000', scale=None,
             fourcc='mp4v'):
        """
        保存字符视频为视频文件
        :param save_file: 视频的保存路径
        :param font: 字体文件路径, **需要等宽字体**, 默认为系统字体 'Courier New'
        :param font_size: 字体大小, 默认为 15
        :param spacing: 行间距, 默认为 0
        :param fill: 字符前景色, 默认为白色 '#FFFFFF'
        :param bg: 视频背景色, 默认为黑色 '#000000'
        :param scale: 按比例缩放生成的视频尺寸, 将第一帧图像按比例缩放, 后面的所有帧保持和第一帧大小一致, 默认不缩放
        :param fourcc: 视频编码器, 默认为 'mp4v'
        """
        from ._pygame import get_font

        char_imgs = self._iter_char_imgs()

        font = get_font(font, font_size)

        img0 = self._char2img(font, next(char_imgs), spacing=spacing, fill=fill, bg=bg, scale=scale, size=None)
        height, width, _ = img0.shape
        size = (width, height)

        fourcc = cv2.VideoWriter_fourcc(*fourcc)
        video = cv2.VideoWriter(save_file, fourcc, self._fps, size)
        video.write(img0)
        for char_img in char_imgs:
            img = self._char2img(font, char_img, spacing=spacing, fill=fill, bg=bg, scale=None, size=size)
            video.write(img)
        video.release()

    def _get_frames(self, from_=0):
        """内部函数, 生成逐帧的灰度图像"""
        self._cap.set(cv2.CAP_PROP_POS_FRAMES, from_)
        while True:
            ret, frame = self._cap.read()
            if not ret:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            yield frame

    def _iter_char_imgs(self):
        """内部函数, 返回字符帧的可迭代对象"""
        if self._char_img is not None:
            char_imgs = iter(self._char_img)
        else:
            if self._frames is not None:
                frames = self._frames
            else:
                frames = self._get_frames()
            char_imgs = (self._gray2char_img(frame, self.size, self._char_lut) for frame in frames)
        return char_imgs
