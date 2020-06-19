# UPD2Runner: generator of patched version from unified diff


## Set up:

Dependency: https://github.com/matiasb/python-unidiff

## How to use it:

## Case 1: Analyzing folder with several diffs


```
input = "Path_to_folder_with diffs"
output = "Path_to_output"

runvisit(input,output)
```



## Case 2: Analyzing a single diff

```
runsingle(file_name,path_to_diff_file, path_to_output)

```