# Datel XML Transliterator

Pure python 99.9% losless transformation of XML to python `dict`s, JSON, or JSON Lines.

All the headaches of XML, but with a flattened tree.

## Datel Data Element and Record Scheme

Input XML with your records and an
[XPath](https://docs.python.org/3/library/xml.etree.elementtree.html#supported-xpath-syntax)
pointing to the root element of records to extract.

The first step is to apply the XPath to the XML Document, iterating
over each record.

For each record, the next step is to iterate over each record node,
creating an array for each record containing Datel Date Elements
(if the `--text-nodes` option is used, direct children of the matched
XPath node will be incuded in the array).

The command outputs the XML as JSON Lines of Datel Records.

## install

```
pip install https://github.com/tingletech/datel/archive/refs/heads/main.tar.gz
```

## notes
Command line use:
```
datel -h
```

Library use and format specification:
```
pydoc datel
```

for example:

```
./datel.py ./test/oai.xml ".//{http://www.openarchives.org/OAI/2.0/}metadata/.." | jq . - | more
```
outputs jsonl -- one line per record matched by the user supplied XPath

for the `test/oai.xml` file; `"//{http://www.openarchives.org/OAI/2.0/oai_dc/}dc/../.."` and `"//{http://www.openarchives.org/OAI/2.0/}metadata/.."` return the same thing
