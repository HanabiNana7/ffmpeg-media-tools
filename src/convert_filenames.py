import os
import glob
from opencc import OpenCC


def convert_filenames_simplified_to_traditional(directory: str) -> None:
    cc = OpenCC("s2t")

    for old_path in glob.glob(os.path.join(directory, "*")):
        if not os.path.isfile(old_path):
            continue
        new_path = os.path.join(directory, cc.convert(os.path.basename(old_path)))
        if old_path != new_path:
            os.rename(old_path, new_path)
