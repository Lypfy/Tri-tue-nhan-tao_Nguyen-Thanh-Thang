import sys
sys.path.insert(0, 'e:/Documents/ArtificialInteligence/VSCode/git_repo/AlgorithmsVisualization')

print("Testing backtracking_search...")
try:
    from algorithms.csp.backtracking import backtracking_search
    steps = backtracking_search()
    print(f"OK: {len(steps)} steps")
    if steps:
        print(f"Last: {steps[-1]['message']}")
except Exception as e:
    import traceback
    traceback.print_exc()

print("\nTesting mac_search...")
try:
    from algorithms.csp.ac3 import mac_search
    steps = mac_search()
    print(f"OK: {len(steps)} steps")
    if steps:
        print(f"Last: {steps[-1]['message']}")
except Exception as e:
    import traceback
    traceback.print_exc()

print("\nTesting min_conflicts_search...")
try:
    from algorithms.csp.min_conflicts import min_conflicts_search
    steps = min_conflicts_search()
    print(f"OK: {len(steps)} steps")
    if steps:
        print(f"Last: {steps[-1]['message']}")
except Exception as e:
    import traceback
    traceback.print_exc()
