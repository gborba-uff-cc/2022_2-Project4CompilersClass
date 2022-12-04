'''
Compiler front-end entry point
'''

# run with:
# python -B -OO .\src\main.py .\input.cm --sourceScan --echoSourceLines --echoTraceScanner --sourceParse --echoTraceParser

import argparse
import dataclasses
import io
import sys
import typing

import finite_automaton.automaton_language_cminus as fa_alc
import scanner.scanner as ss
import parser.parser as pp
import structures.token as st


def Main() -> int:
    """
    Execute the compiler front-end code.
    """
    moduleOptions = CreateCLIArgumentParser().parse_args(namespace=ModuleOptions())
    moduleOptions.scannerOutputFile = f'{moduleOptions.sourcePath}{moduleOptions.scannerOutputFileSuffix}'
    moduleOptions.parserOutputFile = f'{moduleOptions.sourcePath}{moduleOptions.parserOutputFileSuffix}'

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
    """
    Generate and configure this module cli parser.
    """
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
    scannerOutputFile: str
    # ----------
    sourceParse: bool
    echoTraceParser: bool
    parserOutputFile: str
    # ----------
    scannerOutputFileSuffix: str = '.scannero'
    parserOutputFileSuffix: str = '.parsero'
    filesEncoding: str = 'utf-8'
    # NOTE - define where to print
    outputTo: typing.TextIO = sys.stdout

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


def RunScanner(options: ModuleOptions):
    """
    Scan the source file provided on options and generate the scanner output file.
    """
    textEchoBuffer = options.outputTo

    with open(options.sourcePath, mode='r', encoding=options.filesEncoding) as sourceCode, \
         open(options.scannerOutputFile, mode='w', encoding=options.filesEncoding) as fileTokens:
        token = st.Token(st.TokenType.ERROR, '')
        sourceScanner = ss.Scanner(
            sourceCode,
            textEchoBuffer,
            options.echoSourceLines,
            options.echoTraceScanner)
        while token.type is not st.TokenType.EOF:
            token = sourceScanner.GetToken()
            if __ShouldOutputToken(token):
                fileTokens.write(f'{token}\n')
    return

def __ShouldOutputToken(token: st.Token) -> bool:
    """
    Return True if the token will be printed to scanner output.
    """
    # NOTE - reject errors token that are blanks
    return not (
        (token.type is  st.TokenType.ERROR and token.value in fa_alc.blanks) or
        (token.type is st.TokenType.COMMENT))

def RunParser(options: ModuleOptions):
    """
    Parse the scanner output related to the source file provided on options and
    generate the parser output file.
    """
    textEchoBuffer = options.outputTo

    # print(NotImplementedError(f'["if moduleOptions.sourceParse:" branch on {Main.__qualname__} isn\'t implemented yet]'))
    # exit(1)
    with open(options.scannerOutputFile, mode='r', encoding=options.filesEncoding) as inputFile, \
         open(options.sourcePath, mode='r', encoding=options.filesEncoding) as outputFile:
        sourceParser = pp.Parser(inputFile, textEchoBuffer, options.echoTraceParser)
        sourceParser.Parse()
        pass
    return

if __name__ == '__main__':
    exit_code = Main()
    exit(exit_code)
