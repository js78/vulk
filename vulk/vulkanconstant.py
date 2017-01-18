'''
This module contains useful mapping or constants.

Vulkan enum are translated to Python enum.
There are two types of enumeration, `IntEnum` and `IntFlag`.
`IntEnum` are classic enumeration whereas `IntFlag` are different.
`IntFlag` allows to realize bitwise operation and corresponds to
the Vulkan enumeration that ends by '_BIT'. All enumerations have a
specific field `NONE` which is equals to 0.
'''
from enum import Enum, IntEnum, IntFlag, auto
import numpy as np
import vulkan as vk  # pylint: disable=import-error


# ----------
# CONSTANTS
# ----------
SUBPASS_EXTERNAL = vk.VK_SUBPASS_EXTERNAL
QUEUE_FAMILY_IGNORED = vk.VK_QUEUE_FAMILY_IGNORED


# ----------
# ENUMS
# ----------
class Access(IntFlag):
    NONE = 0
    INDIRECT_COMMAND_READ = vk.VK_ACCESS_INDIRECT_COMMAND_READ_BIT
    INDEX_READ = vk.VK_ACCESS_INDEX_READ_BIT
    VERTEX_ATTRIBUTE_READ = vk.VK_ACCESS_VERTEX_ATTRIBUTE_READ_BIT
    UNIFORM_READ = vk.VK_ACCESS_UNIFORM_READ_BIT
    INPUT_ATTACHMENT_READ = vk.VK_ACCESS_INPUT_ATTACHMENT_READ_BIT
    SHADER_READ = vk.VK_ACCESS_SHADER_READ_BIT
    SHADER_WRITE = vk.VK_ACCESS_SHADER_WRITE_BIT
    COLOR_ATTACHMENT_READ = vk.VK_ACCESS_COLOR_ATTACHMENT_READ_BIT
    COLOR_ATTACHMENT_WRITE = vk.VK_ACCESS_COLOR_ATTACHMENT_WRITE_BIT
    DEPTH_STENCIL_ATTACHMENT_READ = vk.VK_ACCESS_DEPTH_STENCIL_ATTACHMENT_READ_BIT # noqa
    DEPTH_STENCIL_ATTACHMENT_WRITE = vk.VK_ACCESS_DEPTH_STENCIL_ATTACHMENT_WRITE_BIT # noqa
    TRANSFER_READ = vk.VK_ACCESS_TRANSFER_READ_BIT
    TRANSFER_WRITE = vk.VK_ACCESS_TRANSFER_WRITE_BIT
    HOST_READ = vk.VK_ACCESS_HOST_READ_BIT
    HOST_WRITE = vk.VK_ACCESS_HOST_WRITE_BIT
    MEMORY_READ = vk.VK_ACCESS_MEMORY_READ_BIT
    MEMORY_WRITE = vk.VK_ACCESS_MEMORY_WRITE_BIT


class AttachmentLoadOp(IntEnum):
    NONE = 0
    LOAD = vk.VK_ATTACHMENT_LOAD_OP_LOAD
    CLEAR = vk.VK_ATTACHMENT_LOAD_OP_CLEAR
    DONT_CARE = vk.VK_ATTACHMENT_LOAD_OP_DONT_CARE


class AttachmentStoreOp(IntEnum):
    NONE = 0
    STORE = vk.VK_ATTACHMENT_STORE_OP_STORE
    DONT_CARE = vk.VK_ATTACHMENT_STORE_OP_DONT_CARE


class BlendFactor(IntEnum):
    NONE = 0
    ZERO = vk.VK_BLEND_FACTOR_ZERO
    ONE = vk.VK_BLEND_FACTOR_ONE
    SRC_COLOR = vk.VK_BLEND_FACTOR_SRC_COLOR
    ONE_MINUS_SRC_COLOR = vk.VK_BLEND_FACTOR_ONE_MINUS_SRC_COLOR
    DST_COLOR = vk.VK_BLEND_FACTOR_DST_COLOR
    ONE_MINUS_DST_COLOR = vk.VK_BLEND_FACTOR_ONE_MINUS_DST_COLOR
    SRC_ALPHA = vk.VK_BLEND_FACTOR_SRC_ALPHA
    ONE_MINUS_SRC_ALPHA = vk.VK_BLEND_FACTOR_ONE_MINUS_SRC_ALPHA
    DST_ALPHA = vk.VK_BLEND_FACTOR_DST_ALPHA
    ONE_MINUS_DST_ALPHA = vk.VK_BLEND_FACTOR_ONE_MINUS_DST_ALPHA
    CONSTANT_COLOR = vk.VK_BLEND_FACTOR_CONSTANT_COLOR
    ONE_MINUS_CONSTANT_COLOR = vk.VK_BLEND_FACTOR_ONE_MINUS_CONSTANT_COLOR
    CONSTANT_ALPHA = vk.VK_BLEND_FACTOR_CONSTANT_ALPHA
    ONE_MINUS_CONSTANT_ALPHA = vk.VK_BLEND_FACTOR_ONE_MINUS_CONSTANT_ALPHA
    SRC_ALPHA_SATURATE = vk.VK_BLEND_FACTOR_SRC_ALPHA_SATURATE
    SRC1_COLOR = vk.VK_BLEND_FACTOR_SRC1_COLOR
    ONE_MINUS_SRC1_COLOR = vk.VK_BLEND_FACTOR_ONE_MINUS_SRC1_COLOR
    SRC1_ALPHA = vk.VK_BLEND_FACTOR_SRC1_ALPHA
    ONE_MINUS_SRC1_ALPHA = vk.VK_BLEND_FACTOR_ONE_MINUS_SRC1_ALPHA


class BlendOp(IntEnum):
    NONE = 0
    ADD = vk.VK_BLEND_OP_ADD
    SUBSTRACT = vk.VK_BLEND_OP_SUBTRACT
    REVERSE_SUBSTRACT = vk.VK_BLEND_OP_REVERSE_SUBTRACT
    MIN = vk.VK_BLEND_OP_MIN
    MAX = vk.VK_BLEND_OP_MAX


class BorderColor(IntEnum):
    NONE = 0
    FLOAT_TRANSPARENT_BLACK = vk.VK_BORDER_COLOR_FLOAT_TRANSPARENT_BLACK
    INT_TRANSPARENT_BLACK = vk.VK_BORDER_COLOR_INT_TRANSPARENT_BLACK
    FLOAT_OPAQUE_BLACK = vk.VK_BORDER_COLOR_FLOAT_OPAQUE_BLACK
    INT_OPAQUE_BLACK = vk.VK_BORDER_COLOR_INT_OPAQUE_BLACK
    FLOAT_OPAQUE_WHITE = vk.VK_BORDER_COLOR_FLOAT_OPAQUE_WHITE
    INT_OPAQUE_WHITE = vk.VK_BORDER_COLOR_INT_OPAQUE_WHITE


