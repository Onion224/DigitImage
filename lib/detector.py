"""
    The detector wrapper of ULPR. It will detect the plate roi of a raw image.
"""

import cv2

from lib.config import cfg
# lib methods
from lib.easypr import plate_detect as easypr_detect
from lib.mrcnn import plate_detect as mrcnn_detect
from lib.utils import find_last

_methods = [
    'easypr',  # 0
    'mrcnn',   # 1
]


def detect(src):
    """
        Detector factory
    :param src: raw image
    :return: [[x1, y1, x2, y2, x3, y3, x4, y4]]
    """
    method = cfg.DETECTOR.METHOD
    return eval('_detect_' + _methods[method])(src)


# method 0
def _detect_easypr(src):
    pd = easypr_detect.PlateDetect()
    pd.setPDLifemode(True)
    dir_name = find_last.find_last(cfg.OUTPUT_DIR, 'whether_car')
    return pd.plateDetect(src, str(cfg.OUTPUT_DIR / dir_name / 'models'))


def _detect_mrcnn(src):
    src = cv2.cvtColor(src, cv2.COLOR_RGB2BGR)
    pd = mrcnn_detect.PlateDetect()
    return pd.detect(src, str(cfg.OUTPUT_DIR))
