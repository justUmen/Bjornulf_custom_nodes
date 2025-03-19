import { app } from "../../../scripts/app.js";

app.registerExtension({
  name: "Bjornulf.LoadTextFromFolder",
  async nodeCreated(node) {
    if (node.comfyClass === "Bjornulf_LoadTextFromFolder") {
      // Add a refresh button widget
      // Assuming this is inside your node's setup function
      const refreshButton = node.addWidget(
        "button",
        "Refresh File List",
        null,
        () => {
          fetch("/get_text_files", {
            method: "POST",
          })
            .then((response) => response.json())
            .then((data) => {
              if (data.success) {
                // Update the dropdown with the new file list
                node.widgets[0].options.values = data.files; // Assuming the dropdown is the first widget
                node.widgets[0].value = data.files[0] || ""; // Set default value
                app.ui.dialog.show(
                  "[LoadTextFromFolder] File list refreshed successfully!"
                );
              } else {
                app.ui.dialog.show(
                  `[LoadTextFromFolder] Failed to refresh file list: ${
                    data.error || "Unknown error"
                  }`
                );
              }
            })
            .catch((error) => {
              console.error(
                "[LoadTextFromFolder] Error fetching text files:",
                error
              );
              app.ui.dialog.show(
                "[LoadTextFromFolder] An error occurred while refreshing the file list."
              );
            });
        }
      );
    }
  },
});
