'''Vulkan objects modules

This module contains the *High* level Vulkan object. It's not that *high*
level, you need to understand fully Vulkan to use theses objects.
This module must be use by Vulkan expert and is very complicated to work with.
You will see a lot of namedtuple here, they are used to better document the
object arguments. Instead of passing a dict whith unknow keys, you pass a
documented namedtuple, I think it's better.
If you want to understand internal Vulkan functions, you can hack around this
module.

**Note: In this module, when it's needed, the parameter type is indicated. If
        the type begins with Vk..., it means a real Vulkan object and not an
        object in this module.**
'''

from collections import namedtuple
from contextlib import contextmanager
import logging
import vulkan as vk

from vulk.exception import VulkError
from vulk import vulkanconstant

logger = logging.getLogger()

STAGE_MAPPING = {
    'vertex': vk.VK_SHADER_STAGE_VERTEX_BIT,
    'tessellation_control': vk.VK_SHADER_STAGE_TESSELLATION_CONTROL_BIT, # noqa
    'tessellation_evaluation': vk.VK_SHADER_STAGE_TESSELLATION_EVALUATION_BIT, # noqa
    'geometry': vk.VK_SHADER_STAGE_GEOMETRY_BIT,
    'fragment': vk.VK_SHADER_STAGE_FRAGMENT_BIT,
    'compute': vk.VK_SHADER_STAGE_COMPUTE_BIT
}


def vk_const(v):
    '''Get constant

    if v is str, we get the constant in vulkan
    else we return it as is
    '''

    if isinstance(v, str):
        if '|' in v:
            result = 0
            for attr in v.split('|'):
                result |= vk_const(attr)
            return result
        return getattr(vk, v)
    return v


def btov(b):
    '''Convert boolean to Vulkan boolean'''
    return vk.VK_TRUE if b else vk.VK_FALSE


def find_memory_type(context, type_filter, properties):
    '''
    Graphics cards can offer different types of memory to allocate from.
    Each type of memory varies in terms of allowed operations and performance
    characteristics. We need to combine the requirements of the memory and our
    own application requirements to find the right type of memory to use.

    *Parameters:*

    - `context`: The `VulkContext`
    - `type_filter`: Bit field of the memory types that are suitable
                     for the memory (int)
    - `properties`: `VkMemoryPropertyFlags` Vulkan constant, type of
                    memory we want

    **Todo: I made a bitwise comparaison with `type_filter`, I have to test
            it to be sure it's working**
    '''
    if not find_memory_type.cache_properties:
        find_memory_type.properties = vk.vkGetPhysicalDeviceMemoryProperties(
            context.physical_device)

    for i, memory_type in enumerate(find_memory_type.properties.memoryTypes):
        # TODO: Test type_filter
        if (type_filter & (1 << i)) and \
           (memory_type.propertyFlags & properties) == properties:
            return i

    msg = "Can't find suitable memory type"
    logger.critical(msg)
    raise VulkError(msg)


# Set physical device memory properties in cache since it depends
# only on the physical device
find_memory_type.cache_properties = None


class ShaderModule():
    '''ShaderModule Vulkan object

    A shader module is a Spir-V shader loaded into Vulkan.
    After being created, it must be inserted in a pipeline stage.
    The real Vulkan module can be accessed by the 'module' property.
    '''

    def __init__(self, context, code):
        '''
        Initialize the module

        *Parameters:*

        - `context`: The `VulkContext` object
        - `code`: Binary Spir-V loaded file (bytes)

        *Returns:*

        The created `ShaderModule`
        '''
        if not isinstance(code, bytes):
            logger.info("Type of code is not 'bytes', it may be an error")

        self.code = code

        # Create the shader module
        shader_create = vk.VkShaderModuleCreateInfo(
            sType=vk.VK_STRUCTURE_TYPE_SHADER_MODULE_CREATE_INFO,
            flags=0, codeSize=len(code), pCode=code)
        self.module = vk.vkCreateShaderModule(context.device, shader_create)


#  Objects used in Renderpass
AttachmentDescription = namedtuple('AttachmentDescription',
                                   ['format', 'samples', 'load', 'store',
                                    'stencil_load', 'stencil_store',
                                    'initial_layout', 'final_layout'])
AttachmentDescription.__doc__ = '''
    AttachmentDescription describes the attachment.

    *Parameters:*

    - `format`: VkFormat vulkan constant
    - `samples`: VkSampleCountFlagBits vulkan constant
    - `load`: VkAttachmentLoadOp vulkan constant
    - `store`: VkAttachmentStoreOp vulkan constant
    - `stencil_load`: VkAttachmentLoadOp vulkan constant
    - `stencil_store`: VkAttachmentStoreOp vulkan constant
    - `initial_layout`: VkImageLayout vulkan constant
    - `final_layout`: VkImageLayout vulkan constant
    '''


AttachmentReference = namedtuple('AttachmentReference', ['index', 'layout'])
AttachmentReference.__doc__ = '''
    AttachmentReference links an attachment index with a layout.

    *Parameters:*

    - `index`: Index of attachment description
    - `layout`: VkImageLayout vulkan constant
    '''


SubpassDescription = namedtuple('SubpassDescription',
                                ['colors', 'inputs', 'resolves',
                                 'preserves', 'depth_stencil'])
SubpassDescription.__new__.__defaults__ = \
        ([],) * len(SubpassDescription._fields)
SubpassDescription.__doc__ = '''
    SubpassDescription describes all attachments in the subpass.
    All parameters are of type AttachmentReference. The order of
    If you don't want an attachment, don't set it, its default
    value is an empty list.

    *Parameters:*

    - `colors`: list of colors attachments
    - `inputs`: list of inputs attachments
    - `resolves`: list of resolves attachments (must be the same
                  size as inputs)
    - `preserves`: list of preserves attachments
    - `depth_stencil`: list containing only one attachment
    '''


SubpassDependency = namedtuple('SubpassDependency',
                               ['src_subpass', 'src_stage', 'src_access',
                                'dst_subpass', 'dst_stage', 'dst_access'])
