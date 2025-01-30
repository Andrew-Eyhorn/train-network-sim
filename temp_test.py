def dynamic_scale_alt(boundaries: list[float], multipliers: list[float], x: float) -> float:
    """
    Given a list of boundaries and boarder multipliers, scales the coordinate value based where it falls on the map
    """
    assert len(boundaries) == len(multipliers)
    assert x >= 0

    values = [boundaries[0]*multipliers[0]] * len(boundaries) #stores how much  to add depending on the boundary surpassed
    for i in range(1, len(boundaries)):
        values[i] = (boundaries[i] - boundaries[i-1]) * multipliers[i] + values[i-1]
    

    i = 0
    output = 0
    if x < boundaries[0]:
        return x * multipliers[0]
    while i < len(boundaries) and x > boundaries[i]:
        output = values[i]
        i += 1


    i-=1
    diff = x - boundaries[i]
    return diff * multipliers[min(i+1, len(boundaries)-1)] + output



if __name__ == "__main__":
    boundaires = [50, 100, 150]
    multipliers = [2,1,0.5]
    for i in range(0, 200):
        print(dynamic_scale_alt(boundaires, multipliers, i))
    print(dynamic_scale_alt(boundaires, multipliers, 300))
    print(dynamic_scale_alt(boundaires, multipliers, 299))
    print(dynamic_scale_alt(boundaires, multipliers, 102))
