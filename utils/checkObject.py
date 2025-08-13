import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

BACKGROUND_IMAGE_PATH = "./images/no_object.png" # This should be the image of the empty area
CURRENT_IMAGE_PATH = "./images/pra_cropped_gray.png"
CHANGE_THRESHOLD = 30
MIN_OBJECT_AREA = 500 # Example: A small biscuit might be 500-1000 pixels or more
# --- Helper Function to Load Image Safely ---
def load_image_safely(path, name="Image"):
    """Loads an image and checks if it was loaded successfully."""
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"{name} not found at '{path}'. Please check the path.")
    return img

# --- Main Detection Logic ---
def detect_object_presence(background_img_path, current_img_path):
    """
    Detects if an object is present in the current image by comparing it to a background.

    Args:
        background_img_path (str): Path to the image of the empty background.
        current_img_path (str): Path to the current image (with or without object).

    Returns:
        tuple: (bool) True if an object is detected, False otherwise.
               (numpy.ndarray) The image with detected changes highlighted.
    """
    print(f"Loading background image from: {background_img_path}")
    background_img = load_image_safely(background_img_path, "Background Image")

    print(f"Loading current image from: {current_img_path}")
    current_img = load_image_safely(current_img_path, "Current Image")

    # Ensure images are of the same size
    if background_img.shape != current_img.shape:
        print("Warning: Background and current images have different dimensions. Resizing current image.")
        current_img = cv2.resize(current_img, (background_img.shape[1], background_img.shape[0]))

    # Convert both images to grayscale for comparison
    gray_background = cv2.cvtColor(background_img, cv2.COLOR_BGR2GRAY)
    gray_current = cv2.cvtColor(current_img, cv2.COLOR_BGR2GRAY)

    # Compute the absolute difference between the two grayscale images
    # This highlights areas where changes have occurred
    diff_img = cv2.absdiff(gray_background, gray_current)
    print("Computed absolute difference between images.")

    # Apply a threshold to the difference image to get a binary mask of changes
    # Pixels with difference > CHANGE_THRESHOLD become white (255), others black (0)
    _, thresh_img = cv2.threshold(diff_img, CHANGE_THRESHOLD, 255, cv2.THRESH_BINARY)
    print(f"Applied thresholding to difference image with threshold: {CHANGE_THRESHOLD}")

    # Perform morphological operations to clean up noise and fill small gaps
    # Opening (erosion followed by dilation) removes small white noise (speckles)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)) # Adjust kernel size if needed
    thresh_img_clean = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, kernel, iterations=2)
    # Closing (dilation followed by erosion) fills small black holes in white regions
    thresh_img_clean = cv2.morphologyEx(thresh_img_clean, cv2.MORPH_CLOSE, kernel, iterations=2)
    print("Performed morphological operations to clean the mask.")

    # Find contours in the cleaned thresholded image
    # Contours represent continuous boundaries of objects
    contours, _ = cv2.findContours(thresh_img_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f"Found {len(contours)} contours.")

    object_detected = False
    output_display_img = current_img.copy() # Create a copy to draw on

    # Iterate through detected contours and check their area
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > MIN_OBJECT_AREA:
            object_detected = True
            # Draw a bounding box around the detected object
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(output_display_img, (x, y), (x + w, y + h), (0, 255, 0), 2) # Green rectangle
            cv2.putText(output_display_img, f"Object ({int(area)}px)", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            print(f"  - Significant object detected with area: {area} pixels.")
        else:
            print(f"  - Small change (area: {area} pixels) ignored as noise.")

    return object_detected, output_display_img, diff_img, thresh_img_clean

# --- Main Execution ---
def idObjectPresent() -> bool:
    """
    Checks if an object is present in the current image by comparing it to a background image.
    Returns:
        bool: True if an object is detected, False otherwise.
    """
    if not os.path.exists(BACKGROUND_IMAGE_PATH):
        print(f"Creating a dummy background image at {BACKGROUND_IMAGE_PATH}")
        dummy_bg = np.zeros((400, 600, 3), dtype=np.uint8)
        dummy_bg.fill(150) # Fill with a medium gray color
        cv2.putText(dummy_bg, "BACKGROUND (No Object)", (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imwrite(BACKGROUND_IMAGE_PATH, dummy_bg)

    # Perform detection
    is_object_present, result_img, diff_img, clean_mask = \
        detect_object_presence(BACKGROUND_IMAGE_PATH, CURRENT_IMAGE_PATH)


    print("\n--- Detection Result ---")
    if is_object_present:
        print("STATUS: Object Detected!")
        return True
    else:
        print("STATUS: No Object Detected.")
        return False

if __name__ == "__main__":
    idObjectPresent()