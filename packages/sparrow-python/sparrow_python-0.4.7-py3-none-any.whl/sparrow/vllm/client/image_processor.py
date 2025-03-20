import asyncio
import base64
import os
import hashlib
from copy import deepcopy
from io import BytesIO
from mimetypes import guess_type
from pathlib import Path

import aiohttp
import requests
from loguru import logger
from PIL import Image
from sparrow.decorators.core import async_retry

# 兼容不同版本的PIL
try:
    LANCZOS = Image.LANCZOS
except AttributeError:
    # 在较旧版本的PIL中，LANCZOS可能被称为ANTIALIAS
    LANCZOS = Image.ANTIALIAS

# 默认的缓存目录
DEFAULT_CACHE_DIR = os.path.expanduser("~/.cache/sparrow/image_cache")

def get_cache_path(url: str, cache_dir: str = DEFAULT_CACHE_DIR) -> Path:
    """获取图片的缓存路径"""
    # 使用URL的MD5作为文件名
    url_hash = hashlib.md5(url.encode()).hexdigest()
    # 获取URL中的文件扩展名
    ext = os.path.splitext(url)[-1].lower()
    if not ext or ext not in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
        ext = '.png'  # 默认使用.png 而不是 .jpg，因为 PNG 支持透明通道
    return Path(cache_dir) / f"{url_hash}{ext}"

def ensure_cache_dir(cache_dir: str = DEFAULT_CACHE_DIR):
    """确保缓存目录存在"""
    os.makedirs(cache_dir, exist_ok=True)


def encode_base64_from_local_path(file_path, return_with_mime=True):
    """Encode a local file to a Base64 string, with optional MIME type prefix."""
    mime_type, _ = guess_type(file_path)
    mime_type = mime_type or "application/octet-stream"
    with open(file_path, "rb") as file:
        base64_data = base64.b64encode(file.read()).decode("utf-8")
        if return_with_mime:
            return f"data:{mime_type};base64,{base64_data}"
        return base64_data


async def encode_base64_from_url(
    url, session: aiohttp.ClientSession, return_with_mime=True
):
    """Fetch a file from a URL and encode it to a Base64 string, with optional MIME type prefix."""
    async with session.get(url) as response:
        response.raise_for_status()
        content = await response.read()
        mime_type = response.headers.get("Content-Type", "application/octet-stream")
        base64_data = base64.b64encode(content).decode("utf-8")
        if return_with_mime:
            return f"data:{mime_type};base64,{base64_data}"
        return base64_data


def encode_base64_from_pil(image: Image.Image, return_with_mime=True):
    """Encode a PIL image object to a Base64 string, with optional MIME type prefix."""
    buffer = BytesIO()
    image_format = image.format or "PNG"  # Default to PNG if format is unknown
    mime_type = f"image/{image_format.lower()}"
    image.save(buffer, format=image_format)
    buffer.seek(0)
    base64_data = base64.b64encode(buffer.read()).decode("utf-8")
    if return_with_mime:
        return f"data:{mime_type};base64,{base64_data}"
    return base64_data


# deprecated
def encode_base64_from_url_slow(url):
    response = requests.get(url)
    response.raise_for_status()
    return base64.b64encode(response.content).decode("utf-8")


