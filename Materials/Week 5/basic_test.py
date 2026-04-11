import pytest
from src.temperature_converter_function import convert

@pytest.mark.parametrize(
    "scale, temp, expected_celsius, expected_fahrenheit, expected_kelvin",
    [
        ("C", "0", 0.0, 32.0, 273.15),
        ("F", "32", 0.0, 32.0, 273.15),
        ("K", "273.15", 0.0, 32.0, 273.15),
        ("Z", "273.15", 0.0, 32.0, 273.15),
    ],
)
def test_temperature_converter(scale, temp, expected_celsius, expected_fahrenheit, expected_kelvin):
    celsius, fahrenheit, kelvin = convert(scale, temp)
    assert celsius == pytest.approx(expected_celsius, abs=0.01)
    assert fahrenheit == pytest.approx(expected_fahrenheit, abs=0.01)
    assert kelvin == pytest.approx(expected_kelvin, abs=0.01)
    