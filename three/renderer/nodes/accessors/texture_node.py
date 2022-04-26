from ..core.uniform_node import UniformNode
from .uv_node import UVNode

class TextureNode(UniformNode):

    def __init__(self, value, uvNode = None, biasNode = None ) -> None:
        super().__init__(value, 'vec4')

        self.uvNode = uvNode or UVNode()
        self.biasNode = biasNode

    def getUniformHash( self, *args): #  /*builder*/ 
        return self.value.uuid

    def getInputType( self, *args): #  /*builder*/ 
        return 'texture'

    def generate( self, builder, output ):
        texture = self.value

        if texture is None or texture.isTexture != True:
            raise Exception( 'TextureNode: Need a three.js texture.' )
        
        textureProperty = super().generate( builder, 'texture' )

        if output == 'sampler':
            return textureProperty + '_sampler'
        elif builder.isReference( output ):
            return textureProperty
        else:
            nodeData = builder.getDataFromNode( self )
            snippet = nodeData.snippet
            if snippet is None:
                uvSnippet = self.uvNode.build( builder, 'vec2' )
                biasNode = self.biasNode

                if biasNode:
                    biasSnippet = biasNode.build( builder, 'float' )
                    snippet = builder.getTexture( textureProperty, uvSnippet, biasSnippet )
                else:
                    snippet = builder.getTexture( textureProperty, uvSnippet )

                nodeData.snippet = snippet
            return builder.format( snippet, 'vec4', output )


    def serialize( self, data ):
        super().serialize( data )
        #data.value = self.value.toJSON( data.meta ).uuid

    def deserialize( self, data ):
        super().deserialize( data )
        #self.value = data.meta.textures[ data.value ]