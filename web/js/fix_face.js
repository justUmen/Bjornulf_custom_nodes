import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "Bjornulf.FixFace",
    async nodeCreated(node) {
        if (node.comfyClass === "Bjornulf_FixFace") {
            const updateInputs = () => {
                const initialWidth = node.size[0];
                const numFacesWidget = node.widgets.find(w => w.name === "number_of_faces");
                if (!numFacesWidget) return;

                const numFaces = numFacesWidget.value;
                
                // Initialize node.inputs if it doesn't exist
                if (!node.inputs) {
                    node.inputs = [];
                }
                
                // Filter existing FACE_SETTINGS inputs
                const existingInputs = node.inputs.filter(input => input.name.startsWith('FACE_SETTINGS_'));
                
                // Add or remove inputs based on number_of_faces
                if (existingInputs.length < numFaces) {
                    for (let i = existingInputs.length + 1; i <= numFaces; i++) {
                        const inputName = `FACE_SETTINGS_${i}`;
                        if (!node.inputs.find(input => input.name === inputName)) {
                            node.addInput(inputName, "FACE_SETTINGS");
                        }
                    }
                } else {
                    node.inputs = node.inputs.filter(input => !input.name.startsWith('FACE_SETTINGS_') || 
                                                              parseInt(input.name.split('_')[2]) <= numFaces);
                }
                
                node.setSize(node.computeSize());
                node.size[0] = initialWidth; // Keep width fixed
            };

            // Move number_of_faces widget to the top and set callback
            const numFacesWidget = node.widgets.find(w => w.name === "number_of_faces");
            if (numFacesWidget) {
                node.widgets = [numFacesWidget, ...node.widgets.filter(w => w !== numFacesWidget)];
                numFacesWidget.callback = () => {
                    updateInputs();
                    app.graph.setDirtyCanvas(true);
                };
            }

            // Initial update after node creation
            setTimeout(updateInputs, 0);
        }
    }
});