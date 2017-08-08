import xml.etree.ElementTree as ET
from collections import defaultdict
import re
import pprint
import json
from pymongo import MongoClient

# Load the OSM-File
osm_file=open("boston.osm", "r", encoding="utf8")
#osm_file=open("sample.osm", "r", encoding="utf8")

# Regular expression
street_type_re=re.compile(r'\b\S+\.?$', re.IGNORECASE)

#Dictionarys  for the audit
zip_codes=defaultdict(int)
street_types=defaultdict(set)
house_numbers=defaultdict(set)
cuisine_types=defaultdict(set)
amenity_types=defaultdict(set)
amenity_names=defaultdict(set)



def audit_street_type(street_name):
    '''Add the street name (value) to street type (key)
    
    Keyword arguments:
    street_name --name of a street
    '''
    m=street_type_re.search(street_name)
    if m:
        street_type=m.group()
        street_types[street_type].add(street_name)


 
def audit_zip_codes(zipCode):
    '''Count the appearing zipcodes
    
    Keyword arguments:
    zipCode -- a zipcode of an adress
    '''      
    if zipCode not in zip_codes:
        zip_codes[zipCode]=1
    else:
        zip_codes[zipCode]+=1



def audit_house_number(house_number):
    '''Count the appearing house numbers
    
    Keyword arguments:
    house_number -- house number in an adress
    '''
    if house_number not in house_numbers:
        house_numbers[house_number]=1
    else:
        house_numbers[house_number]+=1



def audit_cuisine(cuisine):
    '''Count the appearing cuisine
    
    Keyword arguments:
    cuisine -- kind of cuisine in the dataset
    '''
    if cuisine not in cuisine_types:
        cuisine_types[cuisine]=1
    else:
        cuisine_types[cuisine]+=1
    
    
    
    
def audit_amenity(amenity):
    '''Count the appearing amenity
    
    Keyword arguments:
    amenity -- kind of amenity in the dataset
    '''
    if amenity not in amenity_types:
        amenity_types[amenity]=1
    else:
        amenity_types[amenity]+=1
                     
                     
                     
def audit_amenity_name(name):
    '''Count the appearing amenity names
    
    Keyword arguments:
    name -- amenity name in the dataset
    '''
    if name not in amenity_names:
        amenity_names[name]=1
    else:
        amenity_names[name]+=1
    
        
                 
def print_sorted_dict(d):
    '''print the dictionarys
    
    Keyword arguments:
    d -- a dictionary 
    ''' 
    keys=d.keys()
    keys=sorted(keys, key=lambda s: s.lower())   
    for k in keys:
        v=d[k]
        print("%s: %d" % (k, v))



def is_street_name(elem):
    '''Check if element attribute is of type "street" 
    
    Keyword arguments:
    elem -- element from the osm-file
    ''' 
    return (elem.tag=="tag") and (elem.attrib["k"]=="addr:street") 



def is_zip_code(elem):
    '''Check if element attribute is of type "postcode" 
    
    Keyword arguments:
    elem -- element from the osm-file
    '''  
    return (elem.tag=="tag") and (elem.attrib["k"]=="addr:postcode")



def is_house_number(elem):
    '''Check if element attribute is of type "housenumber" 
    
    Keyword arguments:
    elem -- element from the osm-file
    '''  
    return (elem.tag=="tag") and (elem.attrib["k"]=="addr:housenumber")



def is_cuisine(elem):
    '''Check if element attribute is of type "cuisine" 
    
    Keyword arguments:
    elem -- element from the osm-file
    '''  
    return (elem.tag=="tag") and (elem.attrib["k"]=="cuisine")



def is_amenity(elem):
    '''Check if element attribute is of type "amenity" 
    
    Keyword arguments:
    elem -- element from the osm-file
    '''  
    return (elem.tag=="tag") and (elem.attrib["k"]=="amenity")



def is_amenity_name(elem):
    '''Check if element attribute is of type "amenity name" 
    
    Keyword arguments:
    elem -- element from the osm-file
    '''  
    return (elem.tag=="tag") and (elem.attrib["k"]=="name")
    


