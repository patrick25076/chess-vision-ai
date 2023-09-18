import cv2
import numpy as np
import os 
import time
import matplotlib.pyplot as plt

IMAGE_PATH=r"data\32.jpeg"
image=cv2.imread(IMAGE_PATH)
if image is None:
    raise ValueError("Could not read the input image")

def sort_corners(corners):
    """Sorting the corners to maintain a constant order
    
    Parameters:
    corners (list) -- The 4 corners of the table

    Returns:
        The sorted corners
    """  
    top_left , bottom_right , top_right , bottom_left= 0,0,0,0
    for corner in corners:
        if corner[0]<150 and corner[1]<150:
            top_left=corner
        if corner[0]>200 and corner[1]>200:
            bottom_right=corner
        if corner[0]<150 and corner[1]>200:
            bottom_left=corner
        if corner[0]>200 and corner[1]<150:
            top_right=corner
    if top_left==0 or bottom_right==0 or top_right==0 or bottom_left==0:
        raise ValueError("The input image is not clear enough")
    return top_left, top_right, bottom_right, bottom_left

def board_detection(chessboard):
    """Applying Computer Vision techniques to detect the 4 corners of the table
    
    Parameters:
    image (image) -- The image of the chessboard

    Returns:
    chessboard (image) -- the image with the rectified and cropped chessboard  
    corners (list) -- list of the 4 corners of the table
    """    
    gray_image = cv2.cvtColor(chessboard, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    _, image_result = cv2.threshold(
        blurred_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU,
    )
    edges = cv2.Canny(image_result, 100, 200)
    kernel = np.ones((3, 3), np.uint8)

    # Perform dilation
    dilated_image = cv2.dilate(edges, kernel, iterations=1)
    contours, _ = cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)
    roi = chessboard[y:y+h, x:x+w]

    # Calculate the angles of the lines connecting the corners to the center
    epsilon = 0.03 * cv2.arcLength(largest_contour, True)
    approx = cv2.approxPolyDP(largest_contour, epsilon, True)
    hull = cv2.convexHull(approx)
    corners=[tuple(hull[0][0]) , tuple(hull[1][0]) , tuple(hull[2][0]) , tuple(hull[3][0])]
    return roi ,corners

def resize_image(image,target_width):
    """Resize an image according to a width
    
    Parameters:
    image (image) -- The image 
    target_width (int) -- target width of the new image

    Returns:
    resized_image (image) -- the resized image with the target width
    """    
    original_height, original_width = image.shape[:2]
    target_height = int(original_height * (target_width / original_width))
    resized_image = cv2.resize(image, (target_width, target_height), interpolation=cv2.INTER_LINEAR)
    return resized_image

def rectify_chessboard(chessboard, corners):
    """Rectify the image to contain only the chessboard
    
    Parameters:
    chessboard (image) -- The image of the chessboard
    corners (list) -- list of the 4 corners 

    Returns:
    rectified_chessboard (image) -- rectified image of the chessboard only
    """
    top_right, bottom_right, bottom_left, top_left =corners
    # Calculate the width and height of the rectified chessboard
    width = max(np.linalg.norm(np.array(top_left) - np.array(top_right)),
                np.linalg.norm(np.array(bottom_left) - np.array(bottom_right)))
    height = max(np.linalg.norm(np.array(top_left) - np.array(bottom_left)),
                 np.linalg.norm(np.array(top_right) - np.array(bottom_right)))
    #Points for the perspective transformation
    pts=[[0, height - 1],[width - 1, 0], [width - 1, height - 1],[0, 0]]
    dst_pts = np.array([pts[2],pts[0],pts[3],pts[1]], dtype=np.float32)
    src_pts = np.array(corners, dtype=np.float32)
    #Performing the perspective transform
    perspective_transform_matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
    rectified_chessboard = cv2.warpPerspective(chessboard, perspective_transform_matrix, (int(width), int(height)))

    return rectified_chessboard
