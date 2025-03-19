import { api } from '../../../scripts/api.js';
import { app } from "../../../scripts/app.js";

// Function to display the audio preview
function displayAudioPreview(component, filename, category, autoplay, mute, loop) {
    let audioWidget = component._audioWidget;

    // Create the audio widget if it doesn't exist
    if (!audioWidget) {
        const container = document.createElement("div");

        // Add the DOM widget to the component
        audioWidget = component.addDOMWidget("Bjornulf", "preview", container, {
            serialize: false,
            hideOnZoom: false,
            getValue() {
                return container.value;
            },
            setValue(v) {
                container.value = v;
            },
        });

        // Initialize widget properties
        audioWidget.value = { hidden: false, paused: false, params: {} };
        audioWidget.parentElement = document.createElement("div");
        audioWidget.parentElement.className = "audio_preview";
        audioWidget.parentElement.style.width = "100%";
        audioWidget.parentElement.style.marginBottom = "50px";
        container.appendChild(audioWidget.parentElement);

        // Create the audio element
        audioWidget.audioElement = document.createElement("audio");
        audioWidget.audioElement.controls = true;
        audioWidget.audioElement.style.width = "100%";

        // Hide the audio player on error
        audioWidget.audioElement.addEventListener("error", () => {
            audioWidget.parentElement.hidden = true;
        });

        audioWidget.parentElement.hidden = audioWidget.value.hidden;
        audioWidget.parentElement.appendChild(audioWidget.audioElement);
        component._audioWidget = audioWidget; // Store for reuse
    }

    // Set audio source and properties
    const params = {
        "filename": filename,
        "subfolder": category,
        "type": "temp",
        "rand": Math.random().toString().slice(2, 12) // Cache-busting random parameter
    };

    const urlParams = new URLSearchParams(params);
    audioWidget.audioElement.src = `api/view?${urlParams.toString()}`;
    audioWidget.audioElement.autoplay = autoplay && !audioWidget.value.paused && !audioWidget.value.hidden;
    audioWidget.audioElement.loop = loop;
}

// Register the extension
app.registerExtension({
    name: "Bjornulf.AudioPreview",
    async beforeRegisterNodeDef(nodeType, nodeData, appInstance) {
        if (nodeData?.name === "Bjornulf_AudioPreview") {
            // Define behavior when the node executes
            nodeType.prototype.onExecuted = function(data) {
                const autoplay = this.widgets.find(w => w.name === "autoplay")?.value ?? false;
                const loop = this.widgets.find(w => w.name === "loop")?.value ?? false;
                displayAudioPreview(this, data.audio[0], data.audio[1], autoplay, loop);
            };

            // Override computeSize to set a fixed height
            nodeType.prototype.computeSize = function() {
                const size = LiteGraph.LGraphNode.prototype.computeSize.call(this);
                size[1] = 150; // Fixed height of 150px
                return size;
            };
        }
    }
});