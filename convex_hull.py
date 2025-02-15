# Uncomment this line to import some functions that can help
# you debug your algorithm
from plotting import draw_line, draw_hull, circle_point

def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""
    # Sorting algorithm: O(nlogn) time
    return divide(sorted(points))

def slope(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2:
        return float('inf')
    return (y2 - y1) / (x2 - x1)

def divide(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    # Divide list into two parts in O(1) time
    if len(points) <= 3:
        return points
    midpoint = len(points) // 2
    left_half = points[:midpoint]
    right_half = points[midpoint:]

    
    def sort3(half):
        half.sort()
        p1, p2, p3 = half
        slope2 = slope(p1, p2)
        slope3 = slope(p1, p3)
        if slope2 > slope3:
            return [p1, p2, p3]
        else:
            return [p1, p3, p2]
    
    # Recursively divide into smaller pieces in O(logn) time
    if len(left_half) > 3:
        left_half = divide(left_half)
    else:
        # Simple, constant time sorting
        if len(left_half) == 3:
            left_half = sort3(left_half)
        elif len(left_half) < 3:
            left_half.sort()
    if len(right_half) > 3:
        right_half = divide(right_half)
    else:
        # Simple, constant time sorting
        if len(right_half) == 3:
            right_half = sort3(right_half)
        elif len(right_half) < 3:
            right_half.sort()

    # Go to conquer (merge) algorithm
    return conquer(left_half, right_half)

def conquer(left_half: list[tuple[float, float]], right_half: list[tuple[float, float]]) -> list[tuple[float, float]]:
    # Find rightmost point of left hull and leftmost point of right hull in O(n) time
    starting_points = [left_half.index(max(left_half, key=lambda p: p[0])), right_half.index(min(right_half, key=lambda p: p[0]))]

    # Find tangent lines in O(n) time
    upper_tangent = find_tangent(left_half, right_half, starting_points, True)
    lower_tangent = find_tangent(left_half, right_half, starting_points, False)

    # draw_line(left_half[upper_tangent[0]], right_half[upper_tangent[1]])
    # draw_line(left_half[lower_tangent[0]], right_half[lower_tangent[1]])

    # Combine hulls in O(n) time
    hull = combine_hulls(left_half, right_half, upper_tangent, lower_tangent)

    # draw_hull(hull)
    return hull

def find_tangent(left_half, right_half, starting_points, is_upper):
    # Find tangent line in O(n) time
    left_tangent = starting_points[0]
    right_tangent = starting_points[1]

    while True:
        left_stable = True
        right_stable = True

        # Move counter if upper, move clockwise if lower
        next_left_index = (left_tangent - 1) % len(left_half) if is_upper else (left_tangent + 1) % len(left_half)

        next_left = left_half[next_left_index]

        # Check if left tangent point is valid
        if is_above(left_half[left_tangent], right_half[right_tangent], next_left) if is_upper else is_below(left_half[left_tangent], right_half[right_tangent], next_left):
            left_tangent = next_left_index
            left_stable = False

        # Move clockwise if upper, move counter if lower
        next_right_index = (right_tangent + 1) % len(right_half) if is_upper else (right_tangent - 1) % len(right_half)

        next_right = right_half[next_right_index]

        if is_above(left_half[left_tangent], right_half[right_tangent], next_right) if is_upper else is_below(left_half[left_tangent], right_half[right_tangent], next_right):
            right_tangent = next_right_index
            right_stable = False

        if left_stable and right_stable:
            break

    return [left_tangent, right_tangent]

def is_above(p1, p2, p):
    x1, y1 = p1
    x2, y2 = p2
    x, y = p

    if x1 == x2:  # Vertical line
        return x > x1  # Assuming "above" means to the right for a vertical line
    else:
        m = slope(p1, p2)
        b = y1 - m * x1
        return y > m * x + b

def is_below(p1, p2, p):
    return (p2[0] - p1[0]) * (p[1] - p1[1]) - (p2[1] - p1[1]) * (p[0] - p1[0]) < 0

def combine_hulls(left_half, right_half, upper_tangent, lower_tangent):
    # Find hull in O(n) time
    hull = []
    
    # Start at left lower tangent
    index = lower_tangent[0]
    while index != upper_tangent[0]:
        circle_point(left_half[index])
        hull.append(left_half[index])
        # circle clockwise
        index = (index + 1) % len(left_half)
        # until we reach the left upper tangent
    hull.append(left_half[index])

    # Start at the right upper tangent
    index = upper_tangent[1]
    while index != lower_tangent[1]:
        circle_point(right_half[index])
        hull.append(right_half[index])
        # circle clockwise
        index = (index + 1) % len(right_half)
        # until we reach the right lower tangent
    hull.append(right_half[index])
    return hull