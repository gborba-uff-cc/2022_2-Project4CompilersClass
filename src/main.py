'''
Compiler front-end entry point
'''

# run with:
# python -B -OO .\src\main.py .\src\input.cm
# python -B -OO .\src\main.py .\src\input.cm --sourceScan --echoSource


import argparse
import dataclasses
import sys
import typing

import scanner.scanner as ss


def Main() -> int:
    moduleOptions = CreateCLIArgumentParser().parse_args(namespace=ModuleOptions())
    # ----------
    # NOTE - open the source file, show error if file not found
    if moduleOptions.sourceScan:
        RunScanner(moduleOptions)
    # ----------
    if moduleOptions.sourceParse:
        RunParser(moduleOptions)
    # ----------
    return 0


def CreateCLIArgumentParser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(
        prefix_chars = '-',
        description = '',
        epilog = ''
    )
    cli.add_argument(
        'sourcePath',
        help='Path to source file going to be compiled.')
    # ----------
    cli.add_argument(
        '--sourceScan',
        help='Run scan step on source',
        action='store_true')
    cli.add_argument(
        '--echoSourceLines',
        help='Show line number and content while scanning source',
        action='store_true')
    cli.add_argument(
        '--echoTraceScanner',
        help='Show recognized token information while scanning source',
        action='store_true')
    # ----------
    cli.add_argument(
        '--sourceParse',
        help='Run parse step on source',
        action='store_true')
    cli.add_argument(
        '--echoTraceParser',
        help='Show statements information while parsing source',
        action='store_true')
    return cli

@dataclasses.dataclass
class ModuleOptions(argparse.Namespace):
    sourcePath: str
    # ----------
    sourceScan: bool
    echoSourceLines: bool
    echoTraceScanner: bool
    # ----------
    sourceParse: bool
    echoTraceParser: bool
    # ----------
    # NOTE - define where to print
    outputTo: typing.TextIO = sys.stdout

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


def RunScanner(options: ModuleOptions):
    with open(options.sourcePath, mode='r', encoding='utf-8') as sourceCode:
        # NOTE - scan if should scan
        token = ss.Token(ss.TokenType.ERROR, '')
        sourceScanner = ss.Scanner(
            sourceCode,
            options.outputTo,
            options.echoSourceLines,
            options.echoTraceScanner)
        while token.type is not ss.TokenType.EOF:
            token = sourceScanner.GetToken()
    return


def RunParser(options: ModuleOptions):
    print(NotImplementedError(f'["if moduleOptions.sourceParse:" branch on {Main.__qualname__} isn\'t implemented yet]'))
    exit(1)
    with open('', mode='r', encoding='utf-8') as sourceCode:
        pass
    return

if __name__ == '__main__':
    exit_code = Main()
    exit(exit_code)
