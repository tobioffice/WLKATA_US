import cv2
import numpy as np

def analyze_image_colors(image_path):
    """Analyze RGB characteristics of an image"""
    image = cv2.imread(image_path)
    if image is None:
        print(f"Could not load {image_path}")
        return
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    avg_color = np.mean(image_rgb, axis=(0, 1))
    avg_gray = np.mean(gray)
    std_gray = np.std(gray)
    min_gray = np.min(gray)
    max_gray = np.max(gray)
    
    print(f"\n{image_path}:")
    print(f"  Average RGB: [{avg_color[0]:.1f}, {avg_color[1]:.1f}, {avg_color[2]:.1f}]")
    print(f"  Average Gray: {avg_gray:.1f}")
    print(f"  Gray Range: {min_gray:.1f} - {max_gray:.1f}")
    print(f"  Gray Std: {std_gray:.1f}")

# Analyze key images
images_to_check = [
    # "images/no_object.png",
    "images/burnedStates/overBurned.png",
    "images/burnedStates/good.png",
    "images/burnedStates/unBurned.png",
    "images/burnedStates/underBurned.png"
]

print("=== Image Analysis for Object Detection ===")
for img_path in images_to_check:
    analyze_image_colors(img_path)
