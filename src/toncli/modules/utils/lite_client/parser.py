def split_get_output(output: str):
    """'
    Parse output like:
    -1 0 CS{Cell{...} bits: 64..66; refs: 0..0} CS{Cell{...} bits: 66..333; refs: 0..0} C{...}
    To:
    [-1, 0, "CS{Cell{...} bits: 64..66; refs: 0..0}", "CS{Cell{...} bits: 66..333; refs: 0..0}", "C{...}"]

    """

    data = output.split()
    result = []

    to_fix = 0
    for i in data:
        if to_fix > 0:
            result[-1] += f" {i}"
        else:
            result.append(i)

        tmp_to_fix = i.count('{')
        tmp_to_not_fix = i.count("}")
        to_fix += tmp_to_fix - tmp_to_not_fix

    return result


if __name__ == "__main__":
    print(split_get_output("-1 0 CS{Cell{...} bits: 64..66; refs: 0..0} CS{Cell{...} bits: 66..333; refs: 0..0} C{...}"))
