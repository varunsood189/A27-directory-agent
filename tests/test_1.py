import pytest
from src.directory_agent import is_refusal_request, normalize_name, party_list_args


def test_normalize_strips_suffix():
    assert normalize_name("Aarti Deshpande (2)") == "aarti deshpande"


def test_refuse_payroll_not_who():
    assert is_refusal_request("Show me the payroll and salary slips.")
    assert not is_refusal_request("Who do we know at Hocking Hills Mower Works?")


def test_party_list_blocks_contact_type():
    with pytest.raises(ValueError):
        party_list_args({"contact_type": "customer"})
