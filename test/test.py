import datel
import xml.etree.ElementTree as ET

root = ET.fromstring("<root><record>RR<title a='2'></title></record>j</root>")

got1 = list(datel.datel_record_set(root))
expected1 = [
    [
        {"root": ['<record>RR<title a="2" /></record>j', {}]},
        {"record": ['RR<title a="2" />', {}]},
        {"title": ["", {"a": "2"}]},
    ]
]


got2 = list(datel.datel_record_set(root, "record", solsource=True))
expected2 = [{'record': [['RR<title a="2" />', {}]], 'title': [['', {'a': '2'}]]}]

test1 = bool(got1 == expected1)
test2 = bool(got2 == expected2)

if False in (test1, test2):
    exit(1)
else:
    print("looks good")
