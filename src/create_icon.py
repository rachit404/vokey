"""
Generate .ico file for vokey application
==========================================
Creates a microphone icon in .ico format for the executable.
"""

from PIL import Image, ImageDraw


def create_microphone_icon(size: int = 256) -> Image.Image:
    """
    Create a microphone icon suitable for .exe files.
    
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
        width=int(size * 0.03)
    )
    
    # Draw microphone stand (vertical line)
    stand_top = mic_bottom
    stand_bottom = center_y + mic_height // 2 + 4
    draw.line(
        [(center_x, stand_top), (center_x, stand_bottom)],
        fill='#FFFFFF',
        width=int(size * 0.05)
    )
    
    # Draw base (horizontal line)
    base_y = stand_bottom
    base_width = mic_width // 2
    draw.line(
        [(center_x - base_width, base_y), (center_x + base_width, base_y)],
        fill='#FFFFFF',
        width=int(size * 0.05)
    )
    
    # Draw curved line below mic (arc)
    arc_bbox = [
        (center_x - mic_width, mic_bottom - 4),
        (center_x + mic_width, stand_bottom)
    ]
    draw.arc(arc_bbox, start=180, end=360, fill='#FFFFFF', width=int(size * 0.03))
    
    return image


def create_ico_file(output_path: str = "vokey_icon.ico"):
    """
    Create a multi-resolution .ico file for Windows.
    
    Args:
        output_path: Path where the .ico file will be saved
    """
    # Create icons at multiple resolutions
    sizes = [16, 32, 48, 64, 128, 256]
    images = []
    
    for size in sizes:
        icon = create_microphone_icon(size)
        images.append(icon)
    
    # Save as .ico with multiple sizes
    images[0].save(
        output_path,
        format='ICO',
        sizes=[(img.width, img.height) for img in images],
        append_images=images[1:]
    )
    
    print(f"Icon created: {output_path}")
    print(f"   Sizes included: {', '.join(str(s) for s in sizes)}px")


if __name__ == "__main__":
    import sys
    import os
    
    # Change to project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)
    
    # Create the icon
    output_file = "./artifacts/vokey_icon.ico"
    create_ico_file(output_file)
    
    print(f"\nIcon saved to: {os.path.abspath(output_file)}")
    print(f"\nNext steps:")
    print(f"   1. The icon is ready to use")
    print(f"   2. Run: python scripts/build.py")
    print(f"   3. Your .exe files will have the custom icon!")
