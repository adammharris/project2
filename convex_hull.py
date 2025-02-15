# Uncomment this line to import some functions that can help
# you debug your algorithm
from plotting import draw_line, draw_hull, circle_point
import math, random, itertools

def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""
    # Sorting algorithm: O(nlogn) time
    #left_half = sort_points(left_half)
    #right_half = sort_points(right_half)
    return divide(sorted(points))

def cross_product(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

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
    else:
        if len(left_half) == 3:
            p1, p2, p3 = left_half
            if cross_product(p1, p2, p3) > 0:
                left_half = (p1, p3, p2)
            else:
                left_half = (p1, p2, p3)
        elif len(left_half) < 3:
            left_half.sort()
    if len(right_half) > 3:
        right_half = divide(right_half)

    # Go to conquer (merge) algorithm
    return conquer(left_half, right_half)

def conquer(left_half: list[tuple[float, float]], right_half: list[tuple[float, float]]) -> list[tuple[float, float]]:

    starting_points: list[tuple[float, float], tuple[float, float]] = [random.choice(left_half), random.choice(right_half)]
    draw_hull(left_half)
    draw_hull(right_half)
    
    # Find rightmost point of left hull and leftmost point of right hull in O(n) time
    starting_points = [max(left_half, key=lambda p: p[0]), min(right_half, key=lambda p: p[0])]

    upper_tangent = find_tangent(left_half, right_half, starting_points, True)
    lower_tangent = find_tangent(left_half, right_half, starting_points, False)

    draw_line(lower_tangent[0], lower_tangent[1])
    draw_line(upper_tangent[0], upper_tangent[1])

    # Delete contained points from hull 
    hull = combine_hulls(left_half, right_half, upper_tangent, lower_tangent)

    draw_hull(hull)
    return hull

def find_tangent(left_half, right_half, starting_points, is_upper):
    raise NotImplementedError

def is_above(p1, p2, p):
    return (p2[0] - p1[0]) * (p[1] - p1[1]) - (p2[1] - p1[1]) * (p[0] - p1[0]) > 0

def is_below(p1, p2, p):
    return (p2[0] - p1[0]) * (p[1] - p1[1]) - (p2[1] - p1[1]) * (p[0] - p1[0]) < 0

def combine_hulls(left_half, right_half, upper_tangent, lower_tangent):
    raise NotImplementedError