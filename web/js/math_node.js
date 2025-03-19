import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "Bjornulf.MathNode",
    async nodeCreated(node) {
        if (node.comfyClass === "Bjornulf_MathNode") {
            const updateInputs = () => {
                const initialWidth = node.size[0];
                const numInputsWidget = node.widgets.find(w => w.name === "num_inputs");
                if (!numInputsWidget) return;

                const numInputs = numInputsWidget.value;
                
                // Initialize node.inputs if it doesn't exist
                if (!node.inputs) {
                    node.inputs = [];
                }
                
                // Filter existing value inputs
                const existingInputs = node.inputs.filter(input => input.name.startsWith("value_"));
                
                // Add new inputs if needed
                if (existingInputs.length < numInputs) {
                    for (let i = existingInputs.length + 1; i <= numInputs; i++) {
                        const inputName = `value_${i}`;
                        if (!node.inputs.find(input => input.name === inputName)) {
                            node.addInput(inputName);  // Type is defined in Python
                        }
                    }
                } 
                // Remove excess inputs if too many
                else {
                    node.inputs = node.inputs.filter(input => 
                        !input.name.startsWith("value_") || 
                        parseInt(input.name.split("_")[1]) <= numInputs
                    );
                }
                
                // Adjust node size while preserving width
                node.setSize(node.computeSize());
                node.size[0] = initialWidth;
            };

            // Ensure num_inputs widget is at the top and set its callback
            const numInputsWidget = node.widgets.find(w => w.name === "num_inputs");
            if (numInputsWidget) {
                node.widgets = [numInputsWidget, ...node.widgets.filter(w => w !== numInputsWidget)];
                numInputsWidget.callback = () => {
                    updateInputs();
                    app.graph.setDirtyCanvas(true);
                };
            }

            // Perform initial input update after node creation
            setTimeout(updateInputs, 0);
        }
    }
});