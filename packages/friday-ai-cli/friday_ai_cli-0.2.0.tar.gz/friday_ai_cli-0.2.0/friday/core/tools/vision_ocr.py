import asyncio
import mimetypes
from google.cloud import vision
from google.oauth2 import service_account
from anthropic.types.beta import BetaToolUnionParam
from typing import TypedDict, NotRequired
from typing import ClassVar, Literal, Optional
from pathlib import Path
from .base import BaseAnthropicTool, ToolError, ToolResult
import os


class FunctionParameter(TypedDict):
    """Type definition for function parameters in tool schema."""

    type: Literal["object"]
    properties: dict[str, dict[str, str]]
    required: list[str]


class FunctionDefinition(TypedDict):
    """Type definition for function in tool schema."""

    name: str
    description: str
    parameters: FunctionParameter


class VisionOCRTool(BaseAnthropicTool):
    """Tool for performing OCR on images using Google Cloud Vision API."""

    tool_name: ClassVar[Literal["vision_ocr"]] = "vision_ocr"

    _client: Optional[vision.ImageAnnotatorClient] = None

    _credentials_path: str = ""
    _supported_mime_types = {
        "image/jpeg",
        "image/png",
        "image/gif",
        "image/bmp",
        "image/webp",
    }
    _max_file_size = 10 * 1024 * 1024  # 10MB limit

    def __init__(self, credentials_path: str):
        super().__init__()
        self._credentials_path = credentials_path
        try:
            # Initialize the Google Cloud Vision client
            credentials = service_account.Credentials.from_service_account_file(
                self._credentials_path
            )
            self._client = vision.ImageAnnotatorClient(credentials=credentials)
        except Exception as e:
            raise ToolError(
                f"Failed to initialize Google Cloud Vision client: {str(e)}"
            )

    def _validate_image_file(self, path: Path) -> None:
        """
        Validates that the file is a supported image file.

        Args:
            path: Path to the image file

        Raises:
            ToolError: If the file is invalid
        """
        # Check basic path validation
        if not path.is_absolute():
            raise ToolError(f"The path {path} must be absolute (start with '/')")
        if not path.exists():
            raise ToolError(f"Image file not found: {path}")
        if not path.is_file():
            raise ToolError(f"Path {path} exists but is not a file")

        # Check file size
        file_size = path.stat().st_size
        if file_size > self._max_file_size:
            raise ToolError(
                f"Image file size ({file_size/1024/1024:.1f}MB) exceeds maximum allowed size (10MB)"
            )

        # Check file type
        mime_type, _ = mimetypes.guess_type(str(path))
        if not mime_type or mime_type not in self._supported_mime_types:
            raise ToolError(
                f"Unsupported file type: {mime_type or 'unknown'}. "
                f"Supported types: {', '.join(sorted(self._supported_mime_types))}"
            )

    async def __call__(self, *, image_path: str, **kwargs) -> ToolResult:
        """
        Executes OCR on the provided image asynchronously.

        Args:
            image_path: Path to the image file to process
            **kwargs: Additional keyword arguments (ignored)

        Returns:
            ToolResult containing the extracted text or error
        """
        if not self._client:
            return ToolResult(error="Google Cloud Vision client not initialized")

        try:
            # Validate image file
            path = Path(image_path)
            self._validate_image_file(path)

            # Read image file in a separate thread to not block the event loop
            def read_image():
                with open(path, "rb") as image_file:
                    return image_file.read()

            content = await asyncio.to_thread(read_image)

            # Perform OCR in a separate thread
            def perform_ocr():
                image = vision.Image(content=content)
                return self._client.text_detection(image=image)

            response = await asyncio.to_thread(perform_ocr)

            if not response.text_annotations:
                return ToolResult(error="No text detected in the image.")

            whole_image_text = response.text_annotations[0].description
            return ToolResult(output=whole_image_text.strip())

        except ToolError as e:
            return ToolResult(error=str(e))
        except Exception as e:
            return ToolResult(error=f"Failed to extract text from image: {str(e)}")

    def to_params(self) -> BetaToolUnionParam:
        """Convert tool to API parameters."""
        param: BetaToolUnionParam = {
            "name": self.tool_name,
            "description": (
                "Extract text from images using OCR (Optical Character Recognition). "
                "Supports JPEG, PNG, GIF, BMP, and WebP images up to 10MB in size."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Absolute path to the image file to process",
                    }
                },
                "required": ["image_path"],
            },
        }
        return param
