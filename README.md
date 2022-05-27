Experimentally testing various List based approaches for data access

Knowing Lists use dynamic arrays I was interested in understanding
the specific performance hit in using sequential appends (forcing dynamic array resize)
vs generating null arrays, list comprehensions, and generators for a variety of tasks

See results and lessons learned at Analyzing Performance.ipynb
See full code for each approach at compare_perf.py