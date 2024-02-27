# Intruder-Detector
The Google AIY Vision Kit is set up to detect and take a picture when a face is recognized and send as a text or email with a timestamp to your smartphone or email account.

Catch that guy stealing your yogurt.  You can use the AIY Vision Kit to take a picture and send the image to yourself by sms text or email.  The AIY kit includes a neural net chip (Vision Bonnet) as well as the necessary software models to recognize a human face.  You must add a raspberry pi zero W, a raspberry pi camera, and an sd card.  They are all contained in an inconspicuous cardboard box.  The python program "face_camera_trigger.py" can start at boot time of the vision kit. 

Setup required:
1.  Create a free smtp2go account and record the password and username to send text and email.
2.  To execute at boot time, put the "face_camera_detect.service" file in the /lib/systemd/system directory.  Edit the file so that it reflects the location of the python file.  In a terminal window of the AIY pi zero, start the service with the command "systemctl enable --now face_camera_trigger.service."
3.  Edit the "face_camera_detect.py" file to reference 1) the smtp2go username and password, 2) your smartphone number, 3) your email address.

The Vision Kit uses a lot of power when the face model is deployed.  Best to use plugged in (power port not data port) and not by battery.  

Of course, you could use a PIR motion sensor to detect an intruder and trigger pictures but there would be no guarantee of a recognizable face image.  And that would bypass the Vision Bonnet which is the whole point of the Vision Kit.
