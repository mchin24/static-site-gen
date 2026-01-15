from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        props = ""
        if self.value is None:
            raise ValueError("LeafNode must have a value.")
        if self.tag is None:
            return str(self.value)
        props = self.props_to_html()
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        ret_tag = f"'{self.tag}'" if self.tag is not None else "None"
        ret_value = f"'{self.value}'" if self.value is not None else "None"
        ret_props = f"'{self.props}'" if self.props is not None else "None"

        return f"HTMLNode(tag={ret_tag}, value={ret_value}, props={ret_props})"
