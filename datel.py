#!/usr/bin/env python
"""Datel XML to JSONL Converter
"""

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from typing import Iterator


def datel(element: ET.Element, xpath: str, options: dict) -> Iterator[dict]:
    """
    Takes an element, and an XPath expression pointing to the records.

    Returns an Iterator of Datel Records matching the XPath in the XML
    """
    for record in element.findall(xpath):
        yield datel_record(record, options)


def datel_record(record, options):
    """A Datel Record is an array Datel Data Elements.

    A Datel Record is in the same order as the XML source, but the
    hierarchy is flattened.

    The last element of a Datel Record's array is a dict of any
    attributes of the record XML element.  The record XML element's
    tag is recorded with the key `@_datel_record_@` in the attributes
    dict.  This name would be illegal in an XML attribute, so won't be
    in the source XML.

    Text nodes will be intermixed with Data Data Elements as strings
    in the Datel record array if `options = {text_nodes: True}`.

    ```
    <r><b>B</b></r>
    [{"b": ["B", {}]}, {"@_datel_record_@": "r"}]
    ```
    """
    this_record = []
    text = normalize_space(record.text)  # this is rare leading text node of the record
    if text and options.get("text_nodes", False):
        this_record.append(text)

    for element in record.findall(".//*"):
        this_record.append(datel_element(element))  # the normal case
        if options.get("text_nodes", False):
            tail = normalize_space(element.tail)  # yet more rare child text nodes
            if tail:
                this_record.append(tail)

    attributes = {}
    if record.attrib:  # also probably not too common?
        attributes = record.attrib

    attributes["@_datel_record_@"] = record.tag  # might as well note the record's tag
    this_record.append(attributes)
    return this_record


def datel_element(element):
    """
    Datel Data Element

    Goal: represent an XML element as a python data structure suitable for converting to JSON.

    The XML element is converted to a dict with a single key.

    The key is the XML element's tag name with namespaces in James Clark notation.

    The value of the key is an array of two array elements.

    - The first array element is a string containing the inner markup of XML element.

    - The second array element is a dict of the attributes of the XML element.

    The whole thing is a datel data element.

    ```
    <tag attribute="value">string of <inner>content</inner></tag>
    {"tag": ["string of <inner>content</inner>", {"attribute": "value"}]}
    ```
    """
    return dict({element.tag: [innerxml(element), dict(element.attrib)]})


def innerxml(element):
    """like .innerHTML in javascript"""
    return "".join(
        (element.text or "", "".join(ET.tostring(e, "unicode") for e in element))
    )


def normalize_space(string: str) -> str:
    """sort of like XPath normalize-space(), returns a string or False"""
    if not isinstance(string, str) or string == "":
        return False  # so as to use in `if` tests
    return " ".join(string.split())


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "xml",
        help="source xml file",
    )
    parser.add_argument(
        "xpath",
        help="xpath to a record (one line per record in the output)",
        nargs="?",
        default=".",
    )
    parser.add_argument(
        "--text-nodes",
        action="store_true",
        help="mix text nodes into record array",
    )

    if argv is None:
        argv = parser.parse_args()

    tree = ET.parse(argv.xml).getroot()
    records = datel(tree, argv.xpath, {"text_nodes": argv.text_nodes})

    had_output = False
    for record in records:
        had_output = True
        print(json.dumps(record))

    if not had_output:
        print(
            f'WARNING: the supplied xpath "{argv.xpath}" found 0 results in {argv.xml}',
            file=sys.stderr,
        )


# main() idiom for importing into REPL for debugging
if __name__ == "__main__":
    sys.exit(main())


"""
Copyright © 2022, Regents of the University of California
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
- Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
- Neither the name of the University of California nor the names of its
  contributors may be used to endorse or promote products derived from this
  software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""
