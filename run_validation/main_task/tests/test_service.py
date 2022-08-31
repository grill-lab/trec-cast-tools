import time
import multiprocessing
import random

import pytest

from passage_validator import PassageValidator
from main import validate

def test_service_startup(servicer_params_test):
    pv = PassageValidator(*servicer_params_test)
    assert(pv.db.rowcount == servicer_params_test[1])

def test_service_startup_invalid_rows(servicer_params_test):
    with pytest.raises(SystemExit) as pytest_exc:
        pv = PassageValidator(servicer_params_test[0], 12345)

    assert(pytest_exc.type == SystemExit)
    assert(pytest_exc.value.code == 255)

def validate_wrapper(run_file, file_root, max_warnings, skip_validation, strict, start_delay):
    time.sleep(start_delay)
    turns_validated, warning_count, service_errors = validate(run_file, file_root, max_warnings, skip_validation, strict)
    return (turns_validated, warning_count, service_errors)

@pytest.mark.slow
def test_service_multiple_clients(default_validate_args, grpc_server_full):
    num_clients = 25
    args = default_validate_args

    validation_args = [(args.path_to_run_file,
                        args.fileroot,
                        args.max_warnings,
                        args.skip_passage_validation,
                        args.strict,
                        random.random()) for x in range(num_clients)]

    with multiprocessing.Pool(processes=num_clients) as pool:
        results = pool.starmap(validate_wrapper, validation_args)

    for i in range(num_clients):
        assert(results[i] == (205, 0, 1))
