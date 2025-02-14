# Uncomment this line to import some functions that can help
# you debug your algorithm
from plotting import draw_line, draw_hull, circle_point
import math, random, itertools

def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""
    # Sorting algorithm: O(nlogn) time
    #left_half = sort_points(left_half)
    #right_half = sort_points(right_half)
    return divide(sort_points(points))

def sort_points(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    # Sort points in counter-clockwise order
    center_x = sum(p[0] for p in points) / len(points)
    center_y = sum(p[1] for p in points) / len(points)
    
    def angle(point):
        return math.atan2(point[1] - center_y, point[0] - center_x)
    
    return sorted(points, key=angle)

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
    left_tangent, right_tangent = starting_points
    done = False

    while not done:
        done = True
        # The loop continues as long as the point before the current left_tangent is above the line formed by left_tangent and right_tangent.

        while is_above(left_tangent, right_tangent, left_half[(left_half.index(left_tangent) - 1) % len(left_half)]) if is_upper else is_below(left_tangent, right_tangent, left_half[(left_half.index(left_tangent) + 1) % len(left_half)]):
            #circle_point(left_half[left_half.index(left_tangent) - 1])
            #draw_line(left_tangent, right_tangent)
            left_tangent = left_half[(left_half.index(left_tangent) - 1) % len(left_half)] if is_upper else left_half[(left_half.index(left_tangent) + 1) % len(left_half)]
            done = False
        while is_above(left_tangent, right_tangent, right_half[(right_half.index(right_tangent) + 1) % len(right_half)]) if is_upper else is_below(left_tangent, right_tangent, right_half[(right_half.index(right_tangent) - 1) % len(right_half)]):
            right_tangent = right_half[(right_half.index(right_tangent) + 1) % len(right_half)] if is_upper else right_half[(right_half.index(right_tangent) - 1) % len(right_half)]
            done = False
    return [left_tangent, right_tangent]

def is_above(p1, p2, p):
    return (p2[0] - p1[0]) * (p[1] - p1[1]) - (p2[1] - p1[1]) * (p[0] - p1[0]) > 0

def is_below(p1, p2, p):
    return (p2[0] - p1[0]) * (p[1] - p1[1]) - (p2[1] - p1[1]) * (p[0] - p1[0]) < 0

def combine_hulls(left_half, right_half, upper_tangent, lower_tangent):
    hull = []
    
    index = left_half.index(upper_tangent[0])
    while left_half[index] != lower_tangent[0]:
        circle_point(left_half[index])
        hull.append(left_half[index])
        index = (index - 1) % len(left_half)
    hull.append(lower_tangent[0])

    index = right_half.index(lower_tangent[1])
    while right_half[index] != upper_tangent[1]:
        circle_point(right_half[index])
        hull.append(right_half[index])
        index = (index - 1) % len(right_half)
    hull.append(upper_tangent[1])
    return hull