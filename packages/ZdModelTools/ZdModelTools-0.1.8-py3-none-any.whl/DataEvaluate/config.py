import pandas as pd
import numpy as np


class Config:
    def __init__(self, data, target, features, test_size=0.2, random_state=42):
        self.data_path = data
        self.target = target
        self.features = features
        self.test_size = test_size
        self.random_state = random_state

