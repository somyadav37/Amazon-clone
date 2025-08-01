import math

# Define pi as a constant since some languages don't support math.pi
PI = 3.14159265358979323846

def surface_function(x, A, B):
    """Calculate Y = sum(sin(A[i] + B[i]*x)) for i=0 to n-1"""
    y = 0
    for i in range(len(A)):
        y += math.sin(A[i] + B[i] * x)
    return y

def find_local_maxima(A, B):
    """Find all local maxima in the range [0, 2π] using high-precision numerical methods"""
    if not A or not B:
        return []
    
    # Use very fine granularity for accurate peak detection
    num_points = 50000
    step = (2 * PI) / num_points
    
    maxima = []
    x_values = []
    y_values = []
    
    # Calculate function values at all sample points
    for i in range(num_points + 1):
        x = i * step
        y = surface_function(x, A, B)
        x_values.append(x)
        y_values.append(y)
    
    # Find local maxima by comparing with neighbors
    # Use a small tolerance for numerical stability
    tolerance = 1e-10
    
    for i in range(1, len(y_values) - 1):
        # Check if current point is higher than both neighbors
        if (y_values[i] > y_values[i-1] + tolerance and 
            y_values[i] > y_values[i+1] + tolerance):
            maxima.append(x_values[i])
        # Also check for flat regions that might be maxima
        elif (abs(y_values[i] - y_values[i-1]) <= tolerance and 
              abs(y_values[i] - y_values[i+1]) <= tolerance):
            # Check if this is part of a flat maximum
            left_slope = (y_values[i] - y_values[max(0, i-2)]) if i >= 2 else 0
            right_slope = (y_values[min(len(y_values)-1, i+2)] - y_values[i]) if i < len(y_values)-2 else 0
            if left_slope >= 0 and right_slope <= 0:
                maxima.append(x_values[i])
    
    # Check boundary points more carefully
    # At x = 0: check if function is decreasing immediately after
    if len(y_values) >= 3:
        if y_values[0] >= y_values[1] - tolerance and y_values[1] >= y_values[2]:
            if 0.0 not in [round(x, 10) for x in maxima]:
                maxima.insert(0, 0.0)
    
    # At x = 2π: check if function is increasing immediately before
    if len(y_values) >= 3:
        if y_values[-1] >= y_values[-2] - tolerance and y_values[-2] >= y_values[-3]:
            two_pi = 2 * PI
            if round(two_pi, 10) not in [round(x, 10) for x in maxima]:
                maxima.append(two_pi)
    
    # Remove duplicates and sort
    unique_maxima = []
    for x in maxima:
        x_rounded = round(x, 10)
        found = False
        for existing in unique_maxima:
            if abs(x_rounded - existing) < 1e-8:
                found = True
                break
        if not found:
            unique_maxima.append(x_rounded)
    
    return sorted(unique_maxima)

def solve_borewell_problem():
    # Read input
    n = int(input().strip())
    A = list(map(int, input().strip().split()))
    B = list(map(int, input().strip().split()))
    
    # Find local maxima
    maxima = find_local_maxima(A, B)
    
    if len(maxima) < 2:
        # If less than 2 maxima, there's only one possible valley
        print(1)
        return
    
    # Calculate valley widths
    valley_widths = []
    for i in range(len(maxima) - 1):
        width = maxima[i + 1] - maxima[i]
        valley_widths.append(width)
    
    # Find the widest valley (leftmost if there are ties)
    max_width = max(valley_widths)
    widest_valley_index = -1
    
    for i, width in enumerate(valley_widths):
        if abs(width - max_width) < 1e-10:  # Account for floating point precision
            widest_valley_index = i + 1  # 1-indexed
            break
    
    print(widest_valley_index)

if __name__ == "__main__":
    solve_borewell_problem()