from lxml import etree
import sys
tree = etree.parse("C:/Users/inooh/Downloads/cdd latest.cdd")

class ValueType(object):
    def __init__(self,
                 bit_length,
                 byte_order,
                 encoding,
                 sig,
                 data_format,
                 qty,
                 sz,
                 minsz,
                 maxsz,
                 unit):
        self.bit_length = bit_length
        self.byte_order = byte_order
        self.encoding = encoding
        self.sig = sig
        self.data_format = data_format
        self.qty = qty
        self.sz = sz
        self.minsz = minsz
        self.maxsz = maxsz
        self.unit = unit


class DataType(object):

    def __init__(self,
                #type of dataType(IDENT,LINCOMP,TEXTTBL,STRUCTDT,NUMITERDT,EOSITERDT,MUXDT
                type,
                id,
                type_name,
                #description of the data type
                description,
                #qualifier
                qual,

                cValueType,
                pValueType

                # factor,
                # offset,
                # isContainer,
                # dataList
                ):
        self.type = type
        self.id = id
        self.type_name = type_name
        self.description = description
        self.qual = qual
        self.cValueType = cValueType
        self.pValueType = pValueType
        # self.factor = factor
        # self.offset = offset
        # self.isContainer = isContainer
        # self.dataList = dataList

#####################################################################################
def get_valueType(data_type, type):
    if type == "c":
        value_type = data_type.find('CVALUETYPE')
    elif type == "p":
        value_type = data_type.find('CVALUETYPE')
    else:
        print("c or p omly are suported in get_valueType")
        sys.exit()
    if value_type is not None:
        bit_length = value_type.attrib["bl"]
        byte_order = value_type.attrib["bo"]
        encoding = value_type.attrib["enc"]
        sig = value_type.attrib["sig"]
        data_format = value_type.attrib["df"]
        qty = value_type.attrib["qty"]
        sz = value_type.attrib["sz"]
        minsz = value_type.attrib["minsz"]
        if data_type.tag == "EOSITERDT":
            maxsz = "NO_MAX"
        else:
            maxsz = value_type.attrib["maxsz"]
    else:
        bit_length = "0"
        byte_order = "xx"
        encoding = "NONE"
        sig = "0"
        data_format = "NONE"
        qty = "NONE"
        sz = "NONE"
        minsz = "0"
        maxsz = "0"

    try:
        unit = data_type.find("PVALUETYPE/UNIT").text
    except:
        unit = "uunitless"

    return ValueType(bit_length,
                     byte_order,
                     encoding,
                     sig,
                     data_format,
                     qty,
                     sz,
                     minsz,
                     maxsz,
                     unit)

def CDD_getAllDataTypes(tree):
    data_types_list = []
    data_types = tree.xpath("""
                             ./ECUDOC/DATATYPES/IDENT
                            |./ECUDOC/DATATYPES/LINCOMP
                            |./ECUDOC/DATATYPES/TEXTTBL
                            |./ECUDOC/DATATYPES/STRUCTDT
                            |./ECUDOC/DATATYPES/EOSITERDT
                            """)
    for data_type in data_types:

        #generic for all data types:
        type = data_type.tag
        id = data_type.attrib["id"]

        # oid = data_type.attrib["oid"]

        try:
            type_name = data_type.find('NAME/TUV[1]').text
        except:
            type_name = "un named data type"
            print("for better visualization in cdd name this data type")

        try:
            description = data_type.find('DESC/TUV[1]').text
        except:
            description = "data type has no description"

        try:
            qual = data_type.find('QUAL').text
        except:
            print("data type has no qualifier, this causes inconsistency")
            sys.exit()

        cValueType = get_valueType(data_type, "c")
        pValueType = get_valueType(data_type, "p")


        #specific:
        # if type == "TEXTTBL":
        #     text_maps = {}
        #     for text_map_ in  data_type.findall('TEXTMAP'):
        #         start = text_map_.attrib["s"]
        #         #end = text_map_.attrib["e"]
        #         text_maps[start] = text_map_.find("TEXT/TUV[1]")

        data_types_list.append(DataType(type,
                                id,
                                type_name,
                                description,
                                qual,

                                cValueType,
                                pValueType

                                # factor,
                                # offset,
                                # isContainer,
                                # dataList
                                )
                               )
    return data_types_list

data_types_list = CDD_getAllDataTypes(tree)
for item in data_types_list:
    print(item.type, item.cValueType.byte_order)








# import xml.dom.minidom
# dom = xml.dom.minidom.parse("cdd latest.cdd") # or xml.dom.minidom.parseString(xml_string)
# pretty_xml_as_string = dom.toprettyxml()
# print(pretty_xml_as_string.encode('utf-8'))
