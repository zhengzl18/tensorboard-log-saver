# tensorboard-log-saver
A script for automatically downloading the csv files from tensorboard log files

## Requirement
+ tensorboard

Tested on tensorboard 2.10.1 and 2.12.2.

## Usage
1. `log_path`: a list of strings, each of which specifies a directory, containing the tensorboard log files you want to download data from. All the log files in the directories will be loaded. It's able to use either absolute paths or relative paths.
2. `root`: a string specifying the root directory of all log files. Only the components of the subdirectories will appear in the names of the csv files. Make sure that `root` is a component of every element in your `log_path`.
3. `scalar_name`: a list of strings containing the scalar tags of which the data you want to download.

Note that the final csv files are named by the same rule with that of tensorboard.

## Example
Suppose your log directory looks like this:
```
--log
  --algo1
    --exp1
      --events.out.tfevents.....0
  --algo2
    --exp2
      --events.out.tfevents.....0
    --exp3
      --events.out.tfevents.....0
  --algo3
    --exp4
      --events.out.tfevents.....0
```
And you want to download the return curves (tagged with 'Return') of exp1 and exp4. You may set
```python
log_path = [
    "/home/xxx/example_path/log/algo1",
    "/home/xxx/example_path/log/algo3",
]
root = 'log'
scalar_name = [
    "Return",
]
```
Run the script and you will find the csv files in "/home/xxx/example_path/log/algo1/exp1/" and "/home/xxx/example_path/log/algo3/exp4/", named "run-algo1_exp1-tag-Return.csv" and "run-algo3_exp4-tag-Return.csv", respectively.
