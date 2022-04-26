#from three.renderer.nodes import Node, NodeBuilder
from .node import Node
from .node_builder import NodeBuilder

class TempNode(Node):

    def __init__(self, type = None) -> None:
        super().__init__(type)

    # def build( self, builder:'NodeBuilder', output ):
    #     type = builder.getVectorType( self.getNodeType( builder ) )

    #     if type != 'void':
    #         nodeVar = builder.getVarFromNode( self, type )
    #         propertyName = builder.getPropertyName( nodeVar )

    #         nodeData = builder.getDataFromNode( self )

    #         snippet = nodeData.snippet

    #         if snippet is None:
    #             snippet = super().build( builder, type )
    #             builder.addFlowCode(f'{propertyName} = {snippet}' )
    #             nodeData.snippet = snippet

    #         return builder.format( propertyName, type, output )

    #     else:
    #         return super().build( builder, output )

    def build( self, builder:'NodeBuilder', output = None ):
        type = builder.getVectorType( self.getNodeType( builder, output ) )
        nodeData = builder.getDataFromNode( self )
        #if builder.context.temp != False and type != 'void ' and output != 'void' and nodeData.dependenciesCount and nodeData.dependenciesCount > 1:
        if nodeData.propertyName:
            return builder.format( nodeData.propertyName, type, output )

        elif builder.context.temp != False and type != 'void ' and output != 'void' and nodeData.dependenciesCount and nodeData.dependenciesCount > 1:
            snippet = super().build( builder, type )

            nodeVar = builder.getVarFromNode( self, type )
            propertyName = builder.getPropertyName( nodeVar )

            builder.addFlowCode( f'{propertyName} = {snippet}' )

            nodeData.snippet = snippet
            nodeData.propertyName = propertyName

            return builder.format( nodeData.propertyName, type, output )
        else:
            return super().build( builder, output )