# Timing - Sculpt

Set up an alias, if needed.

```sh
alias sculpt='/Applications/Cubit-16.14/Cubit.app/Contents/MacOS/sculpt'
cd ~/autotwin/automesh/book/analysis/sphere_with_shells/
```

Use `automesh` to create `.spn` files from the `.npy` files.

```sh
automesh convert -i spheres_resolution_1.npy -o spheres_resolution_1.spn
automesh convert -i spheres_resolution_2.npy -o spheres_resolution_2.spn
automesh convert -i spheres_resolution_3.npy -o spheres_resolution_3.spn
automesh convert -i spheres_resolution_4.npy -o spheres_resolution_4.spn
```

```sh
    automesh 0.2.9
     Reading spheres_resolution_1.npy
        Done 751.583µs
     Writing spheres_resolution_1.spn
        Done 1.06475ms
       Total 2.683ms
    automesh 0.2.9
     Reading spheres_resolution_2.npy
        Done 584.458µs
     Writing spheres_resolution_2.spn
        Done 2.841667ms
       Total 3.562583ms
    automesh 0.2.9
     Reading spheres_resolution_3.npy
        Done 805.417µs
     Writing spheres_resolution_3.spn
        Done 14.427833ms
       Total 15.353708ms
    automesh 0.2.9
     Reading spheres_resolution_4.npy
        Done 2.367291ms
     Writing spheres_resolution_4.spn
        Done 235.7805ms
       Total 238.266791ms
```

Run Sculpt.

```sh
sculpt --num_procs 1 --input_spn "spheres_resolution_1.spn" \
-x 24 -y 24 -z 24 \
--xtranslate -24 --ytranslate -24 --ztranslate -24 \
--spn_xyz_order 0 \
--exodus_file "spheres_resolution_1" \
--stair 3
```

```sh
Total Time on 1 Procs	0.122201 sec. (0.002037 min.)
```

```sh
sculpt --num_procs 1 --input_spn "spheres_resolution_2.spn" \
-x 48 -y 48 -z 48 \
--xscale 0.5 --yscale 0.5 --zscale 0.5 \
--xtranslate -12 --ytranslate -12 --ztranslate -12 \
--spn_xyz_order 0 \
--exodus_file "spheres_resolution_2" \
--stair 3
```

```sh
Total Time on 1 Procs	0.792997 sec. (0.013217 min.)
```

```sh
sculpt --num_procs 1 --input_spn "spheres_resolution_3.spn" \
-x 96 -y 96 -z 96 \
--xscale 0.25 --yscale 0.25 --zscale 0.25 \
--xtranslate -12 --ytranslate -12 --ztranslate -12 \
--spn_xyz_order 0 \
--exodus_file "spheres_resolution_3" \
--stair 3
```

```sh
Total Time on 1 Procs	7.113380 sec. (0.118556 min.)
```

```sh
sculpt --num_procs 1 --input_spn "spheres_resolution_4.spn" \
-x 240 -y 240 -z 240 \
--xscale 0.1 --yscale 0.1 --zscale 0.1 \
--xtranslate -12 --ytranslate -12 --ztranslate -12 \
--spn_xyz_order 0 \
--exodus_file "spheres_resolution_4" \
--stair 3
```

```sh
Total Time on 1 Procs	135.636523 sec. (2.260609 min.)
```

The table below summarizes the relative processing times, Sculpt versus `automesh`.

resolution | 1 vox/cm | 2 vox/cm | 4 vox/cm | 10 vox/cm
---------- | -------: | -------: | -------: | --------:
`automesh` | 1 | 1 | 1 | 1
Sculpt | 6.73 | 31.6 | 97.8 | 141
