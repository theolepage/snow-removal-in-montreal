# snow-removal-in-montreal

Program to find the optimized path to clear snow efficiently in a city.

## Structure

The entry point of our implementation is the function **solve** in `snowymontreal.py`.
However, there is a faster one, **solve_fast**, based on NetworkX for undirected graphs only.
Main algorithms are implemented in `solve_directed.py` and `solve_undirected.py` and utilities functions are in the `utils/` directory.

## Usage

To run the program for a specific location use the following command.
```
python3 main.py 'Le Tronquay, France' --oriented
python3 main.py 'Le Tronquay, France'
python3 main.py -h
```

Alternatively, you can use it as a library as shown below.
```python
from snowymontreal import solve
res = solve(True, num_vertices, edge_list)
```

## Tests

You can run the suite by typing `python3 -m unittest`.

## Authors

- Arielle Levi
- Theo Lepage
- Viviane Garese
- Sebastien Lanyi
- Maxime Castaing
