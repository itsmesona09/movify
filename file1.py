from lxml import etree

# Load the XML file
tree = etree.parse("your_file.xml")
root = tree.getroot()

# Recursively print elements
def print_element(element, indent=0):
    print("  " * indent + f"<{element.tag}>")
    for child in element:
        print_element(child, indent + 1)

print_element(root)