SubpassDependency.__doc__ = '''
    SubpassDependency describes all dependencies of the subpass.

    *Parameters:*

    - `src_subpass`: Source subpass (int)
    - `src_stage`: Source stage (VkPipelineStageFlagBits)
    - `src_access`: Source access (VkAccessFlagBits)
    - `dst_subpass`: Destination subpass (int)
    - `dst_stage`: Destination stage (VkPipelineStageFlagBits-
    - `dst_access`: Destination access (VkAccessFlagBits)
    '''


class Renderpass():
    '''Renderpass object

    When creating the pipeline, we need to tell Vulkan about the
    framebuffer attachments that will be used while rendering. We need to
    specify how many color and depth buffers there will be, how many samples
    to use for each of them and how their contents should be handled
    throughout the rendering operations. All of this information is wrapped
    in a RenderPass object
    '''

    def __init__(self, context, attachments, subpasses, dependencies):
        '''Renderpass constructor

        *Parameters:*

        - `context`: The `VulkContext`
        - `attachments`: List of `AttachmentDescription`
        - `subpasses`: List of `SubpassDescription`
        - `dependencies`: List of `SubpassDependency`

        **Warning: Arguments ar not checked, you must kwnow
                   what you are doing.**
        '''

        vk_attachments = []
        for a in attachments:
            vk_attachments.append(vk.VkAttachmentDescription(
                flags=0,
                format=vk_const(a.format),
                samples=vk_const(a.samples),
                loadOp=vk_const(a.load),
                storeOp=vk_const(a.store),
                stencilLoadOp=vk_const(a.stencil_load),
                stencilStoreOp=vk_const(a.stencil_store),
                initialLayout=vk_const(a.initial_layout),
                finalLayout=vk_const(a.final_layout)
            ))

        # Loop through the list of subpasses to create the reference
        # reference key is index_layout
        vk_references = {}
        for s in subpasses:
            all_list = [s.setdefault(k, []) for k in ('colors', 'inputs',
                        'resolves', 'preserves', 'depth_stencil')]
            all_list = [item for sublist in all_list for item in sublist]

            for r in (s.colors + s.inputs + s.resolves +
                      s.preserves + s.depth_stencil):
                key = (r.index, r.layout)
                if key not in vk_references:
                    vk_references[key] = vk.VkAttachmentReference(
                        attachment=r.index,
                        layout=vk_const(r.layout)
                    )

        # Create the subpasses using references
        vk_subpasses = []
        for s in subpasses:
            leninputs = len(s.inputs)
            lenpreserves = len(s.preserves)
            lencolors = len(s.colors)
            lenresolves = len(s.resolves)
            inputs = s.inputs or None
            preserves = s.preserves or None
            colors = s.colors or None
            resolves = s.resolves or None
            depth_stencil = next(iter(s.depth_stencil), None)

            if resolves and inputs and lenresolves != lencolors:
                msg = "resolves and inputs list must be of the same size"
                logger.error(msg)
                raise VulkError(msg)

            vk_subpasses.append(vk.VkSubpassDescription(
                flags=0,
                pipelineBindPoint=vk.VK_PIPELINE_BIND_POINT_GRAPHICS,
                inputAttachmentCount=leninputs,
                pInputAttachments=inputs,
                colorAttachmentCount=lencolors,
                pColorAttachments=colors,
                pResolveAttachments=resolves,
                preserveAttachmentCount=lenpreserves,
                pPreserveAttachments=preserves,
                pDepthStencilAttachment=depth_stencil
            ))

        # Create the dependancies
        vk_dependencies = []
        for d in dependencies:
            vk_dependencies.append(vk.VkSubpassDependency(
                dependencyFlags=0,
                srcSubpass=vk_const(d.src_subpass),
                dstSubpass=vk_const(d.dst_subpass),
                srcStageMask=vk_const(d.src_stage),
                dstStageMask=vk_const(d.dst_stage),
                srcAccessMask=vk_const(d.src_access),
                dstAccessMask=vk_const(d.dst_access)
            ))

        # Create the render pass
        renderpass_create = vk.VkRenderPassCreateInfo(
            flags=0,
            sType=vk.VK_STRUCTURE_TYPE_RENDER_PASS_CREATE_INFO,
            attachmentCount=len(vk_attachments),
            pAttachments=vk_attachments,
            subpassCount=len(vk_subpasses),
            pSubpasses=vk_subpasses,
            dependencyCount=len(vk_dependencies),
            pDependencies=vk_dependencies
        )

        self.renderpass = vk.vkCreateRenderPass(
            context.device, renderpass_create)


#  Objects used in Pipeline
PipelineShaderStage = namedtuple('PipelineShaderStage', ['module', 'stage'])
PipelineShaderStage.__doc__ = '''
    *Parameters:*

    - `module`: The `ShaderModule` to bind
    - `stage`: Stage name in ['vertex', 'fragment', 'geometry', 'compute',
               'tesselation_control', 'tesselation_evaluation']
    '''

PipelineVertexInputState = namedtuple('PipelineVertexInputState',
                                      ['bindings', 'attributes'])
PipelineVertexInputState.__new__.__defaults__ = \
        ([],) * len(PipelineVertexInputState._fields)
PipelineVertexInputState.__doc__ = '''
    *Parameters:*

    - `bindings`: List of vertice bindings
    - `attributes`: List of vertice attributes
    '''

PipelineInputAssemblyState = namedtuple('PipelineInputAssemblyState',
                                        'topology')
PipelineInputAssemblyState.__doc__ = '''
    *Parameters:*

    - `topology`: The `VkPrimitiveTopology` to use when drawing
    '''

PipelineViewportState = namedtuple('PipelineViewportState',
                                   ['viewports', 'scissors'])
PipelineViewportState.__doc__ = '''
    The PipelineViewportState object contains viewports and scissors.

    *Parameters:*

    - `viewports`: List of viewport
    - `scissors`: List of scissor

    **Warning:: The viewports and scissors are real Vulkan objects
                (`vk.VkRect2D`) and not Vulk objects.**

    **Todo: Viewport and scissor should not be real Vulkan objects**
    '''

