from textnode import (TextNode,
                      text_type_text,
                      text_type_bold,
                      text_type_italic,
                      text_type_code,
                      text_type_link,
                      text_type_image)

import re

def text_to_textnodes(text: str) -> list[TextNode]:
    """
    This method takes a piece of text that may include different
    types of text, .e.g regular text and bold text. It splits the 
    text into multiple TextNode objects. See TextNode class in
    textnode.py for different types of text.
    """

    node = TextNode(text=text,
                    text_type=text_type_text)
    nodes = [node]
    nodes = split_nodes_delimiter(old_nodes=nodes, 
                                  delimiter="**",
                                  text_type=text_type_bold)
    nodes = split_nodes_delimiter(old_nodes=nodes, 
                                  delimiter="*",
                                  text_type=text_type_italic)
    nodes = split_nodes_delimiter(old_nodes=nodes, 
                                  delimiter="`",
                                  text_type=text_type_code)
    
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes


# Redo this function: use length of .split() return value
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: str) -> list[TextNode]:
    """
    This method takes a list of TextNode objects and a specified delimiter, namely:
    - asterisk (italics): *
    - double asterisk (bold): **
    - backtick (inline code): `

    For each TextNode object in the input list, new TextNode objects are created for 
    the original text as well as the text inside a pair of delimiters. Original text 
    remains the same, just in a new TextNode object with the original type. For each 
    piece of text found inside a pair of delimiters, the correct text type is used to 
    create a new TextNode object. New and original TextNode objects are inserted into 
    a new list in a manner which reflects the original list order.

    Note: This method splits only on single-level elements. It does not account for
    nested elements e.g. bold text inside of italic text. It is possible to add this 
    functionality.
    """

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
    """
    This method takes a list of TextNode objects. For each TextNode object,
    this method finds all images nested inside the text. New TextNode objects
    are created for the original text and for the image(s). The functionality
    is similar to that of split_nodes_delimiter().
    """

    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        
        old_text = old_node.text
        image_tups = extract_markdown_images(old_text)
        if len(image_tups) == 0:
            new_nodes.append(old_node)
            continue

        for image_tup in image_tups:
            split_text = old_text.split(f"![{image_tup[0]}]({image_tup[1]})", 1)
            if len(split_text) != 2:
                raise Exception(f"Invalid markdown in {old_text}. Check image text and link syntax.")
            
            if split_text[0]:
                new_nodes.append(TextNode(text=split_text[0],
                                          text_type=text_type_text))
                
            new_nodes.append(TextNode(text=image_tup[0],
                                      text_type=text_type_image,
                                      url=image_tup[1]))
            
            old_text = split_text[1]
        
        if old_text:
            new_nodes.append(TextNode(text=old_text,
                                      text_type=text_type_text))
        
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    This method takes a list of TextNode objects. For each TextNode object,
    this method finds all links nested inside the text. New TextNode objects
    are created for the original text and for the link(s). The functionality
    is similar to that of split_nodes_delimiter().
    """
    
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        
        old_text = old_node.text
        link_tups = extract_markdown_links(old_text)
        if len(link_tups) == 0:
            new_nodes.append(old_node)
            continue

        for link_tup in link_tups:
            split_text = old_text.split(f"[{link_tup[0]}]({link_tup[1]})", 1)
            if len(split_text) != 2:
                raise Exception(f"Invalid markdown in {old_text}. Check link text and link syntax.")
        
            if split_text[0]:
                new_nodes.append(TextNode(text=split_text[0],
                                          text_type=text_type_text))
            
            new_nodes.append(TextNode(text=link_tup[0],
                                      text_type=text_type_link,
                                      url=link_tup[1]))

            old_text = split_text[1]
        
        if old_text:
            new_nodes.append(TextNode(text=old_text,
                                      text_type=text_type_text))

    return new_nodes


def extract_markdown_images(text) -> list[tuple]:
    """
    This method finds all expressions that match 
    "![image_text](link)" where image_text and link are 
    arbitrary and returns a list of tuples of the form 
    [(image_text_1, link_1), (image_text_2, link_2), ..., (image_text_n, link_n)]
    """

    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text) -> list[tuple]:
    """
    This method finds all expressions that match 
    "[link_text](link)" where link_text and link are 
    arbitrary and returns a list of tuples of the form 
    [(link_text_1, link_1), (link_text_2, link_2), ..., (link_text_n, link_n)]
    """

    return re.findall(r"\[(.*?)\]\((.*?)\)", text)