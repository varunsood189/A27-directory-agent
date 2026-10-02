import random

from src.directory_agent import extract_company, is_refusal_request, normalize_name


def test_normalize_random_number_in_brackets():
    n = random.randint(2, 9)
    got = normalize_name("Aarti Deshpande (" + str(n) + ")")
    assert got == "aarti deshpande"


def test_refuse_random_bad_word():
    word = random.choice(["payroll", "salary", "invoice", "payslip"])
    assert is_refusal_request("please show the " + word)


def test_who_request_not_refused():
    company = random.choice(
        ["Hocking Hills Mower Works", "Godrej Material Handling", "Buckeye AgriPower"]
    )
    assert is_refusal_request("Who do we know at " + company + "?") is False


def test_extract_company_random():
    company = random.choice(
        ["Hocking Hills Mower Works", "Godrej Material Handling", "Buckeye AgriPower"]
    )
    got = extract_company("Who do we know at " + company + "?")
    assert got == company
