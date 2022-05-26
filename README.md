requires `lxml` (python library) which requires `libxml2` (c library)


to run, for example:

```
./datel.py ./test/oai.xml "//*[local-name()='metadata']/.." | jq . - | more
```

outputs jsonl

for the `test/oai.xml` file; `"//*[local-name()='dc']/../.."` and `"//*[local-name()='metadata']/.."` return the same thing
