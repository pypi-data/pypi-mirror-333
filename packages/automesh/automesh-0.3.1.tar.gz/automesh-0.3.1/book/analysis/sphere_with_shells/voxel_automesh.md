# Voxel Mesh with `automesh`

Build the latest release version of `automesh`.

```sh
cd ~/autotwin/automesh
cargo build --release
...
   Compiling automesh v0.2.9 (/Users/chovey/autotwin/automesh)
    Finished `release` profile [optimized] target(s) in 2m 59s
```

Set up.

```sh
alias automesh='/Users/chovey/autotwin/automesh/target/release/automesh'
cd ~/autotwin/automesh/book/analysis/sphere_with_shells/
```

## Mesh Creation

Use `automesh` to convert the segmentations into finite element meshes.

**Remark:** In the analysis below, we use the Exodus II output format (`.exo`) instead of the Abaqus output format (`.inp`).  The Exodus format results in faster mesh creation and smaller file size due to compression.

```sh
automesh mesh -i spheres_resolution_1.npy \
-o spheres_resolution_1.exo \
--remove 0 \
--xtranslate -12 --ytranslate -12 --ztranslate -12
```

```sh
    automesh 0.2.9
     Reading spheres_resolution_1.npy
        Done 9.991084ms
     Meshing spheres_resolution_1.exo [xtranslate: -12, ytranslate: -12, ztranslate: -12]
        Done 567.75µs
     Writing spheres_resolution_1.exo
        Done 7.369708ms
       Total 18.158ms
```

```sh
automesh mesh -i spheres_resolution_2.npy \
-o spheres_resolution_2.exo \
--remove 0 \
--xscale 0.5 --yscale 0.5 --zscale 0.5 \
--xtranslate -12 --ytranslate -12 --ztranslate -12
```

```sh
    automesh 0.2.9
     Reading spheres_resolution_2.npy
        Done 6.601875ms
     Meshing spheres_resolution_2.exo [xscale: 0.5, yscale: 0.5, zscale: 0.5, xtranslate: -12, ytranslate: -12, ztranslate: -12]
        Done 4.208542ms
     Writing spheres_resolution_2.exo
        Done 13.984917ms
       Total 25.056125ms
```

```sh
automesh mesh -i spheres_resolution_3.npy \
-o spheres_resolution_3.exo \
--remove 0 \
--xscale 0.25 --yscale 0.25 --zscale 0.25 \
--xtranslate -12 --ytranslate -12 --ztranslate -12
```

```sh
    automesh 0.2.9
     Reading spheres_resolution_3.npy
        Done 701.959µs
     Meshing spheres_resolution_3.exo [xscale: 0.25, yscale: 0.25, zscale: 0.25, xtranslate: -12, ytranslate: -12, ztranslate: -12]
        Done 32.522625ms
     Writing spheres_resolution_3.exo
        Done 39.280292ms
       Total 72.724167ms
```

```sh
automesh mesh -i spheres_resolution_4.npy \
-o spheres_resolution_4.exo \
--remove 0 \
--xscale 0.1 --yscale 0.1 --zscale 0.1 \
--xtranslate -12 --ytranslate -12 --ztranslate -12
```

```sh
    automesh 0.2.9
     Reading spheres_resolution_4.npy
        Done 5.540458ms
     Meshing spheres_resolution_4.exo [xscale: 0.1, yscale: 0.1, zscale: 0.1, xtranslate: -12, ytranslate: -12, ztranslate: -12]
        Done 458.92225ms
     Writing spheres_resolution_4.exo
        Done 495.663416ms
       Total 960.318042ms
```

## Visualization

Cubit is used for the visualizations with the following recipe:

```sh
reset
cd "/Users/chovey/autotwin/automesh/book/analysis/sphere_with_shells"

import mesh "spheres_resolution_1.exo" lite

graphics scale on

graphics clip off
view iso
graphics clip on plane location 0 -1.0 0 direction 0 1 0
view up 0 0 1
view from 100 -100 100

graphics clip manipulation off

view bottom
```

resolution | 1 vox/cm | 2 vox/cm | 4 vox/cm | 10 vox/cm
---------- | -------: | -------: | -------: | --------:
midline   | ![resolution_1.png](img/resolution_1.png) | ![resolution_2.png](img/resolution_2.png) | ![resolution_3.png](img/resolution_3.png) | ![resolution_4.png](img/resolution_4.png)
isometric  | ![resolution_1_iso.png](img/resolution_1_iso.png) | ![resolution_2_iso.png](img/resolution_2_iso.png) | ![resolution_3_iso.png](img/resolution_3_iso.png) | ![resolution_4_iso.png](img/resolution_4_iso.png)
block 1 (green) #elements | 3,648 | 31,408 | 259,408 | 4,136,832
block 2 (yellow) #elements | 1,248 | 10,400 | 86,032 | 1,369,056
block 3 (magenta) #elements | 1,376 | 12,280 | 103,240 | 1,639,992
total #elements | 6,272 | 54,088 | 448,680 | 7,145,880
