# Utility functions for collision detection and polygon operations

# Polygon collision system
POLYGON_COORDINATES = []

def point_in_polygon(x, y, polygon):
    """Check if point (x, y) is inside polygon using ray casting algorithm"""
    n = len(polygon)
    inside = False
    
    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    
    return inside

def check_polygon_collision(x, y, width=50, height=100):
    """Check if the character position is inside the allowed polygon area"""
    if not POLYGON_COORDINATES:
        return False  # No polygon defined, allow movement
    
    # Check all four corners of the character rectangle
    corners = [
        (x, y),                    # Top-left
        (x + width, y),            # Top-right
        (x, y + height),           # Bottom-left
        (x + width, y + height)    # Bottom-right
    ]
    
    # If any corner is outside the polygon, block movement
    for corner_x, corner_y in corners:
        if not point_in_polygon(corner_x, corner_y, POLYGON_COORDINATES):
            return True  # Collision detected
    
    return False  # All corners inside polygon, allow movement

def set_polygon_boundaries(coordinates):
    """Set the polygon coordinates for movement boundaries"""
    global POLYGON_COORDINATES
    POLYGON_COORDINATES = coordinates
    print(f"Polygon boundaries set with {len(coordinates)} points")