async def encode_to_base64(
    file_source,
    session: aiohttp.ClientSession,
    return_with_mime: bool = True,
    return_pil: bool = False,
) -> str | tuple[str, Image.Image] | Image.Image:
    """A unified function to encode files to Base64 strings or return PIL Image objects.

    Args:
        file_source: File path, URL, or PIL Image object
        session: aiohttp ClientSession for async URL fetching
        return_with_mime: Whether to include MIME type prefix in base64 string
        return_pil: Whether to return PIL Image object (for image files)

    Returns:
        If return_pil is False: base64 string (with optional MIME prefix)
        If return_pil is True and input is image: (base64_string, PIL_Image) or just PIL_Image
        If return_pil is True and input is not image: base64 string
    """
    mime_type = None
    pil_image = None

    if isinstance(file_source, str):
        if file_source.startswith("file://"):
            file_path = file_source[7:]
            if not os.path.exists(file_path):
                raise ValueError("Local file not found.")
            mime_type, _ = guess_type(file_path)
            if return_pil and mime_type and mime_type.startswith("image"):
                pil_image = Image.open(file_path)
                if return_pil and not return_with_mime:
                    return pil_image
            with open(file_path, "rb") as file:
                content = file.read()

        elif os.path.exists(file_source):
            mime_type, _ = guess_type(file_source)
            if return_pil and mime_type and mime_type.startswith("image"):
                pil_image = Image.open(file_source)
                if return_pil and not return_with_mime:
                    return pil_image
            with open(file_source, "rb") as file:
                content = file.read()

        elif file_source.startswith("http"):
            async with session.get(file_source) as response:
                response.raise_for_status()
                content = await response.read()
                mime_type = response.headers.get(
                    "Content-Type", "application/octet-stream"
                )
                if return_pil and mime_type.startswith("image"):
                    pil_image = Image.open(BytesIO(content))
                    if return_pil and not return_with_mime:
                        return pil_image
        else:
            raise ValueError("Unsupported file source type.")

    elif isinstance(file_source, Image.Image):
        pil_image = file_source
        if return_pil and not return_with_mime:
            return pil_image

        buffer = BytesIO()
        image_format = file_source.format or "PNG"
        mime_type = f"image/{image_format.lower()}"
        file_source.save(buffer, format=image_format)
        content = buffer.getvalue()

    else:
        raise ValueError("Unsupported file source type.")

    base64_data = base64.b64encode(content).decode("utf-8")
    result = (
        f"data:{mime_type};base64,{base64_data}" if return_with_mime else base64_data
    )

    if return_pil and pil_image:
        return result, pil_image
    return result


async def encode_image_to_base64(
    image_source,
    session: aiohttp.ClientSession,
    max_width: int | None = None,
    max_height: int | None = None,
    max_pixels: int | None = None,
    return_with_mime: bool = True,
    use_cache: bool = False,
    cache_dir: str = DEFAULT_CACHE_DIR,
    force_refresh: bool = False
) -> str:
    """Encode an image to base64 string with optional size constraints.

    Args:
        image_source: Can be a file path (str), URL (str), or PIL Image object
        session: aiohttp ClientSession for async URL fetching
        max_width: Optional maximum width for image resizing
        max_height: Optional maximum height for image resizing
        max_pixels: Optional maximum number of pixels (width * height)
        return_with_mime: Whether to include MIME type prefix in the result
        use_cache: Whether to use cache for URL images
        cache_dir: Cache directory path
        force_refresh: Whether to force refresh the cache even if cached image exists

    Returns:
        Base64 encoded string (with optional MIME prefix)
    """
    # Get image as PIL Image object
    if isinstance(image_source, Image.Image):
        image = image_source
    else:
        # Use encode_to_base64 with return_pil=True to get PIL Image directly
        image = await get_pil_image(image_source, session, use_cache=use_cache, cache_dir=cache_dir, force_refresh=force_refresh)

    # Make a copy of the image to avoid modifying the original
    image = image.copy()

    # Store original format
    original_format = image.format or "PNG"

    # Resize image based on provided constraints
    if max_width and max_height:
        # Use thumbnail to maintain aspect ratio while fitting within max dimensions
        image.thumbnail((max_width, max_height), LANCZOS)
    elif max_width:
        # Use thumbnail with unlimited height
        image.thumbnail((max_width, float("inf")), LANCZOS)
    elif max_height:
        # Use thumbnail with unlimited width
        image.thumbnail((float("inf"), max_height), LANCZOS)

    # Handle max_pixels constraint (after other resizing to avoid unnecessary work)
    if max_pixels and (image.width * image.height > max_pixels):
        # Calculate the ratio needed to get to max_pixels
        ratio = (max_pixels / (image.width * image.height)) ** 0.5
        # Use thumbnail to maintain aspect ratio
        target_width = int(image.width * ratio)
        target_height = int(image.height * ratio)
        image.thumbnail((target_width, target_height), LANCZOS)

    # Convert processed image to base64
    buffer = BytesIO()
    mime_type = f"image/{original_format.lower()}"
    image.save(buffer, format=original_format)
    buffer.seek(0)

    base64_data = base64.b64encode(buffer.getvalue()).decode("utf-8")

    if return_with_mime:
        return f"data:{mime_type};base64,{base64_data}"
    return base64_data


