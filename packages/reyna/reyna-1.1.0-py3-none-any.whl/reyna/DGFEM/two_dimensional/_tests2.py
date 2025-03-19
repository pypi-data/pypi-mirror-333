import numpy as np
import time
import matplotlib.pyplot as plt

from reyna.polymesher.two_dimensional.domains import RectangleDomain
from reyna.polymesher.two_dimensional.main import poly_mesher
from reyna.polymesher.two_dimensional.visualisation import display_mesh

from reyna.DGFEM.two_dimensional.main import DGFEM
from reyna.geometry.two_dimensional.DGFEM import DGFEMGeometry
from reyna.DGFEM.two_dimensional.plotter import plot_DG


def is_block_lower_triangular(matrix, block_size):

    n = matrix.shape[0]

    if matrix.shape[1] != n or n % block_size != 0:
        return False

    num_blocks = n // block_size

    for i in range(num_blocks):
        for j in range(i + 1, num_blocks):
            row_start, col_start = i * block_size, j * block_size
            row_end, col_end = row_start + block_size, col_start + block_size

            if not np.all(matrix[row_start:row_end, col_start:col_end] == 0):
                return False

    return True


solution = lambda x: np.sin(np.pi * x[:, 0]) * np.sin(np.pi * x[:, 1])

dom = RectangleDomain(np.array([[-1, 1], [-1, 1]]))

_original_time = 5.83502

_time = time.time()

poly_mesh = poly_mesher(dom, max_iterations=10, n_points=10_000)

print(f"Time: {time.time() - _time:.5f}")
print(f"Time saved: {_original_time - (time.time() - _time):.5f}")

display_mesh(poly_mesh)

raise ValueError
# display_mesh(poly_mesh)
# The cleaner is working like a charm....?
# poly_mesh = poly_mesher_cleaner(poly_mesh)
# display_mesh(poly_mesh)

geometry = DGFEMGeometry(poly_mesh)

# raise ValueError

# Section: Testing

from matplotlib.patches import Polygon

# Test triangle to polygon

# fig, ax = plt.subplots()
#
# for k, region in enumerate(geometry.mesh.filtered_regions):
#     ax.add_patch(Polygon(geometry.nodes[region, :], linewidth=1.0, edgecolor="black"))
#     centroid = np.mean(geometry.nodes[region, :], axis=0)
#     ax.annotate(f"{k}", centroid, c='red')
#
# for k, triangle in enumerate(geometry.subtriangulation):
#     ax.add_patch(Polygon(geometry.nodes[triangle, :], linewidth=1.0, edgecolor="black", alpha=0.1))
#     centroid = np.mean(geometry.nodes[triangle, :], axis=0)
#     ax.annotate(f"{geometry.triangle_to_polygon[k]}", centroid)
#
#
# ax.set_xlim(-1.15, 1.15)
# ax.set_ylim(-1.15, 1.15)
# plt.show()

# Test boundary edges + normals
# fig, ax = plt.subplots()
#
# for k, region in enumerate(geometry.mesh.filtered_regions):
#     ax.add_patch(Polygon(geometry.nodes[region, :], linewidth=1.0, edgecolor="black"))
#     centroid = np.mean(geometry.nodes[region, :], axis=0)
#     ax.annotate(f"{k}", centroid, c='red')
#
# for k, edge in enumerate(geometry.boundary_edges):
#     ax.plot(geometry.nodes[edge, 0], geometry.nodes[edge, 1], 'o', ls='-', ms=8, c="r")
#     centroid = np.mean(geometry.nodes[edge, :], axis=0)
#     ax.quiver(*centroid, *geometry.boundary_normals[k])
#
# ax.set_xlim(-1.15, 1.15)
# ax.set_ylim(-1.15, 1.15)
# plt.show()

# Test interior edges + normals

# print(geometry.interior_edges.shape, geometry.interior_normals.shape, geometry.interior_edges_to_element.shape)