class BufferCreate(IntFlag):
    NONE = 0
    SPARSE_BINDING = vk.VK_BUFFER_CREATE_SPARSE_BINDING_BIT
    SPARSE_RESIDENCY = vk.VK_BUFFER_CREATE_SPARSE_RESIDENCY_BIT
    SPARSE_ALIASED = vk.VK_BUFFER_CREATE_SPARSE_ALIASED_BIT


class BufferUsage(IntFlag):
    NONE = 0
    TRANSFER_SRC = vk.VK_BUFFER_USAGE_TRANSFER_SRC_BIT
    TRANSFER_DST = vk.VK_BUFFER_USAGE_TRANSFER_DST_BIT
    UNIFORM_TEXEL_BUFFER = vk.VK_BUFFER_USAGE_UNIFORM_TEXEL_BUFFER_BIT
    STORAGE_TEXEL_BUFFER = vk.VK_BUFFER_USAGE_STORAGE_TEXEL_BUFFER_BIT
    UNIFORM_BUFFER = vk.VK_BUFFER_USAGE_UNIFORM_BUFFER_BIT
    STORAGE_BUFFER = vk.VK_BUFFER_USAGE_STORAGE_BUFFER_BIT
    INDEX_BUFFER = vk.VK_BUFFER_USAGE_INDEX_BUFFER_BIT
    VERTEX_BUFFER = vk.VK_BUFFER_USAGE_VERTEX_BUFFER_BIT
    INDIRECT_BUFFER = vk.VK_BUFFER_USAGE_INDIRECT_BUFFER_BIT


class ColorComponent(IntFlag):
    NONE = 0
    R = vk.VK_COLOR_COMPONENT_R_BIT
    G = vk.VK_COLOR_COMPONENT_G_BIT
    B = vk.VK_COLOR_COMPONENT_B_BIT
    A = vk.VK_COLOR_COMPONENT_A_BIT


class CommandBufferLevel(IntEnum):
    NONE = 0
    PRIMARY = vk.VK_COMMAND_BUFFER_LEVEL_PRIMARY
    SCONDARY = vk.VK_COMMAND_BUFFER_LEVEL_SECONDARY


class CommandBufferReset(IntFlag):
    NONE = 0
    RELEASE_RESOURCES = vk.VK_COMMAND_BUFFER_RESET_RELEASE_RESOURCES_BIT


class CommandBufferUsage(IntFlag):
    NONE = 0
    ONE_TIME_SUBMIT = vk.VK_COMMAND_BUFFER_USAGE_ONE_TIME_SUBMIT_BIT
    RENDER_PASS_CONTINUE = vk.VK_COMMAND_BUFFER_USAGE_RENDER_PASS_CONTINUE_BIT
    SIMULTANEOUS_USE = vk.VK_COMMAND_BUFFER_USAGE_SIMULTANEOUS_USE_BIT


class CommandPoolCreate(IntFlag):
    NONE = 0
    TRANSIENT = vk.VK_COMMAND_POOL_CREATE_TRANSIENT_BIT
    RESET_COMMAND_BUFFER = vk.VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT


class CompareOp(IntEnum):
    NONE = 0
    NEVER = vk.VK_COMPARE_OP_NEVER
    LESS = vk.VK_COMPARE_OP_LESS
    EQUAL = vk.VK_COMPARE_OP_EQUAL
    LESS_OR_EQUAL = vk.VK_COMPARE_OP_LESS_OR_EQUAL
    GREATER = vk.VK_COMPARE_OP_GREATER
    NOT_EQUAL = vk.VK_COMPARE_OP_NOT_EQUAL
    GREATER_OR_EQUAL = vk.VK_COMPARE_OP_GREATER_OR_EQUAL
    ALWAYS = vk.VK_COMPARE_OP_ALWAYS


class ComponentSwizzle(IntEnum):
    NONE = 0
    IDENTITY = vk.VK_COMPONENT_SWIZZLE_IDENTITY
    ZERO = vk.VK_COMPONENT_SWIZZLE_ZERO
    ONE = vk.VK_COMPONENT_SWIZZLE_ONE
    R = vk.VK_COMPONENT_SWIZZLE_R
    G = vk.VK_COMPONENT_SWIZZLE_G
    B = vk.VK_COMPONENT_SWIZZLE_B
    A = vk.VK_COMPONENT_SWIZZLE_A


class CullMode(IntFlag):
    NONE = vk.VK_CULL_MODE_NONE
    FRONT = vk.VK_CULL_MODE_FRONT_BIT
    BACK = vk.VK_CULL_MODE_BACK_BIT
    FRONT_AND_BACK = vk.VK_CULL_MODE_FRONT_AND_BACK


class DataType(IntEnum):
    UINT8 = auto()
    SINT8 = auto()
    UINT16 = auto()
    SINT16 = auto()
    UINT32 = auto()
    SINT32 = auto()
    SFLOAT16 = auto()
    SFLOAT32 = auto()
    UNORM8 = auto()
    SNORM8 = auto()
    UNORM16 = auto()
    SNORM16 = auto()
    UNORM32 = auto()
    SNORM32 = auto()


class Dependency(IntFlag):
    NONE = 0
    BY_REGION = vk.VK_DEPENDENCY_BY_REGION_BIT


class DescriptorPoolCreate(IntFlag):
    NONE = 0
    FREE_DESCRIPTOR_SET = vk.VK_DESCRIPTOR_POOL_CREATE_FREE_DESCRIPTOR_SET_BIT


class DescriptorType(IntEnum):
    NONE = 0
    SAMPLER = vk.VK_DESCRIPTOR_TYPE_SAMPLER
    COMBINED_IMAGE_SAMPLER = vk.VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER
    SAMPLED_IMAGE = vk.VK_DESCRIPTOR_TYPE_SAMPLED_IMAGE
    STORAGE_IMAGE = vk.VK_DESCRIPTOR_TYPE_STORAGE_IMAGE
    UNIFORM_TEXEL_BUFFER = vk.VK_DESCRIPTOR_TYPE_UNIFORM_TEXEL_BUFFER
    STORAGE_TEXEL_BUFFER = vk.VK_DESCRIPTOR_TYPE_STORAGE_TEXEL_BUFFER
    UNIFORM_BUFFER = vk.VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER
    STORAGE_BUFFER = vk.VK_DESCRIPTOR_TYPE_STORAGE_BUFFER
    UNIFORM_BUFFER_DYNAMIC = vk.VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER_DYNAMIC
    STORAGE_BUFFER_DYNAMIC = vk.VK_DESCRIPTOR_TYPE_STORAGE_BUFFER_DYNAMIC
    INPUT_ATTACHMENT = vk.VK_DESCRIPTOR_TYPE_INPUT_ATTACHMENT