def get_squares(chessboard , corners):
    """Getting the coordinates of the corners of each square
    
    Parameters:
    image (image) -- The image of the rectified chessboard

    Returns:
    squares (list) -- list of the corners of each of the 64 squares
    """
    height,width=chessboard.shape[:2]
    print(corners)
    corners=sort_corners(corners)
    tl,tr,br,bl=corners
    x1,y1=tl
    if x1>40:
        x1=0
    x2,y2=bl
    if x2>40:
        x2=0
    num_points = 8
    slope = (y2 - y1) / (x2 - x1)
    step_x = (x2 - x1) / num_points
    step_y = slope * step_x
    points_on_line_l = [(int(x1 + i * step_x), int(y1 + i * step_y)) for i in range(num_points)]
    points_on_line_l.append(bl)
    x1_r,y1_r=tr
    if width-x1_r>40:
        x1_r+= width-x1_r-20
    x2_r,y2_r=br
    if width-x2_r>40:
        x2_r+= width-x2_r-20

    num_points = 8
    slope = (y2_r - y1_r) / (x2_r - x1_r)
    step_x = (x2_r - x1_r) / num_points
    step_y = slope * step_x
    points_on_line_r = [(int(x1_r + i * step_x), int(y1_r + i * step_y)) for i in range(num_points)]
    points_on_line_r.append(br)
    points=[]
    k=0
    for y in range(5,height+1,int((height-5)/8)):
        left_limit_x=points_on_line_l[k][0]
        right_limit_x=points_on_line_r[k][0]
        step_x=int((right_limit_x-left_limit_x)/8)
        k=k+1
        if step_x==0:
            step_x=1
        for x in range(left_limit_x,right_limit_x+1,step_x):
            points.append((x,y))
    squares={}
    k=1
    forbidden=[x for x in range(8,81,9)]
    for i ,_ in enumerate(points):
        if i==71:
            return squares
        if i not in forbidden or i==0:
            squares[k]=[points[i],points[i+1],points[i+9],points[i+10]]
            k=k+1 
    return squares
def square_detection(image,physical):
    """Combines all functions and detects the rectified chessboard , the corners of all squares 
       and the 4 corners of the table
    
    Parameters:
    image (image) -- The image of the chessboard
    physical (boolean) -- True for physical tables , False for digital tables
    
    Returns:
    squares (list) -- list of the corners of each of the 64 squares
    chessboard (image) -- the image with the rectified and cropped chessboard  
    corners (list) -- list of the 4 corners of the table
    """

    #Detect the board and the corners
    output_image,org_c=board_detection(image)
    print(org_c)
    #Resize the new image
    resized_image=resize_image(output_image,400)
    #Detect the board in the resized image
    chessboard,_=board_detection(resized_image)
    #Get the corners of the new board
    _ , resized_corners=board_detection(chessboard)
    if physical==True:
        chessboard = rectify_chessboard(chessboard, resized_corners) #used for another approach 
    squares=get_squares(chessboard,resized_corners)
    resized_corners=sort_corners(resized_corners)
    return squares,chessboard ,resized_corners

def save_to_path(folder,name,image):
    """Save to path
    
    Parameters:
    folder (string) -- The name of the folder to be created
    name (string) -- The name of the file to be created
    image (image) -- The image to be saved

    Returns:
    Saving the image to that certain path 
    """
    os.makedirs(folder, exist_ok=True)
    output_path=os.path.join(folder, f'{name}.jpeg')
    cv2.imwrite(output_path , image)
    return output_path

def show_corners(image,corners):
    """Drawing the corners for testing 
    
    Parameters:
    image (image) -- The original image
    corners (list) -- list of the 4 corners of the table

    Returns:
    Showing the image with red highlighted corners of the chessboard
    """
    cv2.circle(image, corners[0], 5, (0,0,255), -1)
    cv2.circle(image, corners[1], 5, (0,0,255), -1)
    cv2.circle(image, corners[2], 5, (0,0,255), -1)
    cv2.circle(image, corners[3], 5, (0,0,255), -1)
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def get_image_of_square(chessboard , squares , number):
    """Get the image of a certain square
    
    Parameters:
    chessboard (image) -- The image of the rectified chessboard
    squares (list) -- list of the coordinates of corners of all 64 squares
    number (int) -- the number of the selected square

    Returns:
    roi (image) -- image of selected square only 
    """
    top_left,top_right,bottom_left,bottom_right=squares[number]
    x=top_left[0]
    y=top_left[1]
    bottom_left_y=bottom_left[1]
    height=bottom_left_y-y
    top_right_x=top_right[0]
    width=top_right_x-x
    roi=chessboard[y:y+height , x:x+width,:]
    return roi

def show_table(chessboard,squares):
    """Show an image containing all 64 squares separately
    
    Parameters:
    chessboard (image) -- The image of the rectified chessboard
    squares (list) -- list of the coordinates of corners of all 64 squares

    Returns:
    fig (matplotlib figure) -- containing all 64 squares 
    """
    num_rows, num_cols = 8, 8
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(8, 8))
    k=1
    for i in range(num_rows):
        for j in range(num_cols):
            square=get_image_of_square(chessboard,squares,k)  
            k=k+1 
            rgb = cv2.cvtColor(square, cv2.COLOR_BGR2RGB)
            axes[i, j].imshow(rgb)
            axes[i, j].axis('off')  
    #plt.tight_layout()
    return fig

if __name__ == "__main__":
    start=time.time()
    squares,rectified_chessboard,corners=square_detection(image , True)
    square=get_image_of_square(rectified_chessboard,squares,2)
    fig=show_table(rectified_chessboard,squares)
    fig.show()
    plt.show()