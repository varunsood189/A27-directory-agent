from src.directory_agent import normalize_name

def test_normalize_strips_number_two():
	got = normalize_name("Aarti Deshpande (2)")
	assert got == "aarti deshpande"

