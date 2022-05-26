requires `lxml` (python library) which requires [`libxml2`](http://www.xmlsoft.org/) (c library) and provides [XPath 1.0](https://www.w3.org/TR/xpath-10/) support.  XPath is a powerfully little language for traversing XML structures.


to run, for example:

```
./datel.py ./test/oai.xml "//*[local-name()='metadata']/.." | jq . - | more
```

outputs jsonl -- one line per record matched by the user supplied XPath

for the `test/oai.xml` file; `"//*[local-name()='dc']/../.."` and `"//*[local-name()='metadata']/.."` return the same thing


```
usage: datel.py [-h] xml xpath

create json data elements from xml

positional arguments:
  xml         source xml file
  xpath       xpath to a record

optional arguments:
  -h, --help  show this help message and exit
  ```
