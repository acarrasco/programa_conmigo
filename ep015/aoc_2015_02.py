from itertools import combinations

boxes = [sorted(map(int, line.split('x'))) for line in open('input.txt')]

# part 1
def git_wrapping_area(box):
    # w, h, l = box
    # return 2*w*h + 2*w*l + 2*h*l + w*h
    return box[0] * box[1] + 2 * sum(a*b for a, b in combinations(box, 2))

total_wrapping_area = sum(map(git_wrapping_area, boxes))
print(total_wrapping_area)

# part 2

def git_ribbon_length(box):
    w, h, l = box
    return 2*w + 2*h + w*h*l

total_ribbon_length = sum(map(git_ribbon_length, boxes))
print(total_ribbon_length)
