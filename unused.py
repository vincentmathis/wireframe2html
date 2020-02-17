# from skimage.morphology import skeletonize
# from skimage.util import img_as_float, img_as_ubyte


# def to_threshold(image, inverted=False):
#     method = cv.THRESH_BINARY_INV if inverted else cv.THRESH_BINARY
#     _, thresh = cv.threshold(image, 0, 255, cv.THRESH_OTSU | method)
#     return thresh


# def detect_edges(image):
#     # sigma?
#     return imutils.auto_canny(image)


# def fill_holes(image):
#     _, image = cv.threshold(image, 0, 255, cv.THRESH_OTSU | cv.THRESH_BINARY_INV)
#     kernel = np.ones((5, 5), np.uint8)
#     img_dilated = cv.dilate(image, kernel, iterations=3)
#     # cv.imshow("dilated", img_dilated)
#     # cv.waitKey(0)

#     height, width = img_dilated.shape[:2]
#     mask = np.zeros((height + 2, width + 2), np.uint8)
#     # Floodfill from black point
#     img_floodfill = img_dilated.copy()
#     for y in range(0, height, 10):
#         for x in range(0, width, 10):
#             if img_dilated[y, x] == 0.0:
#                 cv.floodFill(img_floodfill, mask, (x, y), 255)
#                 break

#     # Invert floodfilled image
#     img_floodfill_inv = cv.bitwise_not(img_floodfill)

#     # Combine the two images to get the foreground.
#     img_out = img_dilated | img_floodfill_inv
#     return img_out


# def detect_corners(image):
#     img_float = np.float32(image)
#     dst = cv.cornerHarris(img_float, 10, 9, 0.04)
#     # result is dilated for marking the corners, not important
#     dst = cv.dilate(dst, None)
#     # Threshold for an optimal value, it may vary depending on the image.
#     image = cv.cvtColor(image, cv.COLOR_GRAY2BGR)
#     image[dst > 0.01 * dst.max()] = [0, 0, 255]
#     cv.imwrite("corner_detection_filled_001.jpg", image)


# def normalize_linethickness(image):
#     skel = imutils.skeletonize(image, size=(3, 3))
#     cv.imwrite("images/skeletonize-input.jpg", cv.bitwise_not(image))
#     cv.imwrite("images/skeletonize-imutils.jpg", skel)
#     image[image == 255] = 1
#     ski_image = img_as_float(image)
#     ski_skel = skeletonize(image)
#     cv_skel = img_as_ubyte(ski_skel)
#     cv.imwrite("images/skeletonize-skimage.jpg", cv_skel)
#     kernel = np.ones((3, 3), np.uint8)
#     skel_dilated = cv.dilate(skel, kernel, iterations=1)
#     return skel_dilated


# def crop_bboxes_from_image(image, contours):
#     crops = []
#     for contour in contours:
#         bbox = x_pos, y_pos, width, height = cv.boundingRect(contour)
#         crop = image[y_pos : y_pos + height, x_pos : x_pos + width]
#         crops.append((bbox, crop))
#     return crops


# def crop_polys_from_image(image, contours):
#     crops = []
#     for contour in contours:
#         epsilon = 0.04 * cv.arcLength(contour, True)
#         approx = cv.approxPolyDP(contour, epsilon, True)
#         approx.reshape(4, 2)
#         warped = four_point_transform(image, approx.reshape(4, 2))
#         crops.append(warped)
#     return crops


# def four_point_transform(image, pts):
#     # obtain a consistent order of the points and unpack them
#     # individually
#     rect = order_points(pts)
#     (top_l, top_r, bot_r, bot_l) = rect

#     # compute the width of the new image, which will be the
#     # maximum distance between bottom-right and bottom-left
#     # x-coordiates or the top-right and top-left x-coordinates
#     width_a = np.sqrt(((bot_r[0] - bot_l[0]) ** 2) + ((bot_r[1] - bot_l[1]) ** 2))
#     width_b = np.sqrt(((top_r[0] - top_l[0]) ** 2) + ((top_r[1] - top_l[1]) ** 2))
#     max_width = max(int(width_a), int(width_b))

#     # compute the height of the new image, which will be the
#     # maximum distance between the top-right and bottom-right
#     # y-coordinates or the top-left and bottom-left y-coordinates
#     height_a = np.sqrt(((top_r[0] - bot_r[0]) ** 2) + ((top_r[1] - bot_r[1]) ** 2))
#     height_b = np.sqrt(((top_l[0] - bot_l[0]) ** 2) + ((top_l[1] - bot_l[1]) ** 2))
#     max_height = max(int(height_a), int(height_b))

#     # now that we have the dimensions of the new image, construct
#     # the set of destination points to obtain a "birds eye view",
#     # (i.e. top-down view) of the image, again specifying points
#     # in the top-left, top-right, bottom-right, and bottom-left
#     # order
#     dst = np.array(
#         [
#             [0, 0],
#             [max_width - 1, 0],
#             [max_width - 1, max_height - 1],
#             [0, max_height - 1],
#         ],
#         dtype="float32",
#     )

#     # compute the perspective transform matrix and then apply it
#     matrix = cv.getPerspectiveTransform(rect, dst)
#     warped = cv.warpPerspective(image, matrix, (max_width, max_height))

#     # return the warped image
#     return warped


# def order_points(pts):
#     x_sorted = sorted(pts, key=lambda p: p[0])
#     xy_sorted_left = sorted(x_sorted[:2], key=lambda p: p[1])
#     xy_sorted_right = sorted(x_sorted[2:], key=lambda p: p[1])

#     # topleft, topright, bottomright, bottomleft
#     return np.array(
#         [
#             xy_sorted_left[0],
#             xy_sorted_right[0],
#             xy_sorted_right[1],
#             xy_sorted_left[1],
#         ],
#         dtype="float32",
#     )


# Replace crops
# import glob
# import os

# src_files = glob.glob("data-raw/*_crop_*.png")
# dest_files = glob.glob("data/*/*_crop_*.png")
# for src_path in src_files:
#     for dest_path in dest_files:
#         if os.path.basename(src_path) == os.path.basename(dest_path):
#             print(src_path, dest_path)
#             os.replace(src_path, dest_path)
