import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "Bjornulf.ModelClipVaeSelector",
    async nodeCreated(node) {
        if (node.comfyClass === "Bjornulf_ModelClipVaeSelector") {
            const updateInputs = () => {
                const numInputsWidget = node.widgets.find(w => w.name === "number_of_inputs");
                if (!numInputsWidget) return;

                const numInputs = numInputsWidget.value;
                
                // Initialize node.inputs if it doesn't exist
                if (!node.inputs) {
                    node.inputs = [];
                }
                
                // Filter existing model, clip, and vae inputs
                const existingModelInputs = node.inputs.filter(input => input.name.startsWith('model_'));
                const existingClipInputs = node.inputs.filter(input => input.name.startsWith('clip_'));
                const existingVaeInputs = node.inputs.filter(input => input.name.startsWith('vae_'));
                
                // Determine if we need to add or remove inputs
                if (existingModelInputs.length < numInputs || existingClipInputs.length < numInputs || existingVaeInputs.length < numInputs) {
                    // Add new model, clip, and vae inputs if not enough existing
                    for (let i = Math.max(existingModelInputs.length, existingClipInputs.length, existingVaeInputs.length) + 1; i <= numInputs; i++) {
                        const modelInputName = `model_${i}`;
                        const clipInputName = `clip_${i}`;
                        const vaeInputName = `vae_${i}`;
                        if (!node.inputs.find(input => input.name === modelInputName)) {
                            node.addInput(modelInputName, "MODEL");
                        }
                        if (!node.inputs.find(input => input.name === clipInputName)) {
                            node.addInput(clipInputName, "CLIP");
                        }
                        if (!node.inputs.find(input => input.name === vaeInputName)) {
                            node.addInput(vaeInputName, "VAE");
                        }
                    }
                } else {
                    // Remove excess model, clip, and vae inputs if too many
                    node.inputs = node.inputs.filter(input => 
                        (!input.name.startsWith('model_') && !input.name.startsWith('clip_') && !input.name.startsWith('vae_')) || 
                        (parseInt(input.name.split('_')[1]) <= numInputs)
                    );
                }
                
                node.setSize(node.computeSize());
            };

            // Move number_of_inputs to the top initially
            const numInputsWidget = node.widgets.find(w => w.name === "number_of_inputs");
            if (numInputsWidget) {
                node.widgets = [numInputsWidget, ...node.widgets.filter(w => w !== numInputsWidget)];
                numInputsWidget.callback = () => {
                    updateInputs();
                    app.graph.setDirtyCanvas(true);
                };
            }

            // Set seed widget to hidden input
            const seedWidget = node.widgets.find((w) => w.name === "seed");
            if (seedWidget) {
              seedWidget.type = "HIDDEN";
            }

            // Delay the initial update to ensure node is fully initialized
            setTimeout(updateInputs, 0);
        }
    }
});