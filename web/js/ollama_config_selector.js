import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "Bjornulf.OllamaConfig",
    async nodeCreated(node) {
        if (node.comfyClass === "Bjornulf_OllamaConfig") {
            // Add model_list combo widget
            const modelListWidget = node.addWidget(
                "combo",
                "select_model_here",
                "",
                (v) => {
                    try {
                        // When model_list changes, update model_name
                        const modelNameWidget = node.widgets.find(w => w.name === "model_name");
                        if (modelNameWidget) {
                            modelNameWidget.value = v;
                        } else {
                            console.error('[Ollama Config] Model name widget not found');
                        }
                    } catch (error) {
                        console.error('[Ollama Config] Error updating model name:', error);
                    }
                },
                { values: [] }
            );

            // Add update button
            node.addCustomWidget({
                name: "Update model_list",
                type: "button",
                value: "Update Models",
                callback: async function() {
                    try {
                        const url = node.widgets.find(w => w.name === "ollama_url")?.value;
                        if (!url) {
                            console.error('[Ollama Config] Ollama URL is not set');
                            return;
                        }

                        console.log('[Ollama Config] Fetching models from:', url);
                        const response = await fetch(`${url}/api/tags`);
                        
                        if (!response.ok) {
                            console.error('[Ollama Config] Server response not OK:', response.status, response.statusText);
                            return;
                        }

                        const data = await response.json();
                        
                        if (data.models) {
                            const modelNames = data.models.map(m => m.name);
                            if (modelNames.length > 0) {
                                console.log('Found models:', modelNames);
                                // Update model_list widget
                                modelListWidget.options.values = modelNames;
                                modelListWidget.value = modelNames[0];
                                
                                // Update model_name widget
                                const modelNameWidget = node.widgets.find(w => w.name === "model_name");
                                if (modelNameWidget) {
                                    modelNameWidget.value = modelNames[0];
                                } else {
                                    console.error('[Ollama Config] Model name widget not found');
                                }
                            } else {
                                console.error('[Ollama Config] No models found in response');
                            }
                        } else {
                            console.error('[Ollama Config] Invalid response format:', data);
                        }
                    } catch (error) {
                        console.error('[Ollama Config] Error updating models:', error);
                        console.error('[Ollama Config] Error details:', {
                            message: error.message,
                            stack: error.stack,
                            name: error.name
                        });
                    }
                }
            });
        }
    }
});