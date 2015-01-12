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