PipelineRasterizationState = namedtuple(
    'PipelineRasterizationState',
    ['depth_clamp_enable', 'polygon_mode', 'line_width', 'cull_mode',
     'front_face', 'depth_bias_constant', 'depth_bias_clamp',
     'depth_bias_slope']
)
PipelineRasterizationState.__doc__ = '''
    *Parameters:*

    - `depth_clamp_enable`: Whether to enable depth clamping (`boolean`)
    - `polygon_mode`: Which `VkPolygonMode` to use
    - `line_width`: Width of line (`float`)
    - `cull_mode`: The way of culling (`VkCullModeFlagBits`)
    - `front_face`: `VkFrontFace`
    - `depth_bias_constant`: Constant to add to depth (`float`)
    - `depth_bias_clamp`: Max depth bias (`float`)
    - `depth_bias_slope`: Factor to slope (`float`)
    '''

PipelineMultisampleState = namedtuple('PipelineMultisampleState',
                                      ['shading_enable', 'samples',
                                       'min_sample_shading'])
PipelineMultisampleState.__doc__ = '''
    *Parameters:*

    - `shading_enable`: Enable multisampling (`boolean`)
    - `samples`: Number of samples (`VkSampleCountFlagBits`)
    - `min_sample_shading`: Minimum of sample (`float`)
    '''

PipelineDepthStencilState = namedtuple(
    'PipelineDepthStencilState',
    ['depth_test_enable', 'depth_write_enable', 'depth_bounds_test_enable',
     'depth_compare', 'stencil_test_enable', 'front', 'back', 'min', 'max']
)
PipelineDepthStencilState.__doc__ = '''
    *Parameters:*

    - `depth_test_enable`: Enable depth test
    - `depth_write_enable`: Enable depth write
    - `depth_bounds_test_enable`: Enable bounds test
    - `depth_compare`: Condition to overwrite depth (`VkCompareOp`)
    - `stencil_test_enable`: Enable stencil test
    - `front`: Control stencil parameter (`VkStencilOpState`)
    - `back`: Control stencil parameter (`VkStencilOpState`)
    - `min`: Define the min value in depth bound test (`float`)
    - `max`: Define the max value in depth bound test (`float`)
    '''

PipelineColorBlendAttachmentState = namedtuple(
    'PipelineColorBlendAttachmentState',
    ['enable', 'src_color', 'dst_color', 'color_op',
     'src_alpha', 'dst_alpha', 'alpha_op', 'color_mask']
)
PipelineColorBlendAttachmentState.__doc__ = '''
    *Parameters:*

    - `enable`: Enable blending
    - `src_color`: Blending factor for source color (`VkBlendFactor`)
    - `dst_color`: Blending factor for destination color (`VkBlendFactor`)
    - `color_op`: Operation on color (`VkBlendOp`)
    - `src_alpha`: Blending factor for source alpha (`VkBlendFactor`)
    - `dst_alpha`: Blending factor for destination alpha (`VkBlendFactor`)
    - `alpha_op`: Operation on alpha (`VkBlendOp`)
    - `color_mask`: Bitmask selecting which of the R, G, B, and A components
                    are enabled for writing (`VkColorComponentFlags`)
    '''

PipelineColorBlendState = namedtuple('PipelineColorBlendState',
                                     ['op_enable', 'op', 'attachments',
                                      'constants'])
PipelineColorBlendState.__doc__ = '''
    *Parameters:*

    - `op_enable`: Enable bitwise combination
    - `op`: Operation to perform (`VlLogicOp`)
    - `attachments`: List of blend attachments for each framebuffer
    - `constants`: Constants depending on blend factor (`list` of 4 `float`)
    '''

PipelineDynamicState = namedtuple('PipelineDynamicState', 'states')
PipelineDynamicState.__doc__ = '''
    - `states`: List of `VkDynamicState`
    '''


