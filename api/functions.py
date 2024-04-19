from PIL import Image, ImageFont

# Create image from text
def CreateImage(text :str, font_size :int = 36, color :tuple[int, int, int, int] = (255, 255, 255, 255), filename :str = "temp"):
    font = ImageFont.truetype("assets/ComicMono.ttf", size=font_size)
    mask_image = font.getmask(text, "L")
    img = Image.new("RGB", mask_image.size)
    img.im.paste(color, (0, 0) + mask_image.size, mask_image)
    img.save(f"temp\\{filename}.png")
    return f"temp\\{filename}.png"