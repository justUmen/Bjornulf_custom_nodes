import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "Bjornulf.AllLoraSelector",
    async nodeCreated(node) {
        if (node.comfyClass === "Bjornulf_AllLoraSelector") {
            node.properties = node.properties || {};
            
            const updateLoraInputs = () => {
                const initialWidth = node.size[0];
                const numLorasWidget = node.widgets.find(w => w.name === "number_of_loras");
                if (!numLorasWidget) return;

                const numLoras = numLorasWidget.value;
                const loraList = node.widgets.find(w => w.name === "lora_1")?.options?.values || [];

                // Save existing values
                node.widgets.forEach(w => {
                    if (w.name.startsWith("lora_") || w.name.startsWith("strength_model_") || w.name.startsWith("strength_clip_")) {
                        node.properties[w.name] = w.value;
                    }
                });

                // Remove existing LoRA-related widgets
                node.widgets = node.widgets.filter(w => 
                    !w.name.startsWith("lora_") && 
                    !w.name.startsWith("strength_model_") && 
                    !w.name.startsWith("strength_clip_")
                );

                // Add number_of_loras widget if it doesn't exist
                const ensureWidget = (name, type, defaultValue, config) => {
                    let widget = node.widgets.find(w => w.name === name);
                    if (!widget) {
                        widget = node.addWidget(type, name, 
                            node.properties[name] !== undefined ? node.properties[name] : defaultValue,
                            value => { node.properties[name] = value; },
                            config
                        );
                    }
                };

                ensureWidget("number_of_loras", "number", 3, { min: 1, max: 20, step: 1 });

                // Add LoRA widgets for each slot
                for (let i = 1; i <= numLoras; i++) {
                    const loraName = `lora_${i}`;
                    const strengthModelName = `strength_model_${i}`;
                    const strengthClipName = `strength_clip_${i}`;

                    // Add LoRA selector
                    node.addWidget("combo", loraName,
                        node.properties[loraName] || loraList[0],
                        value => { node.properties[loraName] = value; },
                        { values: loraList }
                    );

                    // Add strength sliders
                    node.addWidget("number", strengthModelName,
                        node.properties[strengthModelName] !== undefined ? node.properties[strengthModelName] : 1.0,
                        value => { node.properties[strengthModelName] = value; },
                        { min: -100.0, max: 100.0, step: 0.01 }
                    );

                    node.addWidget("number", strengthClipName,
                        node.properties[strengthClipName] !== undefined ? node.properties[strengthClipName] : 1.0,
                        value => { node.properties[strengthClipName] = value; },
                        { min: -100.0, max: 100.0, step: 0.01 }
                    );
                }

                node.setSize(node.computeSize());
                node.size[0] = Math.max(initialWidth, node.size[0]);
            };

            // Set up number_of_loras widget callback
            const numLorasWidget = node.widgets.find(w => w.name === "number_of_loras");
            if (numLorasWidget) {
                numLorasWidget.callback = () => {
                    updateLoraInputs();
                    app.graph.setDirtyCanvas(true);
                };
            }

            // Handle serialization
            const originalOnSerialize = node.onSerialize;
            node.onSerialize = function(info) {
                if (originalOnSerialize) {
                    originalOnSerialize.call(this, info);
                }
                info.properties = { ...this.properties };
            };

            // Handle deserialization
            const originalOnConfigure = node.onConfigure;
            node.onConfigure = function(info) {
                if (originalOnConfigure) {
                    originalOnConfigure.call(this, info);
                }
                if (info.properties) {
                    Object.assign(this.properties, info.properties);
                }
                updateLoraInputs();
            };

            // Initial setup
            updateLoraInputs();
        }
    }
});