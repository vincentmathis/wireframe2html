import argparse
import sys

import cv2 as cv
import imutils
import numpy as np

import logger


def resize_to_target_size(image):
    longer_side = max(image.shape)
    target_size = 1600
    scaling = target_size / longer_side
    # Choose better interpolation Method depending on down or upscaling
    interpolation = cv.INTER_CUBIC if scaling > 1 else cv.INTER_AREA
    return cv.resize(image, (0, 0), fx=scaling, fy=scaling, interpolation=interpolation)


def assess_noise(image):
    img_blur = cv.GaussianBlur(image, (9, 9), 0)
    mse, _ = cv.quality.QualityMSE_compute(image, img_blur)
    if mse[0] > 1000:
        logger.log_warning("Image might be too noisy")


def assess_blur(image):
    laplacian_variance = cv.Laplacian(image, cv.CV_64F).var()
    if laplacian_variance < 200:
        logger.log_warning("Image might be too blurry")


def detect_ridges(image):
    ridge_filter = cv.ximgproc.RidgeDetectionFilter_create(scale=0.3)
    ridges = ridge_filter.getRidgeFilteredImage(image)
    _, thresh = cv.threshold(ridges, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    return thresh


def close_gaps(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv.dilate(image, kernel, iterations=4)


def find_external_contours(image):
    contours, _ = cv.findContours(image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    external_contours = []
    for contour in contours:
        epsilon = 0.04 * cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, epsilon, True)
        # Not the right shape
        if len(approx) != 4 or not cv.isContourConvex(approx):
            continue
        # Too small
        if cv.contourArea(approx) < 4096:
            continue
        external_contours.append(contour)

    count = len(external_contours)
    if count == 0:
        logger.log_failure("Couldn't find any elements")
        sys.exit(1)
    logger.log_info(f"Extracted {count} elements")
    external_contours.sort(key=lambda x: x[0].min(axis=0)[1])
    return external_contours


def remove_external_contours(image, contours):
    mask = np.zeros_like(image)
    cv.drawContours(mask, contours, -1, 255, -1)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv.erode(mask, kernel, iterations=6)
    out = np.zeros_like(image)
    out[mask == 255] = image[mask == 255]
    return out


def extract_elements(image, contours):
    elements = []
    for contour in contours:
        center, size, angle = cv.minAreaRect(contour)
        x_pos, y_pos, width, height = cv.boundingRect(contour)
        x_pos += 10
        y_pos += 10
        width -= 20
        height -= 20
        bbox = [x_pos, y_pos, width, height]
        crop = image[y_pos : y_pos + height, x_pos : x_pos + width]
        angle = angle if angle > -45 else 90 + angle
        rotated = imutils.rotate(crop, angle)
        elements.append([rotated, bbox])
    return elements


def get_elements_from_path(path):
    img = cv.imread(path, cv.IMREAD_GRAYSCALE)
    return get_elements_from_image(img)


def get_elements_from_image(image):
    assess_noise(image)
    img_resized = resize_to_target_size(image)
    assess_blur(img_resized)
    img_segmented = detect_ridges(img_resized)
    img_closed_gaps = close_gaps(img_segmented)
    external_contours = find_external_contours(img_closed_gaps)
    img_cleaned = remove_external_contours(img_segmented, external_contours)
    elements = extract_elements(img_cleaned, external_contours)
    return img_resized, elements


def process_image_from_args(args):
    bboxes, crops = get_elements_from_path(args.image)
    if args.show_crops:
        for crop in crops:
            cv.imshow("CROP", crop)
            cv.waitKey(0)
    if args.write_crops:
        for i, crop in enumerate(crops):
            out_filename = args.image.replace(".jpg", f"_crop_{i}.png")
            cv.imwrite(out_filename, crop)


def main():
    parser = argparse.ArgumentParser(description="Extract wireframes from image.")
    parser.add_argument("image")
    parser.add_argument("-s", "--show-crops", action="store_true")
    parser.add_argument("-w", "--write-crops", action="store_true")
    parser.set_defaults(func=process_image_from_args)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
