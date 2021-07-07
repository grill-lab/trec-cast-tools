# Year 3 Trecweb scripts

The scripts in this directory help with creating trecweb files (from the Marco document, KILT, and WaPo collections) that can be used for creating indexes. As part of the trecweb creation process, each document in a collection is chunked into smaller passages. 

Each document has an ID, url, title, and body. You can refer to http://www.treccast.ai/ to learn more about the Document ID format used for CAsT. Passage Number is based on the position of a passage within a document. 

Below is an example of the trecweb file that will be generated for MARCO:

```
<DOC>
<DOCNO>MARCO_D3178380</DOCNO>
<DOCHDR>
</DOCHDR>
<HTML>
<TITLE>What is a Crystal?</TITLE>
<URL>https://www.gemsociety.org/article/crystal/</URL>
<BODY>
<passage id=0>
What is a Crystal?by International Gem Society“Crystal 1” by Brenda Clarke. Licensed under CC By 2.0. What comes to mind when you think of crystals? Many people might visualize beautiful, mineral objects with smooth faces in regular geometric patterns. Others might imagine elegant glassware. For gemologists, the scientific definition of a crystal goes right to the atomic level. A crystal is a solid whose atoms are arranged in a “highly ordered” repeating pattern. These patterns are called crystal systems. If a mineral has its atoms arranged in one of them, then that mineral is a crystal. Crystal Systems There are seven crystal systems: isometric, tetragonal, orthorhombic, monoclinic, triclinic, hexagonal, and trigonal. Each is distinguished by the geometric parameters of its unit cell, the arrangement of atoms repeated throughout the solid to form the crystal object we can see and feel. For example, an isometric or cubic crystal has a cube as its unit cell. 
</passage>
<passage id=1>
All its sides are equal in length and all its angles are right angles. Well-known gems in this system include diamonds, garnets, and spinels. The isometric crystal system has three axes of the same length that intersect at 90º angles. On the other hand, a triclinic crystal has all sides of different lengths and none of its angles are right angles. These geometric variations mean triclinic crystals can take on many intricate shapes. Well-known gems in the triclinic system include labradorite and turquoise. None of the axes in the triclinic system intersect at 90º and all are different lengths. Non-Crystalline Solids Some objects may appear to be crystals to the naked eye, but outward appearances can be misleading. For gemologists, the atomic structure of the object is the determining factor. Not all objects with regular geometric faces are crystals, not are all solid materials crystals. Amorphous Solids Glass, for example, has a non-crystalline, amorphous atomic structure. 
</passage>
<passage id=2>
Although glassmakers can pour and harden glass into geometric shapes, its atomic structure remains unchanged. People commonly refer to some glassware, such as this, as crystal. However, scientifically speaking, these objects aren’t crystals. Photo by liz west. Licensed under CC By 2.0. Polycrystalline Solids Water that hardens into a single large snowflake is, in fact, a crystal. It crystallizes as it cools, freezes, and moves through the atmosphere. “Snowflake-23” by Yellowcloud. Licensed under CC By 2.0. However, water that hardens into a cube in your freezer’s ice tray isn’t a crystal. Ice cubes, rocks, and common metals are examples of polycrystalline materials. They may contain many crystalline objects. (In the case of ice cubes, they may contain actual ice crystals). Nevertheless, you can’t describe the entire ice cube as having a uniform crystalline structure. 
</passage>
<passage id=3>
“Frozen Ice Cubes IMG_1021” by Steven Depolo. Licensed under CC By 2.0. Cryptocrystalline or microcrystalline rocks consist of microscopic crystals, but, again, those rocks lack a uniform crystalline structure. Some cryptocrystalline materials, such as chalcedony, find use as gem materials in jewelry or decorative objects. The Origins of Crystals Most crystals have natural origins. They can form through inorganic means, such as geological processes within the earth. Others form through organic processes within living creatures. For example, some human kidney stones consist in part of weddellite crystals. Weddellite occurs at the bottom of the Weddell Sea near Antarctica. It can also be found passing very painfully through urinary tracts. “Surface of a Kidney Stone” by Kempf EK. Licensed under CC By-SA 3.0. Laboratories can also create crystals artificially. For example, cubic zirconia, a synthetic gem material, forms with a cubic crystal structure when zirconium and zirconium dioxide are superheated. 
</passage>
<passage id=4>
The resulting material commonly finds use as a diamond imitation or simulant. Colorless cubic zirconia gems often serve as diamond imitations. However, labs can also synthesize this material in many colors. “Multicolor Cubic Zirconia” by Michelle Jo. Licensed under CC By 3.0.
</passage>
</BODY>
</HTML>
</DOC>
```

## How to use

1. Create and Activate a Python Virtual Environment using `python3 -m venv env` and `source env/bin/activate`
2. Install the required modules using `pip install -r requirements.txt`

### Creating the Trecweb scripts:

Ensure you have a copy of the Marco document, KILT, and WaPo collections and any relevant duplicate files (duplicates file for Marco can be found in the `duplicate_files` folder). Then:

Generate the **trecweb file for the Marco document collection** by running:

`python marco_trecweb.py path-to-msmarco-docs.tsv path-to-dump-directory path-to-duplicates-file`

Generate the **trecweb file for KILT** by running:

`python kilt_trecweb.py path-to-kilt_knowledgesource.json path-to-dump-directory`

Generate the **trecweb file for WaPo** by running:

`python wapo_trecweb.py path-to-TREC_Washington_Post_collection.v4.jl path-to-dump-directory path-to-wapo-near-duplicates`