# sam-plot-extraction
plot extraction using segment anything model


# install virtual environment
```bash
conda create -n spet python=3.10 -y
conda activate spet
```

# install sam plot extraction tool
```bash
pip install sam-plot-extraction
```

# install dependencies
```bash
pip install d2spy openrs-python git+https://github.com/facebookresearch/segment-anything.git

(CPU)
pip install torch torchvision
(GPU)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

conda install gdal -y
```