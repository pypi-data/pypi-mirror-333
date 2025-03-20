
# TermStyler 🎨✨  
A lightweight Python library for adding **colors, backgrounds, and text styles** to terminal output.  

## 🌟 Features  
✅ Supports **16 colors** (normal & bright)  
✅ **RGB colors** for custom styling  
✅ **Text styles** (bold, italic, underline, etc.)  
✅ **Background colors**  
✅ Works on **Windows, Linux, and macOS**  

## Installation:
```md
pip install termstyler
```

## Usage  
### **Importing the Library**
```python
from termstyler import TermStyler
```
### **Basic Colors**
```python
print(TermStyler.color("Hello in bright blue!", "bright_blue"))
print(TermStyler.color("This is red text!", "red"))
print(TermStyler.color("Cyan colored text!", "cyan"))
```
### **Text Styles**
```python
print(TermStyler.style("Bold text!", "bold"))
print(TermStyler.style("Italic text!", "italic"))
print(TermStyler.style("Underlined text!", "underline"))
```
### **Background Colors**
```python
print(TermStyler.background("Text with red background!", "red"))
print(TermStyler.background("Blue background!", "blue"))
```
### **RGB Colors**
```python
print(TermStyler.rgb(255, 165, 0, "Orange Text!"))
print(TermStyler.bg_rgb(0, 255, 0, "Green Background!"))
```
## 🛠 Full API Reference  
### **`TermStyler.color(text, color)`**  
✔ Changes the color of the text  
✔ **Example:**  
```python
TermStyler.color("Hello", "blue")
```
### **`TermStyler.background(text, bg_color)`**  
✔ Changes the background color of text  
✔ **Example:**  
```python
TermStyler.background("Text with red background", "red")
```
### **`TermStyler.style(text, style)`**  
✔ Applies a text style (bold, italic, etc.)  
✔ **Example:**  
```python
TermStyler.style("Bold text!", "bold")
```
### **`TermStyler.rgb(r, g, b, text)`**  
✔ Sets text color using RGB values  
✔ **Example:**  
```python
TermStyler.rgb(255, 165, 0, "Orange Text!")
```
### **`TermStyler.bg_rgb(r, g, b, text)`**  
✔ Sets background color using RGB values  
✔ **Example:**  
```python
TermStyler.bg_rgb(0, 255, 0, "Green Background!")
```
## 🎭 Available Styles & Colors  
| Type          | Options |
|--------------|----------------------------------------|
| **Colors**   | `black, red, green, yellow, blue, magenta, cyan, white` (also `bright_` versions) |
| **Text Styles** | `bold, dim, italic, underline, blink, reverse, hidden` |
| **Backgrounds** | Same as text colors |

## 📜 License  
This project is licensed under the **MIT License**.  

## 🤝 Contributing  
Pull requests are welcome! If you have ideas, feel free to open an issue.  