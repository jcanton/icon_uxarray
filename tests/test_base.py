"""
Test module.
"""

import os
import pytest
import xarray as xr
import uxarray as ux
from icon_uxarray.base import (
    icon_grid_2_ugrid,
    is_boundary_triangle,
    remove_torus_boundaries,
)

ICON_GRID_FNAME = "Torus_Triangles_100m_x_100m_res5m.nc"


def test_icon_grid_2_ugrid():
    """
    Test function for converting ICON grid to UGRID format.

    This function tests the conversion of an ICON grid file to UGRID format.
    It checks if the output file exists and verifies the correctness of the
    topology information stored in the UGRID dataset.

    Returns:
        None
    """
    # Call the function
    ugrid_fname = icon_grid_2_ugrid(ICON_GRID_FNAME)

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

    # test file overwriting
    ugrid_fname = icon_grid_2_ugrid(ICON_GRID_FNAME)
    assert os.path.isfile(ugrid_fname)

    # Clean up the temporary files
    os.remove(ugrid_fname)


def test_is_boundary_triangle():
    """
    Test case for the is_boundary_triangle function.

    This function tests the behavior of the is_boundary_triangle function by
    calling it with a grid, triangle index, and boundary limits, and asserting
    that the result is a boolean value.

    It also cleans up any temporary files created during the test.

    Returns:
        None
    """
    ugrid_fname = icon_grid_2_ugrid(ICON_GRID_FNAME)

    # Call the function
    grid = ux.open_grid(ugrid_fname)
    itri = 0
    lims = [
        float(grid.node_lon.min()),
        float(grid.node_lon.max()),
        float(grid.node_lat.min()),
        float(grid.node_lat.max()),
    ]
    result = is_boundary_triangle(grid, itri, lims)

    # Assert the result
    assert isinstance(result, bool)

    face_ids = []
    for itri in range(grid.n_face):
        if is_boundary_triangle(grid, itri, lims):
            face_ids.append(itri)

    expected = [
        30, 31, 62, 63, 94, 95, 126, 127, 158, 159, 189, 190, 191, 217,
        218, 219, 220, 222, 223, 245, 246, 247, 248, 254, 255, 273, 274, 275,
        276, 286, 287, 301, 302, 303, 304, 318, 319, 329, 330, 331, 332, 350,
        351, 357, 358, 359, 360, 382, 383, 384, 385, 386, 387, 388, 414, 415
        ]

    assert face_ids == expected

    # Clean up the temporary files
    os.remove(ugrid_fname)


def test_remove_torus_boundaries():
    """
    Test function for removing torus boundary triangles from a UX grid or
    dataset.
    """

    ugrid_fname = icon_grid_2_ugrid(ICON_GRID_FNAME)
    grid = ux.open_grid(ugrid_fname)

    # Call the function
    result = remove_torus_boundaries(grid)

    # Assert the result
    assert isinstance(result, ux.Grid)
    assert result.n_face == 360
    assert result.node_lon.values.shape == (208,)
    assert result.face_node_connectivity.shape == (360, 3)

    # Create a sample UX dataset
    dataset = ux.UxDataset(
        uxgrid=grid,
        data_vars={
            "temperature": xr.DataArray(range(grid.n_face), dims="n_face")
            },
    )

    # Call the function
    result = remove_torus_boundaries(dataset)

    # Assert the result
    assert isinstance(result, ux.UxDataset)
    assert isinstance(result.uxgrid, ux.Grid)
    assert result.uxgrid.n_face == 360
    assert result.uxgrid.node_lon.values.shape == (208,)
    assert result.uxgrid.face_node_connectivity.shape == (360, 3)
    assert float(result.temperature.min()) == 0.0
    assert float(result.temperature.max()) == 413

    # Test with invalid grid
    invalid_grid = None
    with pytest.raises(Exception) as e_info:
        remove_torus_boundaries(invalid_grid)

    # Clean up the temporary files
    os.remove(ugrid_fname)
