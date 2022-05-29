## install

```
pip install https://github.com/tingletech/datel/archive/refs/heads/main.tar.gz
```

## notes

for example:

```
./datel.py ./test/oai.xml ".//{http://www.openarchives.org/OAI/2.0/}metadata/.." | jq . - | more
```

outputs jsonl -- one line per record matched by the user supplied XPath

for the `test/oai.xml` file; `"//{http://www.openarchives.org/OAI/2.0/oai_dc/}dc/../.."` and `"//{http://www.openarchives.org/OAI/2.0/}metadata/.."` return the same thing


For more notes:
```
datel -h
pydoc datel
```

## XPath Support

Python's built in support for XPath is sort of limited; reading the
source for `xml/etree/ElementPath.py` we find a `# FIXME: replace with real parser!!!` 
in the section on predicates, and only these "signatures" are picked up
and convered to predicates (copied from comments in the python source below).

```
[@attribute] predicate
[@attribute='value'] or [@attribute!='value']
[tag]
[.='value'] or [tag='value'] or [.!='value'] or [tag!='value']
[index] or [last()] or [last()-index]
```

It does not support absolute paths.

It does support James Clark namespace notation.
