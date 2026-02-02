"""
Icon Generator for System Tray
================================
Generates a simple microphone icon for the system tray using PIL.
"""

from PIL import Image, ImageDraw


def create_microphone_icon(size: int = 64) -> Image.Image:
    """
    Create a simple microphone icon.
    
    Args:
        size: Size of the icon in pixels (square)
    
    Returns:
        PIL Image object
    """
    # Create a new image with transparent background
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Calculate dimensions
    center_x = size // 2
    center_y = size // 2
    
    # Microphone body (capsule shape)
    mic_width = size // 3
    mic_height = size // 2
    mic_top = center_y - mic_height // 2
    mic_bottom = center_y + mic_height // 4
    
    # Draw microphone capsule (rounded rectangle)
    draw.rounded_rectangle(
        [(center_x - mic_width // 2, mic_top),
         (center_x + mic_width // 2, mic_bottom)],
        radius=mic_width // 2,
        fill='#00AAFF',
        outline='#FFFFFF',
        width=2
    )
    
    # Draw microphone stand (vertical line)
    stand_top = mic_bottom
    stand_bottom = center_y + mic_height // 2 + 4
    draw.line(
        [(center_x, stand_top), (center_x, stand_bottom)],
        fill='#FFFFFF',
        width=3
    )
    
    # Draw base (horizontal line)
    base_y = stand_bottom
    base_width = mic_width // 2
    draw.line(
        [(center_x - base_width, base_y), (center_x + base_width, base_y)],
        fill='#FFFFFF',
        width=3
    )
    
    # Draw curved line below mic (arc)
    arc_bbox = [
        (center_x - mic_width, mic_bottom - 4),
        (center_x + mic_width, stand_bottom)
    ]
    draw.arc(arc_bbox, start=180, end=360, fill='#FFFFFF', width=2)
    
    return image


if __name__ == "__main__":
    # Test the icon generation
    icon = create_microphone_icon(64)
    icon.save("tray_icon.png")
    print("Icon saved as tray_icon.png")
