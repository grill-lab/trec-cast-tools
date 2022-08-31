import pytest

from passage_validator import PassageValidator

def test_service_startup(servicer_params_test):
    pv = PassageValidator(*servicer_params_test)
    assert(pv.db.rowcount == servicer_params_test[1])

def test_service_startup_invalid_rows(servicer_params_test):
    with pytest.raises(SystemExit) as pytest_exc:
        pv = PassageValidator(servicer_params_test[0], 12345)

    assert(pytest_exc.type == SystemExit)
    assert(pytest_exc.value.code == 255)
