// // style_selector.js
// import { app } from "../../../scripts/app.js";

// app.registerExtension({
//   name: "Bjornulf.StyleSelector",
//   async nodeCreated(node) {
//     // Only apply to the Bjornulf_StyleSelector node
//     if (node.comfyClass !== "Bjornulf_StyleSelector") return;

//     // Find the widgets for LOOP_random_LIST and LOOP_style_LIST
//     const loopRandomWidget = node.widgets.find(w => w.name === "LOOP_random_LIST");
//     const loopStyleWidget = node.widgets.find(w => w.name === "LOOP_style_LIST");

//     // Check if widgets exist to avoid errors
//     if (!loopRandomWidget || !loopStyleWidget) {
//       console.error("LOOP widgets not found in Bjornulf_StyleSelector node.");
//       return;
//     }

//     // Function to toggle the other widget off when one is turned on
//     const toggleExclusive = (widgetToToggle, otherWidget) => {
//       if (widgetToToggle.value === true) {
//         otherWidget.value = false;
//       }
//     };

//     // Add event listeners to handle toggling
//     loopRandomWidget.callback = () => {
//       toggleExclusive(loopRandomWidget, loopStyleWidget);
//     };

//     loopStyleWidget.callback = () => {
//       toggleExclusive(loopStyleWidget, loopRandomWidget);
//     };

//     // Ensure initial state has only one enabled (if both are true, disable one)
//     if (loopRandomWidget.value && loopStyleWidget.value) {
//       loopStyleWidget.value = false; // Default to disabling LOOP_style_LIST
//     }

//     // Find the category and style widgets
//     const categoryWidget = node.widgets.find(w => w.name === "category");
//     const styleWidget = node.widgets.find(w => w.name === "style");

//     // Define categories and styles (must match the Python file)
//     const BRANCHES = {
//       "Painting": [
//         "Renaissance", "Baroque", "Rococo", "Neoclassicism",
//         "Romanticism", "Realism", "Impressionism", "Post-Impressionism",
//         "Expressionism", "Fauvism", "Cubism", "Futurism", "Dadaism",
//         "Surrealism", "Abstract Expressionism", "Pop Art", "Op Art",
//         "Minimalism"
//       ],
//       "Photography": [
//         "Black and White", "Color", "Vintage", "Sepia Tone", "HDR",
//         "Long Exposure", "Macro", "Portrait", "Landscape", "Street",
//         "Fashion", "Analog Film", "Cinematic"
//       ],
//       "Digital Art": [
//         "Digital Painting", "Vector Art", "Pixel Art", "Fractal Art",
//         "Algorithmic Art", "Glitch Art"
//       ],
//       "3D Rendering": [
//         "Low Poly", "Voxel", "Isometric", "Ray Tracing"
//       ],
//       "Illustration": [
//         "Line Art", "Cartoon", "Comic Book", "Manga", "Anime",
//         "Technical Illustration", "Botanical Illustration",
//         "Architectural Rendering", "Concept Art", "Storyboard Art"
//       ],
//     };

//     // Function to update the style dropdown based on the selected category
//     const updateStyles = () => {
//       const selectedCategory = categoryWidget.value;
//       const styles = BRANCHES[selectedCategory] || [];
//       styleWidget.options.values = styles;
//       if (styles.length > 0) {
//         styleWidget.value = styles[0]; // Set to the first style
//       } else {
//         styleWidget.value = ""; // Fallback if no styles
//       }
//       node.setDirtyCanvas(true); // Refresh the UI
//     };

//     // Initialize the style dropdown
//     updateStyles();

//     // Update the style dropdown whenever the category changes
//     categoryWidget.callback = updateStyles;
//   }
// });
import { app } from "../../../scripts/app.js";

app.registerExtension({
  name: "Bjornulf.StyleSelector",
  async nodeCreated(node) {
    if (node.comfyClass !== "Bjornulf_StyleSelector") return;

    // Find loop widgets
    const loopRandomWidget = node.widgets.find(w => w.name === "LOOP_random_LIST");
    const loopStyleWidget = node.widgets.find(w => w.name === "LOOP_style_LIST");
    const loopSequentialWidget = node.widgets.find(w => w.name === "LOOP_SEQUENTIAL");

    // Function to toggle the other widget off when one is turned on
    const toggleExclusive = (widgetToToggle, otherWidget) => {
      if (widgetToToggle.value === true) {
        otherWidget.value = false;
      }
    };

    // Add event listeners to handle toggling
    loopRandomWidget.callback = () => {
      toggleExclusive(loopRandomWidget, loopStyleWidget);
    };
    loopStyleWidget.callback = () => {
      toggleExclusive(loopStyleWidget, loopRandomWidget);
    };

    // Ensure initial state has only one enabled (if both are true, disable one)
    if (loopRandomWidget.value && loopStyleWidget.value) {
      loopStyleWidget.value = false; // Default to disabling LOOP_style_LIST
    }

    // Add reset button for style list counter
    const styleResetButton = node.addWidget(
      "button",
      "Reset Style Counter",
      null,
      async () => {
        try {
          const response = await fetch("/reset_style_list_counter", { method: "POST" });
          const data = await response.json();
          if (data.success) {
            app.ui.dialog.show("[Style Selector] Style counter reset successfully.");
          } else {
            app.ui.dialog.show("[Style Selector] Failed to reset style counter.");
          }
        } catch (error) {
          app.ui.dialog.show("[Style Selector] Error resetting style counter.");
        }
      }
    );

    // Add reset button for model list counter
    const modelResetButton = node.addWidget(
      "button",
      "Reset Model Counter",
      null,
      async () => {
        try {
          const response = await fetch("/reset_model_list_counter", { method: "POST" });
          const data = await response.json();
          if (data.success) {
            app.ui.dialog.show("[Style Selector] Model counter reset successfully.");
          } else {
            app.ui.dialog.show("[Style Selector] Failed to reset model counter.");
          }
        } catch (error) {
          app.ui.dialog.show("[Style Selector] Error resetting model counter.");
        }
      }
    );

    // Function to update visibility of reset buttons
    const updateButtonVisibility = () => {
      const sequentialEnabled = loopSequentialWidget.value;
      styleResetButton.type = sequentialEnabled && loopStyleWidget.value ? "button" : "hidden";
      modelResetButton.type = sequentialEnabled && loopRandomWidget.value ? "button" : "hidden";
    };

    // Initial update of button visibility
    setTimeout(updateButtonVisibility, 0);

    // Update visibility when widgets change
    loopSequentialWidget.callback = updateButtonVisibility;
    loopStyleWidget.callback = () => {
      toggleExclusive(loopStyleWidget, loopRandomWidget);
      updateButtonVisibility();
    };
    loopRandomWidget.callback = () => {
      toggleExclusive(loopRandomWidget, loopStyleWidget);
      updateButtonVisibility();
    };
  }
});