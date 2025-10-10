#!/usr/bin/env python3
"""
Script to generate a QR code for the Google Slides presentation link
"""

import qrcode
import os

def generate_qr_code():
    # The Google Slides link
    url = "https://docs.google.com/presentation/d/1zc_dKEHlZj5wfBe7FRIXpup8jAMJUAWY3GQzKCr_7Ek/edit?usp=sharing"
    
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,  # Controls the size of the QR Code
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Controls the error correction used for the QR Code
        box_size=10,  # Controls how many pixels each "box" of the QR code is
        border=4,  # Controls how many boxes thick the border should be
    )
    
    # Add data to the QR code
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create QR code image
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    # Save the image
    output_path = "/workspaces/vibeCoding101/PolyUGuestLecture10Oct/Slides/google_slides_qr_code.png"
    qr_image.save(output_path)
    
    print(f"QR code generated successfully and saved to: {output_path}")
    print(f"QR code contains the URL: {url}")

if __name__ == "__main__":
    generate_qr_code()