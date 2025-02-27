import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";

app.registerExtension({
  name: "Bjornulf.GlobalSeedManager",
  async nodeCreated(node) {
    // Ensure the button is added only to RandomSeedNode
    if (node.comfyClass !== "Bjornulf_GlobalSeedManager") return;

    // Add a button widget to the node
    const deleteButton = node.addWidget(
      "button",              // Widget type
      "Delete Seeds LIST",   // Button label
      null,                  // Initial value (not needed for buttons)
      async () => {
        // Ensure the node is still in the graph
        if (!node.graph) return;

        try {
          // Make a POST request to the delete endpoint
          const response = await fetch("/delete_random_seeds", {
            method: "POST",
          });
          const data = await response.json();

          // Show feedback to the user
          if (data.success) {
            app.ui.dialog.show("Seeds file deleted successfully.");
          } else {
            app.ui.dialog.show(`Failed to delete seeds file: ${data.error}`);
          }
        } catch (error) {
          app.ui.dialog.show("An error occurred while deleting the seeds file.");
        }
      }
    );
  },
});