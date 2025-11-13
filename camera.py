# 1. Import the deepface library
from deepface import DeepFace

# 2. Tell the program which picture to analyze
my_image = "img1.jpg" 

# 3. This is the main command. 
#    It tells deepface to "analyze" the image and find these "actions".
results = DeepFace.analyze(
    img_path = my_image, 
    actions = ['age', 'gender', 'emotion', 'race'],
    detector_backend = 'retinaface'
)

# 4. Print the results to the screen
print(results)