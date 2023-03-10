# Crease Pattern to Diagrams
Create a precreasing guide from a crease pattern.

Start with a blank square and iteratively add creases using known rules until all the lines in the crease pattern have been reached. 

There may be some utility in creating such a guide for solving crease patterns. However, I currently have plans to use this as a tool for other projects. I hope the framework of searching for valid creases using known rules may help resolve some of the ambiguity I encountered when trying to convert an image into a crease pattern. Being able to handle more ambiguity in converting an image into a crease pattern may eventually allow natural images (photo of a crease pattern) to be converted into crease patterns. The end goal is to implement a useful diagram creator that keeps track of the collapsed form. The pipeline could then be natural image -> crease pattern -> diagrams which I believe would help many fold models that might otherwise be inaccessible.

### Usage
`python diagramSearch.py path/To/CreasePattern.cp`

### Current Development
- Implement rest of folding rules, currently only have connecting points, perpendicular bisector, and angle bisector.
- Handle other crease pattern file types, currently only ingests .cp
- Better rendering and add fold type/explanation
- Improved search with collapsed form, currently only searches for creases on a flat square
- Use as library for resolving ambiguity with image to cp
