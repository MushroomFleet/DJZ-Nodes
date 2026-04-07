import os

class ProjectFilePathNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "root": ("STRING", {"default": "output"}),
                "project_name": ("STRING", {"default": "MyProject"}),
                "subfolder": ("STRING", {"default": "images"}),
                "filename": ("STRING", {"default": "image"}),
            },
            "optional": {
                "separator": (["auto", "forward_slash", "backslash"], {"default": "auto"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_file_path"
    CATEGORY = "file_management"

    def generate_file_path(self, root, project_name, subfolder, filename, separator="auto"):
        root = self.sanitize_path_component(root)
        project_name = self.sanitize_path_component(project_name)
        subfolder = self.sanitize_path_component(subfolder)
        filename = self.sanitize_filename(filename)

        if separator == "auto":
            sep = os.path.sep
        elif separator == "forward_slash":
            sep = "/"
        else:
            sep = "\\"

        path_components = [root, project_name, subfolder, filename]
        full_path = sep.join(filter(bool, path_components))
        full_path = os.path.normpath(full_path)

        return (full_path,)

    @staticmethod
    def sanitize_path_component(component):
        # Block directory traversal sequences first
        if '..' in component:
            component = component.replace('..', '')
        # Remove any characters that are unsafe for file paths
        unsafe_chars = ['<', '>', ':', '"', '|', '?', '*']
        for char in unsafe_chars:
            component = component.replace(char, '')
        component = component.replace(' ', '_')
        return component.strip('./\\')

    @staticmethod
    def sanitize_filename(filename):
        unsafe_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        for char in unsafe_chars:
            filename = filename.replace(char, '')
        if '..' in filename:
            filename = filename.replace('..', '')
        filename = os.path.splitext(filename)[0]
        return filename

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")

NODE_CLASS_MAPPINGS = {
    "ProjectFilePathNode": ProjectFilePathNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ProjectFilePathNode": "Project File Path Generator"
}
