from typing import Sequence, Union, Optional

__all__ = ['CharImage', 'CharVideo']


class Base:

    @property
    def size(self) -> tuple[int, int]:
        ...

    @size.setter
    def size(self, value: tuple[int, int]) -> None:
        ...

    @property
    def chars(self) -> str:
        ...

    @chars.setter
    def chars(self, value: Sequence[str]) -> None:
        ...


class CharImage(Base):
    def __init__(
            self,
            img_fp: str,
            size: tuple[int, int],
            chars: Sequence[str] = ' .-+{#'
    ) -> None:
        ...

    def __str__(self) -> str:
        ...

    def display(self) -> None:
        ...

    def save(
            self,
            save_file: str,
            *,
            font: str = None,
            font_size: int = 15,
            spacing: int = 0,
            fill: Union[str, tuple[int, int, int]] = '#FFFFFF',
            bg: Union[str, tuple[int, int, int]] = '#000000',
            scale: float = None
    ) -> None:
        ...


class CharVideo(Base):
    def __init__(
            self,
            video_fp: Union[str, int],
            size: tuple[int, int],
            chars: Sequence[str] = ' .-+{#'
    ) -> None:
        ...

    def __del__(self) -> None:
        ...

    def load(self) -> None:
        ...

    def get_frame(self, index: int) -> Optional[CharImage]:
        ...

    def display(self) -> None:
        ...

    def save(
            self,
            save_file: str,
            *,
            font: str = None,
            font_size: int = 15,
            spacing: int = 0,
            fill: Union[str, tuple[int, int, int]] = '#FFFFFF',
            bg: Union[str, tuple[int, int, int]] = '#000000',
            scale: float = None,
            fourcc: str = 'mp4v'
    ) -> None:
        ...
