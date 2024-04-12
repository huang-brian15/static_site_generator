from htmlnode import (LeafNode,
                      ParentNode)
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes

block_type_paragraph = "paragraph"
block_type_heading ="heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_html_node(markdown: str) -> ParentNode:
    """
    Ths method takes a full piece of markdown and returns
    an HTML ParentNode with the children being instances of
    HTML ParentNode, with each representing the contents
    of the block.
    """
    
    block_nodes = []

    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_nodes.append(block_to_html_node(block))
    
    return ParentNode(tag="div", children=block_nodes)


def markdown_to_blocks(markdown: str) -> list[str]:
    """
    This method takes an entire piece of markdown and
    splits it into blocks of text.
    """

    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        block = block.strip()
        if block == "":
            continue
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_html_node(block: str) -> ParentNode:
    """
    This method takes a block and returns an HTML 
    ParentNode which correctly represents the block
    type.
    """

    block_type = block_to_block_type(block)

    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    elif block_type == block_type_heading:
        return heading_to_html_node(block)
    elif block_type == block_type_code:
        return code_to_html_node(block)
    elif block_type == block_type_quote:
        return quote_to_html_node(block)
    elif block_type == block_type_unordered_list:
        return unordered_list_to_html_node(block)
    elif block_type == block_type_ordered_list:
        return ordered_list_to_html_node(block)
    else:
        raise ValueError("Invalid block type.")

def block_to_block_type(block: str) -> str:
    """
    This method takes a block of text and determines
    the type of block as listed:
    - paragraph
    - heading
    - code
    - quote
    - unordered list
    - ordered list
    """

    # Headings
    if (block.startswith("# ") or
        block.startswith("## ") or
        block.startswith("### ") or
        block.startswith("#### ") or
        block.startswith("##### ") or
        block.startswith("###### ")
    ):
        return block_type_heading
    
    # Code
    if block.startswith("```") and block.endswith("```"):
        return block_type_code
    
    lines = block.split("\n")

    # Quote
    if lines[0].startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return block_type_paragraph
        
        return block_type_quote
    
    # Unordered list
    if lines[0].startswith("*"):
        for line in lines:
            if not line.startswith("*"):
                return block_type_paragraph
        
        return block_type_unordered_list
    
    # Unordered list
    if lines[0].startswith("-"):
        for line in lines:
            if not line.startswith("-"):
                return block_type_paragraph
        
        return block_type_unordered_list

    # Ordered list
    if lines[0].startswith("1."):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}."):
                return block_type_paragraph
            
            i += 1
        
        return block_type_ordered_list

    return block_type_paragraph


def text_to_text_nodes_to_leaf_nodes(text: str) -> list[LeafNode]:
    """
    This method takes a piece of text and creates as many TextNode 
    objects as required. For each of these new TextNodes, an HTML 
    LeafNode is created.
    
    Returns a list of LeafNodes.
    """
    text_nodes = text_to_textnodes(text)
    leaf_nodes = []
    for text_node in text_nodes:
        leaf_node = text_node_to_html_node(text_node)
        leaf_nodes.append(leaf_node)
    
    return leaf_nodes


def paragraph_to_html_node(block: str) -> ParentNode:
    """
    This method takes a paragraph block and creates an 
    HTML ParentNode with the nested LeafNode children.
    See test_markdown_blocks.py for test cases.
    """
    
    lines = block.split("\n")
    paragraph = " ".join(lines)
    leaf_nodes = text_to_text_nodes_to_leaf_nodes(paragraph)
    return ParentNode(tag="p", children=leaf_nodes)


def heading_to_html_node(block: str) -> ParentNode:
    """
    This method takes a paragraph block and creates an 
    HTML ParentNode with the nested LeafNode children.
    See test_markdown_blocks.py for test cases.
    """

    level, text = block.split(" ", 1)

    # only contains hashes
    if len(set(level)) > 1 and level[0] == "#":
        raise ValueError(f"Invalid heading level: {level}")

    # only contains 1-6 hashes
    if len(level) < 1 or len(level) > 6:
        raise ValueError(f"Invalid heading level: {level}")

    leaf_nodes = text_to_text_nodes_to_leaf_nodes(text)
    return ParentNode(tag=f"h{len(level)}", children=leaf_nodes)
    

def code_to_html_node(block: str) -> ParentNode:
    """
    This method takes a code block and creates an 
    HTML ParentNode with the nested LeafNode children.
    See test_markdown_blocks.py for test cases.
    """

    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    
    text = block.strip("```").strip()
    leaf_nodes = text_to_text_nodes_to_leaf_nodes(text)
    code_node = ParentNode(tag="code", children=leaf_nodes)
    return ParentNode(tag="pre", children=[code_node])


def quote_to_html_node(block: str) -> ParentNode:
    """
    This method takes a quote block and creates an 
    HTML ParentNode with the nested LeafNode children.
    See test_markdown_blocks.py for test cases.
    """

    quote_lines = []
    split_block = block.split("\n")
    for line in split_block:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        quote_lines.append(line.lstrip(">").strip())
    
    leaf_nodes = text_to_text_nodes_to_leaf_nodes(" ".join(quote_lines))
    return ParentNode(tag="blockquote", children=leaf_nodes)


def unordered_list_to_html_node(block: str) -> ParentNode:
    """
    This method takes an unordered list block and creates an 
    HTML ParentNode with the nested LeafNode children.
    See test_markdown_blocks.py for test cases.
    """

    ul_identifier = None
    if block.startswith("*"):
        ul_identifier = "*"
    elif block.startswith("-"):
        ul_identifier = "-"
    else:
        raise ValueError("Invalid unordered list")

    list_nodes = []

    list_items = block.split("\n")
    for list_item in list_items:
        if not list_item.startswith(ul_identifier):
            raise ValueError(f"Invalid unordered list: list item starts with {list_item[0]} but previous list item starts with {ul_identifier}")
        
        leaf_nodes = text_to_text_nodes_to_leaf_nodes(list_item.lstrip(ul_identifier).strip())
        list_nodes.append(ParentNode(tag="li", children=leaf_nodes))
    
    return ParentNode(tag="ul", children=list_nodes)


def ordered_list_to_html_node(block: str) -> ParentNode:
    """
    This method takes an ordered list block and creates an 
    HTML ParentNode with the nested LeafNode children.
    See test_markdown_blocks.py for test cases.
    """
    
    list_nodes = []

    if not block.startswith("1."):
        raise ValueError("Invalid ordered list: Must start with 1.")

    list_items = block.split("\n")
    item_num = 1
    for list_item in list_items:
        if not list_item.startswith(f"{item_num}."):
            raise ValueError(f"Invalid ordered list: List item numbers must be consecutively increasing.")
        
        leaf_nodes = text_to_text_nodes_to_leaf_nodes(list_item.lstrip(f"{item_num}.").strip())
        list_nodes.append(ParentNode(tag="li", children=leaf_nodes))
        
        item_num += 1
    
    return ParentNode(tag="ol", children=list_nodes)