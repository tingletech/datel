requires `lxml` (python library) which requires `libxml2` (c library)


to run, for example:

```
./datel.py ./test/oai.xml "//*[local-name()='dc']/../.." | jq . - | more
```

outputs jsonl
