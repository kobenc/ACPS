import platform
import sys
import time
from shutil import copyfile
from tempfile import TemporaryDirectory

import numpy
from sklearn.datasets import load_breast_cancer

from concrete.ml.deployment import FHEModelClient, FHEModelDev, FHEModelServer
from concrete.ml.sklearn import XGBClassifier


def handle_uploaded_file(f, username):
    with open("acps/encrypted_data/" + username + ".data", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)




server_dir="acps/server/"
def read_data(username):
    with open("acps/encrypted_data/" + username+".data", "rb") as f:
        encrypted_data = f.read()
        return encrypted_data

     
def predict(encrypted_input,username):
      """Send the input to the server and execute on the server in FHE."""
      with open("acps/keys/" + username + ".key", "rb") as f:
          serialized_evaluation_keys = f.read()
      time_begin = time.time()
      encrypted_prediction = FHEModelServer(server_dir).run(
          encrypted_input, serialized_evaluation_keys
      )
      time_end = time.time()
      with open("acps/predictions/" + username + ".pred", "wb") as f:
          f.write(encrypted_prediction)
      return time_end - time_begin
