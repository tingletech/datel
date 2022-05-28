
to run, for example:

```
./datel.py ./test/oai.xml ".//{http://www.openarchives.org/OAI/2.0/oai_dc/}metadata/.." | jq . - | more
```

outputs jsonl -- one line per record matched by the user supplied XPath

for the `test/oai.xml` file; `"//{http://www.openarchives.org/OAI/2.0/oai_dc/}dc/../.."` and `"//{http://www.openarchives.org/OAI/2.0/oai_dc/}metadata/.."` return the same thing


```
usage: datel.py [-h] xml xpath

create json data elements from xml

positional arguments:
  xml         source xml file
  xpath       xpath to a record

optional arguments:
  -h, --help  show this help message and exit
  ```
