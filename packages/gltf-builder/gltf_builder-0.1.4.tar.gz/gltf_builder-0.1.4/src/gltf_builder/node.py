'''
Builder representation of a gltr node. This will be compiled down during
the build phase.
'''


from collections.abc import Iterable, Mapping
from typing import Optional, Any

import pygltflib as gltf

from gltf_builder.element import (
    Element, BNodeProtocol, BuilderProtocol, EMPTY_SET,
)
from gltf_builder.mesh import BMesh 
from gltf_builder.holder import Holder


class BNodeContainer:
    mesh: Optional[BMesh]
    children: Holder['BNode']
    @property
    def nodes(self):
        return self.children
    @nodes.setter
    def nodes(self, nodes: Holder['BNode']):
        self.children = nodes
    
    def __init__(self, /,
                 children: Iterable['BNode']=(),
                 **_
                ):
        self.children = Holder(*children)
    
    def add_node(self,
                name: str='',
                children: Iterable['BNode']=(),
                mesh: Optional[BMesh]=None,
                extras: Mapping[str, Any]=EMPTY_SET,
                extensions: Mapping[str, Any]=EMPTY_SET,
                ) -> 'BNode':
        root = isinstance(self, BuilderProtocol)
        node = BNode(name=name,
                    root=root,
                    children=children,
                    mesh=mesh,
                    extras=extras,
                    extensions=extensions,
                )
        self.children.add(node)
        return node


class BNode(BNodeContainer, BNodeProtocol):
    
    def __init__(self,
                 name: str ='',
                 children: Iterable['BNode']=(),
                 mesh: Optional[BMesh]=None,
                 root: bool=False,
                 extras: Mapping[str, Any]=EMPTY_SET,
                 extensions: Mapping[str, Any]=EMPTY_SET,
                 ):
        Element.__init__(self, name, extras, extensions)
        BNodeContainer.__init__(self, children=children)
        self.root = root
        self.mesh = mesh
        
    def do_compile(self, builder: BuilderProtocol):
        if self.mesh:
            builder.meshes.add(self.mesh)
            self.mesh.compile(builder)
        for child in self.children:
            child.compile(builder)
        return gltf.Node(
            name=self.name,
            mesh=self.mesh.index if self.mesh else None,
            children=[child.index for child in self.children],
        )
    
