import cv2
import numpy as np
from typing import Union, List


def fix_horizontal_light_patches(image: np.ndarray):
    """
    Corrects uneven horizontal lighting in an image using LAB color space normalization.
    
    Args:
        image (np.ndarray): Input image in BGR format (OpenCV default format).
            Expected shape is (height, width, 3).
            
    Returns:
        np.ndarray: Corrected image in BGR format with normalized horizontal lighting.
            Has the same shape as input image.
            
    Example:
        >>> corrected_img = fix_horizontal_light_patches(img)
        >>> cv2.imshow('Corrected Image', corrected_img)
    """
    
    image_lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(image_lab)

    row_means = np.mean(l, axis = 1)

    factors = 1/(row_means/np.mean(row_means))

    l_corrected = l * factors[:, np.newaxis]
    l_corrected = np.clip(l_corrected, 0, 255)
    l_corrected = l_corrected.astype(np.uint8)
    
    image_lab_corrected = cv2.merge([l_corrected, a, b])
    image_corrected = cv2.cvtColor(image_lab_corrected, cv2.COLOR_LAB2BGR)

    return image_corrected


def fix_directional_light_patches(image: np.ndarray, angle: float = 0.0) -> np.ndarray:
    """
    Corrects uneven directional lighting in an image at any specified angle while ignoring rotated image padding.
    
    Args:
        image (np.ndarray): Input image in BGR format (OpenCV default format).
            Expected shape is (height, width, 3).
        angle (float, optional): Angle of the lighting variation in degrees.
            0° is horizontal, 90° is vertical, etc.
            Positive angles are counterclockwise. Defaults to 0.0.
            
    Returns:
        np.ndarray: Corrected image in BGR format with normalized lighting.
            Has the same shape as input image.
            
    Example:
        >>> # Correct diagonal lighting at 45 degrees
        >>> corrected_img = fix_directional_light_patches(img, angle=45)
        >>> cv2.imshow('Corrected Image', corrected_img)
    """
    # Get image dimensions
    height, width = image.shape[:2]
    
    # Calculate the center of the image
    center = (width // 2, height // 2)
    
    # Create rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D(center, -angle, 1.0)
    
    # Calculate new image dimensions after rotation
    cos = np.abs(rotation_matrix[0, 0])
    sin = np.abs(rotation_matrix[0, 1])
    new_width = int((height * sin) + (width * cos))
    new_height = int((height * cos) + (width * sin))
    
    # Adjust rotation matrix to take into account translation
    rotation_matrix[0, 2] += (new_width / 2) - center[0]
    rotation_matrix[1, 2] += (new_height / 2) - center[1]
    
    # Create a mask for the original image (255 for valid pixels, 0 for padding)
    mask = np.ones((height, width), dtype=np.uint8) * 255
    
    # Rotate both image and mask
    rotated = cv2.warpAffine(image, rotation_matrix, (new_width, new_height))
    rotated_mask = cv2.warpAffine(mask, rotation_matrix, (new_width, new_height))
    
    # Convert to LAB color space
    image_lab = cv2.cvtColor(rotated, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(image_lab)
    
    # Calculate row means only for valid (non-padded) pixels
    row_means = []
    for i in range(rotated_mask.shape[0]):
        valid_pixels = l[i][rotated_mask[i] > 0]
        if len(valid_pixels) > 0:  # Only process rows with valid pixels
            row_means.append(np.mean(valid_pixels))
        else:
            row_means.append(0)
    
    row_means = np.array(row_means)
    
    # Calculate correction factors only for valid rows
    valid_rows = row_means > 0
    mean_value = np.mean(row_means[valid_rows])
    factors = np.ones_like(row_means)
    factors[valid_rows] = 1/(row_means[valid_rows]/mean_value)
    
    # Apply correction only to valid pixels
    l_corrected = l.copy()
    for i in range(l.shape[0]):
        if factors[i] > 0:
            l_corrected[i] = np.clip(l[i] * factors[i], 0, 255)
    
    l_corrected = l_corrected.astype(np.uint8)
    
    # Merge channels and convert back to BGR
    image_lab_corrected = cv2.merge([l_corrected, a, b])
    corrected = cv2.cvtColor(image_lab_corrected, cv2.COLOR_LAB2BGR)
    
    # Create inverse rotation matrix
    inverse_rotation_matrix = cv2.getRotationMatrix2D(
        (new_width // 2, new_height // 2), 
        angle, 
        1.0
    )
    
    # Adjust inverse rotation matrix for translation
    inverse_rotation_matrix[0, 2] += (width / 2) - (new_width / 2)
    inverse_rotation_matrix[1, 2] += (height / 2) - (new_height / 2)
    
    # Rotate back to original orientation
    final_image = cv2.warpAffine(corrected, inverse_rotation_matrix, (width, height))
    
    return final_image


def order_points(pts: np.ndarray):
    """
    Orders a set of 4 points in a consistent order (top-left, top-right, bottom-right, bottom-left).
    
    Args:
        pts (np.ndarray): Input array of 4 points with shape (4, 2) where each point
            is represented as [x, y] coordinates.
            
    Returns:
        np.ndarray: Array of ordered points with shape (4, 2) in float32 format.
            The points are ordered as:
            - rect[0]: top-left
            - rect[1]: top-right
            - rect[2]: bottom-right
            - rect[3]: bottom-left
            
    Example:
        >>> points = np.array([[10, 20], [30, 10], [20, 30], [40, 40]])
        >>> ordered = order_points(points)
    """

    rect = np.zeros((4, 2), dtype = "float32")
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect


def unwarp(image: np.ndarray, warp_cords: Union[np.ndarray, List], sort_points: bool = False):
    """
    Performs perspective transformation to unwarp a distorted image given four corner points.
    
    Args:
        image (np.ndarray): Input image in any color format (BGR, RGB, etc.)
        warp_cords (Union[np.ndarray, List[List[float]]]): Four points representing the
            corners of the region to be unwarped. Should be in the order:
            [top-left, top-right, bottom-right, bottom-left] if sort_points is False.
            Each point should be [x, y] coordinates.
        sort_points (bool, optional): If True, automatically sorts the input points using
            the order_points function. If False, assumes points are already in correct order.
            Defaults to False.
            
    Returns:
        np.ndarray: Unwarped (perspective-corrected) image with dimensions determined by
            the maximum width and height calculated from the input points.
            
    Example:
        >>> # Define four corner points
        >>> points = [[100, 100], [400, 100], [400, 300], [100, 300]]
        >>> # Unwarp the image
        >>> unwarped = unwarp(image, points, sort_points=True)
    """  

    if sort_points:
        rect = order_points(np.array(warp_cords))
    else:
        rect = np.asarray(warp_cords, dtype="float32").copy()
        
    (tl, tr, br, bl) = rect
    
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")
    
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped


def check_blur(image: np.ndarray, threshold: float = 100.):
    """
    Determine if an image is blurry using Laplacian variance.
    
    Args:
        image (np.ndarray): Input image in BGR format (OpenCV default format)
        threshold (float, optional): Laplacian variance threshold to determine
            blurriness. Defaults to 100.
    
    Returns:
        tuple[bool, float]: A tuple containing:
            - bool: True if image is blurry, False if sharp
            - float: The calculated Laplacian variance value
    
    Example:
        >>> is_blurry = is_blurry(img)
        >>> print(f"Image is blurry: {is_blurry[0]}, Variance: {is_blurry[1]}")
    """

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    laplacian_var = cv2.Laplacian(image, cv2.CV_64F).var()
    laplacian_var = round(laplacian_var, 0)
    
    if laplacian_var < threshold:
        return True, laplacian_var
    else:
        return False, laplacian_var
    

def calculate_iou_from_binary_masks(mask1: np.ndarray, mask2: np.ndarray) -> float:
    """
    Calculate the Intersection over Union (IoU) between two binary masks.

    Args:
        mask1 (np.ndarray): First input mask array. Can be binary or contain
            arbitrary values (will be converted to binary where >0 is True).
        mask2 (np.ndarray): Second input mask array. Can be binary or contain
            arbitrary values (will be converted to binary where >0 is True).
    
    Returns:
        float: IoU score between 0 and 1, where:
              - 0 indicates no overlap
              - 1 indicates perfect overlap
              Returns 0 if the union is 0 (both masks are empty)
    """
    
    mask1 = mask1.astype(bool)
    mask2 = mask2.astype(bool)

    intersection = np.count_nonzero(mask1 & mask2)
    union = np.count_nonzero(mask1 | mask2)

    return intersection / union if union > 0 else 0.0


def calculate_conditional_iou_from_binary_masks(mask1: np.ndarray, mask2: np.ndarray):
    """
    Calculate the conditional Intersection over Union (IoU) between two binary masks.
    
    This function computes a modified IoU where the union is determined by the smaller mask area
    instead of the traditional union of both masks. This is useful when comparing masks of
    significantly different sizes or when evaluating partial overlaps.

    Parameters:
        mask1 (numpy.ndarray): First binary mask (containing 0s and 1s or True/False)
        mask2 (numpy.ndarray): Second binary mask (containing 0s and 1s or True/False)
    
    Returns:
        float: Conditional IoU score between 0 and 1, where:
              - 0 indicates no overlap
              - 1 indicates perfect overlap
              Returns 0 if the union is 0 (both masks are empty)
    
    Note:
        The conditional IoU uses min(area1, area2) as the union instead of the
        traditional area1 + area2 - intersection formula.
    """
    
    mask1 = mask1.astype(bool)
    mask2 = mask2.astype(bool)

    intersection = np.count_nonzero(mask1 & mask2)
    union = min(np.count_nonzero(mask1), np.count_nonzero(mask2))

    return intersection / union if union > 0 else 0.0