from typing import List

class ParseNode:
    """Parse tree düğümü"""
    def __init__(self, name: str, children: List['ParseNode'] = None):
        self.name = name
        self.children = children or []
        self.token = None
    
    def add_child(self, child: 'ParseNode'):
        self.children.append(child)
    
    def __str__(self):
        return self.name