def decode_base64_to_pil(base64_string):
    """将base64字符串解码为PIL Image对象"""
    try:
        # 如果base64字符串包含header (如 'data:image/jpeg;base64,')，去除它
        if "," in base64_string:
            base64_string = base64_string.split(",")[1]

        # 解码base64为二进制数据
        image_data = base64.b64decode(base64_string)

        # 转换为PIL Image对象
        image = Image.open(BytesIO(image_data))
        return image
    except Exception as e:
        raise ValueError(f"无法将base64字符串解码为图像: {e!s}")


def decode_base64_to_file(base64_string, output_path, format="JPEG"):
    """将base64字符串解码并保存为图片文件"""
    try:
        # 获取PIL Image对象
        image = decode_base64_to_pil(base64_string)

        # 确保输出目录存在
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        # 保存图像
        image.save(output_path, format=format)
        return True
    except Exception as e:
        raise ValueError(f"无法将base64字符串保存为文件: {e!s}")


def decode_base64_to_bytes(base64_string):
    """将base64字符串解码为字节数据"""
    try:
        # 如果base64字符串包含header，去除它
        if "," in base64_string:
            base64_string = base64_string.split(",")[1]

        # 解码为字节数据
        return base64.b64decode(base64_string)
    except Exception as e:
        raise ValueError(f"无法将base64字符串解码为字节数据: {e!s}")


@async_retry(retry_times=3, retry_delay=0.3)
async def _get_image_from_http(session, image_source):
    async with session.get(image_source) as response:
        response.raise_for_status()
        content = await response.read()
        image = Image.open(BytesIO(content))
        return image


async def get_pil_image(
    image_source,
    session: aiohttp.ClientSession = None,
    use_cache: bool = False,
    cache_dir: str = DEFAULT_CACHE_DIR,
    force_refresh: bool = False
):
    """从图像链接或本地路径获取PIL格式的图像。

    Args:
        image_source: 图像来源，可以是本地文件路径或URL
        session: 用于异步URL请求的aiohttp ClientSession，如果为None且需要时会创建临时会话
        use_cache: 是否使用缓存（仅对URL图片有效）
        cache_dir: 缓存目录路径
        force_refresh: 是否强制刷新缓存，即使缓存存在也重新获取图像

    Returns:
        PIL.Image.Image: 加载的PIL图像对象

    Raises:
        ValueError: 当图像源无效或无法加载图像时
    """
    # 如果已经是PIL图像对象，直接返回
    if isinstance(image_source, Image.Image):
        return image_source

    # 处理字符串类型的图像源（文件路径或URL）
    if isinstance(image_source, str):
        # 处理本地文件路径
        if image_source.startswith("file://"):
            file_path = image_source[7:]
            if not os.path.exists(file_path):
                raise ValueError(f"本地文件不存在: {file_path}")
            return Image.open(file_path)
            
        # 处理普通本地文件路径
        elif os.path.exists(image_source):
            return Image.open(image_source)
            
        # 处理URL
        elif image_source.startswith("http"):
            # 检查缓存
            if use_cache and not force_refresh:
                ensure_cache_dir(cache_dir)
                cache_path = get_cache_path(image_source, cache_dir)
                if cache_path.exists():
                    return Image.open(cache_path)

            # 创建临时会话（如果未提供）
            close_session = False
            if session is None:
                session = aiohttp.ClientSession()
                close_session = True
                
            try:
                image = await _get_image_from_http(session, image_source)
                # 保存到缓存
                if use_cache:
                    try:
                        save_image_with_format(image, cache_path)
                    except Exception as e:
                        logger.warning(f"保存图片到缓存失败: {e}")
                    
                    return image
            finally:
                # 如果是临时创建的会话，确保关闭
                if close_session and session:
                    await session.close()
        else:
            raise ValueError(f"不支持的图像源类型: {image_source}")
    else:
        raise ValueError(f"不支持的图像源类型: {type(image_source)}")


