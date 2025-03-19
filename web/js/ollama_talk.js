import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";

// Node-specific logic
app.registerExtension({
  name: "Bjornulf.OllamaTalk",
  async nodeCreated(node) {
    if (node.comfyClass === "Bjornulf_OllamaTalk") {
      // Set seed widget to hidden input
      // const seedWidget = node.widgets.find((w) => w.name === "seed");
      // if (seedWidget) {
      //   seedWidget.type = "HIDDEN";
      // }

      // Function to update the Reset Button text
      const updateResetButtonTextNode = () => {
        console.log("[ollama_talk]=====> updateResetButtonTextNode:");
        if (!node.graph) return;

        fetch("/get_current_context_size", {
          method: "POST",
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              // console.log("[Ollama] /get_current_context_size fetched successfully");
              if (data.value === 0) {
                resetButton.name = "Save/Reset Context File (Empty)";
              } else {
                resetButton.name = `Reset Context File (${data.value} lines)`;
              }
            } else {
              console.error("[Ollama] Error in context size:", data.error);
              resetButton.name = "Save/Reset Context File (Error)";
            }
          })
          .catch((error) => {
            console.error("[Ollama] Error fetching context size:", error);
            resetButton.name = "Save/Reset Context File (Error)";
          });
      };

      // Add reset button
      const resetButton = node.addWidget(
        "button",
        "Save/Reset Context File",
        null,
        () => {
          fetch("/reset_lines_context", {
            method: "POST",
          })
            .then((response) => response.json())
            .then((data) => {
              if (data.success) {
                // updateLineNumber();
                updateResetButtonTextNode();
                app.ui.dialog.show("[Ollama] Context saved in Bjornulf/ollama and reset successfully!");
              } else {
                app.ui.dialog.show(
                  `[Ollama] Failed to reset Context: ${data.error || "Unknown error"}`);
              }
            })
            .catch((error) => {
              console.error("Error:", error);
              app.ui.dialog.show("[Ollama] An error occurred while resetting the Context.");
            });
        }
      );

      // Add resume button
      const resumeButton = node.addWidget("button", "Resume", "Resume", () => {
        const workflow = app.graph.serialize();
        const nodeData = workflow.nodes.find((n) => n.id === node.id);
        const userPromptValue =
          nodeData.widgets_values?.[
            node.widgets.findIndex((w) => w.name === "user_prompt")
          ];

        fetch("/bjornulf_ollama_send_prompt", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            node_id: node.id,
            user_prompt: userPromptValue,
          }),
        })
          .then((response) => response.text())
          .then((data) => {
            console.log("[Ollama] Resume response:", data);
          })
          .catch((error) => console.error("[Ollama] Error:", error));
      });

      // Function to update button visibility based on widget values
      // const updateButtonVisibility = () => {
      //   // Check context file widget
      //   const contextWidget = node.widgets.find(
      //     (w) => w.name === "use_context_file"
      //   );
      //   const isContextFileEnabled = contextWidget
      //     ? contextWidget.value
      //     : false;
      //   resetButton.type = isContextFileEnabled ? "button" : "HIDDEN";

      //   // Check waiting for prompt widget
      //   const waitingWidget = node.widgets.find(
      //     (w) => w.name === "waiting_for_prompt"
      //   );
      //   const isWaitingForPrompt = waitingWidget ? waitingWidget.value : false;
      //   resumeButton.type = isWaitingForPrompt ? "button" : "HIDDEN";

      //   //ALSO update reset button text node
      //   updateResetButtonTextNode(); // Will trigger when... toggle / refresh page

      //   // Force canvas redraw to update UI
      //   node.setDirtyCanvas(true);
      // };

      // In updateButtonVisibility function - Only update when context is enabled
      const updateButtonVisibility = () => {
        // Check context file widget
        const contextWidget = node.widgets.find(w => w.name === "use_context_file");
        const isContextFileEnabled = contextWidget ? contextWidget.value : false;
        resetButton.type = isContextFileEnabled ? "button" : "HIDDEN";

        // Check waiting for prompt widget
        const waitingWidget = node.widgets.find(w => w.name === "waiting_for_prompt");
        const isWaitingForPrompt = waitingWidget ? waitingWidget.value : false;
        resumeButton.type = isWaitingForPrompt ? "button" : "HIDDEN";

        // ONLY update reset button text if context file is enabled
        if (isContextFileEnabled) {
          updateResetButtonTextNode();
        }

        // Force canvas redraw to update UI
        node.setDirtyCanvas(true);
      };

      // Add a handler for the use_context_file widget
      const contextWidget = node.widgets.find(
        (w) => w.name === "use_context_file"
      );
      if (contextWidget) {
        const originalOnChange = contextWidget.callback;
        contextWidget.callback = function (v) {
          if (originalOnChange) {
            originalOnChange.call(this, v);
          }
          updateButtonVisibility();
        };
      }

      // Add a handler for the waiting_for_prompt widget
      const waitingWidget = node.widgets.find(
        (w) => w.name === "waiting_for_prompt"
      );
      if (waitingWidget) {
        const originalOnChange = waitingWidget.callback;
        waitingWidget.callback = function (v) {
          if (originalOnChange) {
            originalOnChange.call(this, v);
          }
          updateButtonVisibility();
        };
      }

      // Initial update of button visibility
      setTimeout(updateButtonVisibility, 0);

      // Listen for node execution events
      // api.addEventListener("executed", async () => {
      //   updateResetButtonTextNode();
      // });
      api.addEventListener("executed", async () => {
        // Check if context file is enabled before updating
        const contextWidget = node.widgets.find(w => w.name === "use_context_file");
        if (contextWidget && contextWidget.value) {
          updateResetButtonTextNode();
        }
      });

      //If workflow is stopped during pause, cancel the run
      const original_api_interrupt = api.interrupt;
      api.interrupt = function () {
          api.fetchApi('/bjornulf_ollama_interrupt', {
              method: 'POST'
          });
          original_api_interrupt.apply(this, arguments);
      }
    }
  },
});

// // Add listener for workflow execution
// app.addEventListener("workflowExecuted", () => {
//     if (node.graph.isPlaying) {
//         updateContextSize();
//     }
// });
// app.registerExtension({
//     name: "Bjornulf.OllamaContextChat",
//     async nodeCreated(node) {
//         if (node.comfyClass === "Bjornulf_OllamaContextChat") {
//             const resumeButton = node.addWidget("button", "Resume", "Resume", () => {
//                 fetch('/bjornulf_ollama_send_prompt', { method: 'GET' })
//                     .then(response => response.text())
//                     .then(data => {
//                         console.log('Resume response:', data);
//                         // You can update the UI here if needed
//                     })
//                     .catch(error => console.error('Error:', error));
//             });
//         }
//     }
// });

// Set seed widget to hidden input
// const seedWidget = node.widgets.find((w) => w.name === "seed");
// if (seedWidget) {
//   seedWidget.type = "HIDDEN";
// }
