import multiprocessing
from itertools import islice
from .writers import write_md5_hashes, write_to_jsonlines, write_to_trecweb


def process_batch(collection_name, generator, passage_chunker, output_type, output_path, md5_dir_path):
    with multiprocessing.Pool() as pool:
        for batch_id, document_batch in enumerate(pool.imap_unordered(passage_chunker.process_batch, islice(generator, 1))):

            print(
                f"--- Passages generated for {collection_name} documents in batch number {batch_id} ---")
            write_md5_hashes(
                f"{md5_dir_path}/{collection_name}_md5hashes_{batch_id}.csv", document_batch)
            if output_type == 'jsonlines':
                write_to_jsonlines(
                    f"{output_path}/{collection_name}_{batch_id}.jsonl", document_batch)
            elif output_type == 'trecweb':
                write_to_trecweb(
                    f"{output_path}/{collection_name}_{batch_id}.trecweb", document_batch)
            else:
                raise ValueError(
                    "--output type must be 'jsonlines' or 'trecweb'")
            print(
                f"--- Done processing {collection_name} documents in batch number {batch_id} ---")