class Pipeline():
    '''Pipeline (graphic) object

    The graphics pipeline is the sequence of operations that take the
    vertices and textures of your meshes all the way to the pixels in
    the render targets. The pipeline combines the following elements:

      - Shader stages: the shader modules that define the functionality of
                       the programmable stages of the graphics pipeline
      - Fixed-function state: all of the structures that define the
                              fixed-function stages of the pipeline, like
                              input assembly, rasterizer, viewport and
                              color blending
      - Pipeline layout: the uniform and push values referenced by the
                         shader that can be updated at draw time
      - Render pass: the attachments referenced by the pipeline stages
                     and their usage
    '''

    def __init__(self, context, stages, vertex_input, input_assembly,
                 viewport, rasterization, multisample, depth, blend, dynamic,
                 renderpass):
        '''

        - `context`: The `VulkContext`
        - `stages`: List of `PipelineShaderStage`
        - `vertex_input`: `PipelineVertexInputState`
        - `input_assembly`: `PipelineInputAssemblyState`
        - `viewport`: `PipelineViewportState`
        - `rasterization`: `PipelineRasterizationState`
        - `multisample`: `PipelineMultisampleState`
        - `depth`: `PipelineDepthStencilState` (can be `None`)
        - `blend`: `PipelineColorBlendState`
        - `dynamic`: `PipelineDynamicState` (may be `None`)
        - `renderpass`: The `Renderpass` of this pipeline
        '''

        vk_stages = []
        for s in stages:
            try:
                vulkan_stage = STAGE_MAPPING[s.stage]
            except KeyError:
                msg = "Stage %s doesn't exist"
                logger.error(msg)
                raise TypeError(msg)

            vk.VkPipelineShaderStageCreateInfo(
                sType=vk.VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO,
                flags=0,
                stage=vulkan_stage,
                module=s.module,
                pSpecializationInfo=None,
                pName='main'
            )

        vk_vertex_input = vk.VkPipelineVertexInputStateCreateInfo(
            sType=vk.VK_STRUCTURE_TYPE_PIPELINE_VERTEX_INPUT_STATE_CREATE_INFO,
            flags=0,
            vertexBindingDescriptionCount=len(vertex_input.bindings),
            pVertexBindingDescriptions=vertex_input.bindings or None,
            vertexAttributeDescriptionCount=len(vertex_input.attributes),
            pVertexAttributeDescriptions=vertex_input.attributes or None
        )

        vk_input_assembly = vk.VkPipelineInputAssemblyStateCreateInfo(
            sType=vk.VK_STRUCTURE_TYPE_PIPELINE_INPUT_ASSEMBLY_STATE_CREATE_INFO, # noqa
            flags=0,
            topology=vk_const(input_assembly.topology),
            primitiveRestartEnable=vk.VK_FALSE
        )

        vk_viewport = vk.VkPipelineViewportStateCreateInfo(
            sType=vk.VK_STRUCTURE_TYPE_PIPELINE_VIEWPORT_STATE_CREATE_INFO,
            flags=0,
            viewportCount=len(viewport.viewports),
            pViewports=viewport.viewports,
            scissorCount=len(viewport.scissors),
            pScissors=viewport.scissors
        )

        dbe = vk.VK_FALSE
        if (rasterization.depth_bias_constant or
           rasterization.depth_bias_clamp or
           rasterization.depth_bias_slope):
            dbe = vk.VK_TRUE

        vk_rasterization = vk.VkPipelineRasterizationStateCreateInfo(
            sType=vk.VK_STRUCTURE_TYPE_PIPELINE_RASTERIZATION_STATE_CREATE_INFO, # noqa
            flags=0,
            depthClampEnable=btov(rasterization.depth_clamp_enable),
            rasterizerDiscardEnable=vk.VK_FALSE,
            polygonMode=vk_const(rasterization.polygon_mode),
            lineWidth=rasterization.line_width,
            cullMode=vk_const(rasterization.cull_mode),
            frontFace=vk_const(rasterization.front_face),
            depthBiasEnable=dbe,
            depthBiasConstantFactor=rasterization.depth_bias_constant,
            depthBiasClamp=rasterization.depth_bias_clamp,
            depthBiasSlopeFactor=rasterization.depth_bias_slope
        )

        vk_multisample = vk.VkPipelineMultisampleStateCreateInfo(
            sType=vk.VK_STRUCTURE_TYPE_PIPELINE_MULTISAMPLE_STATE_CREATE_INFO,
            flags=0,
            sampleShadingEnable=btov(multisample.shading_enable),
            rasterizationSamples=vk_const(multisample.samples),
            minSampleShading=multisample.min_sample_shading,
            pSampleMask=None,
            alphaToCoverageEnable=vk.VK_FALSE,
            alphaToOneEnable=vk.VK_FALSE
        )

        vk_depth = None
        if depth:
            vk_depth = vk.VkPipelineDepthStencilStateCreateInfo(
                sType=vk.VK_STRUCTURE_TYPE_PIPELINE_DEPTH_STENCIL_STATE_CREATE_INFO, # noqa
                flags=0,
                depthTestEnable=btov(depth.depth_test_enable),
                depthWriteEnable=btov(depth.depth_write_enable),
                depthCompareOp=vk_const(depth.depth_compare),
                depthBoundsTestEnable=btov(depth.depth_bounds_test_enable),
                stencilTestEnable=btov(depth.stencil_test_enable),
                front=depth.front,
                back=depth.back,
                minDepthBounds=depth.min,
                maxDepthBounds=depth.max
            )

        vk_blend_attachments = []
        for a in blend.attachments:
            vk_a = vk.VkPipelineColorBlendAttachmentState(
                colorWriteMask=vk_const(a.color_mask),
                blendEnable=btov(a.enable),
                srcColorBlendFactor=vk_const(a.src_color),
                dstColorBlendFactor=vk_const(a.dst_color),
                colorBlendOp=vk_const(a.color_op),
                srcAlphaBlendFactor=vk_const(a.src_alpha),
                dstAlphaBlendFactor=vk_const(a.dst_alpha),
                alphaBlendOp=vk_const(a.alpha_op)
            )
            vk_blend_attachments.append(vk_a)

        vk_blend = vk.VkPipelineColorBlendStateCreateInfo(
            sType=vk.VK_STRUCTURE_TYPE_PIPELINE_COLOR_BLEND_STATE_CREATE_INFO,
            flags=0,
            logicOpEnable=btov(blend.op_enable),
            logicOp=vk_const(blend.op),
            attachmentCount=len(vk_blend_attachments),
            pAttachments=vk_blend_attachments,
            blendConstants=blend.constants
        )

        vk_dynamic = None
        if dynamic:
            vk_dynamic = vk.VkPipelineDynamicStateCreateInfo(
                sType=vk.VK_STRUCTURE_TYPE_PIPELINE_DYNAMIC_STATE_CREATE_INFO,
                flags=0,
                dynamicStateCount=len(dynamic.states),
                pDynamicStates=dynamic.states
            )

        # Currently layout is unusable, I have to try it
        vk_layout_create = vk.VkPipelineLayoutCreateInfo(
            sType=vk.VK_STRUCTURE_TYPE_PIPELINE_LAYOUT_CREATE_INFO,
            flags=0,
            setLayoutCount=0,
            pSetLayouts=None,
            pushConstantRangeCount=0,
            pPushConstantRanges=None
        )
        vk_layout = vk.vkCreatePipelineLayout(context.device, vk_layout_create)

        pipeline_create = vk.VkGraphicsPipelineCreateInfo(
            sType=vk.VK_STRUCTURE_TYPE_GRAPHICS_PIPELINE_CREATE_INFO,
            flags=0,
            stageCount=len(vk_stages),
            pStages=vk_stages,
            pVertexInputState=vk_vertex_input,
            pInputAssemblyState=vk_input_assembly,
            pTessellationState=None,
            pViewportState=vk_viewport,
            pRasterizationState=vk_rasterization,
            pMultisampleState=vk_multisample,
            pDepthStencilState=vk_depth,
            pColorBlendState=vk_blend,
            pDynamicState=vk_dynamic,
            layout=vk_layout,
            renderPass=renderpass,
            subpass=0,
            basePipelineHandle=None,
            basePipelineIndex=-1
        )

        self.pipeline = vk.vkCreateGraphicsPipelines(context.device, None,
                                                     1, pipeline_create)


Offset2D = namedtuple('Offset2D', ['x', 'y'])
Offset2D.__doc__ = '''
    *Parameters:*

    - `x`: x offset
    - `y`: y offset
    '''


Extent2D = namedtuple('Extent2D', ['width', 'height'])
Extent2D.__doc__ = '''
    *Parameters:*

    - `width`: Width
    - `height`: Height
    '''


