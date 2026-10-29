from histo import HISTOQL_GRAMMAR
from lark.exceptions import UnexpectedInput
from lark import Lark, Transformer, Token

parser = Lark(HISTOQL_GRAMMAR, parser="lalr", start="start")

def test_valid(label, code):
    """The input should be accepted by the grammar."""
    try:
        parser.parse(code)
        print(f"[PASS] {label}")
        return True
    except UnexpectedInput as e:
        print(f"[FAIL] {label}: {e.__class__.__name__}")
        return False


def test_invalid(label, code):
    """The input should be rejected by the grammar."""
    try:
        parser.parse(code)
        print(f"[FAIL] {label}: expected rejection")
        return False
    except UnexpectedInput:
        print(f"[PASS] {label}: rejected as expected")
        return True


# =====================================
# TESTS 1 — VALID INPUTS
# =====================================

valid_tests = [
    ("Basic query",
     'FIND people RETURN name;'),

    ("Query without RETURN",
     'FIND events;'),

    ("Multiple return attributes",
     'FIND people RETURN name, birth_year;'),

    ("Temporal filter",
     'FIND people DURING 1800..1850 RETURN name;'),

    ("Location filter",
     'FIND people IN "Portugal" RETURN name;'),

    ("WHO relation clause",
     'FIND people WHO occupation "scientist" RETURN name;'),

    ("THAT relation clause",
     'FIND people THAT occupation "scientist" RETURN name;'),

    ("WHERE comparison",
     'FIND people WHERE birth_year >= 1800 RETURN name;'),

    ("Multiple clauses",
     'FIND people IN "France" DURING 1800..1900 '
     'WHERE birth_year >= 1850 RETURN name;'),

    ("LET statement",
     'LET researchers = FIND people RETURN name;'),

    ("IF with EXISTS",
     'IF EXISTS researchers { FIND people RETURN name; }'),

    ("IF with COUNT",
     'IF people COUNT >= 2 { FIND people RETURN name; }'),

    ("IF with ELSE",
     'IF EXISTS researchers { FIND people; } '
     'ELSE { FIND events; }'),

    ("FOR EACH loop",
     'FOR EACH person IN researchers { FIND people RETURN name; }'),

    ("RESEARCH block",
     'RESEARCH "Historical study" { '
     'FIND people DURING 1800..1900 RETURN name; }'),

    ("Comment before query",
     '# Test query\nFIND people RETURN name;'),
]


# =====================================
# TESTS 2 — INVALID INPUTS
# =====================================

invalid_tests = [
    ("Missing semicolon",
     'FIND people RETURN name'),

    ("Unknown entity",
     'FIND animals RETURN name;'),

    ("Missing entity",
     'FIND RETURN name;'),

    ("Missing attribute after RETURN",
     'FIND people RETURN;'),

    ("Missing WHERE value",
     'FIND people WHERE birth_year >= RETURN name;'),

    ("Missing second year",
     'FIND people DURING 1834.. RETURN name;'),

    ("Missing relation value",
     'FIND people WHO occupation RETURN name;'),

    ("Missing location value",
     'FIND people IN RETURN name;'),

    ("IF without a block",
     'IF EXISTS researchers FIND people;'),

    ("Incomplete FOR EACH loop",
     'FOR EACH person IN { FIND people; }'),

    ("Unclosed RESEARCH block",
     'RESEARCH "Study" { FIND people;'),

    ("Invalid comparison operator",
     'FIND people WHERE birth_year === 1800;'),
]


# =====================================
# RUN ALL TESTS
# =====================================

results = []

print("\n=== VALID INPUT TESTS ===")
for label, code in valid_tests:
    results.append(test_valid(label, code))

print("\n=== INVALID INPUT TESTS ===")
for label, code in invalid_tests:
    results.append(test_invalid(label, code))
