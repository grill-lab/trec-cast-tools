from compiled_protobufs.passage_validator_pb2 import PassageValidationRequest

def build_request(ids):
    request = PassageValidationRequest()
    request.passage_ids.MergeFrom(ids)
    return request

def get_invalid_indices(response):
    return [i for i, pv in enumerate(response.passage_validations) if not pv.is_valid]

def test_all_invalid_ids(grpc_stub):
    response = grpc_stub.validate_passages(build_request(set(['foo', 'bar', 'foobar', 'barfoo'])))

    assert(get_invalid_indices(response) == [0, 1, 2, 3])

def test_all_valid(grpc_stub, sample_ids):
    valid_ids = set(sample_ids[0:len(sample_ids):100])
    response = grpc_stub.validate_passages(build_request(valid_ids))

    assert(len(get_invalid_indices(response)) == 0)

def test_mixed_ids(grpc_stub, sample_ids):
    mixed_ids = set(sample_ids[0:len(sample_ids):100])
    invalid_ids = ['foo', 'bar', 'foobar', 'barfoo', '', sample_ids[0].replace('_', '|')]
    mixed_ids.update(invalid_ids)

    response = grpc_stub.validate_passages(build_request(mixed_ids))

    assert(len(get_invalid_indices(response)) == len(invalid_ids))

def test_empty(grpc_stub):
    response = grpc_stub.validate_passages(build_request([]))
    assert(len(get_invalid_indices(response)) == 0)
