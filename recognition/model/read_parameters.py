
def read_classes(filename: str) -> list[str]:
    with open(filename, 'r') as desc:
        return [l.rstrip() for l in desc.readlines()]


def read_anchors(filename: str) -> list[list[int]]:
    with open(filename, 'r') as desc:
        result_list = []
        for line in desc.readlines():
            result_list.append([int(num) for num in line.rstrip().split(' ')])
        return result_list
