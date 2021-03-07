
def get_grade(level):
    if level <= 10:
        return 1
    else:
        return min(19, int((level - 1) / 20) + 2)


def get_real_level(level, enhance):
    if level < 240:
        return level
    else:
        return (level - 240) * 10 + 240 + enhance




