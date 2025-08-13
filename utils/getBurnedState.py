import cv2
import numpy as np
import os

def check_burned_state(image_path="images/pra_cropped.png") -> bool:
    """
    Check if the burned state is good
    
    Args:
        image_path: Path to the image file
    
    Returns:
        bool: True if state is 'good', False otherwise (also prints the state)
    """
    # Load image
    try:
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not load image '{image_path}'")
            return False
        
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Calculate average color
        avg_color = np.mean(image_rgb, axis=(0, 1))
        r, g, b = avg_color
        
        print(f"Average image color (RGB): [{r:.1f}, {g:.1f}, {b:.1f}]")
        
    except Exception as e:
        print(f"Error loading image: {e}")
        return False
    
    # Classification based on actual image analysis data
    predicted_state = None
    
    # unBurned: High RGB values, very close to each other (grayish)
    # Expected: ~[172, 174, 170]
    if r > 165 and g > 165 and b > 160 and abs(r - g) < 15 and abs(g - b) < 15:
        predicted_state = "unBurned"
        print("Classification: Light grayish colors detected (unBurned)")
    
    # underBurned: High R and G, much lower B (yellowish)
    # Expected: ~[170, 165, 90]
    elif r > 160 and g > 155 and b < 110 and (r + g - 2*b) > 150:
        predicted_state = "underBurned"
        print("Classification: Yellow tones detected (underBurned)")
    
    # good: Orange/brown tones with R > G > B pattern
    # Expected: ~[170, 128, 86]
    elif r > 160 and g > 120 and g < 140 and b < 100 and r > g > b and (r - b) > 70:
        predicted_state = "good"
        print("Classification: Orange/brown tones detected (good biscuit)")
    
    # overBurned: Lower overall values, more brownish
    # Expected: ~[135, 112, 87]
    elif r < 150 and g < 125 and b < 100 and r > g > b:
        predicted_state = "overBurned"
        print("Classification: Dark brown colors detected (overBurned)")
    
    # Fallback: closest color matching using actual reference values
    if predicted_state is None:
        print("Using fallback: closest color matching")
        
        # Reference colors from actual analysis
        reference_colors = {
            "overBurned": [135.0, 112.0, 87.1],
            "good": [169.8, 128.2, 86.4],
            "unBurned": [171.5, 173.7, 170.0],
            "underBurned": [169.7, 165.1, 89.7]
        }
        
        min_distance = float('inf')
        closest_state = None
        
        for state, ref_color in reference_colors.items():
            # Calculate Euclidean distance
            distance = np.sqrt(sum((avg_color[i] - ref_color[i])**2 for i in range(3)))
            if distance < min_distance:
                min_distance = distance
                closest_state = state
        
        predicted_state = closest_state
        print(f"Closest match: {predicted_state} (distance: {min_distance:.2f})")
    
    # Return result
    if predicted_state == 'good':
        print("✓ Result: GOOD")
        return True
    else:
        print(f"✗ State: {predicted_state}")
        return False

if __name__ == "__main__":
    print("=== Burned State Detection ===\n")
    
    # Test with your specific image
    target_image = "images/pra_cropped.png"
    print(f"Testing target image: {target_image}")
    print("-" * 50)
    result = check_burned_state(target_image)
    print(f"Final Result: {'GOOD ✓' if result else 'NOT GOOD ✗'}")
    print()
