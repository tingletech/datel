# Datel XML Transliterator

Pure python 99.9% losless transformations of XML to python `dict`s, JSON, or JSON Lines.

## Datel Data Element and Record Scheme

Input XML with your records and an
[XPath](https://docs.python.org/3/library/xml.etree.elementtree.html#supported-xpath-syntax)
pointing to the root element of records to extract.

The first step is to apply the XPath to the XML Document, iterating
over each record.

For each record, the next step is to iterate over each record node,
creating an array for each record containing Datel Data Elements.
Then, the datel elements are merged into one dict per record.

The command outputs JSON Lines.

The default format creates one dict per record, supplying the flag
`--no-solsource` will enabling an order-preserving mode with one
dict per XML Element in the source.

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
