browser.contextMenus.create({
    id: "hatespeech-report",
    title: "Report incorrect classification",
    contexts: ["selection"],
});

browser.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === "hatespeech-report") {
        browser.tabs.executeScript(tab.id,{
            file : "src/panel.js"
        }).catch((error) => {
            console.error("Failed to send text: " + error);
        });
    }
});