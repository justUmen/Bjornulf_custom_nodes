import { app } from "../../../scripts/app.js";

app.registerExtension({
  name: "Bjornulf.LoadImagesFromSelectedFolder",
  async nodeCreated(node) {
    if (node.comfyClass !== "Bjornulf_LoadImagesFromSelectedFolder") return;

    // Add a "Refresh Folders" button
    node.addWidget(
      "button",
      "Refresh Folders",
      null,
      async () => {
        if (!node.graph) return;

        try {
          // Fetch the folder list from the server
          const response = await fetch("/get_image_folders");
          const data = await response.json();

          if (data.success && data.folders) {
            const dropdown = node.widgets.find(w => w.name === "selected_folder");
            if (dropdown) {
              // Remember the current selection
              const currentValue = dropdown.value;

              // Update the dropdown with the new folder list
              dropdown.options.values = data.folders;

              // Try to keep the same folder selected (accounting for image count changes)
              const folderNameRegex = /^(.+?)\s*\(\d+\s*images\)$/;
              const match = currentValue.match(folderNameRegex);
              let updatedValue = null;

              if (match) {
                const folderName = match[1]; // e.g., "folder1"
                updatedValue = data.folders.find(f => f.startsWith(folderName + " ("));
              }

              // Set the new value: keep the folder if it exists, otherwise pick the first one
              if (updatedValue) {
                dropdown.value = updatedValue;
              } else if (data.folders.length > 0) {
                dropdown.value = data.folders[0];
              } else {
                dropdown.value = null; // No folders available
              }

              // Let you know it worked
              app.ui.dialog.show("Folder list refreshed successfully.");
            } else {
              app.ui.dialog.show("Dropdown widget not found.");
            }
          } else {
            app.ui.dialog.show("Failed to fetch folder list.");
          }
        } catch (error) {
          app.ui.dialog.show("An error occurred while fetching the folder list.");
        }
      }
    );
  },
});