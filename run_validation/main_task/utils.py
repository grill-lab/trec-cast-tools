from compiled_protobufs.passage_validator_pb2 import PassageValidationRequest, PassageValidationResult

def check_response(response, logger, warning_count, previous_rank, turn):
    if not response.rank:
        logger.warning(f"Response rank for turn {turn.turn_id} is missing or equal  to 0")
        warning_count += 1
    if response.rank <= previous_rank:
        logger.warning(
            f"Current rank {response.rank} is less than or equal to previous rank {previous_rank} for turn {turn.turn_id}. Provenance ranking may not be in descending order"
        )
        warning_count += 1
    if not response.text:
        logger.warning(f"Response text for turn {turn.turn_id} is missing")
        warning_count += 1
    
    return warning_count

def check_provenance(previous_score, provenance, logger, turn, warning_count, provenance_count):
    if previous_score is None:
        previous_score = provenance.score
    elif previous_score <= provenance.score:
        previous_score = provenance.score
    elif previous_score < provenance.score:
        logger.warning(f"{provenance.id} has a greater score than previous passage. Ranking order for turn {turn.turn_id} not correct")
        warning_count += 1
    if provenance_count > 1000:
        logger.warning(f"More than 1000 passages retrieved for turn {turn.turn_id}")
        warning_count += 1
    provenance_count += 1

    return previous_score, provenance_count, warning_count

def validate_passages(passage_validation_client, logger, warning_count, turn):
    # collect passage ids
    passage_validation_request = PassageValidationRequest()
    passage_ids = []
    for response in turn.responses:
        for provenance in response.provenance:
            passage_ids.append(provenance.id)
    # remove duplicates
    passage_ids = list(set(passage_ids))
    passage_validation_request.passage_ids.MergeFrom(passage_ids)
    # validate ids
    passage_validation_result = passage_validation_client.validate_passages(passage_validation_request)
    invalid_indexes = [i for i, passage_validation in enumerate(passage_validation_result.passage_validations) if not passage_validation.is_valid]
    for index in invalid_indexes:
        logger.warning(f"Provenance with ID {passage_ids[index]} does not exist in the passage collection")
    warning_count += len(invalid_indexes)

    return warning_count