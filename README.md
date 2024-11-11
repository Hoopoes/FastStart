<p align="center" width="100%">
  <img src="images/fastapi.svg" alt="fastapi-logo" width="100">
</p>



# FastStart Ultralytics Yolo Implementation Example
This repository's branch demonstrates how to set up a  Ultralytics YOLO for object detection in FastAPI.

## Prerequisites

Before setting up this project, ensure you have a basic understanding of the following tools:

- **[Poetry](https://python-poetry.org)**: Dependency management tool (like npm for Node.js).

- **[Pyenv](https://github.com/pyenv/pyenv)**: Manages multiple Python versions. For windows [pyenv-win](https://github.com/pyenv-win/pyenv-win).


## Setup
1. Initialize Poetry in Your Project:

```bash
poetry init
```

2. Configure Poetry for CPU or GPU Support:

Based on your hardware, you can set up a pyproject.toml file for either CPU or CUDA-enabled GPU (NVIDIA) support.

### CPU Configuration `(pyproject.toml)`
This configuration installs a version of PyTorch optimized for CPU usage.


```toml
[tool.poetry]
name = "project-name"
version = "0.1.0"
description = ""
authors = ["author-name <author-email>"]
readme = "README.md"
package-mode = false


[[tool.poetry.source]]
name = "pytorch-src"
url = "https://download.pytorch.org/whl/cpu"
priority = "explicit"


[[tool.poetry.source]]
name = "PyPI"
priority = "primary"


[tool.poetry.dependencies]
python = "^3.11.0"
torch = {version = "^2.2.0+cpu", source = "pytorch-src"}
torchvision = {version = "^0.17.0+cpu", source = "pytorch-src"}
ultralytics = "8.0.196"
numpy = "1.26.3"


[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

### GPU Configuration `(pyproject.toml)`
This configuration is optimized for NVIDIA GPUs with CUDA support (CUDA 12.1).


```toml
[tool.poetry]
name = "project-name"
version = "0.1.0"
description = ""
authors = ["author-name <author-email>"]
readme = "README.md"
package-mode = false


[[tool.poetry.source]]
name = "pytorch-src"
url = "https://download.pytorch.org/whl/cu121"
priority = "explicit"


[[tool.poetry.source]]
name = "PyPI"
priority = "primary"


[tool.poetry.dependencies]
python = "^3.11.0"
torch = {version = "^2.3.1+cu121", source = "pytorch-src"}
torchvision = {version = "^0.18.0+cu121", source = "pytorch-src"}
ultralytics = "8.2.82"
numpy = "1.26.3"


[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

## Raw Inference (DUMMY NOT YET IMPLEMENTED)

```py
import numpy as np
from fastapi import FastAPI, File, UploadFile
from ultralytics import YOLO


app = FastAPI()
model = YOLO("yolov8n.pt")  # Load a pretrained YOLO model

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    ...
    ...
    return {"detections": detections}
```