class Filter(IntEnum):
    NONE = 0
    NEAREST = vk.VK_FILTER_NEAREST
    LINEAR = vk.VK_FILTER_LINEAR


class Format(IntEnum):
    NONE = 0
    UNDEFINED = vk.VK_FORMAT_UNDEFINED
    R4G4_UNORM_PACK8 = vk.VK_FORMAT_R4G4_UNORM_PACK8
    R4G4B4A4_UNORM_PACK16 = vk.VK_FORMAT_R4G4B4A4_UNORM_PACK16
    B4G4R4A4_UNORM_PACK16 = vk.VK_FORMAT_B4G4R4A4_UNORM_PACK16
    R5G6B5_UNORM_PACK16 = vk.VK_FORMAT_R5G6B5_UNORM_PACK16
    B5G6R5_UNORM_PACK16 = vk.VK_FORMAT_B5G6R5_UNORM_PACK16
    R5G5B5A1_UNORM_PACK16 = vk.VK_FORMAT_R5G5B5A1_UNORM_PACK16
    B5G5R5A1_UNORM_PACK16 = vk.VK_FORMAT_B5G5R5A1_UNORM_PACK16
    A1R5G5B5_UNORM_PACK16 = vk.VK_FORMAT_A1R5G5B5_UNORM_PACK16
    R8_UNORM = vk.VK_FORMAT_R8_UNORM
    R8_SNORM = vk.VK_FORMAT_R8_SNORM
    R8_USCALED = vk.VK_FORMAT_R8_USCALED
    R8_SSCALED = vk.VK_FORMAT_R8_SSCALED
    R8_UINT = vk.VK_FORMAT_R8_UINT
    R8_SINT = vk.VK_FORMAT_R8_SINT
    R8_SRGB = vk.VK_FORMAT_R8_SRGB
    R8G8_UNORM = vk.VK_FORMAT_R8G8_UNORM
    R8G8_SNORM = vk.VK_FORMAT_R8G8_SNORM
    R8G8_USCALED = vk.VK_FORMAT_R8G8_USCALED
    R8G8_SSCALED = vk.VK_FORMAT_R8G8_SSCALED
    R8G8_UINT = vk.VK_FORMAT_R8G8_UINT
    R8G8_SINT = vk.VK_FORMAT_R8G8_SINT
    R8G8_SRGB = vk.VK_FORMAT_R8G8_SRGB
    R8G8B8_UNORM = vk.VK_FORMAT_R8G8B8_UNORM
    R8G8B8_SNORM = vk.VK_FORMAT_R8G8B8_SNORM
    R8G8B8_USCALED = vk.VK_FORMAT_R8G8B8_USCALED
    R8G8B8_SSCALED = vk.VK_FORMAT_R8G8B8_SSCALED
    R8G8B8_UINT = vk.VK_FORMAT_R8G8B8_UINT
    R8G8B8_SINT = vk.VK_FORMAT_R8G8B8_SINT
    R8G8B8_SRGB = vk.VK_FORMAT_R8G8B8_SRGB
    B8G8R8_UNORM = vk.VK_FORMAT_B8G8R8_UNORM
    B8G8R8_SNORM = vk.VK_FORMAT_B8G8R8_SNORM
    B8G8R8_USCALED = vk.VK_FORMAT_B8G8R8_USCALED
    B8G8R8_SSCALED = vk.VK_FORMAT_B8G8R8_SSCALED
    B8G8R8_UINT = vk.VK_FORMAT_B8G8R8_UINT
    B8G8R8_SINT = vk.VK_FORMAT_B8G8R8_SINT
    B8G8R8_SRGB = vk.VK_FORMAT_B8G8R8_SRGB
    R8G8B8A8_UNORM = vk.VK_FORMAT_R8G8B8A8_UNORM
    R8G8B8A8_SNORM = vk.VK_FORMAT_R8G8B8A8_SNORM
    R8G8B8A8_USCALED = vk.VK_FORMAT_R8G8B8A8_USCALED
    R8G8B8A8_SSCALED = vk.VK_FORMAT_R8G8B8A8_SSCALED
    R8G8B8A8_UINT = vk.VK_FORMAT_R8G8B8A8_UINT
    R8G8B8A8_SINT = vk.VK_FORMAT_R8G8B8A8_SINT
    R8G8B8A8_SRGB = vk.VK_FORMAT_R8G8B8A8_SRGB
    B8G8R8A8_UNORM = vk.VK_FORMAT_B8G8R8A8_UNORM
    B8G8R8A8_SNORM = vk.VK_FORMAT_B8G8R8A8_SNORM
    B8G8R8A8_USCALED = vk.VK_FORMAT_B8G8R8A8_USCALED
    B8G8R8A8_SSCALED = vk.VK_FORMAT_B8G8R8A8_SSCALED
    B8G8R8A8_UINT = vk.VK_FORMAT_B8G8R8A8_UINT
    B8G8R8A8_SINT = vk.VK_FORMAT_B8G8R8A8_SINT
    B8G8R8A8_SRGB = vk.VK_FORMAT_B8G8R8A8_SRGB
    A8B8G8R8_UNORM_PACK32 = vk.VK_FORMAT_A8B8G8R8_UNORM_PACK32
    A8B8G8R8_SNORM_PACK32 = vk.VK_FORMAT_A8B8G8R8_SNORM_PACK32
    A8B8G8R8_USCALED_PACK32 = vk.VK_FORMAT_A8B8G8R8_USCALED_PACK32
    A8B8G8R8_SSCALED_PACK32 = vk.VK_FORMAT_A8B8G8R8_SSCALED_PACK32
    A8B8G8R8_UINT_PACK32 = vk.VK_FORMAT_A8B8G8R8_UINT_PACK32
    A8B8G8R8_SINT_PACK32 = vk.VK_FORMAT_A8B8G8R8_SINT_PACK32
    A8B8G8R8_SRGB_PACK32 = vk.VK_FORMAT_A8B8G8R8_SRGB_PACK32
    A2R10G10B10_UNORM_PACK32 = vk.VK_FORMAT_A2R10G10B10_UNORM_PACK32
    A2R10G10B10_SNORM_PACK32 = vk.VK_FORMAT_A2R10G10B10_SNORM_PACK32
    A2R10G10B10_USCALED_PACK32 = vk.VK_FORMAT_A2R10G10B10_USCALED_PACK32
    A2R10G10B10_SSCALED_PACK32 = vk.VK_FORMAT_A2R10G10B10_SSCALED_PACK32
    A2R10G10B10_UINT_PACK32 = vk.VK_FORMAT_A2R10G10B10_UINT_PACK32
    A2R10G10B10_SINT_PACK32 = vk.VK_FORMAT_A2R10G10B10_SINT_PACK32
    A2B10G10R10_UNORM_PACK32 = vk.VK_FORMAT_A2B10G10R10_UNORM_PACK32
    A2B10G10R10_SNORM_PACK32 = vk.VK_FORMAT_A2B10G10R10_SNORM_PACK32
    A2B10G10R10_USCALED_PACK32 = vk.VK_FORMAT_A2B10G10R10_USCALED_PACK32
    A2B10G10R10_SSCALED_PACK32 = vk.VK_FORMAT_A2B10G10R10_SSCALED_PACK32
    A2B10G10R10_UINT_PACK32 = vk.VK_FORMAT_A2B10G10R10_UINT_PACK32
    A2B10G10R10_SINT_PACK32 = vk.VK_FORMAT_A2B10G10R10_SINT_PACK32
    R16_UNORM = vk.VK_FORMAT_R16_UNORM
    R16_SNORM = vk.VK_FORMAT_R16_SNORM
    R16_USCALED = vk.VK_FORMAT_R16_USCALED
    R16_SSCALED = vk.VK_FORMAT_R16_SSCALED
    R16_UINT = vk.VK_FORMAT_R16_UINT
    R16_SINT = vk.VK_FORMAT_R16_SINT
    R16_SFLOAT = vk.VK_FORMAT_R16_SFLOAT
    R16G16_UNORM = vk.VK_FORMAT_R16G16_UNORM
    R16G16_SNORM = vk.VK_FORMAT_R16G16_SNORM
    R16G16_USCALED = vk.VK_FORMAT_R16G16_USCALED
    R16G16_SSCALED = vk.VK_FORMAT_R16G16_SSCALED
    R16G16_UINT = vk.VK_FORMAT_R16G16_UINT
    R16G16_SINT = vk.VK_FORMAT_R16G16_SINT
    R16G16_SFLOAT = vk.VK_FORMAT_R16G16_SFLOAT
    R16G16B16_UNORM = vk.VK_FORMAT_R16G16B16_UNORM
    R16G16B16_SNORM = vk.VK_FORMAT_R16G16B16_SNORM
    R16G16B16_USCALED = vk.VK_FORMAT_R16G16B16_USCALED
    R16G16B16_SSCALED = vk.VK_FORMAT_R16G16B16_SSCALED
    R16G16B16_UINT = vk.VK_FORMAT_R16G16B16_UINT
    R16G16B16_SINT = vk.VK_FORMAT_R16G16B16_SINT
    R16G16B16_SFLOAT = vk.VK_FORMAT_R16G16B16_SFLOAT
    R16G16B16A16_UNORM = vk.VK_FORMAT_R16G16B16A16_UNORM
    R16G16B16A16_SNORM = vk.VK_FORMAT_R16G16B16A16_SNORM
    R16G16B16A16_USCALED = vk.VK_FORMAT_R16G16B16A16_USCALED
    R16G16B16A16_SSCALED = vk.VK_FORMAT_R16G16B16A16_SSCALED
    R16G16B16A16_UINT = vk.VK_FORMAT_R16G16B16A16_UINT
    R16G16B16A16_SINT = vk.VK_FORMAT_R16G16B16A16_SINT
    R16G16B16A16_SFLOAT = vk.VK_FORMAT_R16G16B16A16_SFLOAT
    R32_UINT = vk.VK_FORMAT_R32_UINT
    R32_SINT = vk.VK_FORMAT_R32_SINT
    R32_SFLOAT = vk.VK_FORMAT_R32_SFLOAT
    R32G32_UINT = vk.VK_FORMAT_R32G32_UINT
    R32G32_SINT = vk.VK_FORMAT_R32G32_SINT
    R32G32_SFLOAT = vk.VK_FORMAT_R32G32_SFLOAT
    R32G32B32_UINT = vk.VK_FORMAT_R32G32B32_UINT
    R32G32B32_SINT = vk.VK_FORMAT_R32G32B32_SINT
    R32G32B32_SFLOAT = vk.VK_FORMAT_R32G32B32_SFLOAT
    R32G32B32A32_UINT = vk.VK_FORMAT_R32G32B32A32_UINT
    R32G32B32A32_SINT = vk.VK_FORMAT_R32G32B32A32_SINT
    R32G32B32A32_SFLOAT = vk.VK_FORMAT_R32G32B32A32_SFLOAT
    R64_UINT = vk.VK_FORMAT_R64_UINT
    R64_SINT = vk.VK_FORMAT_R64_SINT
    R64_SFLOAT = vk.VK_FORMAT_R64_SFLOAT
    R64G64_UINT = vk.VK_FORMAT_R64G64_UINT
    R64G64_SINT = vk.VK_FORMAT_R64G64_SINT
    R64G64_SFLOAT = vk.VK_FORMAT_R64G64_SFLOAT
    R64G64B64_UINT = vk.VK_FORMAT_R64G64B64_UINT
    R64G64B64_SINT = vk.VK_FORMAT_R64G64B64_SINT
    R64G64B64_SFLOAT = vk.VK_FORMAT_R64G64B64_SFLOAT
    R64G64B64A64_UINT = vk.VK_FORMAT_R64G64B64A64_UINT
    R64G64B64A64_SINT = vk.VK_FORMAT_R64G64B64A64_SINT
    R64G64B64A64_SFLOAT = vk.VK_FORMAT_R64G64B64A64_SFLOAT
    B10G11R11_UFLOAT_PACK32 = vk.VK_FORMAT_B10G11R11_UFLOAT_PACK32
    E5B9G9R9_UFLOAT_PACK32 = vk.VK_FORMAT_E5B9G9R9_UFLOAT_PACK32
    D16_UNORM = vk.VK_FORMAT_D16_UNORM
    X8_D24_UNORM_PACK32 = vk.VK_FORMAT_X8_D24_UNORM_PACK32
    D32_SFLOAT = vk.VK_FORMAT_D32_SFLOAT
    S8_UINT = vk.VK_FORMAT_S8_UINT
    D16_UNORM_S8_UINT = vk.VK_FORMAT_D16_UNORM_S8_UINT
    D24_UNORM_S8_UINT = vk.VK_FORMAT_D24_UNORM_S8_UINT
    D32_SFLOAT_S8_UINT = vk.VK_FORMAT_D32_SFLOAT_S8_UINT
    BC1_RGB_UNORM_BLOCK = vk.VK_FORMAT_BC1_RGB_UNORM_BLOCK
    BC1_RGB_SRGB_BLOCK = vk.VK_FORMAT_BC1_RGB_SRGB_BLOCK
    BC1_RGBA_UNORM_BLOCK = vk.VK_FORMAT_BC1_RGBA_UNORM_BLOCK
    BC1_RGBA_SRGB_BLOCK = vk.VK_FORMAT_BC1_RGBA_SRGB_BLOCK
    BC2_UNORM_BLOCK = vk.VK_FORMAT_BC2_UNORM_BLOCK
    BC2_SRGB_BLOCK = vk.VK_FORMAT_BC2_SRGB_BLOCK
    BC3_UNORM_BLOCK = vk.VK_FORMAT_BC3_UNORM_BLOCK
    BC3_SRGB_BLOCK = vk.VK_FORMAT_BC3_SRGB_BLOCK
    BC4_UNORM_BLOCK = vk.VK_FORMAT_BC4_UNORM_BLOCK
    BC4_SNORM_BLOCK = vk.VK_FORMAT_BC4_SNORM_BLOCK
    BC5_UNORM_BLOCK = vk.VK_FORMAT_BC5_UNORM_BLOCK
    BC5_SNORM_BLOCK = vk.VK_FORMAT_BC5_SNORM_BLOCK
    BC6H_UFLOAT_BLOCK = vk.VK_FORMAT_BC6H_UFLOAT_BLOCK
    BC6H_SFLOAT_BLOCK = vk.VK_FORMAT_BC6H_SFLOAT_BLOCK
    BC7_UNORM_BLOCK = vk.VK_FORMAT_BC7_UNORM_BLOCK
    BC7_SRGB_BLOCK = vk.VK_FORMAT_BC7_SRGB_BLOCK
    ETC2_R8G8B8_UNORM_BLOCK = vk.VK_FORMAT_ETC2_R8G8B8_UNORM_BLOCK
    ETC2_R8G8B8_SRGB_BLOCK = vk.VK_FORMAT_ETC2_R8G8B8_SRGB_BLOCK
    ETC2_R8G8B8A1_UNORM_BLOCK = vk.VK_FORMAT_ETC2_R8G8B8A1_UNORM_BLOCK
    ETC2_R8G8B8A1_SRGB_BLOCK = vk.VK_FORMAT_ETC2_R8G8B8A1_SRGB_BLOCK
    ETC2_R8G8B8A8_UNORM_BLOCK = vk.VK_FORMAT_ETC2_R8G8B8A8_UNORM_BLOCK
    ETC2_R8G8B8A8_SRGB_BLOCK = vk.VK_FORMAT_ETC2_R8G8B8A8_SRGB_BLOCK
    EAC_R11_UNORM_BLOCK = vk.VK_FORMAT_EAC_R11_UNORM_BLOCK
    EAC_R11_SNORM_BLOCK = vk.VK_FORMAT_EAC_R11_SNORM_BLOCK
    EAC_R11G11_UNORM_BLOCK = vk.VK_FORMAT_EAC_R11G11_UNORM_BLOCK
    EAC_R11G11_SNORM_BLOCK = vk.VK_FORMAT_EAC_R11G11_SNORM_BLOCK
    ASTC_4x4_UNORM_BLOCK = vk.VK_FORMAT_ASTC_4x4_UNORM_BLOCK
    ASTC_4x4_SRGB_BLOCK = vk.VK_FORMAT_ASTC_4x4_SRGB_BLOCK
    ASTC_5x4_UNORM_BLOCK = vk.VK_FORMAT_ASTC_5x4_UNORM_BLOCK
    ASTC_5x4_SRGB_BLOCK = vk.VK_FORMAT_ASTC_5x4_SRGB_BLOCK
    ASTC_5x5_UNORM_BLOCK = vk.VK_FORMAT_ASTC_5x5_UNORM_BLOCK
    ASTC_5x5_SRGB_BLOCK = vk.VK_FORMAT_ASTC_5x5_SRGB_BLOCK
    ASTC_6x5_UNORM_BLOCK = vk.VK_FORMAT_ASTC_6x5_UNORM_BLOCK
    ASTC_6x5_SRGB_BLOCK = vk.VK_FORMAT_ASTC_6x5_SRGB_BLOCK
    ASTC_6x6_UNORM_BLOCK = vk.VK_FORMAT_ASTC_6x6_UNORM_BLOCK
    ASTC_6x6_SRGB_BLOCK = vk.VK_FORMAT_ASTC_6x6_SRGB_BLOCK
    ASTC_8x5_UNORM_BLOCK = vk.VK_FORMAT_ASTC_8x5_UNORM_BLOCK
    ASTC_8x5_SRGB_BLOCK = vk.VK_FORMAT_ASTC_8x5_SRGB_BLOCK
    ASTC_8x6_UNORM_BLOCK = vk.VK_FORMAT_ASTC_8x6_UNORM_BLOCK
    ASTC_8x6_SRGB_BLOCK = vk.VK_FORMAT_ASTC_8x6_SRGB_BLOCK
    ASTC_8x8_UNORM_BLOCK = vk.VK_FORMAT_ASTC_8x8_UNORM_BLOCK
    ASTC_8x8_SRGB_BLOCK = vk.VK_FORMAT_ASTC_8x8_SRGB_BLOCK
    ASTC_10x5_UNORM_BLOCK = vk.VK_FORMAT_ASTC_10x5_UNORM_BLOCK
    ASTC_10x5_SRGB_BLOCK = vk.VK_FORMAT_ASTC_10x5_SRGB_BLOCK
    ASTC_10x6_UNORM_BLOCK = vk.VK_FORMAT_ASTC_10x6_UNORM_BLOCK
    ASTC_10x6_SRGB_BLOCK = vk.VK_FORMAT_ASTC_10x6_SRGB_BLOCK
    ASTC_10x8_UNORM_BLOCK = vk.VK_FORMAT_ASTC_10x8_UNORM_BLOCK
    ASTC_10x8_SRGB_BLOCK = vk.VK_FORMAT_ASTC_10x8_SRGB_BLOCK
    ASTC_10x10_UNORM_BLOCK = vk.VK_FORMAT_ASTC_10x10_UNORM_BLOCK
    ASTC_10x10_SRGB_BLOCK = vk.VK_FORMAT_ASTC_10x10_SRGB_BLOCK
    ASTC_12x10_UNORM_BLOCK = vk.VK_FORMAT_ASTC_12x10_UNORM_BLOCK
    ASTC_12x10_SRGB_BLOCK = vk.VK_FORMAT_ASTC_12x10_SRGB_BLOCK
    ASTC_12x12_UNORM_BLOCK = vk.VK_FORMAT_ASTC_12x12_UNORM_BLOCK
    ASTC_12x12_SRGB_BLOCK = vk.VK_FORMAT_ASTC_12x12_SRGB_BLOCK


