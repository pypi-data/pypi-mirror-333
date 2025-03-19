r"""
Tools for reading and manipulating sites.

.. autosummary::
   :toctree: generated/
   :nosignatures:

   x2site
   sites_to_res_pairs

Sites are user-defined collections of contacts.
They can be constructed by hand or read from
plain ascii files:

>>> cat site.dat
# contacts to look at :
L394-K270
D381-Q229
Q384-Q229
R385-Q229
D381-K232
Q384-I135

For unformatted ascii files (.dat, .txt etc),
if the first line starts with "#", it will be used
as name for the site, otherwise the filename
will be used. Also, any lines starting
with "#" will be ignored

The ascii-files can be annotated if the `JSON <https://www.json.org/json-en.html>`_
format is used:

>>> cat site.json
{"name":"interesting contacts",
"pairs": {"AAresSeq": [
        "L394-K270",
        "D381-Q229",
        "Q384-Q229",
        "R385-Q229",
        "D381-K232",
        "Q384-I135"
        ]}}

Sites can also be used inside the Python script/session
by using dictionaries, e.g.::
       my_site = {"name":"interesting contacts",
                  "pairs":{"AAresSeq":[
                            "L394-K270",
                            "D381-Q229",
                            "Q384-Q229",
                            "R385-Q229",
                            "D381-K232",
                            "Q384-I135"
                            ]}}

Or: ::

       my_site = {"name":"interesting contacts",
                  "pairs":{"AAresSeq":[
                            ["L394","K270"],
                            ["D381","Q229"],
                            ["Q384","Q229"],
                            ["R385","Q229"],
                            ["D381","K232"],
                            ["Q384","I135"]
                            ]}}

You can specify the "pairs" as "AAresSeq" (like above)
or as zero-indexed residue serial indices using "residx"::
       my_site = {"name":"interesting contacts",
                  "pairs":{"residx":[
                            "353-972",
                            "340-956",
                            "343-956",
                            "344-956",
                            "340-959",
                            "343-865"
                            ]}}

In this last case, you can also directly use pairs of integers,
instead of strings::
      my_site = {"name":"interesting contacts",
                 "pairs":{"residx":[
                          [353,972],
                          [340,956],
                          [343,956],
                          [344,956],
                          [340,959],
                          [343,865],
                          ]}}

Finally, you can also use consensus labels, such as "3.50" or "G.H5.26"
if you specificy the "pairs" as "consensus"::
    my_site = {"name":"interesting contacts",
               "pairs": {"consensus": [
                         "G.H5.26-6.32x32",
                         "G.H5.13-5.68x68",
                         "G.H5.16-5.68x68",
                         "G.H5.17-5.68x68",
                         "G.H5.13-5.71x71",
                         "G.H5.16-3.54x54"
                ]}}

although, in order to work with consensus definitions,
you will need to have passed consensus
information (GPCR, CGN or KLIFS) in one way or another.

Using "AAresSeq" or "consensus" makes site-definitions
portable of across topologies:
e.g. "L394" or "G.H5.26" will be picked regardless of the actual
residue index.

Not that "AAresSeq" will have trouble working  if
there's duplicates (e.g. "ALA150" appears two times
in 3SN6). You can use "residx" to avoid this, but first the user
needs to find out which residue index they are interested
in. mdciao offers several ways to do this. From the CLI
you can use:

>>> mdc_residue.py ALA150 3SN6.pdb

From the API, you can use:

>>> mdciao.cli.residue_selection("ALA150",geom);
   Using method 'lig_resSeq+' these fragments were found
   fragment      0 with  349 AAs     THR9           (   0) -   LEU394           (348 ) (0)  resSeq jumps
   fragment      1 with  340 AAs     GLN1           ( 349) -   ASN340           (688 ) (1)
   fragment      2 with  217 AAs     ASN5           ( 689) -  ALA1160           (905 ) (2)  resSeq jumps
   fragment      3 with  284 AAs    GLU30           ( 906) -   CYS341           (1189) (3)  resSeq jumps
   fragment      4 with  128 AAs     GLN1           (1190) -   SER128           (1317) (4)
   fragment      5 with    1 AAs  P0G1601           (1318) -  P0G1601           (1318) (5)
   0.0)       ALA150 in fragment 0 with residue index 113
   0.1)       ALA150 in fragment 0 with residue index 1026
   Your selection 'ALA150' yields:
      residue      residx    fragment      resSeq      GPCR        CGN
       ALA150         113           0        150       None       None
       ALA150        1026           0        150       None       None

Check :obj:`mdciao.cli.residue_selection` for more.


"""
from .siteIO import *