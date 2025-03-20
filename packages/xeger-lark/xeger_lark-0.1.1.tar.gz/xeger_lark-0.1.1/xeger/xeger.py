from lark import Lark, Tree, ParseError
from lark.visitors import Interpreter
import os
import regex as re

cwd = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(cwd, "grammar.lark"), "r") as f:
    MealGrammar = Lark(f.read(), start="regex", parser="lalr")


class CharMap:
    def __init__(self):
        self.chars = [False] * 0x10000

    def set(self, bounds: list[tuple[str, str]]):
        for lower, upper in bounds:
            for i in range(ord(lower), ord(upper) + 1):
                self.chars[i] = True

    def find(self):
        for i, char in enumerate(self.chars):
            if char:
                return chr(i)
        return None

    def find_inverted(self):
        for i, char in enumerate(self.chars):
            if not char:
                return chr(i)
        return None


class XegerInterpreter(Interpreter):
    def __init__(self):
        super().__init__()
        self.result = ""

    def regex(self, tree):
        self.result = self.visit(tree.children[0])
        return self.result

    def expression(self, tree):
        # we don't care about any other options, just take first
        return self.visit(tree.children[0])

    def sub_expression(self, tree):
        res = ""

        for child in tree.children:
            i = self.visit(child)
            res += i

        return res

    def group(self, tree):
        item = self.visit(tree.children[0])

        if len(tree.children) == 2:
            quantifier, lazy_modifier = self.visit(tree.children[1])
            return item * quantifier
        return item

    def match(self, tree):
        item = self.visit(tree.children[0])

        if len(tree.children) == 2:
            quantifier, lazy_modifier = self.visit(tree.children[1])
            return item * quantifier

        return item

    def match_item(self, tree):
        child = tree.children[0]
        if isinstance(child, Tree):
            return self.visit(child)

        return child.value

    def match_any_character(self, tree):
        return "a"

    def match_character_class(self, tree):
        res = self.visit(tree.children[0])

        if isinstance(res, list):
            charmap = CharMap()
            charmap.set(res)
            return charmap.find()

        return res

    def character_group(self, tree):
        inverted = False
        if len(tree.children) == 1:
            charmap = self.visit(tree.children[0])
        else:
            inverted = True
            charmap = self.visit(tree.children[1])

        if inverted:
            return charmap.find_inverted()
        return charmap.find()

    def character_group_items(self, tree):
        charmap = CharMap()

        for child in tree.children:
            res = self.visit(child)
            charmap.set(res)

        return charmap

    def character_class(self, tree):
        return self.visit(tree.children[0])

    def character_class_any_word(self, tree):
        return [("a", "z"), ("A", "Z"), ("0", "9"), ("_", "_")]

    def character_class_any_word_inverted(self, tree):
        return [("\x00", "/"), (":", "@"), ("[", "^"), ("`", "`"), ("{", "\uffff")]

    def character_class_any_decimal_digit(self, tree):
        return [("0", "9")]

    def character_class_any_decimal_digit_inverted(self, tree):
        return [("\x00", "/"), (":", "\uffff")]

    def character_class_any_whitespace(self, tree):
        return [(" ", " "), ("\t", "\t"), ("\n", "\n")]

    def character_class_any_whitespace_inverted(self, tree):
        return [("\x00", "\x08"), ("\x0c", "\x1f"), ("\x1f", "\uffff")]

    def character_class_letters_and_digits(self, tree):
        return [("a", "z"), ("A", "Z"), ("0", "9")]

    def character_class_letters(self, tree):
        return [("a", "z"), ("A", "Z")]

    def character_class_ascii(self, tree):
        return [("\x00", "\x7f")]

    def character_class_blank(self, tree):
        return [(" ", " "), ("\t", "\t")]

    def character_class_control(self, tree):
        return [("\x00", "\x1f"), ("\x7f", "\x7f")]

    def character_class_graph(self, tree):
        return [("\x21", "\x7e")]

    def character_class_lower(self, tree):
        return [("a", "z")]

    def character_class_print(self, tree):
        return [("\x20", "\x7e")]

    def character_class_punct(self, tree):
        return [("!", "/"), (":", "@"), ("[", "`"), ("{", "~")]

    def character_class_upper(self, tree):
        return [("A", "Z")]

    def character_class_hexdigit(self, tree):
        return [("0", "9"), ("a", "f"), ("A", "F")]

    def unicode_category_name(self, tree):
        return tree.children[0].value

    def character_range(self, tree):
        lower_bound = self.visit(tree.children[0])

        if len(tree.children) == 1:
            return [(lower_bound, lower_bound)]

        upper_bound = self.visit(tree.children[1])

        return [(lower_bound, upper_bound)]

    def quantifier(self, tree):
        repeats = self.visit(tree.children[0])

        if len(tree.children) == 1:
            return (repeats, None)

        return [(repeats, tree.children[1].value)]

    def quantifier_type(self, tree):
        return self.visit(tree.children[0])

    def nonrange_quantifier(self, tree):
        match tree.children[0].type:
            case "ZERO_OR_MORE_QUANTIFIER":
                return 0
            case "ZERO_OR_ONE_QUANTIFIER":
                return 0
            case "ONE_OR_MORE_QUANTIFIER":
                return 1
        return 0

    def range_quantifier(self, tree):
        # this is always lower bound, which we can take
        return self.visit(tree.children[0])

    def range_quantifier_lower_bound(self, tree):
        return int(tree.children[0].value)

    def range_quantifier_upper_bound(self, tree):
        return int(tree.children[0].value)

    def anchor(self, tree):
        return tree.children[0].value

    def character(self, tree):
        return tree.children[0].value

    def character_not_backslash(self, tree):
        return tree.children[0].value


class XegerError(Exception):
    pass


class XegerRegexNotMatched(XegerError):
    pass


class XegerParserError(XegerError):
    pass


class XegerRegexCompileError(XegerError):
    pass


class Xeger:
    def __init__(self):
        self.interpreter = XegerInterpreter()

    def generate(self, data: str, check: bool = False) -> str:
        try:
            compiled_expr = re.compile(data)
        except re.error as e:
            raise XegerRegexCompileError(f"Failed to compile regex: {e}")
        try:
            tree = MealGrammar.parse(data)
        except ParseError as e:
            raise XegerParserError(f"Failed to parse regex: {e}")

        result = self.interpreter.visit(tree)

        if check:
            if not compiled_expr.match(result):
                raise XegerRegexNotMatched(
                    f"Generated string '{result}' does not match regex '{data}'"
                )

        return result
