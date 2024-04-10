from textnode import (TextNode,
                      text_type_text,
                      text_type_bold,
                      text_type_italic,
                      text_type_code)

import re

# Splits only single-level elements
# Does not account for nested elements e.g. bold inside of italics
# Redo this function: use length of .split() return value
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: str) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        
        # find delimited words/phrase
        delimited = set()
        p1 = 0
        p2 = 0
        while p2 < len(old_node.text):
            if old_node.text[p2:p2 + len(delimiter)] == delimiter:
                p2 += len(delimiter)
                p1 = p2
                while p2 + len(delimiter) <= len(old_node.text) and old_node.text[p2:p2 + len(delimiter)] != delimiter:
                    p2 += 1
                
                if p2 + len(delimiter) > len(old_node.text):
                    # reached end of text without finding the second delimiter
                    raise Exception(f"Invalid Markdown syntax in {old_node.text}")
                
                delimited.add(old_node.text[p1:p2])
                
            p2 += 1
        
        # new_text = []
        for word_phrase in old_node.text.split(delimiter):
            if not word_phrase: # ignore empty word_phrase
                continue
            if word_phrase not in delimited: # just plain text
                new_nodes.append(TextNode(text=word_phrase, text_type=old_node.text_type))
            else: # delimited word_phrase, i.e. bold, italic, code, etc.
                new_nodes.append(TextNode(text=word_phrase, text_type=text_type))

        return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
    
        image_tup = extract_markdown_images(old_node.text)


# def split_nodes_link(old_nodes):

# This method finds all expressions that match
# "![image_text](link)" where image_text and link are
# arbitrary and returns a list of tuples of the form
# [(image_text_1, link_1), (image_text_2, link_2), ..., (image_text_n, link_n)]
def extract_markdown_images(text) -> list[tuple]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

# This method finds all expressions that match
# "[link_text](link)" where link_text and link are 
# arbitrary and returns a list of tuples of the form
# [(link_text_1, link_1), (link_text_2, link_2), ..., (link_text_n, link_n)]
def extract_markdown_links(text) -> list[tuple]:
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)