def audit():
    '''audit of the streets and zipcodes'''
    for event, elem in ET.iterparse(osm_file):
        
        if is_street_name(elem):
            audit_street_type(elem.attrib['v'])
            
        if is_zip_code(elem):
            audit_zip_codes(elem.attrib['v'])
        
        if is_house_number(elem):
            audit_house_number(elem.attrib['v'])
        
        if is_cuisine(elem):
            audit_cuisine(elem.attrib['v'])
            
        if is_amenity(elem):
            audit_amenity(elem.attrib['v'])
        
        if is_amenity_name(elem):
            audit_amenity_name(elem.attrib['v'])
        
            
    #pprint.pprint(dict(street_types))
    #print_sorted_dict(zip_codes)
    #print_sorted_dict(house_numbers)
    #print_sorted_dict(cuisine_types)
    #print_sorted_dict(amenity_types)
    #print_sorted_dict(amenity_names)
    
#audit()


# After the audit I create a mapping of the found streettypes shortcuts to full expressions
mapping={"Ave": "Avenue",
         "Ave.": "Avenue",
         "Rd": "Road",
         "St": "Street",
         "St.": "Street",
         "Pkwy": "Parkway",
         }



def update_streets(name, mapping):
    '''The street shortcuts are corrected as well as the street name that start with lower case'''
    if name[0].islower():
        name=name[0].upper()+name[1:]

    for key in mapping:
        if key==name.split()[-1]:
            return re.sub(r''+key+'$', mapping[key], name,re.X)
    return name



def update_zipcode(zipCode):
    '''Delete the zipcode attachment after "-"
    
    Keyword arguments:
    zipCode -- zipCode from the dataset 
    '''
    if len(zipCode)>5:
        zipCode = re.sub('-.*$', '', zipCode)
    return zipCode
    



def update_amenity(amenity):
    '''Split (if necessary) the amenity name by _ and/or make first letter
    uppercase 
    
    Keyword arguments:
    amenity -- amenity type  from the dataset
    '''  
    corrected_amenity=""
    temp_string=amenity.split("_")
    
    for s in temp_string:
        if s.islower():
            s=s[0].upper()+s[1:]
            corrected_amenity=corrected_amenity+s+" " 
    return corrected_amenity.strip() 



def update_cusines(cusine):
    '''Split (if necessary) the amenity name by _ or by ; and/or
    make the first letter uppercase 
    
    Keyword arguments:
    cusine -- cusine type  from the dataset
    '''  
    corrected_cusine=""
    temp_string=[]
    
    if "_" in cusine:
        temp_string.append(cusine.split("_"))
    elif ";" in cusine:
        temp_string.append(cusine.split(";"))
        
        for s in temp_string[0]:
            if s.islower():
                s=s[0].upper()+s[1:]
                corrected_cusine=corrected_cusine+s+", " 
    
        return corrected_cusine
        
    else:
        return cusine[0].upper()+cusine[1:]
   
    for s in temp_string[0]:
        if s.islower():
            s=s[0].upper()+s[1:]
            corrected_cusine=corrected_cusine+s+" " 
    
    return corrected_cusine



def update_house_numbers(number):
   '''Exchange strings by numbers
    
    Keyword arguments:
    number -- housenumber from the dataset
    '''   
   if "Zero" in number:
       return 0
   elif "One" in number:
       return 1
   else:
       return number



