import { app } from "../../scripts/app.js";

class LLMPartyExtension {
    constructor() {
        this.apiModal = null;
        this.aboutModal = null;
        this.workflowModal = null;

        this.createAPIModal();
        this.createAboutModal();
        this.createWorkflowModal();
    }

    createAPIModal() {
        this.apiModal = document.createElement('div');
        this.apiModal.style.cssText = `
            display: none;
            position: fixed;
            z-index: 1001;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.4);
        `;

        const modalContent = document.createElement('div');
        modalContent.style.cssText = `
            background-color: #2c2c2c;
            padding: 20px;
            border: 1px solid #888;
            width: 300px;
            border-radius: 5px;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        `;

        const closeBtn = document.createElement('span');
        closeBtn.innerHTML = '&times;';
        closeBtn.style.cssText = `
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
        `;
        closeBtn.onclick = () => this.hideAPIModal();

        const title = document.createElement('h2');
        title.textContent = 'Set API Key';
        title.style.color = 'white';

        const form = document.createElement('form');
        form.onsubmit = (e) => this.submitApiKey(e);

        const baseUrlLabel = document.createElement('label');
        baseUrlLabel.textContent = 'Base URL:';
        baseUrlLabel.style.color = 'white';
        const baseUrlInput = document.createElement('input');
        baseUrlInput.type = 'text';
        baseUrlInput.id = 'baseUrl';
        baseUrlInput.value = 'https://api.openai.com/v1/';
        baseUrlInput.style.cssText = `
            width: 100%;
            padding: 5px;
            margin: 5px 0;
            box-sizing: border-box;
            background-color: #3c3c3c;
            color: white;
            border: 1px solid #555;
        `;

        const apiKeyLabel = document.createElement('label');
        apiKeyLabel.textContent = 'API Key:';
        apiKeyLabel.style.color = 'white';
        const apiKeyInput = document.createElement('input');
        apiKeyInput.type = 'password';
        apiKeyInput.id = 'apiKey';
        apiKeyInput.style.cssText = `
            width: 100%;
            padding: 5px;
            margin: 5px 0;
            box-sizing: border-box;
            background-color: #3c3c3c;
            color: white;
            border: 1px solid #555;
        `;

        const submitButton = document.createElement('button');
        submitButton.type = 'submit';
        submitButton.textContent = 'Set API Key';
        submitButton.style.cssText = `
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 3px;
            cursor: pointer;
            width: 100%;
            margin-top: 10px;
        `;

        form.appendChild(baseUrlLabel);
        form.appendChild(baseUrlInput);
        form.appendChild(apiKeyLabel);
        form.appendChild(apiKeyInput);
        form.appendChild(submitButton);

        modalContent.appendChild(closeBtn);
        modalContent.appendChild(title);
        modalContent.appendChild(form);

        this.apiModal.appendChild(modalContent);
        document.body.appendChild(this.apiModal);
    }

