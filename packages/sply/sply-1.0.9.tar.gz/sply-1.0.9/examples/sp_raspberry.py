#!/usr/bin/env python3

import sys
import random
import sply


def main ():
    model_id = "default-code"
    seed = ""
    temp = 0.0
    num_ctx = 1_000

    for argv in sys.argv[1:]:
        if argv.find("model_id=") == 0:
            model_id = argv[9:]
        elif argv.find("seed=") == 0:
            seed = int(argv[5:])
        elif argv.find("temp=") == 0:
            temp = float(argv[5:])
        elif argv.find("num_ctx=") == 0:
            num_ctx = int(argv[8:])

    sp = sply.sp(
        show=True,
        model_id=model_id,
        seed=seed,
        temp=temp,
        num_ctx=num_ctx,
        )

    sp.runcode("name = \"raspberry\"")

    res = sp.runcode("print(name.count(\"r\"))")
    print(f"**{res}**")

    res = sp.runcode("print(name.count(\"r\"))")
    print(f"**{res}**")

    return 0


if __name__ == "__main__":
    exit(main())


