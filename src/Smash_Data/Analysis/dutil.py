## Dumb
import os
_changed_levels = set()

def parentizeCWD(n=1):
    global _changed_levels
    if n in _changed_levels:
        print(f'Directory unchanged at {os.getcwd()}')
        return
    path = os.path.abspath(os.path.join(os.getcwd(), *(['..'] * n)))
    os.chdir(path)
    print(f'Directory changed to {path}')
    _changed_levels.add(n)