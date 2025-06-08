"""
Create a simple icon for the Hand Gesture Control application
This script generates a basic .ico file using PIL
"""

try:
    from PIL import Image, ImageDraw
    
    def create_icon():
        """Create a simple hand icon"""
        # Create base image
        size = 32
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw a simple hand shape
        # Palm (circle)
        palm_center = size // 2
        palm_radius = size // 4
        draw.ellipse(
            [palm_center - palm_radius, palm_center, 
             palm_center + palm_radius, palm_center + palm_radius],
            fill=(70, 130, 180, 255)  # Steel blue
        )
        
        # Fingers (rectangles)
        finger_width = 3
        finger_positions = [
            (palm_center - 8, 8),   # thumb
            (palm_center - 4, 4),   # index
            (palm_center, 2),       # middle
            (palm_center + 4, 4),   # ring
            (palm_center + 8, 6)    # pinky
        ]
        
        for x, y in finger_positions:
            draw.rectangle(
                [x, y, x + finger_width, palm_center],
                fill=(70, 130, 180, 255)
            )
        
        return img
    
    # Create multiple sizes for the ico file
    sizes = [16, 24, 32, 48, 64]
    images = []
    
    for size in sizes:
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Scale drawing based on size
        palm_center = size // 2
        palm_radius = size // 4
        
        # Palm
        draw.ellipse(
            [palm_center - palm_radius, palm_center, 
             palm_center + palm_radius, palm_center + palm_radius],
            fill=(70, 130, 180, 255)
        )
        
        # Fingers
        finger_width = max(2, size // 16)
        finger_positions = [
            (palm_center - size//4, size//4),
            (palm_center - size//8, size//8),
            (palm_center, size//16),
            (palm_center + size//8, size//8),
            (palm_center + size//4, size//6)
        ]
        
        for x, y in finger_positions:
            draw.rectangle(
                [x, y, x + finger_width, palm_center],
                fill=(70, 130, 180, 255)
            )
        
        images.append(img)
    
    # Save as ICO file
    images[0].save('icon.ico', format='ICO', sizes=[(img.width, img.height) for img in images])
    print("Icon created successfully: icon.ico")
    
except ImportError:
    print("PIL not available. Using default icon.")
    # Create a simple placeholder
    with open('icon.ico', 'wb') as f:
        # Write minimal ICO header (this won't work as a real icon)
        f.write(b'\x00\x00\x01\x00\x01\x00\x20\x20\x00\x00\x01\x00\x08\x00')
        
except Exception as e:
    print(f"Error creating icon: {e}")

if __name__ == "__main__":
    create_icon()
