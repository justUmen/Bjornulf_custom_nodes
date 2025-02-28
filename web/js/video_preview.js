import { api } from '../../../scripts/api.js';
import { app } from "../../../scripts/app.js";

function displayVideoPreview(component, filename, category, autoplay, mute) {
    let videoWidget = component._videoWidget;
    if (!videoWidget) {
        // Create the widget if it doesn't exist
        var container = document.createElement("div");
        const currentNode = component;
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
        videoWidget.computeSize = function(width) {
            if (this.aspectRatio && !this.parentElement.hidden) {
                let height = (currentNode.size[0] - 20) / this.aspectRatio + 10;
                if (!(height > 0)) {
                    height = 0;
                }
                return [width, height];
            }
            return [width, -4];
        };
        videoWidget.value = { hidden: false, paused: false, params: {} };
        videoWidget.parentElement = document.createElement("div");
        videoWidget.parentElement.className = "video_preview";
        videoWidget.parentElement.style['width'] = "100%";
        container.appendChild(videoWidget.parentElement);
        videoWidget.videoElement = document.createElement("video");
        videoWidget.videoElement.controls = true;
        videoWidget.videoElement.loop = false;
        videoWidget.videoElement.muted = false;
        videoWidget.videoElement.style['width'] = "100%";
        videoWidget.videoElement.addEventListener("loadedmetadata", () => {
            videoWidget.aspectRatio = videoWidget.videoElement.videoWidth / videoWidget.videoElement.videoHeight;
            adjustSize(component);
        });
        videoWidget.videoElement.addEventListener("error", () => {
            videoWidget.parentElement.hidden = true;
            adjustSize(component);
        });

        videoWidget.parentElement.hidden = videoWidget.value.hidden;
        videoWidget.videoElement.autoplay = !videoWidget.value.paused && !videoWidget.value.hidden;
        videoWidget.videoElement.hidden = false;
        videoWidget.parentElement.appendChild(videoWidget.videoElement);
        component._videoWidget = videoWidget; // Store the widget for future reference
    }

    // Update the video source
    let params = {
        "filename": filename,
        "subfolder": category,
        "type": "output",
        "rand": Math.random().toString().slice(2, 12)
    };
    const urlParams = new URLSearchParams(params);
    if(mute) videoWidget.videoElement.muted = true;
    else videoWidget.videoElement.muted = false;
    if(autoplay) videoWidget.videoElement.autoplay = !videoWidget.value.paused && !videoWidget.value.hidden;
    else videoWidget.videoElement.autoplay = false;
    // videoWidget.videoElement.src = `http://localhost:8188/api/view?${urlParams.toString()}`;
    videoWidget.videoElement.src = `api/view?${urlParams.toString()}`;

    adjustSize(component); // Adjust the component size
}

function adjustSize(component) {
    component.setSize([component.size[0], component.computeSize([component.size[0], component.size[1]])[1]]);
    component?.graph?.setDirtyCanvas(true);
}

app.registerExtension({
    name: "Bjornulf.VideoPreview",
    async beforeRegisterNodeDef(nodeType, nodeData, appInstance) {
        if (nodeData?.name == "Bjornulf_VideoPreview") {
            nodeType.prototype.onExecuted = function (data) {
                const autoplay = this.widgets.find(w => w.name === "autoplay")?.value ?? false;
                const mute = this.widgets.find(w => w.name === "mute")?.value ?? true;
                displayVideoPreview(this, data.video[0], data.video[1], autoplay, mute);
            };
        }
    }
});