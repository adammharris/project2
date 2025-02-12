# Uncomment this line to import some functions that can help
# you debug your algorithm
# from plotting import draw_line, draw_hull, circle_point


def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""
    pivot = max(points, key=lambda p: (p[0], p[1]))
    points.sort(key=lambda p: math.atan2(p[1] - pivot[1], p[0] - pivot[0]), reverse=True)
    return divide(points)
    # Sorting in place (using .sort()) reduces space complexity
    # Time of sorting algorithm is O(nlogn)

def divide(points: list[tuple(float, float)]) -> list[tuple[float, float]]:
    # Divide list into two parts in O(1) time
    midpoint = len(points) // 2
    left_half = points[:midpoint]
    right_half = points[midpoint:]

    # Recursively divide into smaller pieces in O(logn) time
    left_half = divide(left_half)
    right_half = divide(right_half)

    # Go to conquer (merge) algorithm
    return conquer(left_half, right_half)

def conquer(left_half: list[tuple[float, float]], right_half: list[tuple[float, float]]) -> list[tuple[float, float]]:
    # Find rightmost point of left half, and leftmost point of right half in O(n) time
    rightmost: tuple[float, float] = max(left_half, key=lambda p: (p[0], p[1]))
    leftmost: tuple[float, float] = min(right_half, key=lambda p: (p[0], p[1]))

    # Find upper tangent and lower tangent in O(n) time
    upper_tangent: tuple[tuple[float, float], tuple[float, float]] = tuple[rightmost, leftmost]
    counterwise_rightmost = left_half


