Psychopy Tasks
=======
Complex Span tasks implemented in Psychopy.

Structure
---------
Since most tasks in psychology proceed in a simple sequential order, the goal of
this project is to build simple modular components that can be put together into 
an experiment.

For example, a complex span task consists of three basic parts

1. Present memory item
2. Do simple distractor task (then repeat..)
3. Recall

It tends to be the exception, rather than the rule, that the way a participant
performs on one component affects the next component. Since components tend to 
be independent, we can..

1. Build them to be modular.
2. Generate the instructions for what components to run when beforehand.

Point (2) is especially important. Oftentimes, the logic and order of task components
is hard-coded in advanced. However, if we can generate task recipes, and easily
make tasks from them, then modifying tasks on the fly will be a snap.

Task Design Example
-------------------

in   | item | mode | corr
---- | ---- | ---- | ----
0 | memory A | learn | 
0 | dist A | dist | True
0 | dist B | dist | True
1 | memory B | learn | 
1 | dist A | dist | False
1 | dist B | dist | False
2 | memory C | learn | 
2 | dist A | dist | False
2 | dist B | dist | True
 |  | recall | 

### Running
Here, the `mode` column corresponds to the procedure that we'll be using.
For each row in the data, the corresponding procedure will be called, with all
the column data for that row passed as arguments.

### Logging Data
Ideally, each procedure should provide outputs that could easily be turned into a table.
Thus, the `recall` procedure might return..

pos | out
--- | ---
0   | memory A
1   | memory B

or something similar.
