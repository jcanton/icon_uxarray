from icon_uxarray.base import NAME


def test_base():
    assert NAME == "icon_uxarray"

import os
import xarray as xr
import uxarray as ux
import numpy as np
from icon_uxarray.base import iconGrid2Ugrid, isBoundaryTriangle


def test_iconGrid2Ugrid():
    # Create a temporary ICON grid file
    iconGrid_fname = "temp_icon_grid.nc"
    xr_grid = xr.Dataset(
        {
            "cell_index": (["x", "y"], np.array([[1, 2], [3, 4]])),
            "edge_index": (["x", "y"], np.array([[5, 6], [7, 8]])),
            "vertex_index": (["x", "y"], np.array([[9, 10], [11, 12]])),
        },
        coords={"x": [0, 1], "y": [0, 1]},
    )
    xr_grid.to_netcdf(iconGrid_fname)

    # Call the function
    uGrid_fname = iconGrid2Ugrid(iconGrid_fname)

    # Assert the output file exists
    assert os.path.isfile(uGrid_fname)

    # Assert the topology information is stored correctly
    uGrid = xr.open_dataset(uGrid_fname)
    assert "mesh" in uGrid
    assert uGrid.mesh.cf_role == "mesh_topology"
    assert uGrid.mesh.topology_dimension == 2
    assert uGrid.mesh.node_dimension == "vertex"
    assert uGrid.mesh.edge_dimension == "edge"
    assert uGrid.mesh.face_dimension == "cell"
    assert uGrid.mesh.node_coordinates == "vlon vlat"
    assert uGrid.mesh.edge_coordinates == "elon elat"
    assert uGrid.mesh.face_coordinates == "clon clat"
    assert uGrid.mesh.face_node_connectivity == "vertex_of_cell"
    assert uGrid.mesh.edge_node_connectivity == "edge_vertices"
    assert uGrid.mesh.face_edge_connectivity == "edge_of_cell"
    assert uGrid.mesh.face_face_connectivity == "neighbor_cell_index"
    assert uGrid.mesh.edge_face_connectivity == "adjacent_cell_of_edge"

    # Clean up the temporary files
    os.remove(iconGrid_fname)
    os.remove(uGrid_fname)
    
def test_isBoundaryTriangle():
    # Create a temporary ICON grid file
    iconGrid_fname = "temp_icon_grid.nc"
    xr_grid = xr.Dataset(
        {
            "cell_index": (["x", "y"], np.array([[1, 2], [3, 4]])),
            "edge_index": (["x", "y"], np.array([[5, 6], [7, 8]])),
            "vertex_index": (["x", "y"], np.array([[9, 10], [11, 12]])),
        },
        coords={"x": [0, 1], "y": [0, 1]},
    )
    xr_grid.to_netcdf(iconGrid_fname)

    # Call the function
    grid = ux.Grid.from_netcdf(iconGrid_fname)
    itri = 0
    lims = [0, 1, 0, 1]
    result = isBoundaryTriangle(grid, itri, lims)

    # Assert the result
    assert isinstance(result, bool)

    # Clean up the temporary files
    os.remove(iconGrid_fname)