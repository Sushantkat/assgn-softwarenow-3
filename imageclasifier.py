import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import torch
import torchvision.transforms as transforms
import torchvision.models as models
class AdvancedButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(
            relief=tk.FLAT,  # Removing default button border
            bg="#007bff",  # Background color
            fg="white",  # Text color
            activebackground="#0056b3",  # Background color when button is clicked
            activeforeground="white",  # Text color when button is clicked
            font=("Helvetica", 12),  # Button text font
            padx=10,  # Horizontal padding
            pady=5,  # Vertical padding
            cursor="hand2",  # Cursor style
            borderwidth=0,  # Border width
        )
        self.bind("<Enter>", lambda e: self.config(bg="#0056b3"))  # Changes background color on mouse hover
        self.bind("<Leave>", lambda e: self.config(bg="#007bff"))  # Changes background color back on mouse leave
class ImageClassifierApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Classifier Application")
        self.geometry("600x500")
        self.model = models.resnet18(pretrained=True)
        self.model.eval()  # Setting model to evaluation mode
        self.num_classes = 1000  # Number of classes in the pre-trained ResNet model
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        self.create_widgets()

    def create_widgets(self):
        # Label for displaying the selected image
        self.image_label = tk.Label(self)
        self.image_label.pack(pady=10)

        # Button to select an image
        select_button = AdvancedButton(self, text="Select Image", command=self.select_image)
        select_button.pack(pady=5)

        # Button to classify the selected image
        classify_button = AdvancedButton(self, text="Classify Image", command=self.classify_image)
        classify_button.pack(pady=5)

    def select_image(self):
        # Opening file dialog to select an image file
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            # Opening and displaying the selected image
            image = Image.open(file_path)
            image = self.resize_image(image)  # Resizing image to match ResNet input size
            self.img = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.img)

            # Storing image data for classification
            self.image_data = image

    def classify_image(self):
        if hasattr(self, 'image_data'):
            # Preprocessing the image data
            img_tensor = self.transform(self.image_data)
            img_tensor = img_tensor.unsqueeze(0)  # Adding batch dimension

            # Using the model to classify the image
            with torch.no_grad(): 
                outputs = self.model(img_tensor)
                _, predicted = torch.max(outputs, 1)
                predicted_class = predicted.item()
            
            # Displaying the classification result
            if predicted_class < self.num_classes:
                messagebox.showinfo("Classification Completed", f"The image belongs to class {predicted_class}.")
            else:
                messagebox.showerror("Error", "Couldn't Clasify the image.")
        else:
            messagebox.showwarning("Warning", "You must select an image first.")

    def resize_image(self, image):
        # Resizing and croping the image while maintaining the aspect ratio
        aspect_ratio = image.width / image.height
        if aspect_ratio > 1:
            new_width = 256
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = 256
            new_width = int(new_height * aspect_ratio)
        resized_image = image.resize((new_width, new_height))
        left = (new_width - 224) / 2
        top = (new_height - 224) / 2
        right = (new_width + 224) / 2
        bottom = (new_height + 224) / 2
        cropped_image = resized_image.crop((left, top, right, bottom))
        return cropped_image

if __name__ == "__main__":
    app = ImageClassifierApp()
    app.mainloop()
