
# icon_uxarray

[![codecov](https://codecov.io/gh/jcanton/icon_uxarray/branch/main/graph/badge.svg?token=icon_uxarray_token_here)](https://codecov.io/gh/jcanton/icon_uxarray)
[![CI](https://github.com/jcanton/icon_uxarray/actions/workflows/main.yml/badge.svg)](https://github.com/jcanton/icon_uxarray/actions/workflows/main.yml)

Awesome icon_uxarray created by jcanton

## Install it from PyPI

```bash
pip install icon-uxarray
```

## Usage

Convert an icon grid to be UGRID-compatible

```py
from icon_uxarray import icon_grid_2_ugrid
ugrid_fname = icon_grid_2_ugrid(iconGrid_fname='some_icon_grid.nc')
```

then use it for plotting

```py
import uxarray as ux
import holoviews as hv
import panel as pn

# open dataset
uxds = ux.open_dataset(grid_fname, data_fname)

# static plot
hvplot = uxds['temp'].isel(time=0).isel(height=0).plot()
server = pn.panel(hvplot).show()

# interactive plot
def sliders_plot(itime, iheight):
    return uxds['temp'].isel(time=itime).isel(height=iheight).plot()
torus = hv.DynamicMap(sliders_plot, kdims=['time', 'height'])
hvplot = torus.redim.range(time=(0, len(uxds2.time)), height=(0, len(uxds2.height)))
server = pn.panel(hvplot).show()
```

## Development

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.
