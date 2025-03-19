import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "Bjornulf.CivitAIModelSelector",
    async nodeCreated(node) {
        if (node.comfyClass === "Bjornulf_CivitAIModelSelector") {
            // Find all upload widgets
            const uploadWidgets = node.widgets.filter(w => w.type === "file");
            
            uploadWidgets.forEach(widget => {
                // Store the original draw function
                const originalDraw = widget.draw;
                
                // Override the draw function
                widget.draw = function(ctx, node, width, pos, height) {
                    const result = originalDraw.call(this, ctx, node, width, pos, height);
                    
                    // Hide all file inputs for this widget
                    const fileInputs = document.querySelectorAll(`input[type="file"][data-widget="${this.name}"]`);
                    fileInputs.forEach(input => {
                        input.style.display = 'none';
                    });
                    
                    return result;
                };
            });
        }
    }
});

app.registerExtension({
    name: "Bjornulf.LoadCivitAILinks",
    async nodeCreated(node) {
        if (node.comfyClass === "Bjornulf_LoadCivitAILinks") {
            // Add a refresh button widget
            const refreshButton = node.addWidget(
                "button",
                "Refresh File List",
                null,
                () => {
                    fetch("/get_civitai_links_files", {
                        method: "POST",
                    })
                        .then((response) => response.json())
                        .then((data) => {
                            if (data.success) {
                                // Update the dropdown with the new file list
                                const dropdownWidget = node.widgets.find(w => w.name === "selected_file");
                                if (dropdownWidget) {
                                    dropdownWidget.options.values = ["Not selected", ...data.files];
                                    dropdownWidget.value = "Not selected";
                                    app.ui.dialog.show(
                                        "[LoadCivitAILinks] File list refreshed successfully!"
                                    );
                                }
                            } else {
                                app.ui.dialog.show(
                                    `[LoadCivitAILinks] Failed to refresh file list: ${
                                        data.error || "Unknown error"
                                    }`
                                );
                            }
                        })
                        .catch((error) => {
                            console.error(
                                "[LoadCivitAILinks] Error fetching links files:",
                                error
                            );
                            app.ui.dialog.show(
                                "[LoadCivitAILinks] An error occurred while refreshing the file list."
                            );
                        });
                }
            );
        }
    },
});