class FormatType(Enum):
    '''Mapping between `Format` and `(DataType, num_components)`'''
    R8_UNORM = (DataType.UNORM8, 1)
    R8_SNORM = (DataType.SNORM8, 1)
    R8_UINT = (DataType.UINT8, 1)
    R8_SINT = (DataType.SINT8, 1)
    R8G8_UNORM = (DataType.UNORM8, 2)
    R8G8_SNORM = (DataType.SNORM8, 2)
    R8G8_UINT = (DataType.UINT8, 2)
    R8G8_SINT = (DataType.SINT8, 2)
    R8G8B8_UNORM = (DataType.UNORM8, 3)
    R8G8B8_SNORM = (DataType.UNORM8, 3)
    R8G8B8_UINT = (DataType.UINT8, 3)
    R8G8B8_SINT = (DataType.SINT8, 3)
    R8G8B8A8_UNORM = (DataType.UNORM8, 4)
    R8G8B8A8_SNORM = (DataType.UNORM8, 4)
    R8G8B8A8_UINT = (DataType.UINT8, 4)
    R8G8B8A8_SINT = (DataType.SINT8, 4)
    B8G8R8A8_UINT = (DataType.UINT8, 4)
    B8G8R8A8_SINT = (DataType.SINT8, 4)
    R16_UINT = (DataType.UINT16, 1)
    R16_SINT = (DataType.SINT16, 1)
    R16_SFLOAT = (DataType.SFLOAT16, 1)
    R16G16_UINT = (DataType.UINT16, 2)
    R16G16_SINT = (DataType.SINT16, 2)
    R16G16_SFLOAT = (DataType.SFLOAT16, 2)
    R16G16B16_UINT = (DataType.UINT16, 3)
    R16G16B16_SINT = (DataType.SINT16, 3)
    R16G16B16_SFLOAT = (DataType.SFLOAT16, 3)
    R16G16B16A16_UINT = (DataType.UINT16, 1)
    R16G16B16A16_SINT = (DataType.SINT16, 4)
    R16G16B16A16_SFLOAT = (DataType.SFLOAT16, 4)
    R32_UINT = (DataType.UINT32, 1)
    R32_SINT = (DataType.SINT32, 1)
    R32_SFLOAT = (DataType.SFLOAT32, 1)
    R32G32_UINT = (DataType.UINT32, 2)
    R32G32_SINT = (DataType.SINT32, 2)
    R32G32_SFLOAT = (DataType.SFLOAT32, 2)
    R32G32B32_UINT = (DataType.UINT32, 3)
    R32G32B32_SINT = (DataType.SINT32, 3)
    R32G32B32_SFLOAT = (DataType.SFLOAT32, 3)
    R32G32B32A32_UINT = (DataType.UINT32, 4)
    R32G32B32A32_SINT = (DataType.SINT32, 4)
    R32G32B32A32_SFLOAT = (DataType.SFLOAT32, 4)


