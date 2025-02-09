import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";

app.registerExtension({
  name: "Bjornulf.LoopLinesSequential",
  async nodeCreated(node) {
    if (node.comfyClass !== "Bjornulf_LoopLinesSequential") return;

    // Hide seed widget
    const seedWidget = node.widgets.find((w) => w.name === "seed");
    if (seedWidget) {
      seedWidget.visible = false;
    }

    // Add line number display
    const lineNumberWidget = node.addWidget("html", "Current Line: --", null, {
      callback: () => {},
    });

    // Function to update the Reset Button text
    const updateResetButtonTextNode = () => {
      console.log("[loop_lines_sequential]=====> updateResetButtonTextNode");
      if (!node.graph) return;

      fetch("/get_current_line_number", {
        method: "POST",
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            const jumpWidget = node.widgets.find((w) => w.name === "jump");
            if (data.value === 0) {
              resetButton.name =
                "Reset Counter (Empty, next: " + jumpWidget.value + ")";
            } else {
              //Add to data.value, the current jump value
              let next_value = data.value + jumpWidget.value;
              //   console.log(jumpWidget);
              resetButton.name = `Reset Counter (next: ${next_value})`;
            }
          } else {
            console.error("[Loop Lines Sequential] Error in context size:", data.error);
            resetButton.name = "Reset Counter (Error)";
          }
        })
        .catch((error) => {
          console.error("[Loop Lines Sequential] Error fetching context size:", error);
          resetButton.name = "Reset Counter (Error)";
        });
    };

    // Add reset button
    const resetButton = node.addWidget("button", "Reset Counter", null, () => {
      fetch("/reset_lines_counter", {
        method: "POST",
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            // updateLineNumber();
            updateResetButtonTextNode();
            // app.ui.dialog.show("Counter reset successfully!");
          } else {
            app.ui.dialog.show(
              `[Loop Lines Sequential] Failed to reset counter: ${data.error || "Unknown error"}`);
          }
        })
        .catch((error) => {
          console.error("[Loop Lines Sequential] Error:", error);
          app.ui.dialog.show("[Loop Lines Sequential] An error occurred while resetting the counter.");
        });
    });

    // Add increment button
    const incrementButton = node.addWidget("button", "+1", null, () => {
      fetch("/increment_lines_counter", {
        method: "POST",
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            updateResetButtonTextNode();
            // app.ui.dialog.show("Counter incremented");
          } else {
            app.ui.dialog.show(
              `[Loop Lines Sequential] Failed to increment counter: ${data.error || "Unknown error"}`);
          }
        })
        .catch((error) => {
          console.error("[Loop Lines Sequential] Error:", error);
          app.ui.dialog.show("[Loop Lines Sequential] An error occurred while incrementing the counter.");
        });
    });

    // Add decrement button
    const decrementButton = node.addWidget("button", "-1", null, () => {
      fetch("/decrement_lines_counter", {
        method: "POST",
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            updateResetButtonTextNode();
            // app.ui.dialog.show("Counter decremented");
          } else {
            app.ui.dialog.show(
              `[Loop Lines Sequential] Failed to decrement counter: ${data.error || "Unknown error"}`);
          }
        })
        .catch((error) => {
          console.error("[Loop Lines Sequential] Error:", error);
          app.ui.dialog.show("[Loop Lines Sequential] An error occurred while decrementing the counter.");
        });
    });

    // Update line number periodically
    setTimeout(updateResetButtonTextNode, 0);

    // Listen for node execution events
    api.addEventListener("executed", async () => {
      updateResetButtonTextNode();
    });

    // Add a handler for the jump widget
    const waitingWidget = node.widgets.find((w) => w.name === "jump");
    if (waitingWidget) {
      const originalOnChange = waitingWidget.callback;
      waitingWidget.callback = function (v) {
        if (originalOnChange) {
          originalOnChange.call(this, v);
        }
        updateResetButtonTextNode();
      };
    }

    // Override the original execute function
    const originalExecute = node.execute;
    node.execute = function () {
      const result = originalExecute.apply(this, arguments);
      if (result instanceof Promise) {
        return result.catch((error) => {
          if (error.message.includes("Counter has reached its limit")) {
            app.ui.dialog.show(`[Loop Lines Sequential] Execution blocked: ${error.message}`);
          }
          throw error;
        });
      }
      return result;
    };
  },
});
