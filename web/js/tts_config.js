import { app } from "../../../scripts/app.js";
const language_map = {
    "ar": "Arabic", "cs": "Czech", "de": "German", "en": "English",
    "es": "Spanish", "fr": "French", "hi": "Hindi", "hu": "Hungarian",
    "it": "Italian", "ja": "Japanese", "ko": "Korean", "nl": "Dutch",
    "pl": "Polish", "pt": "Portuguese", "ru": "Russian", "tr": "Turkish",
    "zh-cn": "Chinese"
}
app.registerExtension({
    name: "Bjornulf.XTTSConfig",
    async nodeCreated(node) {
        if (node.comfyClass === "Bjornulf_XTTSConfig") {
            // Add language combo widget
            const languageWidget = node.widgets.find(w => w.name === "language");

            // Add voice_list combo widget
            const voiceListWidget = node.addWidget(
                "combo",
                "select_voice_here",
                "",
                (v) => {
                    // When voice_list changes, update speaker_wav
                    const speakerWidget = node.widgets.find(w => w.name === "speaker_wav");
                    if (speakerWidget) {
                        speakerWidget.value = v;
                    }
                },
                { values: [] }
            );

            // Function to update voices based on selected language
            const updateVoicesForLanguage = async (selectedLanguage) => {
                try {
                    // const response = await fetch('/bjornulf_xtts_get_voices', {
                    const response = await fetch('/bjornulf_TTS_get_voices', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        }
                    });
                    
                    const data = await response.json();
                    
                    if (data.languages) {
                        // Find the language code for the selected language name
                        const languageCode = Object.keys(language_map).find(
                            key => language_map[key] === selectedLanguage
                        );
                        
                        if (languageCode && data.languages[languageCode]) {
                            const voices = data.languages[languageCode].voices;
                            // Voice IDs already include language prefix
                            voiceListWidget.options.values = voices;
                            
                            // Update the widgets with the first voice if available
                            if (voices.length > 0) {
                                voiceListWidget.value = voices[0];
                                
                                // Update speaker_wav widget
                                const speakerWidget = node.widgets.find(w => w.name === "speaker_wav");
                                if (speakerWidget) {
                                    speakerWidget.value = voices[0];
                                }
                            }
                            
                            app.ui.dialog.show(`Successfully loaded ${voices.length} voices for ${selectedLanguage}`);
                        } else {
                            voiceListWidget.options.values = [];
                            app.ui.dialog.show(`No voices found for ${selectedLanguage}`);
                        }
                    }
                } catch (error) {
                    console.error('Error updating voices:', error);
                    app.ui.dialog.show("Error updating voices. Check the console for details.");
                }
            };

            // Add update button
            node.addCustomWidget({
                name: "Update Voices",
                type: "button",
                value: "Update Available Voices",
                callback: async function() {
                    const selectedLanguage = languageWidget.value;
                    await updateVoicesForLanguage(selectedLanguage);
                }
            });

            // Listen for language changes
            if (languageWidget) {
                const originalCallback = languageWidget.callback;
                languageWidget.callback = function(value) {
                    if (originalCallback) {
                        originalCallback(value);
                    }
                    updateVoicesForLanguage(value);
                };
            }
        }
    }
});