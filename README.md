# ROSE Planning Tool
Eric J. Hall, John McDermott
2025-03-26

## Problem Overview

We aim to allocate different types of students to rooms such that:

- Each room is assigned at most one student type.
- Space constraints of each room are satisfied.
- The number of students allocated to a room is allowed to relax
  following an anticipated occupancy for each student type.
- Minimum and maximum student counts are respected.
- The total value of students assigned to rooms is maximized.

This constrainted optimisation can be formulated as a Mixed Integer
Linear Program (MILP).

The MILP finds an optimal number of students of each type to allocate to
each room. The allocation maximises the total value stored in the estate
subject to the specified constraints. This MILP can be adapted for
different scenarios by adjusting room sizes, occupancy allowances,
minimum and maximum student numbers, or the objective function itself.

## Mathematical Formulation of the MILP

### Sets and Indices

- ![S](https://latex.codecogs.com/svg.latex?S "S"): Set of student
  types, indexed by
  ![s \in S](https://latex.codecogs.com/svg.latex?s%20%5Cin%20S "s \in S").
- ![R](https://latex.codecogs.com/svg.latex?R "R"): Set of rooms,
  indexed by
  ![r \in R](https://latex.codecogs.com/svg.latex?r%20%5Cin%20R "r \in R").

### Parameters

- ![A_r \> 0](https://latex.codecogs.com/svg.latex?A_r%20%3E%200 "A_r > 0"):
  Area available in room
  ![r \in R](https://latex.codecogs.com/svg.latex?r%20%5Cin%20R "r \in R").
- ![a_s \> 0](https://latex.codecogs.com/svg.latex?a_s%20%3E%200 "a_s > 0"):
  Space required per student of type
  ![s \in S](https://latex.codecogs.com/svg.latex?s%20%5Cin%20S "s \in S").
- ![v_s \> 0](https://latex.codecogs.com/svg.latex?v_s%20%3E%200 "v_s > 0"):
  Value associated with a student of type
  ![s \in S](https://latex.codecogs.com/svg.latex?s%20%5Cin%20S "s \in S").
- ![o_s \in (0,1\]](https://latex.codecogs.com/svg.latex?o_s%20%5Cin%20%280%2C1%5D "o_s \in (0,1]"):
  Occupancy allowance per student of type
  ![s \in S](https://latex.codecogs.com/svg.latex?s%20%5Cin%20S "s \in S").
- ![l_s \> 0](https://latex.codecogs.com/svg.latex?l_s%20%3E%200 "l_s > 0"):
  Minimum number of students of type
  ![s \in S](https://latex.codecogs.com/svg.latex?s%20%5Cin%20S "s \in S").
- ![u_s \> 0](https://latex.codecogs.com/svg.latex?u_s%20%3E%200 "u_s > 0"):
  Maximum number of students of type
  ![s \in S](https://latex.codecogs.com/svg.latex?s%20%5Cin%20S "s \in S").

### Decision Variables

- ![y\_{s,r} \in \mathbb{Z}\_{\geq 0}](https://latex.codecogs.com/svg.latex?y_%7Bs%2Cr%7D%20%5Cin%20%5Cmathbb%7BZ%7D_%7B%5Cgeq%200%7D "y_{s,r} \in \mathbb{Z}_{\geq 0}"):
  Number of students of type
  ![s \in S](https://latex.codecogs.com/svg.latex?s%20%5Cin%20S "s \in S")
  assigned to room
  ![r \in R](https://latex.codecogs.com/svg.latex?r%20%5Cin%20R "r \in R").
- ![z\_{s,r} \in \\0,1\\](https://latex.codecogs.com/svg.latex?z_%7Bs%2Cr%7D%20%5Cin%20%5C%7B0%2C1%5C%7D "z_{s,r} \in \{0,1\}"):
  Binary variable indicating whether room
  ![r](https://latex.codecogs.com/svg.latex?r "r") is assigned to
  student type ![s](https://latex.codecogs.com/svg.latex?s "s").

### Objective Function

We aim to maximize the total value of students assigned to rooms across
the campus estate:

![\max \sum\_{s \in S} \sum\_{r \in R} v_s \\ y\_{s,r} \\.](https://latex.codecogs.com/svg.latex?%5Cmax%20%5Csum_%7Bs%20%5Cin%20S%7D%20%5Csum_%7Br%20%5Cin%20R%7D%20v_s%20%5C%2C%20y_%7Bs%2Cr%7D%20%5C%2C. "\max \sum_{s \in S} \sum_{r \in R} v_s \, y_{s,r} \,.")

### Constraints

The objective function above must be maximised subject to the following
constraints.

#### 1. Room Capacity Constraint, with Occupancy Relaxation

This constraint ensures that the total space required by each student
type does not exceed the room size while allowing for a study
type-specific occupancy relaxation:

![\sum\_{s \in S} (a_s \\o_s)\\ y\_{s,r} \leq A_r\\, \quad \forall r \in R \\.](https://latex.codecogs.com/svg.latex?%5Csum_%7Bs%20%5Cin%20S%7D%20%28a_s%20%5C%2Co_s%29%5C%2C%20y_%7Bs%2Cr%7D%20%5Cleq%20A_r%5C%2C%2C%20%5Cquad%20%5Cforall%20r%20%5Cin%20R%20%5C%2C. "\sum_{s \in S} (a_s \,o_s)\, y_{s,r} \leq A_r\,, \quad \forall r \in R \,.")

In practice, this reflects that typical occupancy is below 100% for
certain student types. It has the effect of reducing the space required
per student type.

#### 2. One Student Type Per Room

This constraint ensures that each room can have at most one type of
student:

![\sum\_{s \in S} z\_{s,r} \leq 1\\, \quad \forall r \in R \\.](https://latex.codecogs.com/svg.latex?%5Csum_%7Bs%20%5Cin%20S%7D%20z_%7Bs%2Cr%7D%20%5Cleq%201%5C%2C%2C%20%5Cquad%20%5Cforall%20r%20%5Cin%20R%20%5C%2C. "\sum_{s \in S} z_{s,r} \leq 1\,, \quad \forall r \in R \,.")

Additionally, if a student type is assigned to a room, the total space
required by the students must not exceed the room’s capacity:

![(a_s \\o_s) \\y\_{s,r} \leq z\_{s,r} \\ A_r\\, \quad \forall s \in S\\, \quad r \in R \\.](https://latex.codecogs.com/svg.latex?%28a_s%20%5C%2Co_s%29%20%5C%2Cy_%7Bs%2Cr%7D%20%5Cleq%20z_%7Bs%2Cr%7D%20%5C%2C%20A_r%5C%2C%2C%20%5Cquad%20%5Cforall%20s%20%5Cin%20S%5C%2C%2C%20%5Cquad%20r%20%5Cin%20R%20%5C%2C. "(a_s \,o_s) \,y_{s,r} \leq z_{s,r} \, A_r\,, \quad \forall s \in S\,, \quad r \in R \,.")

#### 3. Minimum and Maximum Student Counts

It is desirable to specify a minimum and maximum number of students of
each type for planning purposes. This constraint ensures that each
student type is either greater than the specified minimum or less than
the specified maximum count requirements:

![\sum\_{r \in R} y\_{s,r} \geq l_s\\, \quad \forall s \in S \\,](https://latex.codecogs.com/svg.latex?%5Csum_%7Br%20%5Cin%20R%7D%20y_%7Bs%2Cr%7D%20%5Cgeq%20l_s%5C%2C%2C%20%5Cquad%20%5Cforall%20s%20%5Cin%20S%20%5C%2C%2C "\sum_{r \in R} y_{s,r} \geq l_s\,, \quad \forall s \in S \,,")

and

![\sum\_{r \in R} y\_{s,r} \leq u_s\\, \quad \forall s \in S \\.](https://latex.codecogs.com/svg.latex?%5Csum_%7Br%20%5Cin%20R%7D%20y_%7Bs%2Cr%7D%20%5Cleq%20u_s%5C%2C%2C%20%5Cquad%20%5Cforall%20s%20%5Cin%20S%20%5C%2C. "\sum_{r \in R} y_{s,r} \leq u_s\,, \quad \forall s \in S \,.")

## Implementation in Python (PuLP)

For the constrained optimisation problem outlined above, we coded a MILP
solver using the PuLP Python library. The code runtime varied depending
on the minimum and maximum student numbers specified. This is due to the
iterative nature of the optimisation procedure employed (it uses a
branch-and-bound procedure to find an integer solution for each
allocation). In the code, the problem parameters are included as two
python dictionaries: the first details the room areas
![A_r](https://latex.codecogs.com/svg.latex?A_r "A_r") and the second
contains the parameters that vary by student type
![(a_s, v_s, o_s, l_s, u_s)](https://latex.codecogs.com/svg.latex?%28a_s%2C%20v_s%2C%20o_s%2C%20l_s%2C%20u_s%29 "(a_s, v_s, o_s, l_s, u_s)").
These can be edited to update the estate and student type numbers and
details. The model defined in the code does not need to be updated
unless changes to the objective function or constraints are desired.

A condensed version of the implementation is provided below. It omits
the student data, room data, and routines for output. The full code is
available at the git repository: <https://github.com/dundeemath/rose>.

``` python
from pulp import LpMaximize, LpProblem, LpVariable, lpSum

# Room and student type data
rooms = { ... }
student_types = { ... }

# Define the optimization problem
model = LpProblem("Room_Packing", LpMaximize)

# Decision variables
y = { (s, r): LpVariable(f"y_{s}_{r}", lowBound=0, cat='Integer') for s in student_types for r in rooms }
z = { (s, r): LpVariable(f"z_{s}_{r}", cat='Binary') for s in student_types for r in rooms }

# Objective function
model += lpSum(student_types[s]["value"] * y[s, r] for s in student_types for r in rooms), "Total_Value"

# Constraints
for r in rooms:
    model += lpSum((student_types[s]["size"] * student_types[s]["occupancy"]) * y[s, r] for s in student_types) <= rooms[r], f"Scaled_Area_Constraint_{r}"
    model += lpSum(z[s, r] for s in student_types) <= 1, f"One_Student_Type_Per_Room_{r}"
    for s in student_types:
        model += (student_types[s]["size"] * student_types[s]["occupancy"]) * y[s, r] <= z[s, r] * rooms[r], f"Student_Type_Selection_Constraint_{s}_{r}"

for s in student_types:
    model += lpSum(y[s, r] for r in rooms) >= student_types[s]["min_count"], f"Min_Count_{s}"
    model += lpSum(y[s, r] for r in rooms) <= student_types[s]["max_count"], f"Max_Count_{s}"

# Solve the model
model.solve()
```

## Recommendation

The provided mathematical formulation provides a way of finding an
integer valued solution to the student-estate planning problem first
brought to the attention of Mathematics in early March 2025 by Estates
colleagues. The optimal total value of students assigned to rooms across
the campus estate (optimal value stored) can provide a guide to support
decision-making. For example, planned use of the estate that deviates
significantly from the optimal value stored may indicate an inadequate
use of the estate.

The model might be extended to include additional constraints, such as
the cost associated with delivering a program for a more fine-grained
and realistic recommendations.

The present tool is a Python code that requires manually input of raw
data. This could be streamlined, e.g., to take Excel or CSV formatted
inputs. There is presently no user interface for interacting with the
code. The output of the code are CVS files. There are various
visualisations of the output data that could be provided to aid in
decision-making.

The code can be run at the start of each academic session using
projected intake numbers to provide an optimal allocation of students.
The code could also be run multiple times with small deviations from the
projected intake numbers (e.g., 10% over and 10% under) to model various
best and work case scenarios. This would represent a very crude
sensitivity analysis; one could also run the model dropping out various
student and room types to judge the effects.

We provide the caution that **an optimal solution is not necessarily a
robust one**. There is a risk of falling from a optimum to a
unfavourable position and this is not currently provided. Further
sensitivity analysis could be employed to identify robust profiles that
avoid this risk.

Academic factors should also influence student-estate planning and this
tool is provided in that spirit.

------------------------------------------------------------------------

<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/">

<span property="dct:title">ROSE Planning Tool</span> by
<span property="cc:attributionName">Eric J. Hall and John
McDermott</span> is licensed under
<a href="https://creativecommons.org/licenses/by-sa/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">CC
BY-SA
4.0<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/sa.svg?ref=chooser-v1" alt=""></a>
</p>