class FrontFace(IntEnum):
    NONE = 0
    COUNTER_CLOCKWISE = vk.VK_FRONT_FACE_COUNTER_CLOCKWISE
    CLOCKWISE = vk.VK_FRONT_FACE_CLOCKWISE


class ImageAspect(IntFlag):
    NONE = 0
    COLOR = vk.VK_IMAGE_ASPECT_COLOR_BIT
    DEPTH = vk.VK_IMAGE_ASPECT_DEPTH_BIT
    STENCIL = vk.VK_IMAGE_ASPECT_STENCIL_BIT
    METADATA = vk.VK_IMAGE_ASPECT_METADATA_BIT


class ImageLayout(IntEnum):
    NONE = 0
    UNDEFINED = vk.VK_IMAGE_LAYOUT_UNDEFINED
    GENERAL = vk.VK_IMAGE_LAYOUT_GENERAL
    COLOR_ATTACHMENT_OPTIMAL = vk.VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL
    DEPTH_STENCIL_ATTACHMENT_OPTIMAL = vk.VK_IMAGE_LAYOUT_DEPTH_STENCIL_ATTACHMENT_OPTIMAL # noqa
    DEPTH_STENCIL_READ_ONLY_OPTIMAL = vk.VK_IMAGE_LAYOUT_DEPTH_STENCIL_READ_ONLY_OPTIMAL # noqa
    SHADER_READ_ONLY_OPTIMAL = vk.VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL
    TRANSFER_SRC_OPTIMAL = vk.VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL
    TRANSFER_DST_OPTIMAL = vk.VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL
    PREINITIALIZED = vk.VK_IMAGE_LAYOUT_PREINITIALIZED
    PRESENT_SRC_KHR = vk.VK_IMAGE_LAYOUT_PRESENT_SRC_KHR


