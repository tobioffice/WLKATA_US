import cv2
import os
import numpy as np

def capture_snapshot(output_path='pra.png'):
    cap = cv2.VideoCapture(2)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return False

    ret, frame = cap.read()
    cap.release()
    if not ret:
        print("Failed to capture image from webcam.")
        return False

    cv2.imwrite(output_path, frame)
    print(f"Snapshot saved to: {output_path}")
    return True

def crop_image_with_limits(image, x, y, w, h):
    height, width = image.shape[:2]
    x_end = min(x + w, width)
    y_end = min(y + h, height)

    if x >= width or y >= height:
        raise ValueError("Crop start position is outside the image boundaries.")

    cropped = image[y:y_end, x:x_end]
    return cropped

def processImagesAndSave():
    save_folder = "./images/"
    image_path = os.path.join(save_folder, "pra.png")

    # Capture snapshot first
    if not capture_snapshot(output_path=image_path):
        return

    # Load the saved image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Failed to load image from {image_path}")
        return

    # Crop parameters (adjust as needed)
    crop_x = 215
    crop_y = 80
    crop_width = 120
    crop_height = 180

    try:
        cropped_img = crop_image_with_limits(img, crop_x, crop_y, crop_width, crop_height)
    except ValueError as e:
        print("Error:", e)
        return

    # Convert to grayscale
    gray_cropped_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)

    # Convert grayscale to binary using Otsu's thresholding
    _, binary_image = cv2.threshold(gray_cropped_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)


    # Ensure save folder exists
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    cropped_color_path = os.path.join(save_folder, "pra_cropped.png")
    cropped_gray_path = os.path.join(save_folder, "pra_cropped_gray.png")
    binary_image_path = os.path.join(save_folder, "pra_binary.png")

    # Save images
    cv2.imwrite(cropped_color_path, cropped_img)
    cv2.imwrite(cropped_gray_path, gray_cropped_img)
    cv2.imwrite(binary_image_path, binary_image)

    print(f"Cropped color image saved at: {cropped_color_path}")
    print(f"Cropped grayscale image saved at: {cropped_gray_path}")
    print(f"Binary image saved at: {binary_image_path}")

if __name__ == "__main__":
    processImagesAndSave()
    print("Image processing and saving completed.")