import { app } from "../../../scripts/app.js";
app.registerExtension({
    name: "Bjornulf.ImageNoteLoadImage",
    async nodeCreated(node) {
        if (node.comfyClass !== "Bjornulf_ImageNoteLoadImage") return;

        setTimeout(() => {
            // Update widget positions
            node.onResize(node.size);
            
            // Refresh all widgets
            node.widgets.forEach(w => {
                if (w.onShow?.(true)) {
                    w.onShow?.(false);
                }
            });
            
            app.graph.setDirtyCanvas(true, true);
        }, 500);
    }
});

// app.registerExtension({
//     name: "Bjornulf.ImageNote",
//     async nodeCreated(node) {
//         if (node.comfyClass !== "Bjornulf_ImageNote") return;

//         // Add Save Note button
//         node.addWidget("button", "Save Note", null, () => {
//             const imagePathWidget = node.widgets.find(w => w.name === "image_path");
//             const noteTextWidget = node.widgets.find(w => w.name === "note_text");
            
//             if (!imagePathWidget?.value) {
//                 return;
//             }

//             fetch("/save_note", {
//                 method: "POST",
//                 body: JSON.stringify({
//                     image_path: imagePathWidget.value,
//                     note_text: noteTextWidget?.value || ""
//                 }),
//                 headers: { "Content-Type": "application/json" }
//             })
//             .then(response => response.json())
//             .catch(error => {
//                 console.error("Error saving note:", error);
//             });
//         });

//         // Add Load Note button
//         node.addWidget("button", "Load Note", null, () => {
//             const imagePathWidget = node.widgets.find(w => w.name === "image_path");
            
//             if (!imagePathWidget?.value) {
//                 return;
//             }

//             fetch("/load_note", {
//                 method: "POST",
//                 body: JSON.stringify({ image_path: imagePathWidget.value }),
//                 headers: { "Content-Type": "application/json" }
//             })
//             .then(response => response.json())
//             .then(data => {
//                 if (data.success) {
//                     const noteTextWidget = node.widgets.find(w => w.name === "note_text");
//                     if (noteTextWidget) {
//                         noteTextWidget.value = data.note_text;
//                         // Trigger widget changed event to update UI
//                         app.graph.setDirtyCanvas(true);
//                     }
//                 }
//             })
//             .catch(error => {
//                 console.error("Error loading note:", error);
//             });
//         });
//     }
// });