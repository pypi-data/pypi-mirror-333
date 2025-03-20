import numpy as np
from CifFile import CifFile as pycifRW
from conftest import bad_cif, cif_files_mark, random_keys_mark
from gemmi import cif
from more_itertools import flatten


def remove_invalid(s):
    """Our parser strips newlines and carriage returns.
    TODO: newlines should be retained
    """
    if s is None:
        return None
    return s.replace("\r", "")


def _gemmi_read_keys(filename, keys, as_number=True):
    file_block = cif.read_file(filename).sole_block()
    if as_number:
        return np.array([cif.as_number(file_block.find_value(key)) for key in keys])
    return np.array([remove_invalid(file_block.find_value(key)) for key in keys])


@cif_files_mark
def test_read_key_value_pairs(cif_data):
    pycif = pycifRW(cif_data.filename).first_block()
    invalid = [*flatten(pycif.loops.values()), *cif_data.failing]
    all_keys = [key for key in pycif.true_case.values() if key.lower() not in invalid]

    parsnip_data = cif_data.file[all_keys]
    for i, value in enumerate(parsnip_data):
        assert cif_data.file[all_keys[i]] == value
        assert cif_data.file[all_keys[i]] == cif_data.file.get_from_pairs(all_keys[i])
    gemmi_data = _gemmi_read_keys(cif_data.filename, keys=all_keys, as_number=False)
    np.testing.assert_equal(parsnip_data, gemmi_data, verbose=True)


@cif_files_mark
@random_keys_mark(n_samples=20)
def test_read_key_value_pairs_random(cif_data, keys):
    parsnip_data = cif_data.file[keys]
    np.testing.assert_equal(parsnip_data, cif_data.file.get_from_pairs(keys))
    for i, value in enumerate(parsnip_data):
        assert cif_data.file.pairs.get(keys[i], None) == value
    gemmi_data = _gemmi_read_keys(cif_data.filename, keys=keys, as_number=False)
    np.testing.assert_equal(parsnip_data, gemmi_data, verbose=True)


def test_read_key_value_pairs_badcif(cif_data=bad_cif):
    parsnip_data = cif_data.file[cif_data.manual_keys]
    correct_data = [
        "1.000000(x)",
        "4.32343242",
        "3.1415926535897932384626433832795028841971693993751058209749",
        "90.00000",
        "-10.12345",
        "210.00000",
        "\\t _1.234-56789",
        r"45.6a/\s",
        None,
    ]
    np.testing.assert_array_equal(parsnip_data, correct_data)
