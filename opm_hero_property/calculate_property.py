
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


def get_base_attribute(base_att, level_growth, quality_per, quality_value, grade_value):
    return level_growth * quality_per/10000 + 1

