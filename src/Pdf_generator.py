import sys
import os
from pathlib import Path
import img2pdf
import subprocess
import re
import logging
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QProgressBar, QStatusBar, QComboBox, QLineEdit
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import platform

if platform.system() == "Linux":
    gs_command = "gs"
    log_dir = Path.home() / ".tiff_pdf_logs"
    log_dir.mkdir(parents = True, exist_ok=True)
elif platform.system() == "Windows":
    gs_command = "gswin64c"
    log_dir = Path.home()/"Documents"/"tiff_pdf_logs"
    log_dir.mkdir(parents = True, exist_ok=True)
# Set up logging
logging.basicConfig(filename= log_dir / "converter_log.txt", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

class ImageToPDFConverter(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TIFF PDF Generator")
        self.setGeometry(100, 100, 700, 650)

        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout
        layout = QVBoxLayout()


        # Button to select folder
        self.select_folder_btn = QPushButton("Select Image Folder")
        self.select_folder_btn.clicked.connect(self.select_folder)
        layout.addWidget(self.select_folder_btn)

        # Label to show the selected folder
        self.folder_label = QLabel("No folder selected")
        layout.addWidget(self.folder_label)

        # Resize options dropdown (e.g., screen sizes or DPI options)
        self.resize_option_label = QLabel("Select Resize Option")
        layout.addWidget(self.resize_option_label)
        self.resize_option_combo = QComboBox()
        self.resize_option_combo.addItems(["No Resize", "A4", "Letter", "Custom DPI"])
        layout.addWidget(self.resize_option_combo)

        # Custom DPI input field (only visible when "Custom DPI" is selected)
        self.custom_dpi_label = QLabel("Enter Custom DPI:")
        self.custom_dpi_input = QLineEdit()
        self.custom_dpi_label.setVisible(False)
        self.custom_dpi_input.setVisible(False)
        layout.addWidget(self.custom_dpi_label)
        layout.addWidget(self.custom_dpi_input)

        # Print settings dropdown (e.g., default, ebook, prepress)
        self.print_settings_label = QLabel("Select Print Option")
        layout.addWidget(self.print_settings_label)
        self.print_settings_combo = QComboBox()
        self.print_settings_combo.addItems(["default", "ebook", "prepress", "printer", "screen"])
        layout.addWidget(self.print_settings_combo)

        # Button to start conversion
        self.convert_btn = QPushButton("Convert to PDF")
        self.convert_btn.clicked.connect(self.convert_to_pdf)
        layout.addWidget(self.convert_btn)
        self.convert_btn.setEnabled(False)  # Disabled until folder is selected

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.central_widget.setLayout(layout)

        # Variables
        self.folder_path = ""
        self.image_files = []
        self.output_pdf = ""

        # Connect signals
        self.resize_option_combo.currentIndexChanged.connect(self.toggle_custom_dpi_input)

    def toggle_custom_dpi_input(self):
        """Show or hide the custom DPI input field based on selected resize option."""
        if self.resize_option_combo.currentText() == "Custom DPI":
            self.custom_dpi_label.setVisible(True)
            self.custom_dpi_input.setVisible(True)
        else:
            self.custom_dpi_label.setVisible(False)
            self.custom_dpi_input.setVisible(False)

    def select_folder(self):
        """Opens a dialog to select a folder containing images."""
        try:
            folder = QFileDialog.getExistingDirectory(self, "Select Folder")
            if folder:
                self.folder_path = Path(folder)
                self.folder_label.setText(f"Selected folder: {self.folder_path}")
                self.image_files = self.list_files_numerical(self.folder_path)  # List files in correct order
                self.convert_btn.setEnabled(bool(self.image_files))  # Enable if images found

                if not self.image_files:
                    self.status_bar.showMessage("No images found in the selected folder.")
                    logging.warning("No images found in the selected folder.")
                else:
                    self.status_bar.showMessage(f"{len(self.image_files)} images found.")
                    logging.info(f"{len(self.image_files)} images found in folder: {self.folder_path}")

        except Exception as e:
            logging.error(f"Error selecting folder: {str(e)}")
            self.status_bar.showMessage("Error selecting folder.")

    def list_files_numerical(self, directory):
        """List files in numerical order, filtered by specific image file types."""
        allowed_extensions = ('.png', '.tif', '.tiff', '.jpeg', '.jpg')  # Allowed file extensions
        files = os.listdir(directory)
        # Filter only files with the allowed extensions
        files = [f for f in files if os.path.isfile(os.path.join(directory, f)) and f.lower().endswith(allowed_extensions)]
        
        # Sort files numerically if they contain numbers
        sorted_files = sorted(files, key=lambda f: [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', f)])
        return sorted_files

    def convert_to_pdf(self):
        """Starts the conversion process."""
        try:
            if not self.folder_path or not self.image_files:
                self.status_bar.showMessage("Please provide all inputs including the output file path.")
                logging.warning("Conversion failed due to missing inputs.")
                return

            # Disable convert button during processing
            self.convert_btn.setEnabled(False)
            self.status_bar.showMessage("Reading Files...")
            logging.info("Reading Files.")

            # Automatically set the output file to 'output.pdf' in the same folder
            output_file_path = self.folder_path/ "output.pdf"

            # Start conversion in a separate thread
            resize_option = self.resize_option_combo.currentText()
            print_option = self.print_settings_combo.currentText()
            custom_dpi = self.custom_dpi_input.text() if resize_option == "Custom DPI" else None
            self.status_bar.showMessage("Conversion started...")
            logging.info("Conversion started.")
            self.thread = ConversionThread(self.image_files, self.folder_path, resize_option, print_option, custom_dpi, output_file_path)
            self.thread.progress_updated.connect(self.update_progress)
            self.thread.conversion_finished.connect(self.on_conversion_finished)
            self.thread.start()

        except Exception as e:
            logging.error(f"Error during conversion setup: {str(e)}")
            self.status_bar.showMessage("Error during conversion setup.")

    def update_progress(self, value):
        """Updates the progress bar."""
        self.progress_bar.setValue(value)

    def on_conversion_finished(self, success, output_pdf=None, error_msg=None):
        """Handles the completion of the conversion."""
        if success:
            self.status_bar.showMessage(f"Conversion completed: {output_pdf}")
            logging.info(f"Conversion completed successfully: {output_pdf}")
        else:
            self.status_bar.showMessage(f"Error: {error_msg}")
            logging.error(f"Conversion failed: {error_msg}")

        # Re-enable the convert button
        self.convert_btn.setEnabled(True)


class ConversionThread(QThread):
    """A separate thread for the conversion process to avoid blocking the UI."""
    progress_updated = pyqtSignal(int)
    conversion_finished = pyqtSignal(bool, str, str)

    def __init__(self, image_files, output_folder, resize_option, print_option, custom_dpi, output_file_path):
        super().__init__()
        self.image_files = image_files
        self.output_folder = Path(output_folder)
        self.resize_option = resize_option
        self.print_option = print_option
        self.custom_dpi = custom_dpi
        if self.resize_option != "No Resize":
            self.output_pdf = self.output_folder / "output.pdf" # Output file path set automatically
        else:
            self.output_pdf = self.output_folder / f"{self.output_folder.name}.pdf"
        self.resized_pdf = self.output_folder / f"{self.output_pdf.parent.name}.pdf"  # Resized file path

    def run(self):
        """Performs the conversion to PDF and resizes it using Ghostscript."""
        self.progress_updated.emit(0)
        try:
            total_images = len(self.image_files)

            # # Step 1: Convert all images to a single PDF
            # with open(self.output_pdf, "wb") as f:
            #     f.write(img2pdf.convert([self.output_folder / img for img in self.image_files]))

            with open(self.output_pdf, "wb") as f:
                pdf_pages = []
                for index, img in enumerate(self.image_files):
                    pdf_pages.append(self.output_folder / img)
                    progress = int((index + 1) / total_images * 10)  # Scale to 10%
                    self.progress_updated.emit(progress)

                f.write(img2pdf.convert(pdf_pages))
                self.progress_updated.emit(95)


            logging.info(f"Images converted to PDF: {self.output_pdf}")

            # Step 2: Run Ghostscript for resizing, if needed
            if self.resize_option != "No Resize":
                #print(self.output_pdf)
                ghostscript_command = self.get_ghostscript_command()
                if ghostscript_command:
                    
                    result = subprocess.run(ghostscript_command, shell=True, check=True)
                    #print(result.stdout)
                    logging.info(f"PDF resized using Ghostscript: {self.resized_pdf}")
            else:
                # If no resizing, use the original file as output
                self.resized_pdf = self.output_pdf

            # Emit 100% progress when done
            self.progress_updated.emit(100)
            self.conversion_finished.emit(True, str(self.resized_pdf), None)
            if self.resize_option != "No Resize":
                self.output_pdf.unlink()

        except Exception as e:
            logging.error(f"Error during PDF conversion: {str(e)}")
            self.conversion_finished.emit(False, None, str(e))

    def get_ghostscript_command(self):
        """Constructs the Ghostscript command based on the selected print and resize options."""
        dpi_setting = f"-r{self.custom_dpi}" if self.custom_dpi else ""
        return f'{gs_command} -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/{self.print_option} ' \
               f'-dNOPAUSE -dBATCH {dpi_setting} ' \
               f'-dDownsampleColorImages=true -dColorImageResolution={self.custom_dpi or 250} ' \
               f'-dDownsampleGrayImages=true -dGrayImageResolution={self.custom_dpi or 250} ' \
               f'-dDownsampleMonoImages=true -dMonoImageResolution={self.custom_dpi or 250} ' \
               f'-sOutputFile="{str(self.resized_pdf)}" "{str(self.output_pdf)}"'


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = ImageToPDFConverter()
    window.show()

    sys.exit(app.exec_())
