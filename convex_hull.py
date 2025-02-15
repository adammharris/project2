# Uncomment this line to import some functions that can help
# you debug your algorithm
# from plotting import draw_line, draw_hull, circle_point

def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""
    # Sorting algorithm: O(nlogn) time
    points.sort()
    return divide(points)

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

    # Combine hulls in O(n) time
    hull = combine_hulls(left_half, right_half, upper_tangent, lower_tangent)

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

def orientation(p, q, r):
    """Returns positive if counterclockwise, negative if clockwise, and 0 if collinear"""
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])

def is_above(p1, p2, p):
    return orientation(p1, p2, p) > 0

def is_below(p1, p2, p):
    return orientation(p1, p2, p) < 0

def combine_hulls(left_half, right_half, upper_tangent, lower_tangent):
    hull_size = len(left_half) + len(right_half)
    hull = [None] * hull_size  # Preallocate list
    
    index = 0  # Track insertion index

    # Start at right lower tangent
    i = lower_tangent[0]
    # Iterate until right upper tangent
    while i != upper_tangent[0]:
        hull[index] = left_half[i]
        index += 1
        i = (i + 1) % len(left_half)  # Move clockwise
    hull[index] = left_half[i]
    index += 1

    # Start at left upper tangent
    i = upper_tangent[1]
    # Iterate until left lower tangent
    while i != lower_tangent[1]:
        hull[index] = right_half[i]
        index += 1
        i = (i + 1) % len(right_half)  # Move clockwise
    hull[index] = right_half[i]
    index += 1

    # Return only the used portion of the preallocated list
    return hull[:index]  # Slice to remove unused `None` values