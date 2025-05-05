
import sys
from PyQt5.QtWidgets import (QApplication,QMainWindow,QLabel,QPushButton,QVBoxLayout,QFileDialog,QMessageBox)
from PyQt5.QtGui import QIcon,QFont,QPixmap,QImage
from PyQt5.QtCore import Qt,QBuffer
from rembg import remove
from PIL import Image
import io
from pillow_heif import register_heif_opener
import re

register_heif_opener()

load_btn = None
rem_btn = None
save_btn = None

def label_style():
    return """
            QLabel {  
                color: rgb(0, 0, 0);
                border-radius: 10px;
                text-align: center;
                border: 2px solid rgb(23, 124, 212);  
            }
            """

def clear_image(label):
    global load_btn, rem_btn, save_btn
    label.clear()
    label.setPixmap(QPixmap())
    label.setStyleSheet(label_style())
    load_btn.setEnabled(True)
    rem_btn.setEnabled(True)
    save_btn.setEnabled(True)

def pil_to_pixmap(pil_image):
    buffer = io.BytesIO()
    pil_image.save(buffer, format='PNG')
    buffer.seek(0)
    image = QImage.fromData(buffer.read(), 'PNG')
    return QPixmap.fromImage(image)

def get_btn_style():
    return """
            QPushButton {
        background-color: rgb(23, 124, 212);
        color: white;
        font-size: 20px;
        border-radius: 10px;
    }
    QPushButton:hover {
        background-color: rgb(0, 0, 0);
        color: white;
    }
            """

def load_image(label):
    global load_btn
    file_name, _ = QFileDialog.getOpenFileName(None, "Open Image File", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.HEIC)")
    if file_name:
        if file_name.lower().endswith(".heic"):
            pill_image = Image.open(file_name)
            pixmap = pil_to_pixmap(pill_image)
        else:
            pixmap = QPixmap(file_name)
        label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        label.setAlignment(Qt.AlignCenter)
        load_btn.setEnabled(False)

def remove_bg(pixmap, label):
    global rem_btn
    if not pixmap:
        QMessageBox.warning(None, "Error", "No image loaded.Please load an image first.")
        return

    try:
        
        image=pixmap.toImage()
        buffer=QBuffer()
        buffer.open(QBuffer.ReadWrite)
        image.save(buffer,"PNG")
        input_bytes = buffer.data()
        output_bytes = remove(bytes(input_bytes))
        buffer.seek(0)
        output_image = Image.open(io.BytesIO(output_bytes))
        qt_img = pil_to_pixmap(output_image)

        label.setPixmap(qt_img.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        rem_btn.setEnabled(False)
    
    except Exception as e:
        QMessageBox.critical(None, "Error", f"An error occurred: {str(e)}")
    

def save_image(pixmap):
    global save_btn
    if pixmap:
        pixmap_str = str(pixmap)
        base_name = re.sub(r'[<>]', '', pixmap_str).replace(' ', '_')
        file_name, _ = QFileDialog.getSaveFileName(None, "Save Image File", f"BGGone{base_name}", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.HEIC)")
        if file_name:
            image = pixmap.toImage()
            if image.save(file_name, "PNG"):
                QMessageBox.information(None, "Saved", "Image saved successfully!")
                save_btn.setEnabled(False)
            else:
                QMessageBox.warning(None, "Error", "Failed to save image.")


if __name__ == "__main__":
    # Create the application and main window
    app =QApplication(sys.argv)
    window=QMainWindow()
    window.setWindowTitle("BGGone")
    window.setMinimumSize(1500, 900)
    window.setMaximumSize(1500, 900)
    window.setWindowIcon(QIcon("BGGone.ico"))


    #create App title label
    label= QLabel(window)
    label.setText("BGGone")
    label.setFont(QFont("Times New Roman",40))
    label.setGeometry(0,50, 1500,200)
    label.setStyleSheet("""
                        color: rgb(23, 124, 212);
                        border-radius: 10px;
                        text-align: center;
                        """)
    label.setAlignment(Qt.AlignCenter)

    #add image icon in main window
    icon_label = QLabel(window)
    icon_label.setGeometry(360,30,250,250)
    pixmap = QPixmap("BGGone.png")
    icon_label.setPixmap(pixmap)
    icon_label.setScaledContents(True)
    icon_label.setStyleSheet("""
                        color: rgb(0, 0, 0);
                        border-radius: 10px;
                        text-align: center;
                        """)
    icon_label.setAlignment(Qt.AlignCenter)
    
    #display area of loaded image
    image_label1 = QLabel(window)
    image_label1.setGeometry(700,300,500,500)
    image_label1.setStyleSheet(label_style())
    
    
    #Add load button
    layout=QVBoxLayout(window)
    load_btn=QPushButton("Load Image",window)
    load_btn.setGeometry(100,400,200,80)
    load_btn.setStyleSheet(get_btn_style())
    load_btn.setFont(QFont("Times New Roman",20))
    load_btn.clicked.connect(lambda: load_image(image_label1))
    load_btn.setLayout(layout)

    
    #add remove bg button
    rem_btn=QPushButton("Remove background",window)
    rem_btn.setGeometry(100,500,200,80)
    rem_btn.setStyleSheet(get_btn_style())
    rem_btn.setFont(QFont("Times New Roman",20))
    rem_btn.clicked.connect(lambda: remove_bg(image_label1.pixmap(), image_label1))
    rem_btn.setLayout(layout)


    #save button 
    save_btn=QPushButton("Save Image",window)
    save_btn.setGeometry(100,600,200,80)
    save_btn.setStyleSheet(get_btn_style())
    save_btn.setFont(QFont("Times New Roman",20))
    save_btn.clicked.connect(lambda: save_image(image_label1.pixmap()))
    save_btn.setLayout(layout)

    #Clear button
    clr_btn=QPushButton("Clear",window)
    clr_btn.setGeometry(100,700,200,80)
    clr_btn.setStyleSheet(get_btn_style())
    clr_btn.setFont(QFont("Times New Roman",20))
    clr_btn.clicked.connect(lambda: clear_image(image_label1))
    clr_btn.setLayout(layout)

    
    window.show()
    sys.exit(app.exec_())
