import cv2
import torch
import numpy as np
from pathlib import Path
from pyzjr.utils.check import is_file
from pyzjr.augmentation.augments import resizepad

def read_gray(filename):
    if not is_file(filename):
        raise ValueError(f"The file {filename} does not exist.")
    if isinstance(filename, Path):
        filename = str(filename.resolve())
    return cv2.imdecode(np.fromfile(filename, np.uint8), cv2.IMREAD_GRAYSCALE)

def read_bgr(filename):
    if not is_file(filename):
        raise ValueError(f"The file {filename} does not exist.")
    if isinstance(filename, Path):
        filename = str(filename.resolve())
    return cv2.imdecode(np.fromfile(filename, np.uint8), cv2.IMREAD_COLOR)

def read_rgb(filename):
    if not is_file(filename):
        raise ValueError(f"The file {filename} does not exist.")
    if isinstance(filename, Path):
        filename = str(filename.resolve())
    return cv2.imdecode(np.fromfile(filename, np.uint8), cv2.IMREAD_COLOR)[:, :, ::-1]

def read_tensor(filename, target_shape, device=None, use_pad=False, pad_color=(128, 128, 128)):
    if device is None:
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    rgb_image = read_rgb(filename)
    if use_pad:
        image = resizepad(rgb_image, target_shape, pad_color)
    else:
        image = cv2.resize(rgb_image, target_shape)
    image = image.astype(np.float32) / 255.0
    image_tensor = torch.from_numpy(image).permute(2, 0, 1).unsqueeze(0)
    return image_tensor.to(device)