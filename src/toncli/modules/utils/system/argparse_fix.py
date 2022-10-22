# Copyright (c) 2022 Disintar LLP Licensed under the Apache License Version 2.0


from typing import List, Tuple


# I'm so sorry for this code, sorry, really
def argv_fix(command: List[str], string_kwargs: List[str]) -> Tuple[List[str], List[str]]:
    args = []
    kwargs = []

    next_will_be_kwarg = False
    for word in command:
        if '-' == word[0] and not next_will_be_kwarg:
            if word in string_kwargs:
                next_will_be_kwarg = True
            kwargs.append(word)
        elif next_will_be_kwarg:
            next_will_be_kwarg = False
            kwargs.append(word)
        else:
            args.append(word)
    return args, kwargs
