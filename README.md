
# BGGone

![BGGone Logo](BGGone.png)

BGGone is a simple desktop application built with PyQt5 that allows users to remove backgrounds from images quickly and easily. The application supports various image formats including PNG, JPG, JPEG, BMP, GIF, and HEIC.

## Features
- Load images in multiple formats (PNG, JPG, JPEG, BMP, GIF, HEIC)
- Remove backgrounds with one click using the `rembg` library
- Save processed images
- Clear the current image
- Simple and intuitive user interface

## Requirements 
- Python 3.6 or higher
- PyQt5
- rembg
- Pillow
- pillow-heif

```bash
pip install PyQt5 rembg pillow pillow-heif
```
## Usage
- Run the application:
  ```bash
  python BGGone.py
  ```
- Use the interface:
  - Click `Load Image` to select an image file
  - Click `Remove Background` to process the image
  - Click `Save Image` to save the result
  - Click `Clear` to reset the application

## Screenshot
   ![image](https://github.com/user-attachments/assets/0bee9e42-d209-4d9d-89ed-915031ef67c0)


## Notes
- For best results, use images with clear contrast between foreground and background
- `HEIC` format support requires `pillow-heif` package
- The application has a fixed window size of 1500x900 pixels


