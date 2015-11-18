
import xml.etree.cElementTree as ET
from collections import defaultdict
from bs4 import BeautifulSoup
import re
import pprint

html_file = 'ZipCodes.html'
OSMFILE = "sample.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
has_numbers_in_type = re.compile(r'[0-9]+')
zipcode_search = re.compile(r'^([0-9]+)-([0-9]+)')
prefix_zip = re.compile(r'^[GA\s]+([0-9]+)')



expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons",'Southwest','Southeast','Northwest','Northeast',"Way","Circle"]

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St.": "Street",
            "Ave" : 'Avenue',
            "Rd." : 'Road',
            "Rd" : 'Road',
            "Ln" : "Lane",
            "Trl" : 'Trail',
            "Xing" : 'Crossing',
            "Sq" : "Square",
            "Cir" : "Circle",
            "Pt" : "Point",
            "Pl" : "Place",
            "Ct" : "Court",
            "Blvd": "Boulevard",
            "Lndg" : "Landing",
            "Ave." : "Avenue",
            "Hwy" : "Highway"}
direction_mapping = { "S": "South",
            "W": "West",
            "E" : 'East',
            "N" : 'North',
            "NE" : "Northeast",
            "NW" : "Northwest",
            "SE" : "Southeast",
            "SW" : "Southwest"}

def extract_zip_codes(page):
    '''
    The purpose of this function is to perform the screen scraping 
    task of collecting all of the zip codes that reside in the city of Atlanta
    '''
    data = []
    with open(page, 'r') as html:
        soup = BeautifulSoup(html)
        #print soup.head
        tables = soup.find_all(href=re.compile(r'http://www.zipcodestogo.com/Atlanta/GA/*'))
        #print tables
        for table in tables:
            data.append(table.text)

    return data
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected and street_type not in direction_mapping.keys() and street_type not in mapping.keys():
            found = has_numbers_in_type.search(street_type)
            if found:
                street_types[street_type].add(street_name)

def audit_key_values(key_vals,key_val):
        key_vals.add(key_val)
def audit_postcodes(post_codes,postcode):
    post_codes.add(postcode)
def audit_counties(counties,county):
    counties[county] += 1        
def audit_tag_attribs(tag_names,tags):
    #this function is to check whether the 'k' and 'v' are the only attributes of the tags
    for tag_name in tags:
        tag_names.add(tag_name)
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")
def is_postcode(elem):
    return (elem.attrib['k'] == "addr:postcode")
def is_county(elem):
    return (elem.attrib['k'] == "addr:county")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    #tag_attribs = set()
    key_vals = set()
    post_codes = set()
    counties = defaultdict(int)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                #audit_tag_attribs(tag_attribs, tag.keys())
                audit_key_values(key_vals, tag.attrib['k'])
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
                elif is_postcode(tag):
                    m = zipcode_search.search(tag.attrib['v'])
                    m_ = prefix_zip.search(tag.attrib['v'])
                    if m:
                        zip = m.group(1)
                        print m.group(0)
                        audit_postcodes(post_codes, zip)
                    elif m_:
                        zip = m_.group(1)
                        audit_postcodes(post_codes, zip)
                    else:
                        audit_postcodes(post_codes, tag.attrib['v'])
                elif is_county(tag):
                    audit_counties(counties, tag.attrib['v'])
    return street_types,post_codes,key_vals,counties


def update_name(name, mapping):

    # YOUR CODE HERE
    #names = mapping.keys
    #print names
    for k in mapping.keys():
        pos = name.find(k)
        if pos != -1:
            name = name[:pos] + mapping[k]

    return name


def test():
    zc = extract_zip_codes(html_file)
    st_types,post_codes,key_vals,counties = audit(OSMFILE)
    #for zipcode in post_codes:
     #   if zipcode not in zc:
      #      print zipcode
    #assert len(st_types) == 3
    #pprint.pprint(dict(st_types).keys())
    #pprint.pprint(dict(st_types))
    #pprint.pprint(post_codes)
    pprint.pprint(counties)
    #pprint.pprint(key_vals)

    
if __name__ == '__main__':
    test()