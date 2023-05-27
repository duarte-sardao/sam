Steps to execute the application:

1. Install the requirements by running command "pip install -r requirements"
2. Open and execute the application by running command "python interface.py"

Some notes:
 - At this moment, the application is not working on Apple silicon based MacBooks. We have no Intel based Mac to comprove it, but we suspect that the application runs on this machines. On Windows the application is 100% supported
 - Depending on the PC pre-existing configuration, you might have to install tkinter manually, which varies by Python installation.
 - If the user doesn't want to install the requirements on their general python environment they can:
	1. Create an environment using command "conda create --name <environmentName>"
	2. Activate the environment by running command "conda activate <environmentName>"
	3. Install requirements and execute as normal

Application functionalities:
 - Chroma key editor: Allows users to remove a user-specified color (Red,Green or Blue) from the image and to replace it with another image (like a green screen)
 - Audio editor: Allows users to crop audio files, alter it's speed (mantaining pitch or not) and to loop it until a set time.
 - Picture album video: Allows users to create video from chosen images, with a selected audio playing in the background. The image transitions can be adjusted by using the slide selector. A transition length of 100% means the current image will start to transition to the next one immediately, while a 0% means no transition (fade) occurs.