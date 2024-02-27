#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# modified by C. Masenas 26FEB24
"""Trigger PiCamera when face is detected and send image via text and/or email."""

from aiy.vision.inference import CameraInference
from aiy.vision.models import face_detection

from picamera import PiCamera


def main():
################## This section takes pictures of a face
    with PiCamera() as camera:
        # Configure camera
        camera.resolution = (300, 250)  # kept small for data transmission
        camera.framerate = 10
        camera.start_preview()

        # Do inference on VisionBonnet
        i = 0
        with CameraInference(face_detection.model()) as inference:
            for result in inference.run():
                if len(face_detection.get_faces(result)) >= 1:
                    camera.capture(f'/home/pi/Pictures/face_{i}.jpg')  # update with your folder location
                    i += 1
                    if i > 1:
                        break

        # Stop preview
        camera.stop_preview()
        
################## This section sends a text message
    import smtplib
    import os
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage
    from email.mime.multipart import MIMEMultipart
    from time import localtime, strftime

    ### update the following
    username = 'smtp2go_username'  # personal username
    password = 'smtp2go_password'  # personal password
    sender = 'pandabear802@yahoo.com'      # this appears on email as "sender"
    text_recipient = '15185551212@tmomail.net'    # this is your phone number and domain name
    email_recipient = 'your_address@yahoo.com'    # this is your email address
  
    # Establish a secure session with smtp2go outgoing SMTP server using your account
    server = smtplib.SMTP( 'mail.smtp2go.com', 2525 )

    server.starttls()

    server.login( username, password )
    msg = MIMEMultipart('text','plain')
    msg['Subject'] = 'Intruder'
    body = MIMEText(strftime("%Y-%m-%d %H:%M:%S", localtime()), 'plain')
    msg.attach(body)
    img_file = '/home/pi/Pictures/face_0.jpg'  # update with folder location
    with open(img_file, 'rb') as f:
        img_data = f.read()
    image = MIMEImage(img_data, name=os.path.basename(img_file))
    msg.attach(image)
    # Send text message through SMS gateway of destination number
    server.sendmail( sender, text_recipient, msg.as_string() )
    # Send picture via email
    server.sendmail(sender, email_recipient, msg.as_string())
    server.close()

if __name__ == '__main__':
    main()
