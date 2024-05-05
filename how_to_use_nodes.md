# **Node Usage Instructions**

## API LLM Nodes
1. LLM nodes allow customization of model name, temperature, API_KEY, and base_url. Currently, they only support OpenAI-type API calls.
2. You can directly input system prompts and user prompts on the node, or convert these two small components into inputs for the node, accepting string-type input.
3. Large model nodes can also accept output from tool nodes and receive string-formatted input from the file_content interface. These inputs are treated as the model's knowledge base, using word vector similarity to search for relevant content to input into the model.
4. The `is_memory` parameter of large model nodes determines whether the model has memory. You can set `is_memory` to "disable," and then run the node. In this case, the model will clear the previous conversation history. Switching back to "enable" will allow the model to retain your conversation history in subsequent runs.
5. You can use `assistant_response` to view the model's reply in the current round of conversation, or use `history` to review the history of multi-turn dialogues.
6. Even if external parameters remain unchanged, large model nodes always run because they provide different answers to the same question.
7. The `is_tools_in_sys_prompt` determines whether the information of ‘tools’ will be entered into the system prompt.
8. `is_locked` can lock the results of the previous conversation, allowing the large model to directly return the answer from the previous turn. This helps maintain continuity in the conversation and allows valuable human resources to handle more complex questions.
9. The `main_brain` determines whether the large model interfaces with the user. When disabled, an LLM node can serve as a tool for another LLM node.
10. The `imgbb_api_key` can be set to the imgbb API key, allowing LLM to adapt GPT-4's visual capabilities.

## Local LLM Nodes
1. Currently supports GLM/Llama/Qwen, but only GLM's tool invocation is perfectly compatible. The other two require large parameter versions for normal tool invocation.
2. `is_reload` determines whether the local model will be unloaded after node execution. It is disabled by default to prevent redundant loading of large models and increase runtime. Enable it when GPU memory cannot support simultaneous LLM and SD execution.
3. Fill in `model_path` and `tokenizer_path` with the project folder containing the model. It adapts to any transformer-compatible model.
4. Other parameters are consistent with the API LLM node.

## start_workflow and end_workflow Nodes
1. You can use these two nodes to define the starting and ending points of a workflow. Place your workflow in the `workflow` subfolder of this project.
2. Run `setup_streamlit_app.bat` in the project folder. In the Streamlit interface, click "Settings" and replace it with your workflow.
3. This way, you've quickly built an AI application with Streamlit as the frontend.

## workflow_transfer Node
1. You need to add the start workflow and end workflow nodes at the beginning and end of the workflow to be embedded, and save this workflow as an API in the workflow_api folder of the comfyui_LLM_party project.
2. Open another workflow, and use the workflow transfer node within this workflow, select the workflow you want to embed, and it’s done.
3. The first time you use the workflow transfer node, another port 8189 will be opened, please do not close this new console.

## start_dialog and end_dialog Nodes
1. These two nodes have a `dialog_id`. Connecting dialog IDs creates an archive point for the conversation. When you need to loop two large models, although it cannot be directly implemented in ComfyUI, you can save the output of the second model locally and pass it to the first model in the next run. You can use the ComfyUI API in other frontends to call ComfyUI, creating an infinite self-dialogue loop between the two models.
2. The `start_dialog` node has a `start_dialog` interface, which can serve as a user-provided prompt at the beginning of a conversation, guiding the large model to discuss topics based on the user's input.

## Common Characteristics of Tool Nodes
1. is_enable determines whether the tool is enabled, making it convenient for users to quickly change the tools connected to the model.

## google_tool Node
1. You can input your Google API key and CSE ID to use this node.
2. The node returns the top 10 URLs and summary snippets from Google search results. You can request the model to paginate and view more search results.

## check_web_tool Node
1. You can input the desired website URL into this node as the default search URL for the model.
2. Due to limitations of the `request` module, some websites may not allow crawling. This project does not provide malicious web scraping code.

## time_tool and weather_tool Nodes
1. Used for querying time and weather. The `time_tool` node can change the default time zone for queries, and the `weather_tool` node will eventually add options to change the default location.
2. More practical nodes like these will be added to this project in the future.

## interpreter node
1. It allows the large model to generate Python code, execute it automatically, and obtain the execution results of the code.
2. Currently, it only supports Python code.

## omnipotent Interpreter Node
1. Enables the large model to execute any task. The large model operates within a virtual environment, downloading necessary third-party libraries and executing generated code.
2. Use this tool with caution, as the large model gains the ability to control your computer for any task!

## load_file from comfyui_LLM_party/file Node
1. The file path for reading files is in `comfyui_LLM_party/file`. You can place the file you want to read in this directory and fill in the filename in this node.
2. The output is a string containing all the text information from the file.

## file_conbine and tool_conbine Nodes
1. Used to combine multiple file nodes or multiple tool nodes into one input for the large model.
2. These combine nodes can be nested, but `tool_conbine` and `file_conbine` cannot be mixed. The output of tool nodes is a specific JSON format.
