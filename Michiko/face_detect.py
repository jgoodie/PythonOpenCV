import cv2
import sys
 
 
class FaceDetector():
    def face_count(self, fpath):
        # Get user supplied values
        imagePath = fpath
        cascPath = "haarcascade_frontalface_default.xml"
        
        # Create the haar cascade
        faceCascade = cv2.CascadeClassifier(cascPath)
        
        # Read the image
        image = cv2.imread(imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
        # Detect faces in the image
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
            #flags = cv2.CV_HAAR_SCALE_IMAGE
        )
        
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
 
        # Write image
        cv2.imwrite("./images/_out.jpg", image)
 
        # return number of faces
        return len(faces)
 
    
if __name__ == "__main__":
    fd = FaceDetector()
    print(fd.face_count("image.jpg"))
