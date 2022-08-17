import math

def solution(area):
    # Your code here
    result = []
    while area > 0:
        biggest_square_side = int(area **0.5)
        biggest_sqaure_area = biggest_square_side ** 2
        area -= biggest_sqaure_area
        result.append(biggest_sqaure_area)
    return(result)



print(solution(10))