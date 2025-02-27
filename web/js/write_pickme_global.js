import { app } from "../../../scripts/app.js";

// Function to pick a node within its global_pickme_id group
function pickGlobalNode(node) {
    const global_pickme_idWidget = node.widgets.find(w => w.name === "global_pickme_id");
    const global_pickme_id = global_pickme_idWidget ? global_pickme_idWidget.value : "default";
    
    // Iterate through all nodes in the graph
    app.graph._nodes.forEach(n => {
        if (n.comfyClass === "Bjornulf_WriteTextPickMeGlobal") {
            const nglobal_pickme_idWidget = n.widgets.find(w => w.name === "global_pickme_id");
            const nglobal_pickme_id = nglobal_pickme_idWidget ? nglobal_pickme_idWidget.value : "default";
            if (nglobal_pickme_id === global_pickme_id) {  // Only affect nodes in the same group
                const pickedWidget = n.widgets.find(w => w.name === "picked");
                if (pickedWidget) {
                    pickedWidget.value = (n === node);  // Pick this node, unpick others in group
                }
                n.color = (n === node) ? "#006400" : "";  // Green for picked, default otherwise
            }
        }
    });
    app.graph.setDirtyCanvas(true, true);  // Refresh the canvas
}

app.registerExtension({
    name: "Bjornulf.WriteTextPickMeGlobal",
    async nodeCreated(node) {
        if (node.comfyClass === "Bjornulf_WriteTextPickMeGlobal") {
            // Hide the picked widget from the UI
            const pickedWidget = node.widgets.find(w => w.name === "picked");
            if (pickedWidget && pickedWidget.inputEl) {
                pickedWidget.inputEl.style.display = "none";
            }

            // Add "PICK ME" button
            const buttonWidget = node.addWidget("button", "PICK ME", null, () => {
                pickGlobalNode(node);  // Handle picking within the group
            });
            buttonWidget.computeSize = function () {
                return [node.size[0] - 20, 30];  // Size the button
            };

            // Function to update node color based on picked state
            const updateColors = () => {
                const picked = node.widgets.find(w => w.name === "picked")?.value;
                node.color = picked ? "#006400" : "";  // Green if picked
            };
            updateColors();  // Set initial color

            // Handle global_pickme_id changes
            const global_pickme_idWidget = node.widgets.find(w => w.name === "global_pickme_id");
            if (global_pickme_idWidget) {
                global_pickme_idWidget.onChange = function() {
                    const pickedWidget = node.widgets.find(w => w.name === "picked");
                    if (pickedWidget && pickedWidget.value) {
                        pickedWidget.value = false;  // Unpick if global_pickme_id changes
                        node.color = "";
                        app.graph.setDirtyCanvas(true, true);
                    }
                };
            }

            // State management for saving/loading
            const origSetNodeState = node.setNodeState;
            node.setNodeState = function (state) {
                origSetNodeState?.apply(this, arguments);
                if (state.picked !== undefined) {
                    const widget = this.widgets.find(w => w.name === "picked");
                    if (widget) widget.value = state.picked;
                }
                updateColors();
            };

            const origGetNodeState = node.getNodeState;
            node.getNodeState = function () {
                const state = origGetNodeState?.apply(this, arguments) || {};
                state.picked = this.widgets.find(w => w.name === "picked")?.value ?? false;
                return state;
            };

            // Refresh canvas on load
            app.graph.setDirtyCanvas(true, true);
        }
    }
});