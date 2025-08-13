import cv2
import numpy as np
import math

# --- Helper function to calculate the angle ---
def calculate_angle(p1, p2, p3):
    """
    Calculates the angle in degrees at vertex p2, formed by the vectors p1-p2 and p3-p2.
    """
    vec1 = (p1[0] - p2[0], p1[1] - p2[1])
    vec2 = (p3[0] - p2[0], p3[1] - p2[1])
    dot_product = vec1[0] * vec2[0] + vec1[1] * vec2[1]
    mag_vec1 = math.sqrt(vec1[0]**2 + vec1[1]**2)
    mag_vec2 = math.sqrt(vec2[0]**2 + vec2[1]**2)
    
    if mag_vec1 == 0 or mag_vec2 == 0:
        return 0
        
    cosine_angle = dot_product / (mag_vec1 * mag_vec2)
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
    angle_rad = math.acos(cosine_angle)
    return math.degrees(angle_rad)

# --- Main script ---


def isAreaAndAngleGood() -> bool:
    """
    Checks if the area and angles of a binary image are within specified ranges.
    Returns:
        bool: True if both area and angles are within the specified ranges, False otherwise.
    """

    # --- Define Evaluation Ranges ---
    MIN_AREA = 10200
    MAX_AREA = 12000
    MIN_ANGLE = 86.0
    MAX_ANGLE = 94.0

    # Path to your binary image
    image_path = "./images/pra_binary.png"

    # Load the binary image (ensure it's loaded as grayscale)
    binary_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if binary_image is None:
        raise FileNotFoundError(f"Image '{image_path}' not found or could not be opened.")

    # Ensure the image is truly binary (values 0 and 255 only)
    _, binary_image = cv2.threshold(binary_image, 127, 255, cv2.THRESH_BINARY)

    # ===============================================================
    # === 1. Area Calculation ===
    # ===============================================================

    # Calculate area: count of white pixels (pixel value 255)
    area = np.sum(binary_image == 255)
    # print(f"--- Calculated Area ---")
    print(f"Area (number of white pixels): {area}\n")


    # ===============================================================
    # === 2. Find and Output Angles ===
    # ===============================================================
    # print("--- Calculated Angles ---")

    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    calculated_angles = []

    if not contours:
        print("No contours were found in the image.")
    else:
        main_contour = max(contours, key=cv2.contourArea)
        perimeter = cv2.arcLength(main_contour, True)
        approx_corners = cv2.approxPolyDP(main_contour, 0.02 * perimeter, True)
        points = [tuple(p[0]) for p in approx_corners]
        num_corners = len(points)

        if num_corners < 3:
            print("Shape has too few vertices to calculate angles.")
        else:
            for i in range(num_corners):
                p1 = points[i - 1]
                p2 = points[i]
                p3 = points[(i + 1) % num_corners]
                angle = calculate_angle(p1, p2, p3)
                calculated_angles.append(angle)

    if not calculated_angles:
        print("No angles were calculated.")
    # else:
    #     for i, angle in enumerate(calculated_angles):
    #         print(f"Angle {i+1}: {angle:.2f} degrees")


    # ===============================================================
    # === 3. Evaluation Section ===
    # ===============================================================
    print("\n--- Evaluation Result ---")

    # Evaluate Area
    is_area_good = MIN_AREA <= area <= MAX_AREA
    area_status = "Good" if is_area_good else "Bad"
    print(f"Area Status: {area_status} (Range: {MIN_AREA}-{MAX_AREA})")

    # Evaluate Angles
    # Condition: Must be a 4-corner shape AND all angles must be in range.
    is_angle_count_correct = (len(calculated_angles) == 4)
    all_angles_in_range = all(MIN_ANGLE <= angle <= MAX_ANGLE for angle in calculated_angles)

    is_angles_good = is_angle_count_correct and all_angles_in_range
    angle_status = "Good" if is_angles_good else "Bad"

    # Provide detailed reason for bad angle status
    if not is_angle_count_correct:
        reason = f"Expected 4 corners, but found {len(calculated_angles)}."
    elif not all_angles_in_range:
        reason = "One or more angles were outside the range."
    else:
        reason = "" # No reason needed if good

    print(f"Angle Status: {angle_status} (Range for all 4 angles: {MIN_ANGLE}-{MAX_ANGLE})")
    # if not is_angles_good:
    #     print(f"  - Reason: {reason}")


    # --- Final Verdict ---
    if is_area_good and is_angles_good:
        return True
    else:
        return False
