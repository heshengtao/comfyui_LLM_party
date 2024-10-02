chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "sendToGPT",
    title: "Send to GPT",
    contexts: ["selection"]
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "sendToGPT") {
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      function: sendToGPT,
      args: [info.selectionText]
    });
    // 自动打开插件面板
    chrome.action.openPopup();
  }
});

function sendToGPT(selectedText) {
  chrome.storage.local.get(['baseUrl', 'apiKey', 'modelName', 'systemPrompt'], (data) => {
    const baseUrl = data.baseUrl || 'http://127.0.0.1:8187/v1';
    const apiKey = data.apiKey || 'party';
    const modelName = data.modelName || 'X';
    const systemPrompt = data.systemPrompt || '';

    // 禁用按钮并显示 "Thinking..."
    chrome.storage.local.set({ isThinking: true, markdownResponse: "Thinking..." });

    fetch(`${baseUrl}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      },
      body: JSON.stringify({
        model: modelName,
        messages: [
          { role: "system", content: systemPrompt },
          { role: "user", content: selectedText }
        ]
      })
    })
    .then(response => response.json())
    .then(data => {
      const markdownResponse = data.choices[0].message.content;
      chrome.storage.local.set({ markdownResponse, isThinking: false }, () => {
        // 发送消息通知面板更新状态
        chrome.runtime.sendMessage({ action: "updateUI" });
        // 打开插件面板
        chrome.action.openPopup();
      });
    })
    .catch(error => {
      chrome.storage.local.set({ markdownResponse: "Error: Unable to fetch response.", isThinking: false }, () => {
        // 发送消息通知面板更新状态
        chrome.runtime.sendMessage({ action: "updateUI" });
        // 打开插件面板
        chrome.action.openPopup();
      });
    });
  });
}
