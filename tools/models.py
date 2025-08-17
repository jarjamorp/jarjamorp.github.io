from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ImageAsset:
    webp_url: str
    thumb_url: str
    alt: str = ""

@dataclass
class VideoAsset:
    mp4_url: str
    poster_url: Optional[str] = None

@dataclass
class Gallery:
    slug: str
    title: str
    date: str              # YYYY-MM-DD
    cover_image_url: Optional[str]
    images: List[ImageAsset]
    videos: List[VideoAsset]