Extent3D = namedtuple('Extent3D', ['width', 'height', 'depth'])
Extent3D.__doc__ = '''
    *Parameters:*

    - `width`: Width
    - `height`: Height
    - `depth`: Depth
    '''


class Image():
    '''
    `Image` is a wrapper around a `VkImage` and a `VkMemory`
    '''

    def __init__(self, context, image_type, format, width, height, depth,
                 mip_level, layers, samples, sharing_mode, queue_families,
                 layout, tiling, usage, memory_properties):
        '''Create a new image

        Creating an image is made of several steps:

        - Create the staging image
        - Allocate the staging memory
        - Bind the memory to the image

        *Parameters:*

        - `context`: `VulkContext`
        - `image_type`: Type of image 1D/2D/3D (`VkImageType`)
        - `format`: `VkFormat` of the image
        - `width`: Image width
        - `heigth`: Image height
        - `depth`: Image depth
        - `mip_level`: Level of mip (`int`)
        - `layers`: Number of layers (`int`)
        - `samples`: This `VkSampleCountFlagBits` flag is related
                     to multisampling
        - `sharing_mode`: `VkSharingMode`
        - `queue_families`: List of queue families accessing this image
                            (ignored if sharingMode is not
                            `VK_SHARING_MODE_CONCURRENT`) (can be [])
        - `layout`: `VkImageLayout`
        - `tiling`: `VkImageTiling`
        - `usage`: `VkImageUsageFlags`
        - `memory_properties`: `VkMemoryPropertyFlags` Vulkan constant
        '''
        self.width = width
        self.height = height
        self.depth = depth
        self.format = vk_const(format)
        self.layout = vk_const(layout)
        self.memory_properties = vk_const(memory_properties)

        # Create the VkImage
        vk_extent = vk.VkExtent3D(width=width,
                                  height=height,
                                  depth=depth)

        image_create = vk.VkImageCreateInfo(
            sType=vk.VK_STRUCTURE_TYPE_IMAGE_CREATE_INFO,
            flags=0,
            imageType=vk_const(image_type),
            format=self.format,
            extent=vk_extent,
            mipLevels=mip_level,
            arrayLayers=layers,
            samples=vk_const(samples),
            tiling=vk_const(tiling),
            usage=vk_const(usage),
            sharingMode=vk_const(sharing_mode),
            queueFamilyIndexCount=len(queue_families),
            pQueueFamilyIndices=queue_families if queue_families else None,
            initialLayout=self.layout
        )

        self.image = vk.vkCreateImage(context.device, image_create)

        # Get memory requirements
        requirements = vk.vkGetImageMemoryRequirements(context.device,
                                                       self.image)

        alloc_info = vk.VkMemoryAllocateInfo(
            sType=vk.VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO,
            allocationSize=requirements.size,
            memoryTypeIndex=find_memory_type(
                context,
                requirements.memoryTypeBits,
                self.memory_properties
            )
        )

        self.memory = vk.vkAllocateMemory(context.device, alloc_info)

        # Bind device memory to the image
        vk.vkBindImageMemory(context.device, self.image, self.memory, 0)

    def update_layout(self, commandbuffer, new_layout):
        '''
        Update the image layout.
        Command to update layout are registered in the commandbuffer
        but it's up to you to submit the command buffer to the execution
        queue. You should use buffer specifically created for this function.

        *Parameters:*

        - `commandbuffer`: `CommandBuffer` used to register commands
        - `new_layout`: `VkImageLayout`
        '''
        new_layout = vk_const(new_layout)

        # Set access masks
        if (self.layout == vk.VK_IMAGE_LAYOUT_PREINITIALIZED and
           new_layout == vk.VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL):
            src_mask = vk.VK_ACCESS_HOST_WRITE_BIT
            dst_mask = vk.VK_ACCESS_TRANSFER_READ_BIT
        elif (self.layout == vk.VK_IMAGE_LAYOUT_PREINITIALIZED and
              new_layout == vk.VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL):
            src_mask = vk.VK_ACCESS_HOST_WRITE_BIT
            dst_mask = vk.VK_ACCESS_TRANSFER_WRITE_BIT
        elif (self.layout == vk.VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL and
              new_layout == vk.VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL):
            src_mask = vk.VK_ACCESS_TRANSFER_WRITE_BIT
            dst_mask = vk.VK_ACCESS_SHADER_READ_BIT
        else:
            msg = "Unsupported layout transition"
            logger.error(msg)
            raise VulkError(msg)

        flags = 'VK_COMMAND_BUFFER_USAGE_ONE_TIME_SUBMIT_BIT'
        with commandbuffer.bind(flags) as cmd:
            subresource_range = vk.VkImageSubresourceRange(
                aspectMask=vk.VK_IMAGE_ASPECT_COLOR_BIT,
                baseMipLevel=0,
                levelCount=1,
                baseArrayLayer=0,
                layerCount=1
            )

            barrier = vk.VkImageMemoryBarrier(
                sType=vk.VK_STRUCTURE_TYPE_IMAGE_MEMORY_BARRIER,
                srcAccessMask=src_mask,
                dstAccessMask=dst_mask,
                oldLayout=self.layout,
                newLayout=new_layout,
                srcQueueFamilyIndex=vk.VK_QUEUE_FAMILY_IGNORED,
                dstQueueFamilyIndex=vk.VK_QUEUE_FAMILY_IGNORED,
                image=self.image,
                subresourceRange=subresource_range
            )

            cmd.pipeline_barrier('VK_PIPELINE_STAGE_TOP_OF_PIPE_BIT',
                                 'VK_PIPELINE_STAGE_TOP_OF_PIPE_BIT',
                                 0, 0, 0, [barrier])

        self.layout = new_layout

    def copy_to(self, commandbuffer, dst_image):
        '''
        Copy this image to the destination image.
        Commands to copy are registered in the commandbuffer but it's up to
        you to submit the command buffer to the execution queue.
        You should use buffer specifically created for this function.

        *Parameters:*

        - `commandbuffer`: `CommandBuffer` used to register commands
        - `dst_image`: Destination `Image`

        **Note: Layout of source image should be `TRANSFERT_SRC_OPTIMAL` and
                layout of destination image should be `TRANSFERT_DST_OPTIMAL`**

        **Warning: Format of both images must be compatible**
        '''
        flags = 'VK_COMMAND_BUFFER_USAGE_ONE_TIME_SUBMIT_BIT'
        with commandbuffer.bind(flags) as cmd:
            subresource = vk.VkImageSubresourceLayers(
                aspectMask=vk.VK_IMAGE_ASPECT_COLOR_BIT,
                baseArrayLayer=0,
                mipLevel=0,
                layerCount=1
            )
            extent = vk.VkExtent3D(width=self.width, height=self.height,
                                   depth=self.depth)
            region = vk.VkImageCopy(
                srcSubresource=subresource,
                dstSubresource=subresource,
                srcOffset=vk.VkOffset3D(x=0, y=0, z=0),
                dstOffset=vk.VkOffset3D(x=0, y=0, z=0),
                extent=extent
            )

            cmd.copy_image(self.image, self.layout, dst_image.image,
                           dst_image.layout, [region])

    @contextmanager
    def bind(self, context):
        '''
        Map this image to upload data in it.
        This function is a context manager and must be called with `with`.
        It return a python buffer and let you do what you want with it,
        be careful!

        *Parameters:*

        - `context`: The `VulkContext`

        **Warning: Image memory must be host visible**
        '''
        compatible_memories = {vk.VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT,
                               vk.VK_MEMORY_PROPERTY_HOST_COHERENT_BIT,
                               vk.VK_MEMORY_PROPERTY_HOST_CACHED_BIT}
        if not all([self.memory_properties & m for m in compatible_memories]):
            msg = "Can't map this image, memory must be host visible"
            logger.error(msg)
            raise VulkError(msg)

        format_size = vulkanconstant.VK_FORMAT_SIZE[self.format] / 8
        image_size = (self.width * self.height * self.depth * format_size)

        try:
            data = vk.vkMapMemory(context.device, self.memory, 0,
                                  image_size, 0)
            yield data
        finally:
            vk.vkUnmapMemory(context.device, self.memory)