# fig, ax = plt.subplots()
#
# for k, region in enumerate(geometry.mesh.filtered_regions):
#     # ax.add_patch(Polygon(geometry.nodes[region, :], linewidth=1.0, edgecolor="black", al))
#     centroid = np.mean(geometry.nodes[region, :], axis=0)
#     ax.annotate(f"{k}", centroid)
#
# for k, edge in enumerate(geometry.interior_edges):
#     ax.plot(geometry.nodes[edge, 0], geometry.nodes[edge, 1], 'o', ls='-', ms=8, c="r")
#     centroid = np.mean(geometry.nodes[edge, :], axis=0)
#     ax.quiver(*centroid, *geometry.interior_normals[k])
#
# ax.set_xlim(-1.15, 1.15)
# ax.set_ylim(-1.15, 1.15)
# plt.show()

# Test boundary edges to element

# fig, ax = plt.subplots()
#
# for k, element in enumerate(geometry.mesh.filtered_regions):
#     ax.add_patch(Polygon(geometry.nodes[element, :], linewidth=1.0, edgecolor="black"))
#     centroid = np.mean(geometry.nodes[element, :], axis=0)
#     ax.annotate(f"{k}", centroid)
#
# for k, edge in enumerate(geometry.boundary_edges):
#     ax.plot(geometry.nodes[edge, 0], geometry.nodes[edge, 1], 'o', ls='-', ms=8, c="r")
#     centroid = np.mean(geometry.nodes[edge, :], axis=0)
#     ax.annotate(f"{geometry.boundary_edges_to_element[k]}", centroid)
#
# ax.set_xlim(-1.15, 1.15)
# ax.set_ylim(-1.15, 1.15)
# plt.show()

# Test interior edges to element

# fig, ax = plt.subplots()
#
# for k, element in enumerate(geometry.mesh.filtered_regions):
#     centroid = np.mean(geometry.nodes[element, :], axis=0)
#     ax.annotate(f"{k}", centroid)
#
# for k, edge in enumerate(geometry.interior_edges):
#     ax.plot(geometry.nodes[edge, 0], geometry.nodes[edge, 1], 'o', ls='-', ms=8, c="r")
#     centroid = np.mean(geometry.nodes[edge, :], axis=0)
#     ax.annotate(f"{geometry.interior_edges_to_element[k]}", centroid)
#
# ax.set_xlim(-1.15, 1.15)
# ax.set_ylim(-1.15, 1.15)
#
# plt.show()

# Test boundary edge triangle

# fig, ax = plt.subplots()
#
# for k, region in enumerate(geometry.mesh.filtered_regions):
#     ax.add_patch(Polygon(geometry.nodes[region, :], linewidth=1.0, edgecolor="black"))
#
# for k, element in enumerate(geometry.subtriangulation):
#     ax.add_patch(Polygon(geometry.nodes[element, :], linewidth=1.0, edgecolor="black", alpha=0.1))
#     centroid = np.mean(geometry.nodes[element, :], axis=0)
#     ax.annotate(f"{k}", centroid)
#
# for k, edge in enumerate(geometry.boundary_edge_triangle):
#     ax.plot(geometry.nodes[edge, 0], geometry.nodes[edge, 1], 'o', ls='-', ms=8, c="r")
#     centroid = np.mean(geometry.nodes[edge, :], axis=0)
#     ax.annotate(f"{geometry.boundary_edges_to_element_triangle[k]}", centroid)
#
# plt.show()

# Test interior edge triangle

# fig, ax = plt.subplots()
#
# for k, region in enumerate(geometry.mesh.filtered_regions):
#     ax.add_patch(Polygon(geometry.nodes[region, :], linewidth=1.0, edgecolor="black"))
#
#
# for k, element in enumerate(geometry.subtriangulation):
#     ax.add_patch(Polygon(geometry.nodes[element, :], linewidth=1.0, edgecolor="black", alpha=0.1))
#     centroid = np.mean(geometry.nodes[element, :], axis=0)
#     ax.annotate(f"{k}", centroid)
#
# for k, edge in enumerate(geometry.interior_edge_triangle):
#     ax.plot(geometry.nodes[edge, 0], geometry.nodes[edge, 1], 'o', ls='-', ms=8, c="r")
#     centroid = np.mean(geometry.nodes[edge, :], axis=0)
#     ax.annotate(f"{geometry.interior_edges_to_element_triangle[k]}", centroid)
#
# plt.show()

