from nodes import PreviewImage

class FourImageViewer(PreviewImage):
    """A node that compares four images in the UI."""

    NAME = 'Four Image Comparer'
    CATEGORY = "Bjornulf"
    FUNCTION = "compare_images"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "image_1": ("IMAGE",),
                "image_2": ("IMAGE",),
                "image_3": ("IMAGE",),
                "image_4": ("IMAGE",),
            }
        }

    def compare_images(self, **kwargs):
        result = {"ui": {}}
        
        for i in range(1, 5):
            image_key = f"image_{i}"
            image_data = kwargs.get(image_key)
            
            if image_data is not None and len(image_data) > 0:
                saved_images = self.save_images(image_data)
                result["ui"][f"images_{i}"] = saved_images["ui"]["images"]

        return result