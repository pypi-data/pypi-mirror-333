from xeger.xeger import Xeger, XegerError
import argparse

parser = argparse.ArgumentParser(
    description="Generate a string matching a provided regular expression"
)
parser.add_argument(
    "regex", type=str, help="The regular expression to generate a string for"
)
parser.add_argument(
    "-c",
    "--check",
    action="store_true",
    help="Check if the generated string matches the regular expression using a PCRE regex engine",
)

args = parser.parse_args()

xeger = Xeger()
try:
    result = xeger.generate(args.regex, args.check)
    print(result)
except XegerError as e:
    print(e)
    exit(1)
