class WriteTextPickMeChain:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "picked": ("BOOLEAN", {"default": False}),
                "text": ("STRING", {"multiline": True, "lines": 10})
            },
            "optional": {
                "pickme_chain": ("STRING", {"forceInput": True}),
            },
        }
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("text", "chain_text")
    FUNCTION = "write_text"
    OUTPUT_NODE = True
    CATEGORY = "Bjornulf"
    
    def write_text(self, text, picked, pickme_chain="", **kwargs):
        chain_output = text if picked else pickme_chain
        return (text, chain_output)