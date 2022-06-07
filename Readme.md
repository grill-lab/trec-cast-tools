# TREC CAsT Y4 Tools

Utility tools to create trecweb and jsonlines files from the MARCO, KILT, and WaPo collections can be found in the `src/main/python` directory. During the file creation process, each document in a collection is chunked into smaller passages. 

Each document has an ID, url, title, and body. You can refer to http://www.treccast.ai/ to learn more about the Document ID format used for CAsT. Passage ID is based on the position of a passage within a document. 

Below is an sample document in trecweb format that is generated for MARCO_v2 after running the utility:

```
<DOC>
<DOCNO>MARCO_0_3178380</DOCNO>
<DOCHDR>
</DOCHDR>
<HTML>
<TITLE>What is a Crystal?</TITLE>
<URL>https://www.gemsociety.org/article/crystal/</URL>
<BODY>
<passage id=1>
What is a Crystal?by International Gem Society“Crystal 1” by Brenda Clarke. Licensed under CC By 2.0. What comes to mind when you think of crystals? Many people might visualize beautiful, mineral objects with smooth faces in regular geometric patterns. Others might imagine elegant glassware. For gemologists, the scientific definition of a crystal goes right to the atomic level. A crystal is a solid whose atoms are arranged in a “highly ordered” repeating pattern. These patterns are called crystal systems. If a mineral has its atoms arranged in one of them, then that mineral is a crystal. Crystal Systems There are seven crystal systems: isometric, tetragonal, orthorhombic, monoclinic, triclinic, hexagonal, and trigonal. Each is distinguished by the geometric parameters of its unit cell, the arrangement of atoms repeated throughout the solid to form the crystal object we can see and feel. For example, an isometric or cubic crystal has a cube as its unit cell. 
</passage>
<passage id=2>
All its sides are equal in length and all its angles are right angles. Well-known gems in this system include diamonds, garnets, and spinels. The isometric crystal system has three axes of the same length that intersect at 90º angles. On the other hand, a triclinic crystal has all sides of different lengths and none of its angles are right angles. These geometric variations mean triclinic crystals can take on many intricate shapes. Well-known gems in the triclinic system include labradorite and turquoise. None of the axes in the triclinic system intersect at 90º and all are different lengths. Non-Crystalline Solids Some objects may appear to be crystals to the naked eye, but outward appearances can be misleading. For gemologists, the atomic structure of the object is the determining factor. Not all objects with regular geometric faces are crystals, not are all solid materials crystals. Amorphous Solids Glass, for example, has a non-crystalline, amorphous atomic structure. 
</passage>
<passage id=3>
Although glassmakers can pour and harden glass into geometric shapes, its atomic structure remains unchanged. People commonly refer to some glassware, such as this, as crystal. However, scientifically speaking, these objects aren’t crystals. Photo by liz west. Licensed under CC By 2.0. Polycrystalline Solids Water that hardens into a single large snowflake is, in fact, a crystal. It crystallizes as it cools, freezes, and moves through the atmosphere. “Snowflake-23” by Yellowcloud. Licensed under CC By 2.0. However, water that hardens into a cube in your freezer’s ice tray isn’t a crystal. Ice cubes, rocks, and common metals are examples of polycrystalline materials. They may contain many crystalline objects. (In the case of ice cubes, they may contain actual ice crystals). Nevertheless, you can’t describe the entire ice cube as having a uniform crystalline structure. 
</passage>
<passage id=4>
“Frozen Ice Cubes IMG_1021” by Steven Depolo. Licensed under CC By 2.0. Cryptocrystalline or microcrystalline rocks consist of microscopic crystals, but, again, those rocks lack a uniform crystalline structure. Some cryptocrystalline materials, such as chalcedony, find use as gem materials in jewelry or decorative objects. The Origins of Crystals Most crystals have natural origins. They can form through inorganic means, such as geological processes within the earth. Others form through organic processes within living creatures. For example, some human kidney stones consist in part of weddellite crystals. Weddellite occurs at the bottom of the Weddell Sea near Antarctica. It can also be found passing very painfully through urinary tracts. “Surface of a Kidney Stone” by Kempf EK. Licensed under CC By-SA 3.0. Laboratories can also create crystals artificially. For example, cubic zirconia, a synthetic gem material, forms with a cubic crystal structure when zirconium and zirconium dioxide are superheated. 
</passage>
<passage id=5>
The resulting material commonly finds use as a diamond imitation or simulant. Colorless cubic zirconia gems often serve as diamond imitations. However, labs can also synthesize this material in many colors. “Multicolor Cubic Zirconia” by Michelle Jo. Licensed under CC By 3.0.
</passage>
</BODY>
</HTML>
</DOC>
```

## How to use

1. `cd` into `src/main/python`
1. Create and activate a Python Virtual Environment using `python3 -m venv env` then `source env/bin/activate`
2. Install the dependencies using `pip install -r requirements.txt`

### Processing the Collection:

1. First, use the `download_collection.sh` bash script to download the raw collection and blacklisted document ids
2. Next, run `python3 main.py --output_type trecweb` or `python3 main.py --output_type jsonlines` to generate .trecweb or .jsonl files you can use for indexing

### Notes

1. If you downloaded the raw collection without the `download_collection.sh` script, you may need to pass in the path to your files as argument while using the scripts:
- use `--wapo_collection` to specify the path to your downloaded WaPo collection
- use `--duplicates_file` to specify the path to your downloaded duplicates file
- use `--marco_v2_collection` to specify the path to your downloaded MARCO V2 collection
- use `--kilt_collection` to specify the path to your downloaded KILT collection

2. You can specify a directory to write the output trecweb/jsonlines file to by using `--output_dir`

3. If you want to process a subset of the three collections, you can skip processing the other collections you're not interested. For example, if you just wanted to generate trecweb files for MARCO V2, then you would do `python3 main.py --output_type trecweb --skip_process_kilt --skip_process_wapo`

4. Documents are processed in batches to take advange of Spacy's multiprocessing capabilities. You may want to reduce or increase the `--batch_size` argument (default of 100000) depending on the compute resources available to you. Please note that the `--batch_size` argument also determines the number of document entries that are written out per output file.

<!-- 5. This utility also generates a file with all passage ids and their corresponding passage md5 hashes. You may compare this file with the master version to ensure that you have the right passage splits. -->


## Other Notes
1. The utility was built and tested with Python 3.8.10