class HighPerformanceImage():
    '''
    `HighPerformanceImage` allows to use high performance image to be
    sampled in your shaders.

    To get the maximum performance, we are going to create two `Image`,
    a staging image which memory can be updated (with our texture) and
    a final image with very fast memory that we will use in shaders.
    When we create an image, we first upload the pixels in the staging
    image and then copy the memory in the final image. Of course, both of
    the image have the same properties.
    '''

    def __init__(self, context, image_type, format, width, height,
                 depth, mip_level, layers, samples, sharing_mode,
                 queue_families):
        self.staging_image = Image(
            context, image_type, format, width, height, depth, mip_level,
            layers, samples, sharing_mode, queue_families,
            vk.VK_IMAGE_LAYOUT_PREINITIALIZED, vk.VK_IMAGE_TILING_LINEAR,
            vk.VK_IMAGE_USAGE_TRANSFER_SRC_BIT,
            vk.VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | vk.VK_MEMORY_PROPERTY_HOST_COHERENT_BIT # noqa
        )
        self.texture_image = Image(
            context, image_type, format, width, height, depth, mip_level,
            layers, samples, sharing_mode, queue_families,
            vk.VK_IMAGE_LAYOUT_PREINITIALIZED, vk.VK_IMAGE_TILING_OPTIMAL,
            vk.VK_IMAGE_USAGE_TRANSFER_DST_BIT | vk.VK_IMAGE_USAGE_SAMPLED_BIT,
            vk.VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT
        )

    def _finalize(self, context):
        '''
        Prepare and copy the staging image to the final image.

        *Parameters:*

        - `context`: `VulkContext`
        '''
        commandpool = CommandPool(
            context, context.queue_family_indices['graphic'], 0)

        # Transition the staging image to optimal source transfert layout
        with self._manage_commandbuffer(context, commandpool) as cb:
            self.staging_image.update_layout(
                cb, 'VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL')

        # Transition the final image to optimal destination transfert layout
        with self._manage_commandbuffer(context, commandpool) as cb:
            self.texture_image.update_layout(
                cb, 'VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL')

        # Copy staging image into final image
        with self._manage_commandbuffer(context, commandpool) as cb:
            self.staging_image.copy_to(cb, self.texture_image)

        # Set the best layout for the final image
        with self._manage_commandbuffer(context, commandpool) as cb:
            self.texture_image.update_layout(
                cb, 'VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL')

    @contextmanager
    def _manage_commandbuffer(self, context, commandpool):
        '''
        Manage creation and destruction of commandbuffer

        *Parameters:*

        - `context`: `VulkContext`
        - `commandpool`: `CommandPool`
        '''
        try:
            commandbuffers = commandpool.allocate_buffers(
                context, 'VK_COMMAND_BUFFER_LEVEL_PRIMARY', 1)
            yield commandbuffers[0]
        finally:
            submit = vk.VkSubmitInfo(
                sType=vk.VK_STRUCTURE_TYPE_SUBMIT_INFO,
                waitSemaphoreCount=0,
                pWaitSemaphores=None,
                pWaitDstStgeMask=None,
                commandBufferCount=len(commandbuffers),
                pCommandBuffers=commandbuffers,
                signalSemaphoreCount=0,
                pSignalSemaphores=None
            )

            # TODO: submit must be an array (cvulkan bug!)
            vk.vkQueueSubmit(context.graphic_queue, 1, submit, None)
            vk.vkQueueWaitIdle(context.graphic_queue)
            commandpool.free_buffers(context, commandbuffers)

    @contextmanager
    def bind(self, context):
        try:
            with super().bind(context) as b:
                yield b
        finally:
            self._finalize(context)


ImageSubresourceRange = namedtuple('ImageSubresourceRange',
                                   ['aspect', 'base_miplevel', 'level_count',
                                    'base_layer', 'layer_count'])
ImageSubresourceRange.__doc__ = '''
    `ImageSubresourceRange` object describes what the image's purpose is and
    which part of the image should be accessed.

    *Parameters:*

    - `aspect`: `VkImageAspectFlags` indicating which aspect(s) of the
                image are included in the view
    - `base_miplevel`: The first mipmap level accessible to the view
    - `level_count`: Number of mipmap levels (starting from base_miplevel)
                     accessible to the view
    - `base_layer`: First array layer accessible to the view
    - `layer_count`: Number of array layers (starting from base_layer)
                     accessible to the view
    '''


