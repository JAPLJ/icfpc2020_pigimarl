from pathlib import Path
from typing import List, Tuple

import cv2
import numpy as np


def draw(
        plot_vectors: List[Tuple[int, int]],
        imagemap_size: Tuple[int, int] = (50, 50),
        draw_size: int = 10,
        output_dir: str = '',
        filename: str = 'draw.png',
        draw_color: Tuple[int, int, int] = (255, 255, 255),
        bg_color: Tuple[int, int, int] = (25, 25, 25),
) -> None:
    """
    output_dir配下にimage_size*draw_sizeの大きさの filename(png) を描画・保存する。
    """
    output_path = Path(output_dir) / filename
    img = np.full(
        (
            imagemap_size[0] * draw_size + draw_size,
            imagemap_size[1] * draw_size + draw_size,
            3
        ),
        bg_color,
        dtype=np.uint8
    )
    for vector in plot_vectors:
        x = vector[0] * draw_size
        y = vector[1] * draw_size
        cv2.rectangle(
            img,
            (x, y),
            (x + draw_size, y + draw_size),
            draw_color,
            -1
        )
    cv2.imwrite(str(output_path), img)


def multipul_draw(
        plot_vectors_list: List[List[Tuple[int, int]]],
        draw_size: int = 10,
        output_dir: str = '',
        filename_suffix: str = 'draw',
        draw_color: Tuple[int, int, int] = (255, 255, 255),
        bg_color: Tuple[int, int, int] = (25, 25, 25),
) -> None:
    """
    output_dir配下に
    plot_vectors_listの最大値から判断した画像サイズでpngを描画する.
    draw_sizeは1プロットあたりの大きさ。
    filenameは <filename_suffix>_<i>.png で連番
    """
    width = 0
    height = 0
    for plot_vectors in plot_vectors_list:
        for x, y in plot_vectors:
            width = x if x > width else width
            height = y if y > height else height

    for i in range(len(plot_vectors_list)):
        plot_vectors = plot_vectors_list[i]
        filename = f'{filename_suffix}_{i}.png'
        draw(
            plot_vectors=plot_vectors,
            imagemap_size=(width, height),
            draw_size=draw_size,
            output_dir=output_dir,
            filename=filename,
            draw_color=draw_color,
            bg_color=bg_color,
        )
