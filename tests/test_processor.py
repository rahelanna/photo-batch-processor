from src.processor import calculate_target_size

def test_calculate_target_size_landscape() -> None:
    result = calculate_target_size(4000, 1844, 1600)
    assert result == (1600, 738)

def test_calculate_target_size_portrait() -> None:
    result = calculate_target_size(1844, 4000, 1600)
    assert result == (738, 1600)

def test_calculate_target_size_not_upscale() -> None:
    result = calculate_target_size(1089, 700, 1600)
    assert result == (1089, 700)