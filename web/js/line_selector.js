import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";

app.registerExtension({
  name: "Bjornulf.LineSelector",
  async nodeCreated(node) {
    if (node.comfyClass !== "Bjornulf_LineSelector") return;

    // Hide seed widget
    const seedWidget = node.widgets.find((w) => w.name === "seed");
    if (seedWidget) {
      seedWidget.visible = false;
    }

    // Function to update the Reset Button text
    const updateResetButtonTextNode = () => {
      console.log("[line_selector]=====> updateResetButtonTextNode");
      if (!node.graph) return;

      fetch("/get_line_selector_counter", {
        method: "POST",
      })
        .then((response) => response.json())
        .then((data) => {
          if (!node.graph) return;

          if (data.success) {
            const jumpWidget = node.widgets.find((w) => w.name === "jump");
            const text = node.widgets.find((w) => w.name === "text");

            if (data.value === 0) {
              resetButton.name = "Reset Counter (Empty)";
            } else {
              const lines = text.value
                .split("\n")
                .filter((line) => line.trim() && !line.trim().startsWith("#"));
              const lineCount = lines.length;

              let next_value = data.value + jumpWidget.value;
              if (next_value > lineCount) {
                resetButton.name = `Reset Counter (ABOVE MAX: ${next_value} > ${lineCount})`;
              } else {
                resetButton.name = `Reset Counter (next: ${next_value})`;
              }
            }
          } else if (node.graph) {
            resetButton.name = "Reset Counter (Error)";
          }
        })
        .catch((error) => {
          if (node.graph) {
            resetButton.name = "Reset Counter (Error)";
          }
        });
    };

    // Add reset button
    const resetButton = node.addWidget(
      "button",
      "Reset Counter",
      null,
      async () => {
        if (!node.graph) return;

        try {
          const response = await fetch("/reset_line_selector_counter", {
            method: "POST",
          });
          const data = await response.json();

          if (!node.graph) return;

          if (data.success) {
            app.ui.dialog.show(`[Line Selector] Reset counter successfully.`);
            updateResetButtonTextNode();
          } else {
            app.ui.dialog.show(
              `[Line Selector] Failed to reset counter: ${
                data.error || "Unknown error"
              }`
            );
          }
        } catch (error) {
          if (node.graph) {
            app.ui.dialog.show(
              "[Line Selector] An error occurred while resetting the counter."
            );
          }
        }
      }
    );

    api.addEventListener("executed", async () => {
      const contextWidget = node.widgets.find(
        (w) => w.name === "LOOP_SEQUENTIAL"
      );
      if (contextWidget && contextWidget.value) {
        updateResetButtonTextNode();
      }
    });

    // Override the original execute function
    const originalExecute = node.execute;
    node.execute = function () {
      const result = originalExecute.apply(this, arguments);
      if (result instanceof Promise) {
        return result.catch((error) => {
          if (error.message.includes("Counter has reached") && node.graph) {
            app.ui.dialog.show(`Execution blocked: ${error.message}`);
          }
          throw error;
        });
      }
      return result;
    };

    // Setup widget handlers for updating counter display
    const setupWidgetHandler = (widgetName) => {
      const widget = node.widgets.find((w) => w.name === widgetName);
      if (widget) {
        const originalOnChange = widget.callback;
        widget.callback = function (v) {
          if (originalOnChange) {
            originalOnChange.call(this, v);
          }
          if (node.widgets.find((w) => w.name === "LOOP_SEQUENTIAL")?.value) {
            updateResetButtonTextNode();
          }
        };
      }
    };

    setupWidgetHandler("jump");
    setupWidgetHandler("text");
    setupWidgetHandler("LOOP_SEQUENTIAL");

    // Update button visibility based on LOOP_SEQUENTIAL
    const updateButtonVisibility = () => {
      const loopSeqWidget = node.widgets.find(
        (w) => w.name === "LOOP_SEQUENTIAL"
      );
      if (loopSeqWidget) {
        if (loopSeqWidget.value) {
          resetButton.type = "button";
          updateResetButtonTextNode();
        } else {
          resetButton.type = "hidden";
        }
      }
    };

    // Setup visibility handler for LOOP_SEQUENTIAL
    const loopSeqWidget = node.widgets.find(
      (w) => w.name === "LOOP_SEQUENTIAL"
    );
    if (loopSeqWidget) {
      const originalOnChange = loopSeqWidget.callback;
      loopSeqWidget.callback = function (v) {
        if (originalOnChange) {
          originalOnChange.call(this, v);
        }
        updateButtonVisibility();
      };
    }

    // Initial update
    setTimeout(updateButtonVisibility, 0);
  },
});