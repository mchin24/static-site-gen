from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag_name, children, props=None):
        super().__init__(tag_name, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag name cannot be None")
        if self.children is None or len(self.children) == 0:
            raise ValueError("ParentNode must have at least one child")
        retval = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            if child is None or not isinstance(child, HTMLNode):
                continue
            retval += child.to_html()
        retval += f"</{self.tag}>"
        return retval
    
    def __repr__(self):
        ret_tag = f"'{self.tag}'" if self.tag is not None else "None"
        ret_children = f"'{self.children}'" if self.children is not None else "None"
        ret_props = f"'{self.props}'" if self.props is not None else "None"

        return f"HTMLNode(tag={ret_tag}, value=None, children={ret_children}, props={ret_props})"