class ImageTiling(IntEnum):
    NONE = 0
    OPTIMAL = vk.VK_IMAGE_TILING_OPTIMAL
    LINEAR = vk.VK_IMAGE_TILING_LINEAR


class ImageType(IntEnum):
    NONE = 0
    TYPE_1D = vk.VK_IMAGE_TYPE_1D
    TYPE_2D = vk.VK_IMAGE_TYPE_2D
    TYPE_3D = vk.VK_IMAGE_TYPE_3D


class ImageUsage(IntFlag):
    NONE = 0
    TRANSFER_SRC = vk.VK_IMAGE_USAGE_TRANSFER_SRC_BIT
    TRANSFER_DST = vk.VK_IMAGE_USAGE_TRANSFER_DST_BIT
    SAMPLED = vk.VK_IMAGE_USAGE_SAMPLED_BIT
    STORAGE = vk.VK_IMAGE_USAGE_STORAGE_BIT
    COLOR_ATTACHMENT = vk.VK_IMAGE_USAGE_COLOR_ATTACHMENT_BIT
    DEPTH_STENCIL_ATTACHMENT = vk.VK_IMAGE_USAGE_DEPTH_STENCIL_ATTACHMENT_BIT
    TRANSIENT_ATTACHMENT = vk.VK_IMAGE_USAGE_TRANSIENT_ATTACHMENT_BIT
    INPUT_ATTACHMENT = vk.VK_IMAGE_USAGE_INPUT_ATTACHMENT_BIT