class ImageView():
    '''
    An image view is quite literally a view into an image.
    It describes how to access the image and which part of the image
    to access, for example if it should be treated as a 2D texture depth
    texture without any mipmapping levels.
    '''

    def __init__(self, context, image, view_type, format, subresource_range,
                 swizzle_r='VK_COMPONENT_SWIZZLE_IDENTITY',
                 swizzle_g='VK_COMPONENT_SWIZZLE_IDENTITY',
                 swizzle_b='VK_COMPONENT_SWIZZLE_IDENTITY',
                 swizzle_a='VK_COMPONENT_SWIZZLE_IDENTITY'):
        '''Create ImageView

        *Parameters:*

        - `context`: The `VulkContext`
        - `image`: The `Image` to work on
        - `view_type`: `VkImageViewType` Vulkan constant
        - `format`: `VkFormat` Vulkan constant
        - `subresource_range`: The `ImageSubresourceRange` to use
        - `swizzle_r`: Swizzle of the red color channel
        - `swizzle_g`: Swizzle of the green color channel
        - `swizzle_b`: Swizzle of the blue color channel
        - `swizzle_a`: Swizzle of the alpha color channel
        '''
        components = vk.VkComponentMapping(
            r=vk_const(swizzle_r), g=vk_const(swizzle_g),
            b=vk_const(swizzle_b), a=vk_const(swizzle_a)
        )

        imageview_create = vk.VkImageViewCreateInfo(
            sType=vk.VK_STRUCTURE_TYPE_IMAGE_VIEW_CREATE_INFO,
            flags=0,
            image=image,
            viewType=view_type,
            format=format,
            components=components,
            subresourceRange=subresource_range
        )

        self.imageview = vk.vkCreateImageView(context.device, imageview_create)


class Framebuffer():
    '''
    In Vulkan, a `Framebuffer` references all of the `VkImageView` objects that
    represent the attachments of a `Renderpass`.
    '''

    def __init__(self, context, renderpass, attachments,
                 width, height, layers):
        '''
        *Parameters:*

        - `context`: The `VulkContext`
        - `renderpass`: The compatible `Renderpass` of this `Framebuffer`
        - `attachments`: List of `ImageView`
        - `width`: Width (`int`)
        - `height`: Height (`int`)
        - `layers`: Number of layers (`int`)
        '''
        framebuffer_create = vk.VkFramebufferCreateInfo(
            sType=vk.VK_STRUCTURE_TYPE_FRAMEBUFFER_CREATE_INFO,
            flags=0,
            renderPass=renderpass.renderpass,
            attachmentCount=len(attachments),
            pAttachments=[a.imageview for a in attachments],
            width=width,
            height=height,
            layers=layers
        )

        self.framebuffer = vk.vkCreateFramebuffer(context.device,
                                                  framebuffer_create)


class CommandPool():
    '''
    Command pools manage the memory that is used to store the buffers and
    command buffers are allocated from them.
    '''

    def __init__(self, context, queue_family_index, flags):
        '''
        *Parameters:*

        - `context`: The `VulkContext`
        - `queue_family_index`: Index of the queue family to use
        - `flags`: `VkCommandPoolCreateFlags` Vulkan constant
        '''
        commandpool_create = vk.VkCommandPoolCreateInfo(
            sType=vk.VK_STRUCTURE_TYPE_COMMAND_POOL_CREATE_INFO,
            queueFamilyIndex=queue_family_index,
            flags=vk_const(flags)
        )

        # The Vulkan command pool
        self.commandpool = vk.vkCreateCommandPool(context.device,
                                                  commandpool_create)
        # Command buffers allocated from this pool
        self.commandbuffers = []

    def allocate_buffers(self, context, level, count):
        '''
        Allocate list of `CommandBuffer` from pool.

        *Parameters:*

        - `context`: The `VulkContext`
        - `commandpool`: The source `CommandPool`
        - `level`: `VkCommandBufferLevel` Vulkan constant
        - `count`: Number of buffer to create

        *Returns:*

        `list` of `CommandBuffer`
        '''
        commandbuffers_create = vk.VkCommandBufferAllocateInfo(
            sType=vk.VK_STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO,
            commandPool=self.commandpool,
            level=vk_const(level),
            commandBufferCount=count
        )

        vk_commandbuffers = vk.vkAllocateCommandBuffers(
            context.device,
            commandbuffers_create)

        commandbuffers = [CommandBuffer(cb) for cb in vk_commandbuffers]
        self.commandbuffers.extend(commandbuffers)

        return commandbuffers

    def free_buffers(self, context, buffers):
        '''
        Free list of `CommandBuffer` allocated from this pool.

        *Parameters:*

        - `context`: The `VulkContext`
        - `buffers`: `list` of `CommandBuffer` to free
        '''
        if any([b not in self.commandbuffers for b in buffers]):
            msg = "Can't free a commandbuffer not allocated by this pool"
            logger.error(msg)
            raise VulkError(msg)

        vk.vkFreeCommandBuffers(
            context.device, self.commandpool, len(buffers),
            [b.commandbuffer for b in buffers]
        )


Rect2D = namedtuple('Rect2d', ['offset', 'extent'])
Rect2D.__doc__ = '''
    2D surface with offset.

    *Parameters:*

    - `offset`: `Offset2D` object
    - `extent`: `Extent2D` object
    '''


