from textnode import (TextNode,
                      text_type_text,
                      text_type_bold,
                      text_type_italic,
                      text_type_code)

import re


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: str) -> list[TextNode]:
    out = []

    # text_type_map = {"*": text_type_italic,
    #                  "**": text_type_bold,
    #                  "\'\'": text_type_code}

    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            out.append(old_node)
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
        
        new_text = []
        for word_phrase in old_node.text.split(delimiter):
            if not word_phrase: # ignore empty word_phrase
                continue
            if word_phrase not in delimited: # just plain text
                out.append(TextNode(text=word_phrase, text_type=old_node.text_type))
            else: # delimited word_phrase, i.e. bold, italic, code, etc.
                out.append(TextNode(text=word_phrase, text_type=text_type))

        return out

def extract_markdown_images(text) -> list[tuple]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text) -> list[tuple]:
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)