from datel import datel
import xml.etree.ElementTree as ET

root = ET.fromstring("<root><record>RR<title a='2'></title></record>j</root>")

got1 = list(datel(root))
expected1 = [
    [
        {"root": ['<record>RR<title a="2" /></record>j', {}]},
        {"record": ['RR<title a="2" />', {}]},
        {"title": ["", {"a": "2"}]},
        {"@_datel_record_@": "root"},
    ]
]

got2 = list(datel(root, "record", {"text_nodes": True}))
expected2 = [
    [
        "RR",
        {"record": ['RR<title a="2" />', {}]},
        "j",
        {"title": ["", {"a": "2"}]},
        {"@_datel_record_@": "record"},
    ]
]

if got1 == expected1 and got2 == expected2:
    print("it worked")
else:
    print(got1)
    print(got2)
    exit(1)

exit(1)
