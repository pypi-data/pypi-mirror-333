#!/usr/bin/env python3

import sys
import random
import sply

prompt = "; "\
         "You are a guile interpreter. "\
         "Assume the input code contains no mistakes or typos. "\
         "Your task is to evaulate the single current line of input,"\
         " then display the correct standard output. "\
         "Do not think out loud. "\
         "You will not generate markdown code blocks. "\
         "\n"\
         "scheme@(guile-user)> (+ 1 1)\n"\
         "$1 = 2\n"\
         "scheme@(guile-user)> (+ 2 1)\n"\
         "$1 = 3\n"


def main ():
    model_id = "default-code"
    num_ctx = 1_000

    for argv in sys.argv[1:]:
        if argv.find("model_id=") == 0:
            model_id = argv[9:]

    c = sply.chat(
        model_id=model_id,
        rev_prompt="\nscheme@(guile-user)> ",
        prompt=prompt,
        in_suffix_enabled=False,
        num_ctx=num_ctx,
        )

    print(c.prompt, end="", flush=True)
    c.read(show=True)

    c.write("(* 3 2)\n", show=True)
    c.read(show=True)

    print()
    return 0


if __name__ == "__main__":
    exit(main())


