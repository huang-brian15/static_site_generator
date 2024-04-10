class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self) -> str:
        if self.props:
            out = ""
            for k, v in self.props.items():
                out += f" {k}=\"{v}\""
            return out
        else:
            return ""
    
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag: str = None, value: str = None, props: dict = None):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value == None:
            raise ValueError("Invalid HTML: no value")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag: str = None, children: list = None, props: dict = None):
        super().__init__(tag, None, children, props)
    
    def to_html(self) -> str:
        if self.tag == None:
            raise ValueError("Invalid HTML: no tag")
        if self.children == None or self.children == []:
            raise ValueError("Invalid ParentNode: no children")
        
        out = f"<{self.tag}{self.props_to_html()}>"

        for node in self.children:
            out += node.to_html()
        
        out += f"</{self.tag}>"

        return out

    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"