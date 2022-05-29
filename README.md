## install

```
pip install https://github.com/tingletech/datel/archive/refs/heads/main.tar.gz
```

## notes

for example:

```
./datel.py ./test/oai.xml ".//{http://www.openarchives.org/OAI/2.0/oai_dc/}metadata/.." | jq . - | more
```

outputs jsonl -- one line per record matched by the user supplied XPath

for the `test/oai.xml` file; `"//{http://www.openarchives.org/OAI/2.0/oai_dc/}dc/../.."` and `"//{http://www.openarchives.org/OAI/2.0/oai_dc/}metadata/.."` return the same thing


For more notes:
```
datel -h
pydoc datel
```