class ImageViewType(IntEnum):
    NONE = 0
    TYPE_1D = vk.VK_IMAGE_VIEW_TYPE_1D
    TYPE_2D = vk.VK_IMAGE_VIEW_TYPE_2D
    TYPE_3D = vk.VK_IMAGE_VIEW_TYPE_3D
    TYPE_CUBE = vk.VK_IMAGE_VIEW_TYPE_CUBE
    TYPE_1D_ARRAY = vk.VK_IMAGE_VIEW_TYPE_1D_ARRAY
    TYPE_2D_ARRAY = vk.VK_IMAGE_VIEW_TYPE_2D_ARRAY
    TYPE_CUBE_ARRAY = vk.VK_IMAGE_VIEW_TYPE_CUBE_ARRAY


class IndexType(IntEnum):
    NONE = 0
    UINT16 = vk.VK_INDEX_TYPE_UINT16
    UINT32 = vk.VK_INDEX_TYPE_UINT32


class LogicOp(IntEnum):
    NONE = 0
    CLEAR = vk.VK_LOGIC_OP_CLEAR
    AND = vk.VK_LOGIC_OP_AND
    AND_REVERSE = vk.VK_LOGIC_OP_AND_REVERSE
    COPY = vk.VK_LOGIC_OP_COPY
    AND_INVERTED = vk.VK_LOGIC_OP_AND_INVERTED
    NO_OP = vk.VK_LOGIC_OP_NO_OP
    XOR = vk.VK_LOGIC_OP_XOR
    OR = vk.VK_LOGIC_OP_OR
    NOR = vk.VK_LOGIC_OP_NOR
    EQUIVALENT = vk.VK_LOGIC_OP_EQUIVALENT
    INVERT = vk.VK_LOGIC_OP_INVERT
    OR_REVERSE = vk.VK_LOGIC_OP_OR_REVERSE
    COPY_INVERTED = vk.VK_LOGIC_OP_COPY_INVERTED
    OR_INVERTED = vk.VK_LOGIC_OP_OR_INVERTED
    NAND = vk.VK_LOGIC_OP_NAND
    SET = vk.VK_LOGIC_OP_SET


class MemoryProperty(IntFlag):
    NONE = 0
    DEVICE_LOCAL = vk.VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT
    HOST_VISIBLE = vk.VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT
    HOST_COHERENT = vk.VK_MEMORY_PROPERTY_HOST_COHERENT_BIT
    HOST_CACHED = vk.VK_MEMORY_PROPERTY_HOST_CACHED_BIT
    LAZILY_ALLOCATED = vk.VK_MEMORY_PROPERTY_LAZILY_ALLOCATED_BIT


class PipelineBindPoint(IntEnum):
    NONE = 0
    GRAPHICS = vk.VK_PIPELINE_BIND_POINT_GRAPHICS
    COMPUTE = vk.VK_PIPELINE_BIND_POINT_COMPUTE


class PipelineStage(IntFlag):
    NONE = 0
    TOP_OF_PIPE = vk.VK_PIPELINE_STAGE_TOP_OF_PIPE_BIT
    DRAW_INDIRECT = vk.VK_PIPELINE_STAGE_DRAW_INDIRECT_BIT
    VERTEX_INPUT = vk.VK_PIPELINE_STAGE_VERTEX_INPUT_BIT
    VERTEX_SHADER = vk.VK_PIPELINE_STAGE_VERTEX_SHADER_BIT
    TESSELLATION_CONTROL_SHADER = vk.VK_PIPELINE_STAGE_TESSELLATION_CONTROL_SHADER_BIT # noqa
    TESSELLATION_EVALUATION_SHADER = vk.VK_PIPELINE_STAGE_TESSELLATION_EVALUATION_SHADER_BIT # noqa
    GEOMETRY_SHADER = vk.VK_PIPELINE_STAGE_GEOMETRY_SHADER_BIT
    FRAGMENT_SHADER = vk.VK_PIPELINE_STAGE_FRAGMENT_SHADER_BIT
    EARLY_FRAGMENT_TESTS = vk.VK_PIPELINE_STAGE_EARLY_FRAGMENT_TESTS_BIT
    LATE_FRAGMENT_TESTS = vk.VK_PIPELINE_STAGE_LATE_FRAGMENT_TESTS_BIT
    COLOR_ATTACHMENT_OUTPUT = vk.VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT
    COMPUTE_SHADER = vk.VK_PIPELINE_STAGE_COMPUTE_SHADER_BIT
    TRANSFER = vk.VK_PIPELINE_STAGE_TRANSFER_BIT
    BOTTOM_OF_PIPE = vk.VK_PIPELINE_STAGE_BOTTOM_OF_PIPE_BIT
    HOST = vk.VK_PIPELINE_STAGE_HOST_BIT
    ALL_GRAPHICS = vk.VK_PIPELINE_STAGE_ALL_GRAPHICS_BIT
    ALL_COMMANDS = vk.VK_PIPELINE_STAGE_ALL_COMMANDS_BIT


class PolygonMode(IntEnum):
    NONE = 0
    FILL = vk.VK_POLYGON_MODE_FILL
    LINE = vk.VK_POLYGON_MODE_LINE
    POINT = vk.VK_POLYGON_MODE_POINT


