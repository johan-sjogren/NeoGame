import subprocess
import sys
from pathlib import Path

# install requirements for the eval worker
subprocess.check_output([sys.executable, "-m", "pip", "install", "-r", str(Path(__file__).parent.absolute())+"/requirements.txt"])

from .main import evaluate
