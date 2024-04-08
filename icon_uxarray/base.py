"""
icon_uxarray base module.

This is the principal module of the icon_uxarray project.
here you put your main classes and objects.

"""

import os
import numpy as np
import xarray as xr
import uxarray as ux


#===============================================================================
def iconGrid2Ugrid(iconGrid_fname: str) -> str:
    """
    Convert an ICON grid to being UGRID-compatible.

    Parameters:
    iconGrid_fname (str): The file path of the ICON grid dataset.

    Returns:
    str: The file path of the UGRID-compatible grid dataset.

    References:
    - UGRID conventions: http://ugrid-conventions.github.io/ugrid-conventions/#2d-triangular-mesh-topology
    """

    # Load grid
    xr_grid = xr.open_dataset(iconGrid_fname)

    # Adapt from Fortran zero basednes... only for real index fields (not all int32
    # arrays contain indices) for example refin_ctl whereas in ICON indices and
    # refin_ctl values
    index_lists = [
        "cell_index", "edge_index", "vertex_index",
        "parent_cell_index", "parent_edge_index", "parent_vertex_index",
        "start_idx_c", "end_idx_c",
        "start_idx_e", "end_idx_e",
        "start_idx_v", "end_idx_v",
        "neighbor_cell_index",
        "edge_of_cell", "vertex_of_cell",
        "adjacent_cell_of_edge", "edge_vertices",
        "cells_of_vertex", "edges_of_vertex", "vertices_of_vertex",
    ]

    for vname in index_lists:
        if vname in set(xr_grid.data_vars.keys()):
            #
            # make it zero-indexed
            xr_grid[vname].data = np.where(xr_grid[vname].data>0, xr_grid[vname].data-1, -1)
            xr_grid[vname].attrs["start_index"] = 0
            xr_grid[vname].attrs["_FillValue"] = -1
            #
            # if needed, transpose
            vshape = xr_grid[vname].shape
            if len(vshape)==2 and (vshape[0] < vshape[1]):
                xr_grid[vname] = xr.DataArray(
                    data = xr_grid[vname].data.T,
                    dims = xr_grid[vname].dims[::-1],
                    coords = xr_grid[vname].coords,
                    attrs = xr_grid[vname].attrs,
                )

    # Store topology information
    xr_grid["mesh"] = xr.DataArray(
        -1, # A dummy value for creating the DataArray with the actual attributes
        attrs=dict(
            cf_role="mesh_topology",
            topology_dimension=2,
            node_dimension="vertex",
            edge_dimension="edge",
            face_dimension="cell",
            node_coordinates="vlon vlat",
            edge_coordinates="elon elat",
            face_coordinates="clon clat",
            face_node_connectivity="vertex_of_cell",
            edge_node_connectivity="edge_vertices",
            face_edge_connectivity="edge_of_cell",
            face_face_connectivity="neighbor_cell_index",
            edge_face_connectivity="adjacent_cell_of_edge",
        ),
    )

    # Save to file
    uGrid_fname = os.path.join(os.path.dirname(iconGrid_fname), 'ux_'+os.path.basename(iconGrid_fname))
    if os.path.isfile(uGrid_fname):
        os.remove(uGrid_fname)
    xr_grid.to_netcdf(uGrid_fname, mode='w', format='NETCDF4')

    return uGrid_fname


#===============================================================================
def isBoundaryTriangle(grid: ux.Grid, itri: int, lims: list[float]) -> bool:
    """
    Determines if a triangle in a grid is a boundary triangle.

    Args:
        grid (ux.Grid): The grid containing the triangle.
        itri (int): The index of the triangle.
        lims (list[float]): The minimum and maximum values for x and y coordinates.

    Returns:
        bool: True if the triangle is a boundary triangle, False otherwise.
    """
    x_min, x_max, y_min, y_max = lims
    tol=1e-6
    nodes = grid.face_node_connectivity[itri].data
    if ((np.abs(grid.node_lon[nodes].data-x_min) < tol).any() and (np.abs(grid.node_lon[nodes].data-x_max) < tol).any()) \
    or ((np.abs(grid.node_lat[nodes].data-y_min) < tol).any() and (np.abs(grid.node_lat[nodes].data-y_max) < tol).any()):
        # opposite sides
        return True
    id_edges = grid.face_edge_connectivity[itri].data
    length_edges = grid.edge_node_distances[id_edges].data
    if length_edges.max() > 2*length_edges.min():
        # elongated
        return True
    return False