# Uncomment this line to import some functions that can help
# you debug your algorithm
# from plotting import draw_line, draw_hull, circle_point


def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""

    # Sorting algorithm: O(nlogn) time
    pivot: tuple[float, float] = max(points, key=lambda p: (p[0], p[1]))
    points.sort(key=lambda p: math.atan2(p[1] - pivot[1], p[0] - pivot[0]), reverse=True)

    return divide(points)

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
    starting_points: tuple[tuple[float, float], tuple[float, float]] = tuple(random.choice(left_half), random.choice(right_half))
    rightmost_position: int
    leftmost_position: int
    
    # Find rightmost in left half in O(n) time
    for key, point in enumerate(left_half):
        if point[0] > starting_points[0][0][0]:
            starting_points[0][0] = point
            rightmost_position = key
        elif point[0] == starting_points[0][0][0]:
            if point[1] > starting_points[0][0][1]:
                starting_points[0][0] = point
                rightmost_position = key
            else:
                rightmost_position = key - 1
    
    # Find leftmost in right half O(n) time
    for key, point in enumerate(right_half):
        if point[0] > starting_points[0][0][0]:
            starting_points[0][0] = point
            rightmost_position = key
        elif point[0] == starting_points[0][0][0]:
            if point[1] > starting_points[0][0][1]:
                starting_points[0][0] = point
                rightmost_position = key
            else:
                rightmost_position = key - 1
    
    # Find upper tangent in O(n) time
    upper_tangent = starting_points
    # for key, point in enumerate(left_half):


    # Find upper tangent and lower tangent in O(n) time
    upper_tangent: tuple[tuple[float, float], tuple[float, float]] = tuple[rightmost, leftmost]
    counterwise_rightmost = left_half