def shape_element(element):
    '''Shape a node from xml into a dictionary'''  
    
    basic_information=["id","version","timestamp","changeset","uid", "user"]
    node={}
    node["basic_information"]={}
    node["address"]={}
    node["pos"]={}
    node["amenity"]={}
    
    if element.tag=="node" or element.tag=="way":
        
        node["type"]=element.tag
        
        for elem in basic_information:
            if elem in element.attrib:
                node["basic_information"][elem]=element.attrib[elem]
        
        for tag in element.iter("tag"):
            
            if tag.attrib["k"]=="addr:housenumber":
                node["address"]["housenumber"]=update_house_numbers(tag.attrib["v"])
            if tag.attrib["k"]=="addr:postcode":
                node["address"]["postcode"]=update_zipcode(tag.attrib["v"])
            if tag.attrib["k"]=="addr:street":
                node["address"]["street"]=update_streets(tag.attrib["v"],mapping)
                
            if tag.attrib["k"]=="amenity":
                node["amenity"]["amenity-type"]=update_amenity(tag.attrib["v"])
            if tag.attrib["k"]=="cuisine":
                node["amenity"]["cuisine"]=update_cusines(tag.attrib["v"])
            if tag.attrib["k"]=="name":
                node["amenity"]["name"]=tag.attrib["v"]
                
        if "lat" in element.attrib:
            node["pos"]["lat"]=float(element.attrib["lat"])
        if "lon" in element.attrib:
            node["pos"]["lon"]=float(element.attrib["lon"])
            
    #delete empty nodes
    if node["address"]=={}:
        node.pop("address", None)
    if node["basic_information"]=={}:
        node.pop("basic_information", None)
    if node["pos"]=={}:
        node.pop("pos", None)  
    if node["amenity"]=={}:
        node.pop("amenity",None)
        
    return node

        

def process_map(file_in):
    '''Shape the osm-file into a list of dicionarys to dump the osm-file as .json-file'''   
    data = []
    with open("osm_boston.json", "w") as f:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                f.write(json.dumps(el, indent=2)+"\n")
             
    return data



shaped_data=process_map(osm_file)




#Load the osm-file as a list of dictionarys into the mongoDB
client=MongoClient()
db = client.BostonOSM
collection=db.bostonMap

collection.insert_many(shaped_data)



#Number of Documents
collection.find().count()


#Number of nodes
collection.find({"type":"node"}).count()

#Number of ways
collection.find({"type":"way"}).count()



# Number of Unique Users
result=collection.distinct("basic_information.user")
print(len(result))



# Top 3 Contributing User
pipeline=[{"$group": {"_id":"$basic_information.user", "count":{"$sum":1}}},{"$sort":{"count":-1}}, {"$limit":3}]
result=collection.aggregate(pipeline)
for doc in result:
    print(doc)


# Number of Users with least Contribution
pipeline=[{"$group": {"_id":"$basic_information.user", "count":{"$sum":1}}},{"$group":{"_id":"$count", "num_users":{"$sum":1}}},{"$sort":{"_id":+1}},{"$limit":25}]
result=collection.aggregate(pipeline)
for doc in result:
    print(doc)



# Count of most common restaurant kinds
pipeline=[{"$match":{"amenity":{"$exists":1}, "amenity.amenity-type":"Restaurant"}}, {"$group":{"_id":"$amenity.cuisine", "count":{"$sum":1}}},{"$sort":{"count":-1}},{"$limit":4}]
result=collection.aggregate(pipeline)
for doc in result:
    print(doc)



# Count of  most common amenities in the dataset
pipeline=[{"$match":{"amenity":{"$exists":1}}}, {"$group":{"_id":"$amenity.amenity-type","count":{"$sum":1}}},{"$sort":{"count":-1}},{"$limit":10}]
result=collection.aggregate(pipeline)
for doc in result:
    print(doc)



# Count of three most common banks in the area
pipeline=[{"$match":{"amenity":{"$exists":1}, "amenity.amenity-type":"Bank"}}, {"$group":{"_id":"$amenity.name", "count":{"$sum":1}}},{"$sort":{"count":-1}},{"$limit":4}]
result=collection.aggregate(pipeline)
for doc in result:
    print(doc)



# Hospitals in the Area
pipeline=[{"$match":{"amenity":{"$exists":1}, "amenity.amenity-type":"Hospital"}}, {"$group":{"_id":"$amenity.name"}}]

result=collection.aggregate(pipeline)

for doc in result:
    print(doc)


