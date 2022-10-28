# import sys

# print(sys.version,flush=False)
# print("Olá mundo.",flush=False)

import finite_automaton.automaton_language_cminus as fa_cminus

def main():
    Mk = fa_cminus.CreateDFAKeywords()

    print(f'{Mk.accept("if")=}')
    print(f'{Mk.accept("int")=}')
    print(f'{Mk.accept("else")=}')
    print(f'{Mk.accept("void")=}')
    print(f'{Mk.accept("while")=}')
    print(f'{Mk.accept("return")=}')
    print(f'{Mk.accept("joga muito facil")=}')
    print(f'{Mk.accept("")=}')
    return 0

if __name__ == '__main__':
    exit_code = main()
    exit(exit_code)