    createAboutModal() {
        this.aboutModal = document.createElement('div');
        this.aboutModal.style.cssText = `
            display: none;
            position: fixed;
            z-index: 1001;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.4);
        `;

        const modalContent = document.createElement('div');
        modalContent.style.cssText = `
            background-color: #2c2c2c;
            padding: 20px;
            border: 1px solid #888;
            width: 60%;
            max-width: 600px;
            border-radius: 5px;
            color: white;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        `;

        const closeBtn = document.createElement('span');
        closeBtn.innerHTML = '&times;';
        closeBtn.style.cssText = `
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
        `;
        closeBtn.onclick = () => this.hideAboutModal();

        const title = document.createElement('h2');
        title.textContent = 'ComfyUI LLM Party';

        const content = document.createElement('div');
        content.innerHTML = `
            <p>注意！本项目是基于AGPL协议开源的，请遵守AGPL协议，以避免不必要的法律问题！谢谢您的合作！如果您需要可以闭源商用的版本，请邮箱联系hst97@qq.com</p>
            <p>Attention! This project is open source based on the AGPL agreement, please abide by the AGPL agreement to avoid unnecessary legal problems! Thank you for your cooperation! If you need a closed-source commercial version, please contact hst97@qq.com</p>
            <p>github: <a href="https://github.com/heshengtao/comfyui_LLM_party" target="_blank" style="color: #4CAF50;">heshengtao/comfyui_LLM_party</a></p>
            <p>bilibili: <a href="https://space.bilibili.com/26978344?spm_id_from=333.1007.0.0" target="_blank" style="color: #4CAF50;">@派酱llm-party</a></p>
            <p>youtube: <a href="https://www.youtube.com/@LLM-party" target="_blank" style="color: #4CAF50;">@LLM-party</a></p>
            <p>QQ: <a href="https://github.com/heshengtao/comfyui_LLM_party/blob/main/img/Q%E7%BE%A4.jpg" target="_blank" style="color: #4CAF50;">931057213</a></p>
            <p>feishu: <a href="https://dcnsxxvm4zeq.feishu.cn/wiki/IyUowXNj9iH0vzk68cpcLnZXnYf?fromScene=spaceOverview" target="_blank" style="color: #4CAF50;">use document</a></p>
        `;

        modalContent.appendChild(closeBtn);
        modalContent.appendChild(title);
        modalContent.appendChild(content);

        this.aboutModal.appendChild(modalContent);
        document.body.appendChild(this.aboutModal);
    }

    showAPIModal() {
        this.apiModal.style.display = 'block';
        this.centerModalContent(this.apiModal);
    }

    hideAPIModal() {
        this.apiModal.style.display = 'none';
    }

    showAboutModal() {
        this.aboutModal.style.display = 'block';
        this.centerModalContent(this.aboutModal);
    }

    hideAboutModal() {
        this.aboutModal.style.display = 'none';
    }

