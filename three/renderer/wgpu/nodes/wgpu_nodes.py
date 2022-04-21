from ...nodes import NodeFrame
from .wgpu_node_builder import WgpuNodeBuilder

class WgpuNodes:

    def __init__(self, renderer, properties) -> None:
        
        self.renderer = renderer
        self.properties = properties
        self.nodeFrame = NodeFrame()



    def get( self, object):

        objectProperties = self.properties.get( object )

        nodeBuilder = objectProperties.nodeBuilder

        if nodeBuilder is None:
            fogNode = objectProperties.fogNode
            lightNode = objectProperties.lightNode

            nodeBuilder = WgpuNodeBuilder( object, self.renderer )
            nodeBuilder.lightNode = lightNode
            nodeBuilder.fogNode = fogNode
            nodeBuilder.build()

            objectProperties.nodeBuilder = nodeBuilder

        return nodeBuilder

    def remove( self, object ):
        objectProperties = self.properties.get( object )
        del objectProperties.nodeBuilder

    def updateFrame(self):
        self.nodeFrame.update()


    def update( self, object, camera ):
        renderer = self.renderer
        material = object.material

        nodeBuilder = self.get( object )
        nodeFrame = self.nodeFrame

        nodeFrame.camera = camera
        nodeFrame.object = object
        nodeFrame.renderer = renderer
        nodeFrame.material = material
        for node in nodeBuilder.updateNodes:
            nodeFrame.updateNode( node )

    def dispose(self):
        self.nodeFrame = NodeFrame()