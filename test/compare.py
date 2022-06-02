#!/usr/bin/env python
"""datel vs xmltodict
"""

import argparse
import json
import sys
import xml.etree.ElementTree as ET

import datel
import pyspark
import xmltodict
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession

sc = SparkContext("local")
spark = SparkSession(sc)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "xml",
        help="source xml file",
    )

    if argv is None:
        argv = parser.parse_args()

    tree = ET.parse(argv.xml).getroot()

    datel_ = list(datel.datel_record_set(tree))[0]

    xmltodict_ = ""

    with open(argv.xml) as fd:
        xmltodict_ = xmltodict.parse(fd.read())

    datel_df = spark.read.json(sc.parallelize([json.dumps(datel_)]))
    xmltodict_df = spark.read.json(sc.parallelize([json.dumps(xmltodict_)]))

    print("-------")

    print("xml:")
    print("```xml")
    print(ET.tostring(tree, "utf-8"))
    print("```")

    print("datel (linearized solsource form):")
    print("```json")
    print(json.dumps(datel_, indent=4))
    print("```")
    print("```")
    print(datel_df.printSchema())
    print(datel_df.show(truncate=False))
    print("```")

    print("xmltodict:")
    print("```json")
    print(json.dumps(xmltodict_, indent=4))
    print("```")
    print("```")
    print(xmltodict_df.printSchema())
    print(xmltodict_df.show(truncate=False))
    print("```")




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