class PrimitiveTopology(IntEnum):
    NONE = 0
    POINT_LIST = vk.VK_PRIMITIVE_TOPOLOGY_POINT_LIST
    LINE_LIST = vk.VK_PRIMITIVE_TOPOLOGY_LINE_LIST
    LINE_STRIP = vk.VK_PRIMITIVE_TOPOLOGY_LINE_STRIP
    TRIANGLE_LIST = vk.VK_PRIMITIVE_TOPOLOGY_TRIANGLE_LIST
    TRIANGLE_STRIP = vk.VK_PRIMITIVE_TOPOLOGY_TRIANGLE_STRIP
    TRIANGLE_FAN = vk.VK_PRIMITIVE_TOPOLOGY_TRIANGLE_FAN
    LINE_LIST_WITH_ADJACENCY = vk.VK_PRIMITIVE_TOPOLOGY_LINE_LIST_WITH_ADJACENCY # noqa
    LINE_STRIP_WITH_ADJACENCY = vk.VK_PRIMITIVE_TOPOLOGY_LINE_STRIP_WITH_ADJACENCY # noqa
    TRIANGLE_LIST_WITH_ADJACENCY = vk.VK_PRIMITIVE_TOPOLOGY_TRIANGLE_LIST_WITH_ADJACENCY # noqa
    TRIANGLE_STRIP_WITH_ADJACENCY = vk.VK_PRIMITIVE_TOPOLOGY_TRIANGLE_STRIP_WITH_ADJACENCY # noqa
    PATCH_LIST = vk.VK_PRIMITIVE_TOPOLOGY_PATCH_LIST


class SampleCount(IntFlag):
    NONE = 0
    COUNT_1 = vk.VK_SAMPLE_COUNT_1_BIT
    COUNT_2 = vk.VK_SAMPLE_COUNT_2_BIT
    COUNT_4 = vk.VK_SAMPLE_COUNT_4_BIT
    COUNT_8 = vk.VK_SAMPLE_COUNT_8_BIT
    COUNT_16 = vk.VK_SAMPLE_COUNT_16_BIT
    COUNT_32 = vk.VK_SAMPLE_COUNT_32_BIT
    COUNT_64 = vk.VK_SAMPLE_COUNT_64_BIT


class SamplerAddressMode(IntEnum):
    NONE = 0
    REPEAT = vk.VK_SAMPLER_ADDRESS_MODE_REPEAT
    MIRRORED_REPEAT = vk.VK_SAMPLER_ADDRESS_MODE_MIRRORED_REPEAT
    CLAMP_TO_EDGE = vk.VK_SAMPLER_ADDRESS_MODE_CLAMP_TO_EDGE
    CLAMP_TO_BORDER = vk.VK_SAMPLER_ADDRESS_MODE_CLAMP_TO_BORDER
    MIRROR_CLAMP_TO_EDGE = vk.VK_SAMPLER_ADDRESS_MODE_MIRROR_CLAMP_TO_EDGE


class SamplerMipmapMode(IntEnum):
    NONE = 0
    NEAREST = vk.VK_SAMPLER_MIPMAP_MODE_NEAREST
    LINEAR = vk.VK_SAMPLER_MIPMAP_MODE_LINEAR


class ShaderStage(IntFlag):
    NONE = 0
    VERTEX = vk.VK_SHADER_STAGE_VERTEX_BIT
    TESSELLATION_CONTROL = vk.VK_SHADER_STAGE_TESSELLATION_CONTROL_BIT
    TESSELLATION_EVALUATION = vk.VK_SHADER_STAGE_TESSELLATION_EVALUATION_BIT # noqa
    GEOMETRY = vk.VK_SHADER_STAGE_GEOMETRY_BIT
    FRAGMENT = vk.VK_SHADER_STAGE_FRAGMENT_BIT
    COMPUTE = vk.VK_SHADER_STAGE_COMPUTE_BIT
    ALL_GRAPHICS = vk.VK_SHADER_STAGE_ALL_GRAPHICS
    ALL = vk.VK_SHADER_STAGE_ALL


class SharingMode(IntEnum):
    NONE = 0
    EXCLUSIVE = vk.VK_SHARING_MODE_EXCLUSIVE
    CONCURRENT = vk.VK_SHARING_MODE_CONCURRENT


class SubpassContents(IntEnum):
    NONE = 0
    INLINE = vk.VK_SUBPASS_CONTENTS_INLINE
    SECONDARY_COMMAND_BUFFERS = vk.VK_SUBPASS_CONTENTS_SECONDARY_COMMAND_BUFFERS # noqa


class VertexInputRate(IntEnum):
    NONE = 0
    VERTEX = vk.VK_VERTEX_INPUT_RATE_VERTEX
    INSTANCE = vk.VK_VERTEX_INPUT_RATE_INSTANCE


# ----------
# MAPPING
# ----------
DataTypeByte = {
    DataType.UINT8: 1,
    DataType.SINT8: 1,
    DataType.UINT16: 2,
    DataType.SINT16: 2,
    DataType.UINT32: 4,
    DataType.SINT32: 4,
    DataType.SFLOAT16: 2,
    DataType.SFLOAT32: 4,
    DataType.UNORM8: 1,
    DataType.SNORM8: 1,
    DataType.UNORM16: 2,
    DataType.SNORM16: 2,
    DataType.UNORM32: 4,
    DataType.SNORM32: 4
}


DataTypeNumpy = {
    DataType.UINT8: np.uint8,
    DataType.SINT8: np.int8,
    DataType.UINT16: np.uint16,
    DataType.SINT16: np.int16,
    DataType.UINT32: np.uint32,
    DataType.SINT32: np.int32,
    DataType.SFLOAT16: np.float16,
    DataType.SFLOAT32: np.float32,
    DataType.UNORM8: np.uint8,
    DataType.SNORM8: np.int8
}


# ----------
# FUNCTIONS
# ----------
def format_info(f):
    '''Return detailed information of format `f`

    *Parameters:*

    - `f`: `Format`

    *Returns:*

    Tuple containing:

    - `DataType`
    - Number of components
    - Size in bytes (not bits)
    '''
    ftype = FormatType.__members__[f.name]
    data_type = ftype.value[0]
    num_components = ftype.value[1]
    size = DataTypeByte[data_type] * num_components
    return data_type, num_components, size


def index_type_size(t):
    '''Return the size in byte of the index type

    *Parameters:*

    - `t`: `IndexType`
    '''
    if t == IndexType.UINT16:
        return 2
    return 4


# Mapping between layout value and its name
VK_LAYOUT_NAME = {}
for name in (
    'UNDEFINED', 'GENERAL', 'COLOR_ATTACHMENT_OPTIMAL',
    'DEPTH_STENCIL_ATTACHMENT_OPTIMAL', 'DEPTH_STENCIL_READ_ONLY_OPTIMAL',
    'SHADER_READ_ONLY_OPTIMAL', 'TRANSFER_SRC_OPTIMAL',
    'TRANSFER_DST_OPTIMAL', 'PREINITIALIZED', 'PRESENT_SRC_KHR'
):
    fn = 'VK_IMAGE_LAYOUT_%s' % name
    VK_LAYOUT_NAME[getattr(vk, fn)] = fn
