"""
借用 pygame 库来渲染字符画的图像, pygame 效率要比 pillow 高得多
"""

import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

try:
    import pygame
except ImportError:
    raise ImportError('保存字符画或字符视频需要额外下载第三方库: pygame')

pygame.font.init()


def get_font(font, size):
    """获取 pygame 字体对象"""
    if font is None:
        font = pygame.font.SysFont('couriernew', size)
    else:
        font = pygame.font.Font(font, size)
    return font


def render(font, text, fill, bg, spacing):
    """pygame 字体渲染文本图像"""
    text = text.splitlines()
    surfaces = []
    max_w = 0
    for line in text:
        surface = font.render(line, True, fill, bg)
        surfaces.append(surface)
        w = surface.get_width()
        if w > max_w:
            max_w = w
    h = font.get_linesize()
    if -spacing <= h:
        edge_t = 0
        edge_b = (h + spacing) * (len(text) - 1) + h
    else:
        edge_t = (h + spacing) * (len(text) - 1)
        edge_b = h
    surface2 = pygame.Surface((max_w, edge_b - edge_t))
    surface2.fill(bg)
    t = -edge_t
    dt = h + spacing
    for surface in surfaces:
        surface2.blit(surface, (0, t))
        t += dt
    return pygame.surfarray.array3d(surface2)
