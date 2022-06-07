import argparse
from pathlib import Path

from generators import WaPoGenerator, KILTGenerator, MARCOGenerator
from passage_chunkers import PassageChunker
from utils import write_to_jsonlines, write_to_trecweb

parser = argparse.ArgumentParser(description='Collection Processing Parameters')

# KILT collection path
parser.add_argument(
    '--kilt_collection', 
    type=str, 
    default="files/raw_collection/kilt_knowledgesource.json", # if collection dowloaded with bash script
    help="Path to the raw KILT collection"
)

# MARCO collection path
parser.add_argument(
    '--marco_v2_collection', 
    type=str, 
    default="files/raw_collection/msmarco_v2_doc.tar", 
    help="Path to compressed MARCO V2 collection"
)

# WaPo collection path
parser.add_argument(
    '--wapo_collection', 
    type=str, 
    default="files/raw_collection/WashingtonPost.v4.tar.gz", 
    help="Path to compressed WaPo collection"
)

# Duplicates file path
parser.add_argument(
    '--duplicates_file', 
    type=str, 
    default="files/duplicates_file/all_duplicates.txt", 
    help="Path to duplicates file"
)

parser.add_argument('--batch_size', type=int, default=100000, help="Number of documents per batch")
parser.add_argument('--skip_process_kilt', default=False, action='store_true')
parser.add_argument('--skip_process_marco', default=False, action='store_true')
parser.add_argument('--skip_process_wapo', default=False, action='store_true')
parser.add_argument('--output_dir', type=str, default="files", help="Directory to write files to")
parser.add_argument('--output_type', type=str, default="jsonlines", help="Output file type: trecweb or jsonlines")


if __name__ == '__main__':

    args = parser.parse_args()
    passage_chunker = PassageChunker()
    output_path = f"{args.output_dir}/{args.output_type}"
    Path(output_path).mkdir(parents=True, exist_ok=True)

    if not args.skip_process_kilt:
        print("Processing KILT")

        kilt_generator: KILTGenerator = KILTGenerator(
            args.kilt_collection, args.duplicates_file, args.batch_size
        ).generate_documents()

        for batch_num, document_batch in enumerate(kilt_generator):
            updated_document_batch = passage_chunker.process_batch(document_batch, f"{args.output_dir}/md5_hashes")
            if args.output_type == 'jsonlines':
                write_to_jsonlines(f"{output_path}/kilt_{batch_num}.jsonl", document_batch)
            elif args.output_type == 'trecweb':
                write_to_trecweb(f"{output_path}/kilt_{batch_num}.trecweb", document_batch)
            else:
                raise ValueError("--output type must be 'jsonlines' or 'trecweb'")

    if not args.skip_process_marco:
        print("Processing MARCO")

        marco_generator: MARCOGenerator = MARCOGenerator(
            args.marco_v2_collection, args.duplicates_file, args.batch_size
        ).generate_documents()

        for batch_num, document_batch in enumerate(marco_generator):
            updated_document_batch = passage_chunker.process_batch(document_batch, f"{args.output_dir}/md5_hashes")
            if args.output_type == 'jsonlines':
                write_to_jsonlines(f"{output_path}/marco_{batch_num}.jsonl", document_batch)
            elif args.output_type == 'trecweb':
                write_to_trecweb(f"{output_path}/marco_{batch_num}.trecweb", document_batch)
            else:
                raise ValueError("--output type must be 'jsonlines' or 'trecweb'")
    
    if not args.skip_process_wapo:
        print("Processing WaPo")

        wapo_generator: WaPoGenerator = WaPoGenerator(
            args.wapo_collection, args.duplicates_file, args.batch_size
        ).generate_documents()

        for batch_num, document_batch in enumerate(wapo_generator):
            updated_document_batch = passage_chunker.process_batch(document_batch, f"{args.output_dir}/md5_hashes")
            if args.output_type == 'jsonlines':
                write_to_jsonlines(f"{output_path}/wapo_{batch_num}.jsonl", document_batch)
            elif args.output_type == 'trecweb':
                write_to_trecweb(f"{output_path}/wapo_{batch_num}.trecweb", document_batch)
            else:
                raise ValueError("--output type must be 'jsonlines' or 'trecweb'")

