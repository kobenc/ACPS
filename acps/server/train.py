import platform
import sys
import time
from shutil import copyfile
from tempfile import TemporaryDirectory

import numpy
from sklearn.datasets import load_breast_cancer

from concrete.ml.deployment import FHEModelClient, FHEModelDev, FHEModelServer
from concrete.ml.sklearn import XGBClassifier



class OnDiskNetwork:
    def __init__(self):
        self.server_dir = TemporaryDirectory() # pylint: disable=consider-using-with
        self.client_dir = TemporaryDirectory()  # pylint: disable=consider-using-with
        self.dev_dir = TemporaryDirectory()  # pylint: disable=consider-using-with


    def save_server(self):
        copyfile(self.dev_dir.name + "/server.zip", "./server.zip")

    def save_clientconf(self):
        copyfile(self.dev_dir.name + "/client.zip", "./client.zip")
        copyfile(
            self.dev_dir.name + "/serialized_processing.json",
            "./serialized_processing.json",
        )
        
    def cleanup(self):
        """Clean up the temporary folders."""
        self.server_dir.cleanup()
        self.client_dir.cleanup()
        self.dev_dir.cleanup()

X, y = load_breast_cancer(return_X_y=True)

X_model = X[:-10]
y_model = y[:-10] 

n_estimators = 10

# Train the model and compile it
model_dev = XGBClassifier(n_bits=2, n_estimators=n_estimators, max_depth=3)
model_dev.fit(X_model, y_model)
model_dev.compile(X_model)

print("Model trained and compiled.")

# Let's instantiate the network
network = OnDiskNetwork()

fhemodel_dev = FHEModelDev(network.dev_dir.name, model_dev)
fhemodel_dev.save()
network.save_server()
network.save_clientconf()
