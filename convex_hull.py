# Uncomment this line to import some functions that can help
# you debug your algorithm
# from plotting import draw_line, draw_hull, circle_point
import math, random, itertools

def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""

    # Sorting algorithm: O(nlogn) time
    pivot: tuple[float, float] = max(points, key=lambda p: (p[0], p[1]))
    points.sort(key=lambda p: math.atan2(p[1] - pivot[1], p[0] - pivot[0]), reverse=True)

    return divide(points)

def divide(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    # Divide list into two parts in O(1) time
    if len(points) <= 3:
        return points
    midpoint = len(points) // 2
    left_half = points[:midpoint].copy()
    right_half = points[midpoint:].copy()

    # Recursively divide into smaller pieces in O(logn) time
    if len(left_half) > 3:
        left_half = divide(left_half)
    if len(right_half) > 3:
        right_half = divide(right_half)

    # Go to conquer (merge) algorithm
    return conquer(left_half, right_half)

def conquer(left_half: list[tuple[float, float]], right_half: list[tuple[float, float]]) -> list[tuple[float, float]]:

    starting_points: list[tuple[float, float], tuple[float, float]] = [random.choice(left_half), random.choice(right_half)]
    
    # Find rightmost in left half in O(n) time
    for key, point in enumerate(left_half):
        if point[0] > starting_points[0][0]:
            starting_points[0] = point
    
    # Find leftmost in right half O(n) time
    for key, point in enumerate(right_half):
        if point[0] < starting_points[1][0]:
            starting_points[1] = point

    
    # Find upper tangent in O(n) time
    upper_tangent = starting_points.copy()

    for key,point in enumerate(left_half):
        if point[1] > upper_tangent[0][1]:
            upper_tangent[0] = point
    
    for key, point in enumerate(right_half):
        if point[1] > upper_tangent[1][1]:
            upper_tangent[1] = point
    
    lower_tangent = starting_points.copy()

    for key, point in enumerate(left_half):
        if point[1] < lower_tangent[0][1]:
            lower_tangent[0] = point
    
    for key,point in enumerate(right_half):
        if point[1] < lower_tangent[1][1]:
            lower_tangent[1] = point

    # Delete contained points from hull 
    #hull = list(itertools.chain(left_half, right_half))
    test_point = clockwise(left_half, upper_tangent[0])
    while test_point != lower_tangent[0]:
        next_point = clockwise(left_half, test_point)
        left_half.remove(test_point)
        test_point = next_point

    test_point = clockwise(right_half, upper_tangent[1], True)
    while test_point != lower_tangent[1]:
        next_point = clockwise(right_half, test_point, True)
        right_half.remove(test_point)
        test_point = next_point

    hull = list(itertools.chain(left_half, right_half))
    return hull

def clockwise(points: list[tuple[float, float]], point: tuple[float, float], counter=False) -> tuple[float, float]:
    clockwise_point: tuple[float, float]
    index: int
    try:
        index = points.index(point)
    except:
        raise ValueError
    
    try:
        if counter:
            clockwise_point = points[index - 1]
        else:
            clockwise_point = points[index + 1]
    except:
        if counter:
            clockwise_point = points[-1]
        else:
            clockwise_point = points[0]
    
    return clockwise_point
    


