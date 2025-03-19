# Command Line Interface

```sh
automesh --help
<!-- cmdrun automesh --help -->
```

## Summary

### Segmentation $\mapsto$ Segmentation

$$
\begin{array}{ccc}
{\tt npy} & \xmapsto[]{\tt convert} & {\tt spn}
\\
\\
{\tt spn} & \xmapsto[]{\tt convert} & {\tt npy}
\end{array}
$$

### Mesh $\mapsto$ Mesh

$$
\begin{array}{ccc}
{\tt inp}
&
\xmapsto[]{\tt convert}
&
\left\{
    \begin{array}{l}
        {\tt exo} \\
        {\tt mesh} \\
        {\tt stl} \leftarrow {\rm ?} \\
        {\tt vtk}
    \end{array}
\right.
\end{array}
$$

### Segmentation $\mapsto$ Mesh

$$
\begin{array}{ccc}
\left.
    \begin{array}{l}
        {\tt npy} \\
        {\tt spn}
    \end{array}
\right\}
& \xmapsto[]{\tt mesh}
&
\left\{
    \begin{array}{l}
        {\tt exo} \\
        {\tt inp} \\
        {\tt mesh} \\
        {\tt vtk}
    \end{array}
\right.
\end{array}
$$

### Metrics

$$
\begin{array}{ccc}
{\tt inp}
&
\xmapsto[]{\tt metrics}
&
\left\{
    \begin{array}{l}
        {\tt csv} \\
        {\tt npy}
    \end{array}
\right.
\end{array}
$$

### Smoothing

$$
\begin{array}{ccc}
\left.
    \begin{array}{l}
        {\tt inp} \\
        {\tt stl}
    \end{array}
\right\}
& \xmapsto[]{\tt smooth}
&
\left\{
    \begin{array}{l}
        {\tt exo} \\
        {\tt inp} \\
        {\tt mesh} \\
        {\tt stl} \leftarrow {\rm ?} \\
        {\tt vtk}
    \end{array}
\right.
\end{array}
$$

### Smoothing (Actual?)

$$
\begin{array}{ccc}
{\tt inp}
& \xmapsto[]{\tt smooth}
&
\left\{
    \begin{array}{l}
        {\tt exo} \\
        {\tt inp} \\
        {\tt mesh} \\
        {\tt vtk}
    \end{array}
\right.
\end{array}
$$

$$
\begin{array}{ccc}
{\tt stl}
& \xmapsto[]{\tt smooth}
&
\left\{
    \begin{array}{l}
        {\tt exo} \\
        {\tt inp} \\
        {\tt mesh} \leftarrow {\rm ?} \\
        {\tt stl} \\
        {\tt vtk}
    \end{array}
\right.
\end{array}
$$
