import tkinter as tk
from tkinter import messagebox
import requests
import json
import docker

class DockerImageSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Docker Image")
        self.create_widgets()

    def create_widgets(self):
        # Entry for user to input image name
        self.image_name_entry = tk.Entry(self.root, width=30)
        self.image_name_entry.grid(row=0, column=1, padx=10, pady=20)

        # Search on DockerHub button
        search_dockerhub_button = tk.Button(self.root, text="Search on DockerHub", command=self.search_dockerhub, bg="#0000FF", fg="white")
        search_dockerhub_button.grid(row=1, column=3, padx=10, pady=20)

        # Search Image (Local Storage) button
        search_button = tk.Button(self.root, text="Search Image (Local Storage)", command=self.search_image, bg="#CD5C5C", fg="white")
        search_button.grid(row=1, column=0, padx=10, pady=20)

        # Download/Pull Image button
        pull_image_button = tk.Button(self.root, text="Download/Pull Image", command=self.pull_image,  bg="#999999", fg="white")
        pull_image_button.grid(row=1, column=1, padx=10, pady=20)

    def display_repo_names(self, repo_names):
        new_window = tk.Toplevel(self.root)
        new_window.title("DockerHub Search Results")

        # Customization
        new_window.geometry("600x400")
        custom_font = ("Arial", 16, "bold")

        def pull_image_for_repo(repo_name):
            self.image_name_entry.delete(0, tk.END) 
            self.image_name_entry.insert(tk.END, repo_name)  
            self.pull_image()

        for repo_name in repo_names:
            # Create a Label for each repo name
            repo_label = tk.Label(new_window, text=repo_name, font=custom_font)
            repo_label.pack(side="top", pady=5)

            # Create a button for each repo
            pull_button = tk.Button(new_window, text="Pull", command=lambda name=repo_name: pull_image_for_repo(name), width=10, bg="blue", fg="white")
            pull_button.pack(side="top")

    def search_dockerhub(self):
        image_name = self.image_name_entry.get()
        if not image_name:
            messagebox.showinfo("Error", "Please enter an image name.")
            return

        # DockerHub search API URL
        search_url = f"https://hub.docker.com/v2/search/repositories/?query={image_name}"

        # Make a request to DockerHub search API
        response = requests.get(search_url)

        if response.status_code == 200:
            data = response.json()
            repo_names = [result['repo_name'] for result in data.get('results', [])]

            if repo_names:
                self.display_repo_names(repo_names)
            else:
                messagebox.showinfo("Info", f"No matching images found on DockerHub for {image_name}.")
        else:
            messagebox.showinfo("Error", f"Error searching on DockerHub for {image_name}.")

    def pull_image(self):
        image_name = self.image_name_entry.get()
        if not image_name:
            messagebox.showinfo("Error", "Please enter an image name.")
            return

        try:
            # Use the docker-py library to pull the image from DockerHub
            client = docker.from_env()
            client.images.pull(image_name)

            messagebox.showinfo("Pull Image", f"Pulling image: {image_name}")
        except docker.errors.ImageNotFound:
            messagebox.showinfo("Error", f"Image {image_name} not found on DockerHub.")
        except docker.errors.APIError as e:
            messagebox.showinfo("Error", f"Error pulling image {image_name}. {e}")

    def search_image(self):
        try:
            # Get the image name from the entry widget
            image_name = self.image_name_entry.get()

            # Check if the user entered a search term
            if not image_name:
                messagebox.showinfo("Error", "Please enter an image name.")
                return

            # Use the Docker API to list local images and filter based on the user-entered text
            client = docker.from_env()
            local_images = client.images.list(name=image_name)

            if not local_images:
                messagebox.showinfo("Info", f"No local images found matching: {image_name}")
                return

            # Create a new window to display the matching local images
            self.current_page = tk.Toplevel(self.root)
            self.current_page.title("Local Docker Images")

            self.current_page.geometry("600x400")

            # Create a Text widget for displaying the list of images
            text_widget = tk.Text(self.current_page, wrap="none")
            text_widget.pack(expand=True, fill="both")

            # Display the list of matching images in the Text widget
            for i, image in enumerate(local_images, start=1):
                text_widget.insert(tk.END, f"{i}. {image.tags}\n")

            # Add a scrollbar to the Text widget
            scrollbar = tk.Scrollbar(self.current_page, command=text_widget.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            text_widget.config(yscrollcommand=scrollbar.set)

        except Exception as e:
            messagebox.showinfo("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DockerImageSearchApp(root)
    root.mainloop()