import numpy as np
import PIL
from fastai import vision

import logger

FILENAME = "resnet34_size=256_bs=32_lr=1e-03_epochs=15.pkl"
LEARNER = vision.load_learner("data", file=FILENAME)
logger.log_info(f"Model loaded '{FILENAME}'", dim=True)


def cv_to_torch(array):
    pil = PIL.Image.fromarray(array)
    torch = vision.Image(vision.pil2tensor(pil, np.float32).div_(255))
    return torch


def get_prediction(ele):
    crop, bbox = ele
    # Learn.predict() will automatically use the transformations your model was
    # trained to be tested on (the transforms passed into the initial DataBunch object)
    category, label, probabilities = LEARNER.predict(cv_to_torch(crop))
    prob = probabilities[label.item()].item()
    category = str(category)
    logger.log_prediction(category, prob, bbox)
    return category, prob
