import os
import sys

from openatlas import app

sys.path.append('/usr/local/openatlas/')
os.environ['INSTANCE_PATH'] = f'{os.path.dirname(os.path.abspath(__file__))}/'

if __name__ == "__main__":
    app.run()