# Test node to triangle element

# fig, ax = plt.subplots()
#
# for k, element in enumerate(geometry.subtriangulation):
#     ax.add_patch(Polygon(geometry.nodes[element, :], linewidth=1.0, edgecolor="black"))
#     centroid = np.mean(geometry.nodes[element, :], axis=0)
#     ax.annotate(f"{k}", centroid)
#
#
# for k in range(geometry.nodes.shape[0]):
#     ax.plot(geometry.nodes[k, 0], geometry.nodes[k, 1], 'o', ls='-', ms=8, c="r")
#     ax.annotate(f"{geometry.node_to_triangle_element[k]}", geometry.nodes[k, :])
#
#
# ax.set_xlim(-1.15, 1.15)
# ax.set_ylim(-1.15, 1.15)
#
# plt.show()

diffusion = lambda x: np.repeat([np.identity(2, dtype=float)], x.shape[0], axis=0)
forcing = lambda x: 2 * np.pi ** 2 * np.sin(np.pi * x[:, 0]) * np.sin(np.pi * x[:, 1])

dg = DGFEM(geometry, polynomial_degree=1)
dg.add_data(diffusion=diffusion, dirichlet_bcs=solution, forcing=forcing)
dg.dgfem()

plot_DG(dg.solution, geometry, 1)

advection = lambda x: np.ones(x.shape, dtype=float)
forcing = lambda x: np.pi * (np.cos(np.pi * x[:, 0]) * np.sin(np.pi * x[:, 1]) +
                             np.sin(np.pi * x[:, 0]) * np.cos(np.pi * x[:, 1]))

dga = DGFEM(geometry, polynomial_degree=1)
dga.add_data(advection=advection, dirichlet_bcs=solution, forcing=forcing)
dga.dgfem(solve=True)

plot_DG(dga.solution, geometry, 1)


dists = []
for point in list(geometry.mesh.filtered_points):
    dists.append((point * [1.0, 1.0]).sum())

order = np.argsort(dists)
stretched_order = np.kron(dg.dim_elem * order, np.ones(dg.dim_elem, dtype=int)) + \
    np.tile(np.arange(dg.dim_elem), geometry.n_elements)

B = dg.B.toarray()
B_a = dga.B.toarray()

for i in range(B.shape[1]):
    B[:, i] = B[stretched_order, i]
for i in range(B.shape[0]):
    B[i, :] = B[i, stretched_order]

for i in range(B_a.shape[1]):
    B_a[:, i] = B_a[stretched_order, i]
for i in range(B_a.shape[0]):
    B_a[i, :] = B_a[i, stretched_order]


# unorder = np.argsort(order)
# stretched_unorder = np.kron(dg.dim_elem * unorder, np.ones(dg.dim_elem, dtype=int)) + \
#     np.tile(np.arange(dg.dim_elem), geometry.n_elements)
#
# B_a = np.triu(B_a)
#
# for i in range(B_a.shape[1]):
#     B_a[:, i] = B_a[stretched_unorder, i]
# for i in range(B_a.shape[0]):
#     B_a[i, :] = B_a[i, stretched_unorder]


print(is_block_lower_triangular(B_a, dga.dim_elem))

print(np.all((np.abs(B_a) > 1e-10) == np.logical_and(np.abs(B_a) > 1e-10, np.abs(B) > 1e-10)))
print(np.all((np.abs(B_a.T) > 1e-10) == np.logical_and(np.abs(B_a.T) > 1e-10, np.abs(B) > 1e-10)))


fig, ax = plt.subplots(1, 2)
ax[0].imshow(np.abs(B_a) > 1e-10)
ax[0].set_title('Swept Advection PDE Stiffness matrix')

ax[1].imshow(np.abs(B) > 1e-10)
ax[1].set_title('Swept Diffusion PDE Stiffness matrix')

plt.show()
