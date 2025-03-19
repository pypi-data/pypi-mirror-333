r"""This module, spheres_cont.py, builds on the spheres.py module to create
high resolution, three-material, concentric spheres and export the
voxelization as a .npy file.

Example
-------
source ~/autotwin/automesh/.venv/bin/activate
python spheres_cont.py

Output
------
~/autotwin/automesh/book/analysis/sphere_with_shells/spheres_resolution_1.npy
~/autotwin/automesh/book/analysis/sphere_with_shells/spheres_resolution_2.npy
~/autotwin/automesh/book/analysis/sphere_with_shells/spheres_resolution_3.npy
~/autotwin/automesh/book/analysis/sphere_with_shells/spheres_resolution_4.npy
"""

from pathlib import Path
from typing import Final

from matplotlib.colors import LightSource
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def sphere(resolution: int, dtype=np.uint8) -> np.ndarray:
    """Generate a 3D voxelized representation of three concentric spheres
    of 10, 11, and 12 cm, at a given resolution.

    Parameters
    ----------
    resolution : int
        The resolution as voxels per centimeter.  Minimum value is 1.

    dtype: data-type, optional
        The data type of the output array.  Default is np.uint8.

    Returns
    -------
    np.ndarray
        A 3D numpy array representing the voxelized spheres.  Voxels within
        the inner sphere are set to 1, the intermediate shell are set to 2,
        and the outer shell are set to 3.  Voxels outside the spheres are
        set to 0.

    Raises
    ------
    ValueError
        If the resolution is less than 1.
    """
    print(f"Creating sphere with resolution: {resolution}")
    if resolution < 1:
        raise ValueError("Resolution must be >= 1")

    r10 = 10  # cm
    r11 = 11  # cm
    r12 = 12  # cm

    # We change the algorithm a bit here so we can exactly match the radius:
    # number of voxels per side length (nvps)
    # nvps = 2 * r12 * resolution + 1
    nvps = 2 * r12 * resolution
    vox_z, vox_y, vox_x = np.mgrid[
        -r12: r12: nvps * 1j,
        -r12: r12: nvps * 1j,
        -r12: r12: nvps * 1j,
    ]
    domain = vox_x**2 + vox_y**2 + vox_z**2
    mask_10_in = np.array(domain <= r10 * r10, dtype=dtype)
    mask_11_in = np.array(domain <= r11 * r11, dtype=dtype)
    mask_12_in = np.array(domain <= r12 * r12, dtype=dtype)

    mask_10_11 = mask_11_in - mask_10_in
    mask_11_12 = mask_12_in - mask_11_in

    shell_10_11 = 2 * mask_10_11
    shell_11_12 = 3 * mask_11_12

    result = mask_10_in + shell_10_11 + shell_11_12
    print(f"Completed: Sphere with resolution: {resolution}")
    return result


rr = (1, 2, 4, 10)  # resolutions (voxels per cm)
lims = tuple(map(lambda x: [0, 24 * x], rr))  # limits
tt = tuple(map(lambda x: [0, 12 * x, 24 * x], rr))  # ticks

# User input begin
spheres = {
    "resolution_1": sphere(resolution=rr[0]),
    "resolution_2": sphere(resolution=rr[1]),
    "resolution_3": sphere(resolution=rr[2]),
    "resolution_4": sphere(resolution=rr[3]),
}

aa = Path(__file__)
bb = aa.with_suffix(".png")

# Visualize the elements.
width, height = 10, 5
# width, height = 8, 4
# width, height = 6, 3
fig = plt.figure(figsize=(width, height))

el, az, roll = 63, -110, 0
cmap = plt.get_cmap(name="tab10")
# NUM_COLORS = len(spheres)
NUM_COLORS = 10  # consistent with tab10 color scheme
VOXEL_ALPHA: Final[float] = 0.9

colors = cmap(np.linspace(0, 1, NUM_COLORS))
lightsource = LightSource(azdeg=325, altdeg=45)  # azimuth, elevation
# lightsource = LightSource(azdeg=325, altdeg=90)  # azimuth, elevation
DPI: Final[int] = 300  # resolution, dots per inch
SHOW: Final[bool] = False  # turn to True to show the figure on screen
SAVE: Final[bool] = True  # turn to True to save .png and .npy files
# User input end

N_SUBPLOTS = len(spheres)
for index, (key, value) in enumerate(spheres.items()):
    if SHOW:
        print(f"index: {index}")
        print(f"key: {key}")
        # print(f"value: {value}")
        ax = fig.add_subplot(1, N_SUBPLOTS, index + 1, projection=Axes3D.name)
        ax.voxels(
            value,
            facecolors=colors[index],
            edgecolor=colors[index],
            alpha=VOXEL_ALPHA,
            lightsource=lightsource,
        )
        ax.set_title(key)

        # Set labels for the axes
        ax.set_xlabel("x (voxels)")
        ax.set_ylabel("y (voxels)")
        ax.set_zlabel("z (voxels)")

        ax.set_xticks(ticks=tt[index])
        ax.set_yticks(ticks=tt[index])
        ax.set_zticks(ticks=tt[index])

        ax.set_xlim(lims[index])
        ax.set_ylim(lims[index])
        ax.set_zlim(lims[index])

        # Set the camera view
        ax.set_aspect("equal")
        ax.view_init(elev=el, azim=az, roll=roll)

    if SAVE:
        cc = aa.with_stem("spheres_" + key)
        dd = cc.with_suffix(".npy")
        # Save the data in .npy format
        np.save(dd, value)
        print(f"Saved: {dd}")

# fig.tight_layout()  # don't use as it clips the x-axis label
if SHOW:
    plt.show()

    if SAVE:
        fig.savefig(bb, dpi=DPI)
        print(f"Saved: {bb}")
