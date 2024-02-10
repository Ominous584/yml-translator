import inspect
import sys
import traceback
import yaml
from googletrans import Translator
from jinja2 import Template
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import re
import codecs

def main():
    keys = ['Command', 'Placeholders']
    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout()
    window.setGeometry(100, 100, 800, 400)
    window.setStyleSheet("background-color: #252525;")
    
    label = QLabel('YML Translation Tool')
    label.setFont(QFont('Arial', 20))
    label.setStyleSheet("color: white;")
    label.setAlignment(Qt.AlignCenter)  
    layout.addWidget(label)
    
    lang = QComboBox()
    lang.addItems(["Select a language", "Swedish", "German", "French", "Spanish", "Italian", "Turkish", "Russian", "Chinese", "Japanese", "Korean"])
    layout.addWidget(lang) 
    lang.setStyleSheet("color: white;")
    lang.setFont(QFont('Arial', 14))
    lang.setMaximumWidth(200) 
    
    text_area = QLineEdit()
    layout.addWidget(text_area)
    text_area.setMaximumWidth(200)
    text_area.setStyleSheet("color: white;")
    text_area.returnPressed.connect(lambda: keys.append(text_area.text()) or text_area.clear())
    text_area.setPlaceholderText("Enter a key to ignore in translation")
    
    text_area1 = QPlainTextEdit()
    text_area1.setPlaceholderText("Please select a language and click on the button to open a YML file")
    text_area1.setReadOnly(True)
    text_area1.setStyleSheet("background-color: white;")
    layout.addWidget(text_area1) 
    
    button1 = QPushButton('Open YML File')
    button1.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-size: 16px; font-weight: bold; border: none; border-radius: 10px; padding: 10px 24px; text-align: center; text-decoration: none; display: inline-block; margin: 4px 2px; cursor: pointer;}")
    layout.addWidget(button1)
    
    def done():
        done = QMessageBox()
        done.setWindowTitle("Success")
        replacer1 = "File has been translated to " + lang.currentText()
        done.setText(replacer1)
        done.setIcon(QMessageBox.Information)
        done.setStandardButtons(QMessageBox.Ok)
        done.exec_()
        button1.setText("Done")
        
    def convert_to_swedish_recursive(data, lan):
        if isinstance(data, dict):
            for key, value in data.items():
                if key in keys:
                    continue
                    
                if isinstance(value, (str, dict)):
                    if isinstance(value, str):
                        if value == None:
                            continue
                        if value != '':
                            translated_value = translate_to_swedish(value, lan)
                            data[key] = translated_value
                    else:
                        convert_to_swedish_recursive(value, lan)
                        
                elif isinstance(value, list):
                    for idx, item in enumerate(value):
                        convert_to_swedish_recursive(item, lan)
    
    
    def convert_to_swedish(yml_file, lan, langu):
        try:
            with codecs.open(yml_file, 'r', encoding='utf-8') as file:
                content = file.read()
            template = Template(content)
            rendered_content = template.render()
            try:
                data = yaml.load(rendered_content, Loader=yaml.FullLoader)
            except:
                data = yaml.load(rendered_content)
            convert_to_swedish_recursive(data, lan)

            replacer = "_" + langu + "1" + ".yml"

            output_file = yml_file.replace('.yml', replacer)
            try:
                output_file = output_file.replace('.yaml', replacer)
                with codecs.open(output_file, 'w', encoding='utf-8') as file:
                    yaml.dump(data, file, allow_unicode=True, sort_keys=False)
            except:
                with codecs.open(output_file, 'w', encoding='utf-8') as file:
                    yaml.dump(data, file, allow_unicode=True, sort_keys=False)

            button1.setText("Done")
            pro1 = QMessageBox()
            pro1.setWindowTitle("Success")
            replacer2 = "Process Completed. File has been translated to " + lang.currentText() + " and saved as" +  output_file + "file."
            pro1.setText(replacer2)
            pro1.setIcon(QMessageBox.Information)
            pro1.setStandardButtons(QMessageBox.Ok)
            pro1.exec_()
        except Exception as e:
            line_number = traceback.extract_tb(sys.exc_info()[2])[-1][1]
            error_message = f"Error occurred at line {line_number}: {str(e)}"
            pro1 = QMessageBox()
            pro1.setWindowTitle("Error")
            pro1.setText(error_message)
            pro1.setIcon(QMessageBox.Warning)
            pro1.setStandardButtons(QMessageBox.Ok)
            pro1.exec_()
                
    
    def translate_to_swedish(value, lan):
        translator = Translator()

        # Extract hex codes
        hex_codes = re.findall(r'#[A-Fa-f0-9]{6}|#[A-Fa-f0-9]{3}', value)
        QApplication.processEvents()
        
        # Check if the value is not surrounded by []
        if not re.search(r'<!.*?>|\".*?\"|\[.*?\]|<.*?>', value):
            # Ensure spaces around patterns to properly segment the text
            segments = re.split(r'(\s+)', value.strip())
            QApplication.processEvents()

            # Translate segments and add spaces between translated words
            translated_segments = []
            QApplication.processEvents()
            for segment in segments:
                # Check if the segment contains Minecraft color codes
                if re.search(r'&[0-9a-fA-F]', segment):
                    # Preserve the Minecraft color codes as they are
                    minecraft_color_code = re.findall(r'&[0-9a-fA-F]', segment)[0]
                    main_word = segment.replace(minecraft_color_code, '')
                    translated_main_word = translator.translate(main_word, dest=lan).text
                    translated_segment = minecraft_color_code + translated_main_word
                    QApplication.processEvents()
                else:
                    try:
                        translated_segment = translator.translate(segment, dest=lan).text
                        QApplication.processEvents()
                    except Exception as e:
                        print(f"Translation error: {e}. Using original segment.")
                        translated_segment = segment
                        QApplication.processEvents()

            translated_segment = translated_segment + " "
            translated_segments.append(translated_segment)
            QApplication.processEvents()
            

            # Concatenate translated segments with spaces
            translated_sentence = ' '.join(translated_segments)

            # Reinsert spaces after hex codes
            for hex_code in hex_codes:
                translated_sentence = translated_sentence.replace(hex_code, hex_code + ' ')
            
            text_area1.appendPlainText(translated_sentence)
            text_area1.appendPlainText("\n")
            QApplication.processEvents()

            return translated_sentence
        else:
            text_area1.appendPlainText(value)
            text_area1.appendPlainText("\n")
            QApplication.processEvents()
            return value
    
    def prowin():
        lang.currentText()
        if lang.currentText() == "Select a language":
            pro = QMessageBox()
            pro.setWindowTitle("Error")
            pro.setText("Please select a language")
            pro.setIcon(QMessageBox.Warning)
            pro.setStandardButtons(QMessageBox.Ok)
            pro.exec_()
            return
        else:
            button1.setText("Processing...")
            open_file_dialogue(lang.currentText())
            button1.setText("Processing...")
        
    def open_file_dialogue(lan):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("YML Files (*.yml)")
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                yml_file = selected_files[0]
                
                pro = QMessageBox()
                pro.setWindowTitle("Success")
                pro.setText("File is being translated...")
                pro.setIcon(QMessageBox.Information)
                pro.setStandardButtons(QMessageBox.Ok)
                pro.exec_()
                
                convert_to_swedish(yml_file, lan, lang.currentText())
                print(f"File {yml_file} has been translated to {lan}")
    
    button1.clicked.connect(prowin)
    window.setLayout(layout)
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