    async submitApiKey(e) {
        e.preventDefault();
        const baseUrl = document.getElementById('baseUrl').value;
        const apiKey = document.getElementById('apiKey').value;
        const endpoint = '/party/update_config';

        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    openai_api_key: apiKey,
                    base_url: baseUrl
                })
            });

            if (response.ok) {
                const result = await response.json();
                alert('API Key and Base URL updated successfully!');
                this.hideAPIModal();
            } else {
                const errorMessage = await response.text();
                console.error('Server responded with an error:', response.status, errorMessage);
                alert(`Failed to update API Key and Base URL: ${errorMessage}`);
            }
        } catch (error) {
            console.error('Fetch error:', error);
            alert(`An error occurred: ${error.message}`);
        }
    }

    async sendFastApiRequest() {
        const endpoint = '/party/fastapi';
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            });

            if (response.ok) {
                const result = await response.json();
                console.log('FastAPI request success:', result);
                alert('The FastAPI request was sent and successfully processed!');
            } else {
                const errorMessage = await response.text();
                console.error('FastAPI request failed:', response.status, errorMessage);
                alert(`FastAPI request failed: ${errorMessage}`);
            }
        } catch (error) {
            console.error('FastAPI request failed:', error);
            alert(`Error occurred: ${error.message}`);
        }
    }

    async sendStreamlitRequest() {
        const endpoint = '/party/streamlit';
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            });

            if (response.ok) {
                const result = await response.json();
                console.log('Streamlit request success:', result);
                alert('The Streamlit app is launched! Please check it in a new window.');
            } else {
                const errorMessage = await response.text();
                console.error('Streamlit request failed:', response.status, errorMessage);
                alert(`Streamlit request failed: ${errorMessage}`);
            }
        } catch (error) {
            console.error('Streamlit request failed:', error);
            alert(`Error occurred: ${error.message}`);
        }
    }

    createWorkflowModal() {
        this.workflowModal = document.createElement('div');
        this.workflowModal.style.cssText = `
            display: none;
            position: fixed;
            z-index: 1001;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.4);
        `;

        const modalContent = document.createElement('div');
        modalContent.style.cssText = `
            background-color: #2c2c2c;
            padding: 20px;
            border: 1px solid #888;
            width: 300px;
            border-radius: 5px;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        `;

        const closeBtn = document.createElement('span');
        closeBtn.innerHTML = '&times;';
        closeBtn.style.cssText = `
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
        `;
        closeBtn.onclick = () => this.hideWorkflowModal();

        const title = document.createElement('h2');
        title.textContent = 'Select Workflow';
        title.style.color = 'white';

        const select = document.createElement('select');
        select.id = 'workflowSelect';
        select.style.cssText = `
            width: 100%;
            padding: 5px;
            margin: 5px 0;
            box-sizing: border-box;
            background-color: #3c3c3c;
            color: white;
            border: 1px solid #555;
        `;

        const loadButton = document.createElement('button');
        loadButton.textContent = 'load workflow';
        loadButton.style.cssText = `
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 3px;
            cursor: pointer;
            width: 100%;
            margin-top: 10px;
        `;
        loadButton.onclick = () => this.loadSelectedWorkflow();

        modalContent.appendChild(closeBtn);
        modalContent.appendChild(title);
        modalContent.appendChild(select);
        modalContent.appendChild(loadButton);

        this.workflowModal.appendChild(modalContent);
        document.body.appendChild(this.workflowModal);

        this.loadWorkflowList();
    }

    showWorkflowModal() {
        this.workflowModal.style.display = 'block';
        this.centerModalContent(this.workflowModal);
    }

    hideWorkflowModal() {
        this.workflowModal.style.display = 'none';
    }

    centerModalContent(modal) {
        const content = modal.querySelector('div');
        const windowHeight = window.innerHeight;
        const contentHeight = content.offsetHeight;

        if (contentHeight > windowHeight) {
            content.style.top = '0';
            content.style.transform = 'translateX(-50%)';
        } else {
            content.style.top = '50%';
            content.style.transform = 'translate(-50%, -50%)';
        }
    }

    async loadWorkflowList() {
        const select = document.getElementById('workflowSelect');
        try {
            const response = await fetch('/party/workflow_list');
            if (response.ok) {
                const workflows = await response.json();
                select.innerHTML = '';
                workflows.forEach(workflow => {
                    const option = document.createElement('option');
                    option.value = workflow;
                    option.textContent = workflow;
                    select.appendChild(option);
                });
            } else {
                console.error('Failed to load workflow list');
            }
        } catch (error) {
            console.error('Error loading workflow list:', error);
        }
    }

    async loadSelectedWorkflow() {
        const select = document.getElementById('workflowSelect');
        const selectedWorkflow = select.value;
        if (selectedWorkflow) {
            try {
                const response = await fetch('/party/load_workflow', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ workflow: selectedWorkflow })
                });
                if (response.ok) {
                    const workflow = await response.json();
                    app.loadGraphData(workflow);
                    this.hideWorkflowModal();
                    alert('Workflow loaded successfully!');
                } else {
                    alert('Failed to load workflow');
                }
            } catch (error) {
                console.error('Error loading workflow:', error);
                alert('An error occurred while loading the workflow');
            }
        }
    }
}

let instance = null;

app.registerExtension({
    name: "comfy.LLMPartyExtension",
    async setup() {
        instance = new LLMPartyExtension();
    },
    commands: [
        {
            id: "LLMParty.APIKey",
            icon: "pi pi-key",
            label: "Set API Key",
            function: () => { instance?.showAPIModal(); }
        },
        {
            id: "LLMParty.FastAPI",
            icon: "pi pi-check-circle",
            label: "FastAPI",
            function: () => { instance?.sendFastApiRequest(); }
        },
        {
            id: "LLMParty.Streamlit",
            icon: "pi pi-desktop",
            label: "Streamlit",
            function: () => { instance?.sendStreamlitRequest(); }
        },
        {
            id: "LLMParty.Workflow",
            icon: "pi pi-chart-line",
            label: "Load Workflow",
            function: () => { instance?.showWorkflowModal(); }
        },
        {
            id: "LLMParty.About",
            icon: "pi pi-info-circle",
            label: "About LLM Party",
            function: () => { instance?.showAboutModal(); }
        },
    ],
    menuCommands: [
        {
            path: ["LLM Party"],
            commands: [
                "LLMParty.APIKey",
                "LLMParty.FastAPI",
                "LLMParty.Streamlit",
                "LLMParty.Workflow",
                "LLMParty.About",
            ]
        }
    ],
});
