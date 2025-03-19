import { api } from '../../../scripts/api.js';
import { app } from "../../../scripts/app.js";

// Function to display the video preview
function displayVideoPreview(component, filename, category, autoplay, mute, loop) {
    let videoWidget = component._videoWidget;

    // Create the video widget if it doesn't exist
    if (!videoWidget) {
        const container = document.createElement("div");
        const currentNode = component;

        // Add the DOM widget to the component
        videoWidget = component.addDOMWidget("videopreview", "preview", container, {
            serialize: false,
            hideOnZoom: false,
            getValue() {
                return container.value;
            },
            setValue(v) {
                container.value = v;
            },
        });

        // Define how the widget computes its size
        videoWidget.computeSize = function(width) {
            if (this.aspectRatio && !this.parentElement.hidden) {
                let height = (currentNode.size[0] - 20) / this.aspectRatio + 10;
                return [width, height > 0 ? height : 0];
            }
            return [width, -4];
        };

        // Initialize widget properties
        videoWidget.value = { hidden: false, paused: false, params: {} };
        videoWidget.parentElement = document.createElement("div");
        videoWidget.parentElement.className = "video_preview";
        videoWidget.parentElement.style.width = "100%";
        container.appendChild(videoWidget.parentElement);

        // Create the video element
        videoWidget.videoElement = document.createElement("video");
        videoWidget.videoElement.controls = true;
        videoWidget.videoElement.style.width = "100%";

        // Update aspect ratio when metadata is loaded
        videoWidget.videoElement.addEventListener("loadedmetadata", () => {
            videoWidget.aspectRatio = videoWidget.videoElement.videoWidth / videoWidget.videoElement.videoHeight;
            adjustSize(component);
        });

        // Hide the video on error
        videoWidget.videoElement.addEventListener("error", () => {
            videoWidget.parentElement.hidden = true;
            adjustSize(component);
        });

        videoWidget.parentElement.hidden = videoWidget.value.hidden;
        videoWidget.parentElement.appendChild(videoWidget.videoElement);
        component._videoWidget = videoWidget; // Store for reuse
    }

    // Set video source and properties
    const params = {
        "filename": filename,
        "subfolder": category,
        "type": "output",
        "rand": Math.random().toString().slice(2, 12) // Cache-busting random parameter
    };

    const urlParams = new URLSearchParams(params);
    videoWidget.videoElement.src = `api/view?${urlParams.toString()}`;
    videoWidget.videoElement.muted = mute;
    videoWidget.videoElement.autoplay = autoplay && !videoWidget.value.paused && !videoWidget.value.hidden;
    videoWidget.videoElement.loop = loop;

    // Adjust the component size after setting the video
    adjustSize(component);
}

// Function to adjust the component size
function adjustSize(component) {
    const newSize = component.computeSize([component.size[0], component.size[1]]);
    component.setSize([component.size[0], newSize[1]]);
    component?.graph?.setDirtyCanvas(true);
}

// Register the extension
app.registerExtension({
    name: "Bjornulf.VideoPreview",
    async beforeRegisterNodeDef(nodeType, nodeData, appInstance) {
        if (nodeData?.name === "Bjornulf_VideoPreview") {
            nodeType.prototype.onExecuted = function(data) {
                // Retrieve widget values with defaults
                const autoplay = this.widgets.find(w => w.name === "autoplay")?.value ?? false;
                const mute = this.widgets.find(w => w.name === "mute")?.value ?? true;
                const loop = this.widgets.find(w => w.name === "loop")?.value ?? false;

                // Display the video preview with the retrieved values
                displayVideoPreview(this, data.video[0], data.video[1], autoplay, mute, loop);
            };
        }
    }
});