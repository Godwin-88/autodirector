from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from core import brand
from core.logging import get_logger

logger = get_logger("thumbnail_generator")


class ThumbnailGenerator:
    SIZE = (1280, 720)
    BG_COLOR = (13, 17, 23)
    GOLD = (240, 180, 41)
    WHITE = (230, 237, 243)
    PURPLE = (124, 58, 237)
    MATH_SYMBOLS = ["∑", "∫", "∂", "σ", "Δ", "π", "√", "∞"]

    def generate(self, topic_keyword: str, key_equation_latex: str,
                 episode_number: int, output_path: str) -> Path:
        """Generate a YouTube thumbnail."""
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        img = Image.new("RGB", self.SIZE, self.BG_COLOR)
        draw = ImageDraw.Draw(img)

        # Draw decorative math symbols
        import random
        for symbol in self.MATH_SYMBOLS:
            x = random.randint(50, 1230)
            y = random.randint(50, 670)
            alpha = random.randint(20, 60)
            draw.text((x, y), symbol, fill=(self.GOLD[0], self.GOLD[1], self.GOLD[2], alpha))

        # Topic keyword (large, gold)
        try:
            font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64)
            font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        except (IOError, OSError):
            font_title = ImageFont.load_default()
            font_body = ImageFont.load_default()
            font_small = ImageFont.load_default()

        # Main title
        title_text = topic_keyword[:60].upper()
        bbox = draw.textbbox((0, 0), title_text, font=font_title)
        draw.text(
            ((self.SIZE[0] - (bbox[2] - bbox[0])) // 2, 100),
            title_text,
            fill=self.GOLD,
            font=font_title,
        )

        # Episode number
        ep_text = f"Episode {episode_number}"
        bbox = draw.textbbox((0, 0), ep_text, font=font_body)
        draw.text(
            ((self.SIZE[0] - (bbox[2] - bbox[0])) // 2, 200),
            ep_text,
            fill=self.WHITE,
            font=font_body,
        )

        # Key equation (simplified)
        eq_text = key_equation_latex.replace("\\", "").replace("{", "").replace("}", "")
        if len(eq_text) > 40:
            eq_text = eq_text[:40] + "..."
        bbox = draw.textbbox((0, 0), eq_text, font=font_body)
        draw.text(
            ((self.SIZE[0] - (bbox[2] - bbox[0])) // 2, 300),
            eq_text,
            fill=self.WHITE,
            font=font_body,
        )

        # QUANTIFAYA watermark
        watermark = "QUANTIFAYA"
        bbox = draw.textbbox((0, 0), watermark, font=font_small)
        draw.text(
            (self.SIZE[0] - (bbox[2] - bbox[0]) - 20, self.SIZE[1] - 50),
            watermark,
            fill=self.PURPLE,
            font=font_small,
        )

        img.save(output, "JPEG", quality=95)
        logger.info("thumbnail_generated", path=str(output))
        return output