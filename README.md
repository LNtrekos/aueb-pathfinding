# Aueb Pathfinding: A simple navigation system (for my university)

This is a simple object oriented program that models my university (AUEB) as a graph and its classrooms as nodes,
that implements Dijkstra's algorithm to find the shortest path between classrooms. 
First extract everything from this folder, or clone the repository

```bash
git clone https://github.com/LNtrekos/aueb-pathfinding.git
```

In the aueb_pathfinding folder, you will find:
- ultis.py (helper functions)
- menu.py (Ways to interact with the objects: Classroom, University)
- classes.py (Main objects)
  
For details of the above, read report/aueb_pathfinding.pdf

## Quick Execution

From a command prompt (Windows), navigate to the project directory and run:

```bash
C:\Ecosystem> python main.py
```
You should see the following output:

```bash
Recommendation:
- Maximum Distance: 21
- Floor Weight: 1
These values are suggested when selecting option 2) Create Graph


    =========================
            MENU
    =========================
    1) Load Map
    2) Create Graph
    3) Find the shortest path between two classrooms
    4) Visualize Map
    5) Exit

```
