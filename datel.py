#!/usr/bin/env python
"""Datel XML to JSONL Converter
"""

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from typing import Iterator, List, Tuple


def datel_record_set(
    element: ET.Element,
    xpath: str = ".",
    solsource: bool = True,
) -> Iterator[object]:
    """
    Takes an element, and an XPath expression pointing to the records.

    Returns an Iterator of Datel Records matching the XPath in the XML
    """
    for record in element.findall(xpath):
        if solsource:
            yield datel_record_to_solsource(datel_record(record))
        else:
            yield datel_record(record)


def datel_record(
    record: ET.Element,
) -> List[object]:
    """A Datel Record is an array Datel Data Elements.

    A Datel Record is in the same order as the XML source, but the
    hierarchy is flattened.

    ```
    <r><b>B</b></r>
    [{'r': {'mix()': '<b>B</b>'}}, {'b': {'text()': 'B'}}]
    ```
    """
    return [datel_element(element) for element in record.iter()]


def datel_element(element: ET.Element) -> dict:
    """
    Datel Data Element

    Goal: represent an XML element as a python data structure suitable for converting to JSON.

    The XML element is converted to a dict with a single key.

    The key is the XML element's tag name with namespaces in James Clark notation.

    The value of the key is a dict of the XML element's attributes, with one of two
    additional keys.

     - `text()` contains the text of an element with no children
     - `mix()` contains an xml fragment of an element with children

    ```
    <tag attribute="value">string of <inner>content</inner></tag>
    {'tag': {'attribute': 'value', 'mix()': 'string of <inner>content</inner>'}}
    ```
    """  # noqa
    attributes = dict(element.attrib)
    # add the inner XML or text as an attribute
    k, v = innerxml(element)
    attributes[k] = v
    return dict({element.tag: attributes})


def datel_record_to_solsource(datel_record):
    """reformat as one dict per record (pre-chew for spark)"""
    spark_dict = {}
    for element in datel_record:
        k = list(element.keys())[0]
        try:
            spark_dict[k].append(element[k])
        except KeyError:
            spark_dict[k] = [
                element[k],
            ]
    return spark_dict


def innerxml(element: ET.Element) -> Tuple[str, str]:
    """like .innerHTML in javascript

    why this business with `text()` and `mix()`? Consider this xml

    ```
    <angle_tests>
      <t>></t>
      <t>&lt;</t>
      <t>&lt;></t>
      <t>&lt;false>tag&lt;/false></t>
      <t><true>tag</true></t>
    </angle_tests>
    ```
    w/o it, there would be no way to tell if there are real tags in the
    XML fragment or if there were literal greater than or less than characters.
    """
    if len(element) > 0:  # test elemen for children
        return (
            "mix()",
            "".join(
                (
                    element.text or "",
                    "".join(ET.tostring(e, "unicode") for e in element),
                )
            ),
        )
    else:
        return ("text()", element.text or "")


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
        "--no-solsource",
        action="store_false",
        help="don't merge elements into one dict per record",
    )

    if argv is None:
        argv = parser.parse_args()

    tree = ET.parse(argv.xml).getroot()
    records = datel_record_set(tree, argv.xpath, argv.no_solsource)

    had_output = False
    for record in records:
        had_output = True
        print(json.dumps(record))

    if not had_output:
        print(
            f'WARNING: xpath "{argv.xpath}" found 0 results in {argv.xml}',
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
