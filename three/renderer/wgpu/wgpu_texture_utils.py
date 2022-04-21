from .constants import GPUIndexFormat, GPUFilterMode, GPUPrimitiveTopology
import wgpu

class WgpuTextureUtils:

    def __init__(self, device: 'wgpu.GPUDevice') -> None:
        
        self.device = device

        mipmapVertexSource = '''
struct VarysStruct {
	[[ builtin( position ) ]] Position: vec4<f32>;
	[[ location( 0 ) ]] vTex : vec2<f32>;
};
[[ stage( vertex ) ]]
fn main( [[ builtin( vertex_index ) ]] vertexIndex : u32 ) -> VarysStruct {
	var Varys: VarysStruct;
	var pos = array< vec2<f32>, 4 >(
		vec2<f32>( -1.0,  1.0 ),
		vec2<f32>(  1.0,  1.0 ),
		vec2<f32>( -1.0, -1.0 ),
		vec2<f32>(  1.0, -1.0 )
	);
	var tex = array< vec2<f32>, 4 >(
		vec2<f32>( 0.0, 0.0 ),
		vec2<f32>( 1.0, 0.0 ),
		vec2<f32>( 0.0, 1.0 ),
		vec2<f32>( 1.0, 1.0 )
	);
	Varys.vTex = tex[ vertexIndex ];
	Varys.Position = vec4<f32>( pos[ vertexIndex ], 0.0, 1.0 );
	return Varys;
}
'''

        mipmapFragmentSource = '''
[[ group( 0 ), binding( 0 ) ]]
var imgSampler : sampler;
[[ group( 0 ), binding( 1 ) ]]
var img : texture_2d<f32>;
[[ stage( fragment ) ]]
fn main( [[ location( 0 ) ]] vTex : vec2<f32> ) -> [[ location( 0 ) ]] vec4<f32> {
	return textureSample( img, imgSampler, vTex );
}
'''

        # self.sampler = device.createSampler( { 'minFilter': GPUFilterMode.Linear } )

        self.sampler = device.create_sampler(minFilter = GPUFilterMode.Linear)

		# We'll need a new pipeline for every texture format used.
        self.pipelines = {}

        self.mipmapVertexShaderModule = device.create_shader_module(code = mipmapVertexSource)

        self.mipmapFragmentShaderModule = device.create_shader_module(code = mipmapFragmentSource)

    
    def getMipmapPipeline( self, format ) -> 'wgpu.GPURenderPipeline':

        pipeline = self.pipelines[ format ]

        if pipeline is None:

            pipeline = self.device.create_render_pipeline(
                vertex= {
                    'module': self.mipmapVertexShaderModule,
                    'entry_point': 'main'
                },
                fragment={
                    'module': self.mipmapFragmentShaderModule,
					'entry_point': 'main',
					'targets': [ { 'format':  format} ]
                },
                primitive={
                    'topology': GPUPrimitiveTopology.TriangleStrip,
                    'strip_index_format': GPUIndexFormat.Uint32
                }
            )

            self.pipelines[ format ] = pipeline


        return pipeline

    
    def generateMipmaps( self, textureGPU:'wgpu.GPUTexture', textureGPUDescriptor, baseArrayLayer = 0, mipLevelOffset = 1 ):
        
        pipeline = self.getMipmapPipeline( textureGPUDescriptor.format )

        commandEncoder:'wgpu.GPUCommandEncoder' = self.device.create_command_encoder()
        # bindGroupLayout = pipeline.getBindGroupLayout( 0 ); # @TODO: Consider making this static.
        bindGroupLayout = pipeline.get_bind_group_layout(0)

        srcView = textureGPU.create_view(base_mip_level= 0 , mip_level_count= 1)

        #for i = 1; i < textureGPUDescriptor.mipLevelCount; i ++ ) {
        
        i = mipLevelOffset
        while i < textureGPUDescriptor.mipLevelCount:


            dstView = textureGPU.create_view(base_mip_level= i, mip_level_count= 1, base_array_layer = baseArrayLayer)

            passEncoder:'wgpu.GPURenderPassEncoder' = commandEncoder.begin_render_pass(color_attachments=[{
                'view': dstView,
                'load_value': [ 0, 0, 0, 0 ]
            }])

            bindGroup = self.device.create_bind_group(
                layout=bindGroupLayout,
                entries=[{
                    'binding': 0,
					'resource': self.sampler
                },{
                    'binding': 1,
					'resource': srcView
                }]

            )

            passEncoder.set_pipeline( pipeline )
            passEncoder.set_bind_group( 0, bindGroup )
            passEncoder.draw( 4, 1, 0, 0 )
            passEncoder.end_pass()
            
            srcView = dstView

        self.device.queue.submit( [ commandEncoder.finish() ] )


