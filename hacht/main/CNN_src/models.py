from . import InceptionV3
from . import DenseNet161
from . import TraditionalCNN
from . import SqueezeNet
from . import FractalNet

def get_model(num_classes, weights=None, m=1):
	model = None
	default_size = 229
	img_size = default_size

	if m == "densenet161":
		model = DenseNet161.get_model
	elif m == "inceptionv3":
		model = InceptionV3.get_model
		img_size = 299
	elif m == "traditionalcnn":
		model = TraditionalCNN.get_model
	elif m == "squeezenet":
		model = SqueezeNet.get_model
		img_size = 256
	elif m == "fractalnet":
		model = FractalNet.get_model
		img_size = 128

	return (model(num_classes, weights), img_size)