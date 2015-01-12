from memtask import design
from pandas import DataFrame

df1 = DataFrame(design.simple_span_trial(range(3)))
df1.to_csv('example/trials/simple_span.csv')

df2 = DataFrame(design.complex_span_trial(3, 2))
df2.to_csv('example/trials/complex_span.csv')
