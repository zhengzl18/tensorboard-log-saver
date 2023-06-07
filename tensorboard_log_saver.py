import argparse
import csv
import os
import warnings

from tensorboard.backend.event_processing import io_wrapper
from tensorboard.backend.event_processing.event_accumulator import \
    EventAccumulator

log_path = [
    "/home/xxx/example_path/log",
]
root = 'log'
scalar_name = [
    "example_name",
]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--log_path', type=list, default=log_path)
    parser.add_argument('--root', type=str, default=root)
    parser.add_argument('--scalar_name', type=list, default=scalar_name)
    args = parser.parse_args()

    for path in args.log_path:
        if not io_wrapper.IsTensorFlowEventsFile(path):
            for root, _, files in os.walk(path):
                files = list(map(lambda f: os.path.join(root, f), files))
                args.log_path.extend([file for file in files if io_wrapper.IsTensorFlowEventsFile(file)])
            continue
        
        event_acc = EventAccumulator(path).Reload()
        tokens = path.split('/')
        if args.root is not None:
            log_name = '_'.join(tokens[tokens.index(args.root) + 1:-1])
        else:
            log_name = '_'.join(tokens[:-1])
        
        for sn in args.scalar_name:
            try:
                rows= list(map(lambda se: (se.wall_time, se.step, se.value), event_acc.Scalars(sn)))
                file_name = os.path.join(os.path.dirname(path), f"run-{log_name}-tag-{sn.replace('/', '_')}.csv")
                with open(file_name, 'w') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Wall time", "Step", "Value"])
                    writer.writerows(rows)
            except KeyError:
                warnings.warn(f"\"{sn}\" is not found in the log file \"{path}\". \n The available scalar names are {event_acc.Tags()['scalars']}")
                continue