def get_pil_image_sync(
    image_source,
    use_cache: bool = False,
    cache_dir: str = DEFAULT_CACHE_DIR,
    force_refresh: bool = False
):
    """从图像链接或本地路径获取PIL格式的图像（同步版本）。

    Args:
        image_source: 图像来源，可以是本地文件路径或URL
        use_cache: 是否使用缓存（仅对URL图片有效）
        cache_dir: 缓存目录路径
        force_refresh: 是否强制刷新缓存，即使缓存存在也重新获取图像

    Returns:
        PIL.Image.Image: 加载的PIL图像对象

    Raises:
        ValueError: 当图像源无效或无法加载图像时
    """
    # 如果已经是PIL图像对象，直接返回
    if isinstance(image_source, Image.Image):
        return image_source

    # 处理字符串类型的图像源（文件路径或URL）
    if isinstance(image_source, str):
        # 处理本地文件路径
        if image_source.startswith("file://"):
            file_path = image_source[7:]
            if not os.path.exists(file_path):
                raise ValueError(f"本地文件不存在: {file_path}")
            return Image.open(file_path)
            
        # 处理普通本地文件路径
        elif os.path.exists(image_source):
            return Image.open(image_source)
            
        # 处理URL
        elif image_source.startswith("http"):
            # 检查缓存
            if use_cache and not force_refresh:
                ensure_cache_dir(cache_dir)
                cache_path = get_cache_path(image_source, cache_dir)
                if cache_path.exists():
                    return Image.open(cache_path)
                    
            response = requests.get(image_source)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            
            # 保存到缓存
            if use_cache:
                try:
                    save_image_with_format(image, cache_path)
                except Exception as e:
                    logger.warning(f"保存图片到缓存失败: {e}")
                    
            return image
        else:
            raise ValueError(f"不支持的图像源类型: {image_source}")
    else:
        raise ValueError(f"不支持的图像源类型: {type(image_source)}")


def save_image_with_format(image: Image.Image, path: Path):
    """保存图片，自动处理格式转换问题"""
    # 获取目标格式
    target_format = path.suffix[1:].upper()  # 去掉点号并转大写
    if target_format == 'JPG':
        target_format = 'JPEG'
    
    # 创建图片副本以避免修改原图
    image = image.copy()
    
    # 处理调色板模式（P模式）
    if image.mode == 'P':
        if 'transparency' in image.info:
            # 如果有透明通道，转换为 RGBA
            image = image.convert('RGBA')
        else:
            # 如果没有透明通道，转换为 RGB
            image = image.convert('RGB')
    
    # 如果是 JPEG 格式且图片有 alpha 通道，需要特殊处理
    if target_format == 'JPEG' and image.mode in ('RGBA', 'LA'):
        # 创建白色背景
        background = Image.new('RGB', image.size, (255, 255, 255))
        if image.mode == 'RGBA':
            background.paste(image, mask=image.split()[3])  # 使用alpha通道作为mask
        else:
            background.paste(image, mask=image.split()[1])  # LA模式，使用A通道作为mask
        image = background
    
    # 确保图片模式与目标格式兼容
    if target_format == 'JPEG' and image.mode not in ('RGB', 'CMYK', 'L'):
        image = image.convert('RGB')
    
    # 保存图片
    try:
        if target_format == 'JPEG':
            image.save(path, format=target_format, quality=95)
        else:
            image.save(path, format=target_format)
    except Exception as e:
        logger.warning(f"保存图片到缓存失败（格式：{target_format}，模式：{image.mode}）: {e}")
        # 如果保存失败，尝试转换为 RGB 后保存
        if image.mode != 'RGB':
            image = image.convert('RGB')
            image.save(path, format=target_format)

