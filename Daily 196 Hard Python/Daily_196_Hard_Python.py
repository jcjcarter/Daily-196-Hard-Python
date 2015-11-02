def tokenize(query, operators): # Doesn't really tokenize, but is similar to a tokenization routine
    tokens = []
    while query:
        c = query.pop(0)
        if c.isdigit():
            if tokens and tokens[-1].isdigit():
                tokens[-1] += c
            else:
                tokens += c
        elif c in operators:
            tokens += c
        elif c == "(":
            tokens += [tokenize(query, operators)]
        elif c == ")":
            break
        else:
            print(c, ": no such token!")
    return tokens


def split_recursive(tokens, operators):
    for op, assoc in reversed(operators):
        if op in tokens:
            if assoc == "left":
                index = len(tokens) - list(reversed(tokens)).index(op) - 1
            else:
                index = tokens.index(op)
            left, mid, right = tokens[:index], tokens[index], tokens[index+1:]
            left = split_recursive(left, operators) if len(left) > 1 else left[0]
            right = split_recursive(right, operators) if len(right) > 1 else right[0]
            return [left, mid, right]
    return tokens


def expr_to_string(expr):
    return "(%s)" % "".join(expr_to_string(val) if isinstance(val, list) else val for val in expr)


def main():
    _, *lines, query = open("input.txt").read().splitlines()
    operators = [line.split(":") for line in lines]

    tokens = tokenize(list(query), [op for op, _ in operators])

    for i, val in enumerate(tokens):
        if isinstance(val, list):
            tokens[i] = split_recursive(tokens[i], operators)
    expr = split_recursive(tokens, operators)

    print(expr_to_string(expr))


if __name__ == "__main__":
    main()