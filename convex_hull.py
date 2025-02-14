# Uncomment this line to import some functions that can help
# you debug your algorithm
from plotting import draw_line, draw_hull, circle_point
import math, random, itertools

def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""
    # Sorting algorithm: O(nlogn) time
    return divide(sorted(points))

def divide(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    # Divide list into two parts in O(1) time
    if len(points) <= 3:
        return points
    midpoint = len(points) // 2
    left_half = points[:midpoint]
    right_half = points[midpoint:]

    # Recursively divide into smaller pieces in O(logn) time
    if len(left_half) > 3:
        left_half = divide(left_half)
    if len(right_half) > 3:
        right_half = divide(right_half)

    # Go to conquer (merge) algorithm
    return conquer(left_half, right_half)

def conquer(left_half: list[tuple[float, float]], right_half: list[tuple[float, float]]) -> list[tuple[float, float]]:

    starting_points: list[tuple[float, float], tuple[float, float]] = [random.choice(left_half), random.choice(right_half)]
    draw_hull(left_half)
    draw_hull(right_half)
    
    # Find rightmost in left half in O(n) time
    for key, point in enumerate(left_half):
        if point[0] > starting_points[0][0]:
            starting_points[0] = point
    
    # Find leftmost in right half O(n) time
    for key, point in enumerate(right_half):
        if point[0] < starting_points[1][0]:
            starting_points[1] = point

    
    upper_tangent = find_tangent(left_half, right_half, starting_points)
    lower_tangent = find_tangent(left_half, right_half, starting_points, False)

    draw_line(lower_tangent[0], lower_tangent[1])
    draw_line(upper_tangent[0], upper_tangent[1])
    # Delete contained points from hull 
    hull = list(itertools.chain(left_half, right_half))

    current_index = (left_half.index(upper_tangent[0]) + 1) % len(left_half)
    while left_half[current_index] != lower_tangent[0]:
        next_index = current_index + 1 % len(left_half)
        circle_point(left_half[current_index])
        hull.remove(left_half[current_index])
        current_index = next_index

    current_index = (right_half.index(upper_tangent[1]) - 1) % len(right_half)
    while right_half[current_index] != lower_tangent[1]:
        next_index = current_index - 1 % len(right_half)
        circle_point(right_half[current_index])
        hull.remove(right_half[current_index])
        current_index = next_index

    draw_hull(hull)
    return hull

def find_tangent(left_half, right_half, starting_points, is_upper=True):
    # Find upper tangent in O(n) time
    tangent = starting_points.copy()
    for key,point in enumerate(left_half):
        if is_upper:
            if point[1] > tangent[0][1]:
                tangent[0] = point
        else:
            if point[1] < tangent[0][1]:
                tangent[0] = point

    for key,point in enumerate(right_half):
        if is_upper:
            if point[1] > tangent[1][1]:
                tangent[1] = point
        else:
            if point[1] < tangent[1][1]:
                tangent[1] = point
    return tangent
