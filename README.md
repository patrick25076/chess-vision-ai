# 3D Chess Vision AI

#### <ins>Chess computer vision project that converts physical chessboard positions into digital images and recommend the next best move! </ins>

![first_photo](https://github.com/patrick25076/chess-vision-ai/assets/113384811/7692f786-10e5-40da-a14d-d4941b6412e1)

## Table of Contents

1. [Project](#project)
   - [Board Detection](#board-detection)
   - [Piece Recognition](#piece-recognition)
   - [Final Results](#final-results)
2. [Project Status](#project-status)
3. [How To Use](#how-to-use)
4. [Contact](#contact)

## Project

Welcome to the **3D Chess Vision AI** project, where we combine computer vision, machine learning, and the world of chess to transform physical chessboard images into digital representations. This project serves as a bridge between the physical and digital chess worlds, offering chess enthusiasts a seamless way to analyze and enjoy their games.

### Overview

1. **Image Input**: The project begins with you providing an image of a physical chessboard, taken under varying lighting conditions and with different chess set designs.

2. **Board Detection**: Employing advanced computer vision techniques, the system accurately identifies the boundaries of the chessboard within the image. This process involves:
   - Grayscale conversion
   - Gaussian blurring
   - Thresholding
   - Canny edge detection
   - Contour finding
   - Largest contour selection

3. **Piece Recognition**: Utilizing a pre-trained model, the system recognizes and classifies chess pieces within each square of the board. The model boasts an impressive 80.2% mean average precision (MAP), 93.0% precision, and 75.0% recall, making it proficient at piece identification. The model credits the dataset used for training, available [here](https://universe.roboflow.com/mywork-45pbb/chessv1-ghvlw).

4. **FEN Notation Transformation**: With the pieces identified, the system generates the FEN (Forsyth-Edwards Notation) representation of the chessboard. This concise notation captures the current state of the game, including piece positions and the active player.

5. **Digital Transformation**: The project culminates in the transformation of the physical chessboard into a digital format. Users can analyze their games, obtain links to analyze them on platforms like Lichess, and even receive the best move suggestions from the Stockfish chess engine.

### Project Objectives

The primary goal of the **3D Chess Vision AI** project is to foster personal learning and skill improvement in the realms of computer vision, image processing, and machine learning. It offers chess enthusiasts a unique opportunity to enhance their understanding of these fields while indulging in their passion for the game.

### Limitations

It's essential to acknowledge the project's limitations:
- The system's performance may vary based on lighting conditions and chess set designs.
- In complex board positions, the model may occasionally misclassify pieces.
- The project's primary focus is personal use and may not be suitable for high-stakes or competitive chess analysis.

In conclusion, the **3D Chess Vision AI** project delivers a holistic solution for transforming physical chess games into digital ones. With robust board detection, accurate piece recognition, and FEN notation generation, it offers chess enthusiasts an innovative tool to enrich their chess-playing experiences.


## Board Detection

The **3D Chess Vision AI** project employs advanced computer vision techniques to accurately detect the boundaries of the chessboard within a given image. This crucial step lays the foundation for subsequent piece recognition and digital transformation.

### Techniques Utilized

#### 1. Image Preprocessing
   - **Grayscale Conversion:** The first step involves converting the input image to grayscale. This simplifies subsequent processing by reducing the dimensionality of the image.
   - **Gaussian Blurring:** A Gaussian blur is applied to reduce noise and smoothen the image, making it easier to identify edges.
   - **Thresholding:** The image is thresholded using Otsu's method to create a binary image, enhancing the visibility of edges.

#### 2. Edge Detection
   - **Canny Edge Detection:** Canny edge detection is employed to identify sharp changes in pixel intensity, highlighting edges within the image.
   
#### 3. Contour Detection
   - **Dilation:** Dilation is applied to the edges to connect broken lines and make it easier to find contours.
   - **Contour Finding:** The project then identifies contours in the dilated image. Contours are continuous curves that outline objects or regions of interest.

#### 4. Largest Contour Selection
   - **Selecting the Largest Contour:** Among the detected contours, the project identifies the largest one, as it corresponds to the chessboard.

#### 5. Convex Hull
   - **Approximation and Convex Hull:** The project approximates the largest contour to reduce the number of vertices. It then calculates the convex hull of the approximation to determine the corners of the chessboard.

### Significance
Accurate board detection is crucial for several reasons:
- It defines the region of interest for subsequent piece recognition.
- Properly rectified images ensure that piece recognition models perform optimally.
- It bridges the gap between the physical and digital chess worlds, enhancing the overall chess-playing experience.

### Challenges
While the techniques employed are powerful, challenges may arise:
- Complex or non-standard chessboard orientations may pose difficulties.
- Varied lighting conditions can affect the quality of edge detection.
- Highly cluttered backgrounds may interfere with contour identification.

In summary, the **3D Chess Vision AI** project leverages a combination of image preprocessing, edge detection, and contour analysis techniques to robustly detect the chessboard within images. This precise detection sets the stage for accurate piece recognition and the digital transformation of physical chess games.

![Board](https://github.com/patrick25076/chess-vision-ai/assets/113384811/f835ea36-50f2-4af0-afe3-6aff5c39ffe4)

## Piece Recognition

The heart of the project lies in piece recognition, which involves using a pre-trained machine learning model provided by Roboflow. This model has demonstrated an impressive Mean Average Precision (mAP) of **80.2%**, showcasing its ability to accurately identify chess pieces. The model achieves a remarkable precision of **93.0%** and a recall rate of **75.0%**, making it a reliable choice for classifying chess pieces.

The model used in this project owes its success to the high-quality chess dataset it was trained on. The dataset is credited to its owner and can be found at [this link](https://universe.roboflow.com/mywork-45pbb/chessv1-ghvlw). It plays a pivotal role in training models for chess piece recognition.

The piece recognition component provides information about the pieces on the board and their positions, enabling the digital transformation of physical chess games.

Please note that while the model's performance is impressive, the accuracy of the piece recognition may still vary based on factors such as image quality, lighting conditions, and the specific chess set used. Adjustments and fine-tuning may be necessary to optimize its performance for your specific chessboard setup.

In summary, the **3D Chess Vision AI** project leverages state-of-the-art machine learning models to achieve accurate chess piece recognition, contributing to the seamless transformation of physical chess games into digital experiences.

![Piece_Recognition](https://github.com/patrick25076/chess-vision-ai/assets/113384811/c9af7daf-1c12-4c36-8c81-0a74541ec8fa)


## Final Results
The primary objective of the **3D Chess Vision AI** project is personal learning and skill improvement in the fields of computer vision and machine learning. While the project offers a compelling solution for transforming physical chessboards into digital ones, it's essential to set realistic expectations regarding its performance.

### Objectives and Learning
This project serves as a valuable opportunity for personal learning and skill enhancement. It provides hands-on experience in various domains, including computer vision, image processing, machine learning, and chess-related applications. Building and fine-tuning such a project not only contribute to technical expertise but also foster problem-solving and critical thinking skills.

### Variability in Results
The performance of the project may vary depending on several factors:

- **Lighting Conditions:** The quality and consistency of lighting during image capture play a crucial role. Varied lighting conditions can impact the accuracy of board detection and piece recognition.

- **Chess Sets:** The project's success is influenced by the type and design of the chess set used. Unique piece designs or non-standard boards may pose challenges for recognition.

- **Image Quality:** While a clear and well-framed image is advantageous, it's essential to note that even in ideal conditions, the project may not achieve perfect results. The piece recognition component, despite its impressive 80% accuracy, may occasionally misclassify pieces.

### Limitations
It's important to acknowledge the project's limitations:

- **Complex Positions:** Highly complex chessboard positions with many pieces in close proximity can pose challenges for accurate piece recognition.

- **Adjustments Required:** Depending on your specific chessboard and environmental conditions, adjustments and fine-tuning of the code may be necessary to optimize performance.

- **Practical Usage:** While the project can be a valuable tool for personal use, it may not be suitable for high-stakes or competitive chess analysis due to its occasional inaccuracies.

In summary, the **3D Chess Vision AI** project offers an exciting journey of personal growth and learning. It provides insights into the intricacies of computer vision and machine learning while serving as a bridge between the physical and digital chess worlds. Keep in mind that the project's performance is influenced by various factors, and achieving perfection in every scenario may not be attainable. Nevertheless, it remains a valuable tool for chess enthusiasts looking to enhance their chess-playing experiences.

![Final](https://github.com/patrick25076/chess-vision-ai/assets/113384811/905e9a14-7ad4-4e3d-bb43-9c2ceaa82921)

## Project Status

The **3D Chess Vision AI** project has made significant strides and is nearly ready to fulfill its intended purpose of transforming physical chessboard images into digital representations. However, it's crucial to clarify that this is a personal project and not an advanced, ready-for-deployment application.

#### Almost Ready

The core functionalities of the project are in place, allowing for the detection of chessboards, piece recognition, and FEN notation generation. These functionalities, while functional, leave ample room for enhancement and refinement.

#### Opportunities for Improvement

- **UI/UX Integration**: While the project functions, there is room for improvement in terms of user interface and user experience (UI/UX). Integrating a more intuitive and user-friendly interface would greatly enhance the project's accessibility and usability.

- **Model Enhancement**: The current model performs admirably with an 80.2% mean average precision (MAP). Collaborators with expertise in machine learning can explore opportunities to find even more robust models that enhance piece recognition accuracy.

- **Lighting Conditions**: Adapting the project to different lighting conditions remains a challenge. Exploring advanced computer vision techniques to improve the system's resilience to varying lighting scenarios is a worthwhile endeavor.

#### Collaboration and Contribution

While this project is personal in nature, enthusiasts are welcomed with open arms to explore, experiment, and contribute. If you are passionate about chess, computer vision, machine learning, or any related field and wish to join in enhancing this project, your contributions are genuinely valued.

Please feel free to [contact me](mailto:your.email@example.com) if you have ideas, insights, or the desire to collaborate on making the **3D Chess Vision AI** project even more refined and versatile. Remember that this project is a personal exploration and learning experience, and your involvement can help it reach new heights.

In summary, the **3D Chess Vision AI** project is nearing completion, with exciting opportunities for enhancement. While it remains a personal project, your enthusiasm and contributions can play a vital role in its evolution.


## How to Use

Follow these step-by-step instructions to set up and run the 3D Chess Vision AI project:

**Step 1: Install Required Packages**

Before getting started, ensure you have all the necessary packages installed. Run the following command to install them:

```bash
!pip install -r requirements.txt
```
**Step 2: Clone the Repository**

Clone your project repository using the following command:

```bash
!git clone https://github.com/yourusername/your-chess-vision-repo.git
```
**Step 3: Install Stockfish Engine**

To enable chess analysis, you'll need to install the Stockfish engine, a powerful open-source chess engine.

1. **Download Stockfish:** Visit the [Stockfish Official Website](https://stockfishchess.org/download/) to download the Stockfish binary suitable for your operating system.

2. **Set Stockfish Path:** In the code, locate the section that says "#your stockfish path." Replace it with the actual path to the Stockfish binary you downloaded.

   Example:
   ```python
   STOCKFISH_PATH = '/path/to/stockfish'  # Replace with your Stockfish binary path
  
**Step 4: Set Image Path**

Before running the project, you need to specify the path to your input chessboard image.

1. **Set the Image Path:** In the code, locate the section that says "#your image path." Replace it with the actual path to your input chessboard image.

   Example:
   ```python
   # Set the path to your input chessboard image here
   # Replace '/path/to/your/image.jpg' with the actual image path
   IMAGE_PATH = '/path/to/your/image.jpg'
**Step 5: Run Your Project**

Now that you've configured the project and set the necessary paths, it's time to run it and get the results.

1. **Open Your Terminal:** Open your terminal or command prompt.

2. **Navigate to Your Project Directory:** Use the `cd` command to navigate to your project directory where you've cloned the repository.

3. **Execute the Project:** Run the following command to execute the main.py script:

   ```bash
   python main.py
   
## Contact

- Neicu Patrick
- GitHub: [Profile](https://github.com/yourusername](https://github.com/patrick25076))
- Email: patrickneicu2006@gmail.com
- LinkedIn: [Profile](https://www.linkedin.com/in/patrick-neicu-4bb567263/)
