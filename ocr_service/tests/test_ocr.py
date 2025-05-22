import pytest
from fastapi.testclient import TestClient
from PIL import Image, ImageDraw
import io

from main import app  # Import your FastAPI app

client = TestClient(app)

class TestOCRService:

    @pytest.fixture
    def sample_image_bytes(self):
        """
        Create an in-memory test image with some text.
        """
        image = Image.new("RGB", (200, 100), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        draw.text((10, 40), "Test OCR", fill=(0, 0, 0))

        img_bytes = io.BytesIO()
        image.save(img_bytes, format="PNG")
        img_bytes.seek(0)
        return img_bytes

    def test_ocr_endpoint_success(self, sample_image_bytes):
        response = client.post(
            "/ocr",
            files={"file": ("test.png", sample_image_bytes, "image/png")}
        )

        assert response.status_code == 200
        data = response.json()

        assert "text" in data
        assert "raw" in data
        assert isinstance(data["text"], str)
        assert isinstance(data["raw"], list)

        if data["raw"]:
            assert "box" in data["raw"][0]
            assert "text" in data["raw"][0]
            assert "confidence" in data["raw"][0]

    def test_ocr_endpoint_missing_file(self):
        response = client.post("/ocr", files={})  # No file provided
        assert response.status_code == 422  # Unprocessable Entity