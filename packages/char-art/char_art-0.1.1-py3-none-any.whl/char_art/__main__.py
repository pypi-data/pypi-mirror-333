import argparse
import sys

from . import __version__, default_chars, CharImage, CharVideo


def main(args=None):
    parser = argparse.ArgumentParser(prog='python -m char_art')
    parser.add_argument('-v', '--version', action='version', version=__version__)

    subparsers = parser.add_subparsers(dest='command', required=True)

    # Show command
    display_parser = subparsers.add_parser('display', help='展示字符画或字符视频')
    add_arg = display_parser.add_argument
    add_arg('file', type=str, help='图像或视频的文件路径')
    add_arg('-v', '--video', action='store_true', help='展示字符视频, 若不设置则为字符画')
    add_arg('-s', '--size', type=int, nargs=2, required=True, metavar=('WIDTH', 'HEIGHT'),
            help='字符画或字符视频的尺寸, 按字符数量计')
    add_arg('-c', '--chars', type=str, default=default_chars, help=f"使用的字符序列 (默认为 '{default_chars}')")
    add_arg('-l', '--load', action='store_true', help='在展示字符视频前加载并缓存所有字符帧, 使得播放时更流畅')

    # Save command
    save_parser = subparsers.add_parser('save', help='保存字符画为图像文件 / 字符视频为视频文件')
    add_arg = save_parser.add_argument
    add_arg('file', type=str, help='图像或视频的文件路径')
    add_arg('save_file', type=str, help='生成的图像或视频的保存路径')
    add_arg('-v', '--video', action='store_true', help='保存字符视频, 若不设置则为字符画')
    add_arg('-s', '--size', type=int, nargs=2, required=True, metavar=('WIDTH', 'HEIGHT'),
            help='字符画或字符视频的尺寸, 按字符数量计')
    add_arg('-c', '--chars', type=str, default=default_chars, help=f"使用的字符序列 (默认为 '{default_chars}')")
    add_arg('--font', type=str, default=None, help="字体文件路径, **需要等宽字体** (默认为系统字体 Courier New)")
    add_arg('--font-size', type=int, default=15, help='字体大小 (默认为 15)')
    add_arg('--spacing', type=int, default=0, help='行间距 (默认为 0)')
    add_arg('--fill', type=str, default='#FFFFFF', help="字符前景色 (默认为白色 '#FFFFFF')")
    add_arg('--bg', type=str, default='#000000', help="背景色 (默认为黑色 '#000000')")
    add_arg('--scale', type=float, default=None, help='按比例缩放生成的图像或视频尺寸 (默认不缩放)')
    add_arg('--fourcc', type=str, default='mp4v', help="视频编码器 (默认为 'mp4v')")

    args = parser.parse_args(args)

    try:
        if args.command == 'display':

            if not args.video:
                char_image = CharImage(args.file, args.size, args.chars)
                char_image.display()
            else:
                char_video = CharVideo(args.file, args.size, args.chars)
                if args.load:
                    char_video.load()
                char_video.display()

        elif args.command == 'save':

            if not args.video:
                char_image = CharImage(args.file, args.size, args.chars)
                char_image.save(
                    args.save_file,
                    font=args.font,
                    font_size=args.font_size,
                    spacing=args.spacing,
                    fill=args.fill,
                    bg=args.bg,
                    scale=args.scale
                )
            else:
                char_video = CharVideo(args.file, args.size, args.chars)
                char_video.save(
                    args.save_file,
                    font=args.font,
                    font_size=args.font_size,
                    spacing=args.spacing,
                    fill=args.fill,
                    bg=args.bg,
                    scale=args.scale,
                    fourcc=args.fourcc
                )
    except:
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
