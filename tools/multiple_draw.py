from pathlib import Path
from typing import List, Optional, Tuple

import cv2
import numpy as np

from annotate_picture import Annotation

DRAW_CORORS = [
    (80, 200, 200),
    (200, 80, 200),
    (200, 200, 80),
    (80, 80, 200),
    (80, 200, 80),
    (200, 80, 80),
    (150, 80, 200),
    (80, 200, 150),
]
FONT = cv2.FONT_HERSHEY_SIMPLEX


def index_to_color_alpha(i: int) -> Tuple[Tuple[int, int, int], int]:
    if i == 0:
        return (255, 255, 255), 1
    else:
        return DRAW_CORORS[(i - 1) % len(DRAW_CORORS)], 0.7


def draw_grid(img: np.ndarray, min_x, min_y, draw_size=10) -> np.ndarray:
    img_y, img_x = img.shape[:2]
    step_colors = [
        (1, (80, 80, 80)),
        (5, (200, 100, 100)),
        (10, (100, 180, 100)),
        (50, (100, 100, 200))
    ]
    origin_x = -min_x * draw_size
    origin_y = -min_y * draw_size
    for grid_step, color in step_colors:
        step = draw_size * grid_step
        img[origin_y % step:img_y + origin_y:step, :, :] = color
        img[:, origin_x % step:img_x + origin_x:step, :] = color
    white = (255, 255, 255)
    img[origin_y:origin_y + 2, :, :] = white
    img[:, origin_x:origin_x + 2, :] = white
    # draw grid num
    text_step = 10 * draw_size
    for y in range(origin_y % text_step, img_y, text_step):
        x = origin_x
        cv2.putText(
            img,
            str(int((origin_y - y) / draw_size)), (x, y),
            FONT,
            0.7,
            white,
            1,
            cv2.LINE_AA
        )
    for x in range(origin_x % text_step, img_x, text_step):
        y = origin_y
        cv2.putText(
            img,
            str(int((x - origin_x) / draw_size)), (x, y),
            FONT,
            0.7,
            white,
            1,
            cv2.LINE_AA
        )
    return img


def draw_annotation_list(
        img: np.ndarray,
        annotation_list: List[Annotation],
        draw_size: int,
        min_x: int,
        min_y: int,
        color: Tuple[int, int, int] = (0, 100, 0)
):
    tmp = np.zeros(img.shape, np.uint8)
    # 透過マスク
    for annotation in annotation_list:
        x0 = (annotation.min_x - min_x) * draw_size
        y0 = (annotation.min_y - min_y) * draw_size
        x1 = (annotation.max_x - min_x + 1) * draw_size
        y1 = (annotation.max_y - min_y + 1) * draw_size

        cv2.rectangle(
            tmp,
            (x0, y0),
            (x1, y1),
            color,
            cv2.FILLED
        )
    img = cv2.addWeighted(img, 0.8, tmp, 0.5, 1)
    # もっかいテキスト塗る
    for annotation in annotation_list:
        x0 = (annotation.min_x - min_x) * draw_size
        y0 = (annotation.min_y - min_y) * draw_size
        y1 = (annotation.max_y - min_y) * draw_size
        cv2.putText(
            img,
            str(annotation.val),
            (x0, y1),
            FONT,
            (y1-y0)/50, 
            (0, 0, 0),
            2,
            cv2.LINE_AA
        )
        cv2.putText(
            img,
            str(annotation.val),
            (x0, y1),
            FONT,
            (y1-y0)/50, 
            (255, 255, 255),
            1,
            cv2.LINE_AA
        )
    return img


def draw(
        plot_vectors: List[Tuple[int, int]],
        draw_size: int = 10,
        output_dir: str = '',
        filename: str = 'draw.png',
        draw_color: Tuple[int, int, int] = (255, 255, 255),
        bg_color: Tuple[int, int, int] = (25, 25, 25),
        show_grid: bool = True,
        annotation_list: Optional[List[Annotation]] = None
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

    if show_grid:
        draw_grid(
            img=img,
            min_x=min_x,
            min_y=min_y,
            draw_size=draw_size
        )

    if annotation_list is not None:
        img = draw_annotation_list(
            img=img,
            annotation_list=annotation_list,
            draw_size=draw_size,
            min_x=min_x,
            min_y=min_y,
        )

    cv2.imwrite(str(output_path), img)
    return img


def multipul_draw(
        plot_vectors_list: List[List[Tuple[int, int]]],
        draw_size: int = 10,
        output_dir: str = '',
        filename_suffix: str = 'draw',
        draw_color: Tuple[int, int, int] = (255, 255, 255),
        bg_color: Tuple[int, int, int] = (25, 25, 25),
        annotation_lists: Optional[List[List[Annotation]]] = None
) -> None:
    """
    output_dir配下にpngを描画する.
    draw_sizeは1プロットあたりの大きさ。
    filenameは <filename_suffix>_<i>.png で連番
    """
    for i in range(len(plot_vectors_list)):
        draw_color, _ = index_to_color_alpha(i)
        plot_vectors = plot_vectors_list[i]
        filename = f'{filename_suffix}_{i}.png'
        draw(
            plot_vectors=plot_vectors,
            draw_size=draw_size,
            output_dir=output_dir,
            filename=filename,
            draw_color=draw_color,
            bg_color=bg_color,
            annotation_list=None if annotation_lists is None else annotation_lists[i]
        )

    multilayer_draw(
        plot_vectors_list=plot_vectors_list,
        output_dir=output_dir,
        annotation_lists=annotation_lists,
        filename=f'{filename_suffix}_layered.png',
    )


def multilayer_draw(
        plot_vectors_list: List[List[Tuple[int, int]]],
        draw_size: int = 10,
        output_dir: str = '',
        filename: str = 'draw_layered.png',
        draw_color: Tuple[int, int, int] = (255, 255, 255),
        bg_color: Tuple[int, int, int] = (25, 25, 25),
        show_grid: bool = True,
        annotation_lists: Optional[List[List[Annotation]]] = None
) -> None:
    min_x = 10000
    max_x = -10000
    min_y = 10000
    max_y = -10000
    for plot_vectors in plot_vectors_list:
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

    # 一番最後に最初の画像を
    for i in range(len(plot_vectors_list)):
        plot_vectors = plot_vectors_list[i]
        draw_color, alpha = index_to_color_alpha(i)

        tmp = np.zeros(img.shape, np.uint8)
        for vector in plot_vectors:
            x = (vector[0] - min_x) * draw_size
            y = (vector[1] - min_y) * draw_size
            cv2.rectangle(
                tmp,
                (x, y),
                (x + draw_size - 1, y + draw_size - 1),
                draw_color,
                cv2.FILLED
            )
        img = cv2.addWeighted(img, 1, tmp, alpha, 1)

    draw_grid(
        img=img,
        min_x=min_x,
        min_y=min_y,
        draw_size=draw_size
    )
    if annotation_lists is not None:
        for annotation_list in annotation_lists:
            img = draw_annotation_list(
                img=img,
                annotation_list=annotation_list,
                draw_size=draw_size,
                min_x=min_x,
                min_y=min_y,
            )
    cv2.imwrite(str(output_path), img)
