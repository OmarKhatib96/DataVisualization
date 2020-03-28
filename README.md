# Integrated Process Control Framework


Integrated Process Control Framework is a visualization tool has been developed using Python. It allows us through an interactive
layout to visualize the correlation of different parameters involved in the semiconductor
industry.
After days of searching, we’ve found out that the Python library Plotly is the best package for
visualization, as it allows an interactive use through an HTML file. This library was coupled
with the python-igraph library which is responsible for showing the network in 3D.
As for the GUI, our choice landed on WxPython because it’s an open-source, popular and welldocumented library. Of course, because we couldn’t deal with the algorithmic part of the
visualization, the GUI can still be improved by filling the functions that we left as prototypes
(for exemple in the setting function). However the UI allows to import data and to launch the
visualization.

## Software Requirements

Use the package manager [pip3](https://pip.pypa.io/en/stable/) to install the following python libraries

```bash
pip3 install plotly wxPython pandas python-igraph PIL matplotlib
```

## Installation
Use the package manager [pip3](https://pip.pypa.io/en/stable/) to install Integrated Process Control Framework

```bash
pip3 install -i https://test.pypi.org/simple/ package-visualization-tool-PE-emse2020
```

## Usage

```python

from package_visualization import run_ui
run_ui.run_visualization()
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)









