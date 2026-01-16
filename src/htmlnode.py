class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method")
    
    def props_to_html(self):
        if self.props is None or len(self.props) == 0:
            return ""
        retval = ""
        for key, value in (self.props or {}).items():
            retval += f' {key}="{value}"'
        return retval
    
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)
    
    def __repr__(self):
        ret_tag = f"'{self.tag}'" if self.tag is not None else "None"
        ret_value = f"'{self.value}'" if self.value is not None else "None"
        ret_children = f"'{self.children}'" if self.children is not None else "None"
        ret_props = f"'{self.props}'" if self.props is not None else "None"

        return f"HTMLNode(tag={ret_tag}, value={ret_value}, children={ret_children}, props={ret_props})"