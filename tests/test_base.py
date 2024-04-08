"""
Test module.
"""

import os
import xarray as xr
import uxarray as ux
import numpy as np
from icon_uxarray.base import icon_grid_2_ugrid, is_boundary_triangle


def test_icon_grid_2_ugrid():
    """
    Test function for converting ICON grid to UGRID format.

    This function creates a temporary ICON grid file, calls the
    `icon_grid_2_ugrid` function to convert the grid to UGRID format, and then
    performs various assertions to validate the output file.

    Returns:
        None
    """
    # Create a temporary ICON grid file
    icon_grid_fname = "temp_icon_grid.nc"
    xr_grid = xr.Dataset(
        {
            "cell_index": (["x", "y"], np.array([[1, 2], [3, 4]])),
            "edge_index": (["x", "y"], np.array([[5, 6], [7, 8]])),
            "vertex_index": (["x", "y"], np.array([[9, 10], [11, 12]])),
        },
        coords={"x": [0, 1], "y": [0, 1]},
    )
    xr_grid.to_netcdf(icon_grid_fname)

    # Call the function
    ugrid_fname = icon_grid_2_ugrid(icon_grid_fname)

    # Assert the output file exists
    assert os.path.isfile(ugrid_fname)

    # Assert the topology information is stored correctly
    ugrid = xr.open_dataset(ugrid_fname)
    assert "mesh" in ugrid
    assert ugrid.mesh.cf_role == "mesh_topology"
    assert ugrid.mesh.topology_dimension == 2
    assert ugrid.mesh.node_dimension == "vertex"
    assert ugrid.mesh.edge_dimension == "edge"
    assert ugrid.mesh.face_dimension == "cell"
    assert ugrid.mesh.node_coordinates == "vlon vlat"
    assert ugrid.mesh.edge_coordinates == "elon elat"
    assert ugrid.mesh.face_coordinates == "clon clat"
    assert ugrid.mesh.face_node_connectivity == "vertex_of_cell"
    assert ugrid.mesh.edge_node_connectivity == "edge_vertices"
    assert ugrid.mesh.face_edge_connectivity == "edge_of_cell"
    assert ugrid.mesh.face_face_connectivity == "neighbor_cell_index"
    assert ugrid.mesh.edge_face_connectivity == "adjacent_cell_of_edge"

    # Clean up the temporary files
    os.remove(icon_grid_fname)
    os.remove(ugrid_fname)


def test_is_boundary_triangle():
    """
    Test case for the is_boundary_triangle function.

    This function creates a temporary ICON grid file, calls the
    is_boundary_triangle function with some test parameters, and asserts that
    the result is of type bool.

    It also cleans up the temporary files after the test is completed.
    """
    # Create a temporary ICON grid file
    icon_grid_fname = "temp_icon_grid.nc"
    xr_grid = xr.Dataset(
        {
            "cell_index": (["x", "y"], np.array([[1, 2], [3, 4]])),
            "edge_index": (["x", "y"], np.array([[5, 6], [7, 8]])),
            "vertex_index": (["x", "y"], np.array([[9, 10], [11, 12]])),
        },
        coords={"x": [0, 1], "y": [0, 1]},
    )
    xr_grid.to_netcdf(icon_grid_fname)

    # Call the function
    grid = ux.Grid.from_netcdf(icon_grid_fname)
    itri = 0
    lims = [0, 1, 0, 1]
    result = is_boundary_triangle(grid, itri, lims)

    # Assert the result
    assert isinstance(result, bool)

    # Clean up the temporary files
    os.remove(icon_grid_fname)
