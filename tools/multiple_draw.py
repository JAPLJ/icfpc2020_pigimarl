from pathlib import Path
from typing import List, Tuple

import cv2
import numpy as np


def draw(
        plot_vectors: List[Tuple[int, int]],
        draw_size: int = 10,
        output_dir: str = '',
        filename: str = 'draw.png',
        draw_color: Tuple[int, int, int] = (255, 255, 255),
        bg_color: Tuple[int, int, int] = (25, 25, 25),
        offset: Tuple[int, int] = (156, 108)  # 大宇宙 galaxy
) -> None:
    """
    output_dir配下にimage_size*draw_sizeの大きさの filename(png) を描画・保存する。
    image_sizeはplot_vectors_listの最小値/最大値から判断する。
    """
    min_x = 10000
    max_x = -10000
    min_y = 10000
    max_y = -10000
    for x, y in plot_vectors:
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)

    width = max(1, max_x - min_x + 1)
    height = max(1, max_y - min_y + 1)

    output_path = Path(output_dir) / filename
    img = np.full(
        (
            height * draw_size,
            width * draw_size,
            3
        ),
        bg_color,
        dtype=np.uint8
    )
    for vector in plot_vectors:
        x = (vector[0] - min_x) * draw_size
        y = (vector[1] - min_y) * draw_size
        cv2.rectangle(
            img,
            (x, y),
            (x + draw_size - 1, y + draw_size - 1),
            draw_color,
            -1
        )

    # draw grid
    img_y, img_x = img.shape[:2]
    step_colors = [
        (1, (80, 80, 80)),
        (5, (200, 100, 100)),
        (10, (100, 180, 100)),
        (50, (100, 100, 200))
    ]
    origin_x = offset[0] * draw_size
    origin_y = offset[1] * draw_size
    for grid_step, color in step_colors:
        step = draw_size * grid_step
        img[origin_y % step:img_y + origin_y:step, :, :] = color
        img[:, origin_x % step:img_x + origin_x:step, :] = color
    img[origin_y:origin_y + 2, :, :] = (255, 255, 255)
    img[:, origin_x:origin_x + 2, :] = (255, 255, 255)

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
    output_dir配下にpngを描画する.
    draw_sizeは1プロットあたりの大きさ。
    filenameは <filename_suffix>_<i>.png で連番
    """
    for i in range(len(plot_vectors_list)):
        plot_vectors = plot_vectors_list[i]
        filename = f'{filename_suffix}_{i}.png'
        draw(
            plot_vectors=plot_vectors,
            draw_size=draw_size,
            output_dir=output_dir,
            filename=filename,
            draw_color=draw_color,
            bg_color=bg_color,
        )
