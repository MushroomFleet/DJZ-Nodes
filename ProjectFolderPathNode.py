import os

class ProjectFolderPathNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "root": ("STRING", {"default": "output"}),
                "project_name": ("STRING", {"default": "MyProject"}),
                "subfolder": ("STRING", {"default": "images"}),
            },
            "optional": {
                "separator": (["auto", "forward_slash", "backslash"], {"default": "auto"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_folder_path"
    CATEGORY = "file_management"

    def generate_folder_path(self, root, project_name, subfolder, separator="auto"):
        # Sanitize inputs
        root = self.sanitize_path_component(root)
        project_name = self.sanitize_path_component(project_name)
        subfolder = self.sanitize_path_component(subfolder)

        # Determine the separator
        if separator == "auto":
            sep = os.path.sep
        elif separator == "forward_slash":
            sep = "/"
        else:
            sep = "\\"

        # Construct path
        path_components = [root, project_name, subfolder]
        full_path = sep.join(filter(bool, path_components))

        # Normalize the path
        full_path = os.path.normpath(full_path)

        return (full_path,)

    @staticmethod
    def sanitize_path_component(component):
        # Remove any characters that are unsafe for file paths
        unsafe_chars = ['<', '>', ':', '"', '|', '?', '*']
        for char in unsafe_chars:
            component = component.replace(char, '')
        # Convert spaces to underscores
        component = component.replace(' ', '_')
        # Remove leading/trailing dots and slashes
        return component.strip('./\\')

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        # This ensures the node updates when any input changes
        return float("nan")

NODE_CLASS_MAPPINGS = {
    "ProjectFolderPathNode": ProjectFolderPathNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ProjectFolderPathNode": "Project Folder Path Generator"
}