class CommandBuffer():
    '''
    Commands in Vulkan, like drawing operations and memory transfers, are not
    executed directly using function calls. You have to record all of the
    operations you want to perform in command buffer objects. The advantage of
    this is that all of the hard work of setting up the drawing commands can
    be done in advance and in multiple threads. After that, you just have to
    tell Vulkan to execute the commands in the main loop.

    Commands are executed directly from the `CommandBufferRegister` subclass.
    The naming convention is simple:
    `vkCmd[CommandName]` becomes `command_name`
    '''

    def __init__(self, commandbuffer):
        '''
        This object must be initialized with an existing `VkCommandBuffer`
        because it is generated from `CommandPool`.

        *Parameters:*

        - `commandbuffer`: The `VkCommadBuffer`
        '''
        self.commandbuffer = commandbuffer

    @contextmanager
    def bind(self, flags):
        '''
        Bind this buffer to register command.

        *Parameters:*

        - `flags`: `VkCommandBufferUsageFlags` Vulkan constant

        **Todo: `pInheritanceInfo` must be implemented**
        '''
        commandbuffer_begin_create = vk.VkCommandBufferBeginInfo(
            sType=vk.VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO,
            flags=vk_const(flags),
            pInheritanceInfo=None
        )
        try:
            vk.vkBeginCommandBuffer(
                self.commandbuffer,
                commandbuffer_begin_create)
            yield CommandBuffer.CommandBufferRegister(self.commandbuffer)
        finally:
            vk.vkEndCommandBuffer(self.commandbuffer)

    class CommandBufferRegister():
        '''Allow to call command on command buffer when binding is done'''
        def __init__(self, commandbuffer):
            '''
            *Parameters:*

            - `commandbuffer`: The `VkCommandBuffer`
            '''
            self.commandbuffer = commandbuffer

        def begin_renderpass(self, renderpass, framebuffer, renderarea,
                             clears, contents):
            '''
            Begin a new renderpass

            *Parameters:*

            - `renderpass`: The `RenderPass` to begin an instance of
            - `framebuffer`: The `Framebuffer` containing the attachments that
                             are used with the render pass
            - `renderarea`: `Rect2D` size to render
            - `clears`:  `list` of `ClearValue` for each `Framebuffer`
            - `contents`: `VkSubpassContents` Vulkan constant
            '''
            vk_renderarea = vk.VkRect2D(
                offset=vk.VkOffset2D(
                    x=renderarea.offset.x,
                    y=renderarea.offset.y),
                extent=vk.VkExtent2D(
                    width=renderarea.extent.width,
                    height=renderarea.extent.height)
            )

            renderpass_begin = vk.VkRenderPassBeginInfo(
                sType=vk.VK_STRUCTURE_TYPE_RENDER_PASS_BEGIN_INFO,
                renderPass=renderpass.renderpass,
                framebuffer=framebuffer.framebuffer,
                renderArea=vk_renderarea,
                clearValueCount=len(clears),
                pClearValues=clears
            )

            vk.vkCmdBeginRenderPass(self.commandbuffer, renderpass_begin,
                                    vk_const(contents))

        def bind_pipeline(self, pipeline,
                          bind_point='VK_PIPELINE_BIND_POINT_GRAPHICS'):
            '''
            Bind the pipeline to this `CommandBuffer`.

            *Parameters:*

            - `pipeline`: The `Pipeline` to bind
            - `bind_point`: `VkPipelineBindPoint` Vulkan constant
                            (default to graphic)
            '''
            vk.vkCmdBindPipeline(self.commandbuffer, vk_const(bind_point),
                                 pipeline)

        def draw(self, vertex_count, first_vertex,
                 instance_count=1, first_instance=0):
            '''
            Draw the vertice buffer.

            When the command is executed, primitives are assembled using the
            current primitive topology and vertexCount consecutive vertex
            indices with the first vertexIndex value equal to firstVertex.
            The primitives are drawn instanceCount times with instanceIndex
            starting with firstInstance and increasing sequentially for each
            instance. The assembled primitives execute the currently bound
            graphics pipeline.

            *Parameters:*

            - `vertex_count`: Number of vertices to draw
            - `first_vertex`: Index of the first vertex to draw
            - `instance_count`: Number of instance to draw (default: 1)
            - `first_instance`: First instance to draw (default: 0)
            '''
            vk.vkCmdDraw(self.commandbuffer, vertex_count, instance_count,
                         first_vertex, first_instance)

        def pipeline_barrier(self, src_stage, dst_stage, dependency, memories,
                             buffers, images):
            '''
            Insert a memory dependency

            *Parameters:*

            - `src_stage`: `VkPipelineStageFlags` Vulkan constant
            - `dst_stage`: `VkPipelineStageFlags` Vulkan constant
            - `dependency`: `VkDependencyFlags` Vulkan constant
            - `memories`: `list` of `VkMemoryBarrier` Vulkan objects
            - `buffers`: `list` of `VkBufferMemoryBarrier` Vulkan objects
            - `images`: `list` of `VkImageMemoryBarrier` Vulkan objects
            '''
            vk_memories = memories if memories else None
            vk_buffers = buffers if buffers else None
            vk_images = images if images else None
            vk.vkCmdPipelineBarrier(
                self.commandbuffer, vk_const(src_stage), vk_const(dst_stage),
                vk_const(dependency), len(memories), vk_memories,
                len(buffers), vk_buffers, len(images), vk_images
            )

        def copy_image(self, src_image, src_layout, dst_image,
                       dst_layout, regions):
            '''
            Copy data between images

            *Parameters:*

            - `src_image`: `VkImage`
            - `src_layout`: `VkImageLayout`
            - `dst_image`: `VkImage`
            - `dst_layout`: `VkImageLayout`
            - `regions`: `list` of `VkImageCopy`

            **Note: `VkImage` is raw Vulkan object, not vulk `Image`**
            '''
            vk.vkCmdCopyImage(
                self.commandbuffer, src_image, vk_const(src_layout), dst_image,
                vk_const(dst_layout), len(regions), regions
            )

        def end_renderpass(self):
            '''End the current render pass'''
            vk.vkCmdEndRenderPass(self.commandbuffer)


class Semaphore():
    '''
    Semaphores are a synchronization primitive that can be used to insert a
    dependency between batches submitted to queues. Semaphores have two
    states - signaled and unsignaled. The state of a semaphore can be signaled
    after execution of a batch of commands is completed. A batch can wait for
    a semaphore to become signaled before it begins execution, and the
    semaphore is also unsignaled before the batch begins execution.
    '''

    def __init__(self, context):
        '''
        *Parameters:*

        - `context`: `VulkContext`
        '''
        semaphore_create = vk.VkSemaphoreCreateInfo(
            sType=vk.VK_STRUCTURE_TYPE_SEMAPHORE_CREATE_INFO,
            flags=0
        )

        self.semaphore = vk.vkCreateSemaphore(context.device, semaphore_create)
