import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";

// Add CSS style for the black background button class
const style = document.createElement("style");
style.textContent = `
  .reset-button-exceeded {
    background-color: black !important;
    color: white !important;
  }
`;

app.registerExtension({
  name: "Bjornulf.LoopIntegerSequential",
  async nodeCreated(node) {
    if (node.comfyClass !== "Bjornulf_LoopIntegerSequential") return;

    // Hide seed widget
    const seedWidget = node.widgets.find((w) => w.name === "seed");
    if (seedWidget) {
      seedWidget.visible = false;
    }

    // Function to update the Reset Button text
    const updateResetButtonTextNode = () => {
      console.log("[loop_sequential_integer]=====> updateResetButtonTextNode");
      if (!node.graph) return;
      
      fetch("/get_counter_value", {
        method: "POST",
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            const jumpWidget = node.widgets.find((w) => w.name === "jump");
            const fromThisWidget = node.widgets.find(
              (w) => w.name === "from_this"
            );
            if (data.value === 0) {
              resetButton.name =
                "Reset Counter (Empty, next: " + fromThisWidget.value + ")";
            } else {
              const toThatWidget = node.widgets.find(
                (w) => w.name === "to_that"
              );
              let next_value = data.value + jumpWidget.value - 1;
              if (next_value > toThatWidget.value) {
                resetButton.name = `Reset Counter (ABOVE MAX: ${next_value} > ${toThatWidget.value})`;
                console.log("resetButton", resetButton);
              } else {
                resetButton.name = `Reset Counter (next: ${next_value})`; // - ${toThatWidget.value}
              }
            }
          } else {
            console.error("[Loop Integer Sequential] Error in context size:", data.error);
            resetButton.name = "Reset Counter (Error)";
          }
        })
        .catch((error) => {
          console.error("[Loop Integer Sequential] Error fetching context size:", error);
          resetButton.name = "Reset Counter (Error)";
        });
    };

    // Add reset button
    const resetButton = node.addWidget("button", "Reset Counter", null, () => {
      fetch("/reset_counter", {
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
              `[Loop Integer Sequential] Failed to reset counter: ${data.error || "Unknown error"}`);
          }
        })
        .catch((error) => {
          console.error("[Loop Integer Sequential] Error:", error);
          app.ui.dialog.show("[Loop Integer Sequential] An error occurred while resetting the counter.");
        });
    });

    // Override the original execute function
    const originalExecute = node.execute;
    node.execute = function () {
      const result = originalExecute.apply(this, arguments);
      if (result instanceof Promise) {
        return result.catch((error) => {
          if (error.message.includes("[Loop Integer Sequential] Counter has reached its limit")) {
            app.ui.dialog.show(`[Loop Integer Sequential] Execution blocked: ${error.message}`, {
              type: "error",
              duration: 5000,
            });
          }
          throw error; // Re-throw the error to stop further execution
        });
      }
      return result;
    };

    // Initial update of showing counter number
    setTimeout(updateResetButtonTextNode, 0);

    // Listen for node execution events (update value when node executed)
    api.addEventListener("executed", async () => {
      updateResetButtonTextNode();
    });

    // Add a handler for the jump widget (update value reset on change)
    const jumpWidget = node.widgets.find((w) => w.name === "jump");
    if (jumpWidget) {
      const originalOnChange = jumpWidget.callback;
      jumpWidget.callback = function (v) {
        if (originalOnChange) {
          originalOnChange.call(this, v);
        }
        updateResetButtonTextNode();
      };
    }
    // Add a handler for the to_that widget (update value reset on change)
    const toThatWidget = node.widgets.find((w) => w.name === "to_that");
    if (toThatWidget) {
      const originalOnChange = toThatWidget.callback;
      toThatWidget.callback = function (v) {
        if (originalOnChange) {
          originalOnChange.call(this, v);
        }
        updateResetButtonTextNode();
      };
    }
    // Add a handler for the to_that widget (on change from_this => reset button)
    const fromThisWidget = node.widgets.find((w) => w.name === "from_this");
    if (fromThisWidget) {
      const originalOnChange = fromThisWidget.callback;
      fromThisWidget.callback = function (v) {
        if (originalOnChange) {
          originalOnChange.call(this, v);
        }
        fetch("/reset_counter", {
          method: "POST",
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              // updateLineNumber();
              updateResetButtonTextNode();
              // app.ui.dialog.show("Counter reset successfully!", { duration: 5000 });
            } else {
              app.ui.dialog.show(
                `[Loop Integer Sequential] Failed to reset counter: ${data.error || "Unknown error"}`);
            }
          })
          .catch((error) => {
            console.error("[Loop Integer Sequential] Error:", error);
            app.ui.dialog.show("[Loop Integer Sequential] An error occurred while resetting the counter.");
          });
      };
    }
  },
});
