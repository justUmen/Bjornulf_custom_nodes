// import { app } from "../../../scripts/app.js";

// app.registerExtension({
//     name: "Bjornulf.ImageNoteLoadImage",
//     async nodeCreated(node) {
//         // Ensure the node is of the specific class
//         if (node.comfyClass !== "Bjornulf_ImageNoteLoadImage") return;
// 		console.log("node created");

//         // Store the initial node size
//         let prevSize = [...node.size];
//         let stableCount = 0;
//         const minStableFrames = 3; // Number of frames the size must remain stable

//         // Function to check if the node's size has stabilized
//         const checkSizeStable = () => {
//             if (node.size[0] === prevSize[0] && node.size[1] === prevSize[1]) {
//                 stableCount++;
//                 if (stableCount >= minStableFrames) {
//                     // Size has been stable, simulate a resize to trigger layout update
//                     const originalSize = [...node.size];
//                     node.setSize([originalSize[0] + 1, originalSize[1]]); // Slightly increase width
//                     setTimeout(() => {
//                         node.setSize(originalSize); // Revert to original size
//                         app.graph.setDirtyCanvas(true, true); // Trigger canvas redraw
//                     }, 0);
//                 } else {
//                     // Size is stable but not for enough frames yet, check again
//                     requestAnimationFrame(checkSizeStable);
//                 }
//             } else {
//                 // Size changed, reset counter and update prevSize
//                 prevSize = [...node.size];
//                 stableCount = 0;
//                 requestAnimationFrame(checkSizeStable);
//             }
//         };

//         // Start checking after a short delay to allow node initialization
//         setTimeout(() => {
//             requestAnimationFrame(checkSizeStable);
//         }, 5000);
//     }
// });
