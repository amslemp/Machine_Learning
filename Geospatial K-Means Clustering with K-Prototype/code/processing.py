from math import radians, sin, cos, sqrt, atan2

# Haversine formula to calculate distance between two points
def calculate_distance(fix_lat1, fix_lon1, dflat, dflon, fix_lat2, fix_lon2):
    # Convert latitude and longitude to radians
    rlat1, rlon1, rlat2, rlon2, rlat3, rlon3 = map(radians, [fix_lat1, fix_lon1, dflat, dflon, fix_lat2, fix_lon2])

    # Haversine formula
    dlon = rlon2 - rlon1
    dlat = rlat2 - rlat1
    a = sin(dlat / 2)**2 + cos(rlat1) * cos(rlat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance1 = 3958.8 * c # Radius of Earth is 3958.8
    
    dlon2 = rlon2 - rlon3
    dlat2 = rlat2 - rlat3
    a2 = sin(dlat2 / 2)**2 + cos(rlat3) * cos(rlat2) * sin(dlon2 / 2)**2
    c2 = 2 * atan2(sqrt(a2), sqrt(1 - a2))
    distance2 = 3958.8 * c2
    
    if distance1 < distance2:
        distance = distance1
    else:
        distance = distance2
        
    return distance
