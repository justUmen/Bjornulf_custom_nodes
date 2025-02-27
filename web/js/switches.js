import { app } from "/scripts/app.js";  // Adjust path based on ComfyUI's structure

app.registerExtension({
    name: "Bjornulf.SwitchText",
    async nodeCreated(node) {
        if (node.comfyClass === "Bjornulf_SwitchText") {
            // Store original colors
            const originalColor = "";  // Default ComfyUI node color
            
            // Function to update color based on switch value
            const updateNodeColor = () => {
                const switchWidget = node.widgets?.find(w => w.name === "switch");
                if (switchWidget) {
                    const isTrue = switchWidget.value;
                    node.color = isTrue ? originalColor : "#640000";  // Red when false
                }
            };

            const updateNodeColorPickMe = () => {
                const pickMeWidget = node.widgets?.find(w => w.name === "ONLY_ME_combine_text");
                if (pickMeWidget) {
                    const isPicked = pickMeWidget.value;
                    node.color = isPicked ? "#000064" : originalColor;  // Red when false
                }
            }

            // Initial color update
            updateNodeColor();

            // Hook into widget value changes
            const originalSetValue = node.widgets?.find(w => w.name === "switch")?.callback;
            node.widgets.find(w => w.name === "switch").callback = function(value) {
                updateNodeColor();
                if (originalSetValue) {
                    originalSetValue.apply(this, arguments);
                }
            };

            // Hook into widget value changes
            const originalSetValuePickMe = node.widgets?.find(w => w.name === "ONLY_ME_combine_text")?.callback;
            node.widgets.find(w => w.name === "ONLY_ME_combine_text").callback = function(value) {
                updateNodeColorPickMe();
                if (originalSetValuePickMe) {
                    originalSetValuePickMe.apply(this, arguments);
                }
            };

            // Cleanup on node removal (optional but good practice)
            node.onRemoved = function() {
                node.color = originalColor;
            };
        }
    }
});

app.registerExtension({
    name: "Bjornulf.SwitchAnything",
    async nodeCreated(node) {
        if (node.comfyClass === "Bjornulf_SwitchAnything") {
            // Store original colors
            const originalColor = "";  // Default ComfyUI node color
            
            // Function to update color based on switch value
            const updateNodeColor = () => {
                const switchWidget = node.widgets?.find(w => w.name === "switch");
                if (switchWidget) {
                    const isTrue = switchWidget.value;
                    node.color = isTrue ? originalColor : "#640000";  // Red when false
                }
            };

            // Initial color update
            updateNodeColor();

            // Hook into widget value changes
            const originalSetValue = node.widgets?.find(w => w.name === "switch")?.callback;
            node.widgets.find(w => w.name === "switch").callback = function(value) {
                updateNodeColor();
                if (originalSetValue) {
                    originalSetValue.apply(this, arguments);
                }
            };

            // Cleanup on node removal (optional but good practice)
            node.onRemoved = function() {
                node.color = originalColor;
            };
        }
    }
});