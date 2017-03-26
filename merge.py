from lxml import etree

parent_xml_file = 'data/provenance.xml'
tree = etree.parse(parent_xml_file)

children_xml_file = 'data/silver.xml'
children_tree = etree.parse(children_xml_file)

# Create parent node -- collections
merged_tree = etree.Element("collections")

for _, element in etree.iterparse(parent_xml_file, tag='collection'):
	xpath = '/object[identifier="' + element.findtext('identifier') + '"]'	
	objects = etree.SubElement(element, "objects")

	# find all objects in the current collection, each object is identified by the reference field -- identifier
	for child in children_tree.findall(xpath):
		objects.insert(0, child)
	
	# Merge all the found objects into their collection
	merged_tree.append(element)

# Creating an empty output file
xml = open('data/merged_provenance_silver.xml','w')
xml.close()

# Writing into the .xml file
xml = open('data/merged_provenance_silver.xml','a')
xml.write('<?xml version="1.0" encoding="UTF-8"?>\n')
xml.write(etree.tostring(merged_tree))
xml.close()
