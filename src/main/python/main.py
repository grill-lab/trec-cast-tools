import argparse
from hashlib import md5
from pathlib import Path

from generators import WaPoGenerator, KILTGenerator, MARCO_v2_Generator #, MARCO_v1_Generator
from passage_chunkers import PassageChunker
from utils import process_batch

parser = argparse.ArgumentParser(
    description='Collection Processing Parameters')

# KILT collection path
parser.add_argument(
    '--kilt_collection',
    type=str,
    # if collection dowloaded with bash script
    default="files/raw_collection/kilt_knowledgesource.json",
    help="Path to the raw KILT collection"
)

# MARCO v2 collection path
parser.add_argument(
    '--marco_v2_collection',
    type=str,
    default="files/raw_collection/msmarco_v2_doc.tar",
    help="Path to compressed MARCO V2 collection"
)

# MARCO v1 collection path
# parser.add_argument(
#     '--marco_v1_collection',
#     type=str,
#     default="files/raw_collection/msmarco-docs.tsv.gz",
#     help="Path to compressed MARCO V1 collection"
# )

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

parser.add_argument('--batch_size', type=int, default=100000,
                    help="Number of documents per batch")
parser.add_argument('--skip_process_kilt', default=False, action='store_true')
parser.add_argument('--skip_process_marco_v2', default=False, action='store_true')
# parser.add_argument('--skip_process_marco_v1', default=False, action='store_true')
parser.add_argument('--skip_process_wapo', default=False, action='store_true')
parser.add_argument('--output_dir', type=str, default="files",
                    help="Directory to write files to")
parser.add_argument('--output_type', type=str, default="jsonlines",
                    help="Output file type: trecweb or jsonlines")


if __name__ == '__main__':

    args = parser.parse_args()
    passage_chunker = PassageChunker()
    output_path = f"{args.output_dir}/{args.output_type}"
    md5_dir_path = f"{args.output_dir}/md5_hashes"
    Path(output_path).mkdir(parents=True, exist_ok=True)
    Path(md5_dir_path).mkdir(parents=True, exist_ok=True)

    if not args.skip_process_kilt:
        print("--- Processing KILT ---")

        kilt_generator: KILTGenerator = KILTGenerator(
            args.kilt_collection, args.duplicates_file, args.batch_size
        ).generate_documents()

        process_batch(
            collection_name='KILT',
            generator=kilt_generator,
            passage_chunker=passage_chunker,
            output_type=args.output_type,
            output_path=output_path,
            md5_dir_path=md5_dir_path
        )

    if not args.skip_process_marco_v2:
        print("Processing MARCO v2")

        marco_v2_generator: MARCO_v2_Generator = MARCO_v2_Generator(
            args.marco_v2_collection, args.duplicates_file, args.batch_size
        ).generate_documents()

        process_batch(
            collection_name='MARCO_v2',
            generator=marco_v2_generator,
            passage_chunker=passage_chunker,
            output_type=args.output_type,
            output_path=output_path,
            md5_dir_path=md5_dir_path
        )
    
    # if not args.skip_process_marco_v1:
    #     print("Processing MARCO v1")

    #     marco_v1_generator: MARCO_v1_Generator = MARCO_v1_Generator(
    #         args.marco_v1_collection, args.duplicates_file, args.batch_size
    #     ).generate_documents()

    #     process_batch(
    #         collection_name='MARCO_v1',
    #         generator=marco_v1_generator,
    #         passage_chunker=passage_chunker,
    #         output_type=args.output_type,
    #         output_path=output_path,
    #         md5_dir_path=md5_dir_path
    #     )

    if not args.skip_process_wapo:
        print("Processing WaPo")

        wapo_generator: WaPoGenerator = WaPoGenerator(
            args.wapo_collection, args.duplicates_file, args.batch_size
        ).generate_documents()

        process_batch(
            collection_name='WaPo',
            generator=wapo_generator,
            passage_chunker=passage_chunker,
            output_type=args.output_type,
            output_path=output_path,
            md5_dir_path=md5_dir_path
        )

