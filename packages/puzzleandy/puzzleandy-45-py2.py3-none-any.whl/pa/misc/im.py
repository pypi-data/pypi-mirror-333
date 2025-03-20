import cv2
from enum import Enum
from .lib import from_cv

class Space(Enum):
	RGB = 0

class Im:
	def __init__(self,path):
		arr = cv2.imread(path)
		arr = from_cv(arr)
		self.arr = arr
		self.space = Space.RGB