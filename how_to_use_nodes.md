# **Node Usage Instructions**

## Node Overview
1. The nodes in this project can be divided into LLM nodes, tool nodes, function nodes, mask nodes, and loader nodes.
2. Tool nodes are nodes that are attached to the model’s tools interface and are called internally within the model. For tool nodes, is_enable determines whether the tool is enabled, allowing users to quickly change the tools attached to the model.
3. Mask nodes and function nodes usually appear in pairs; mask nodes are customizable prompt word templates, attached to the model’s system_prompt or user_prompt interface. Large models with attached mask nodes have a specific output format, which can stably call the corresponding external function nodes.
4. Loader nodes can quickly load local files or personality masks.

## LLM_api Nodes
1. LLM nodes allow customization of model name, temperature, API_KEY, and base_url. Currently, they only support OpenAI-type API calls.
2. You can directly input system prompts and user prompts on the node, or convert these two small components into inputs for the node, accepting string-type input.
3. Large model nodes can also accept output from tool nodes and receive string-formatted input from the file_content interface. These inputs are treated as the model's knowledge base, using word vector similarity to search for relevant content to input into the model.
4. Support for GPT-4’s visual capabilities can be integrated with the `img` interface to connect to a large model. To achieve this functionality, you’ll need to use the free image hosting service, imgbb. Please input your imgbb API key in the `imgbb_api_key` field.
5. The `is_memory` parameter of large model nodes determines whether the model has memory. You can set `is_memory` to "disable," and then run the node. In this case, the model will clear the previous conversation history. Switching back to "enable" will allow the model to retain your conversation history in subsequent runs.
6. You can use `assistant_response` to view the model's reply in the current round of conversation, or use `history` to review the history of multi-turn dialogues.
7. Even if external parameters remain unchanged, large model nodes always run because they provide different answers to the same question.
8. The `is_tools_in_sys_prompt` determines whether the information of ‘tools’ will be entered into the system prompt.
9. `is_locked` can lock the results of the previous conversation, allowing the large model to directly return the answer from the previous turn. This helps maintain continuity in the conversation and allows valuable human resources to handle more complex questions.
10. The `main_brain` can determine whether it interfaces with the user. By disabling `main_brain`, you can use this large model as a tool for another large model!

## LLM_local Nodes
1. For model_type, you can currently choose between `GLM` and `llama` formats.
2. For `model_path` and `tokenizer_path`, simply fill in the local model folder and local tokenizer folder respectively.
3. `is_reload` determines whether the local model will be unloaded after the node runs. If enabled, the model will be reloaded each time, ensuring that video memory is not occupied. If disabled, the model will not be reloaded repeatedly, shortening inference time.
4. `device` determines whether to run on `cuda` or `cpu`, as well as whether to use `float16/int8/int4` quantization.
5. Other parameters are consistent with the `LLM_api` node.

## start_workflow and end_workflow Nodes
1. define the starting and ending points of a workflow. Place your workflow in the workflow subfolder of this project, then run setup_streamlit_app.bat in the project folder. In the Streamlit interface, click on settings and replace it with your workflow.
**Congratulations! You’ve built an intelligent application!**
2. You can test the “Test Drawing App” workflow to verify its functionality. Ensure that all models within the workflow are working correctly before testing.

## start_dialog and end_dialog Nodes
1. These two nodes have a `dialog_id`. Connecting dialog IDs creates an archive point for the conversation. When you need to loop two large models, although it cannot be directly implemented in ComfyUI, you can save the output of the second model locally and pass it to the first model in the next run. You can use the ComfyUI API in other frontends to call ComfyUI, creating an infinite self-dialogue loop between the two models.
2. The `start_dialog` node has a `start_dialog` interface, which can serve as a user-provided prompt at the beginning of a conversation, guiding the large model to discuss topics based on the user's input.

## ebd_tool node
1. Enter the absolute path of your word embedding model and attach this node as a tool to the LLM node.
2. Attach the files you need to search to the ebd_tool node. When the LLM model runs, it will perform RAG on these files.

## google_tool node
1. You can input your Google API key and CSE ID to use this node.
2. The node returns the top 10 URLs and summary snippets from Google search results. You can request the model to paginate and view more search results.

## check_web_tool node
1. You can input the desired website URL into this node as the default search URL for the model.
2. Due to limitations of the `request` module, some websites may not allow crawling. This project does not provide malicious web scraping code.

## time_tool and weather_tool nodes
1. Used for querying time and weather. The `time_tool` node can change the default time zone for queries, and the `weather_tool` node will eventually add options to change the default location.
2. More practical nodes like these will be added to this project in the future.

## interpreter node
1. It allows the large model to generate Python code, execute it automatically, and obtain the execution results of the code.
2. Currently, it only supports Python code.

## omnipotent interpreter node 
1. executes code within an isolated virtual environment.
2. It automatically installs any missing third-party libraries before execution. Be cautious about the security of the executed code, as this tool can control your computer to perform any task!

## load_file node
1. The path for reading files is in comfyui_LLM_party/file. You can place the file you want to read in this path, and then enter the file name into this node.
2. You can choose Absolute_Path and enter the absolute path of the file for it to be loaded correctly.
3. The output is a string that contains all the text information from the file.

## file_conbine and tool_conbine Nodes
1. Used to combine multiple file nodes or multiple tool nodes into one input for the large model.
2. These combine nodes can be nested, but `tool_conbine` and `file_conbine` cannot be mixed. The output of tool nodes is a specific JSON format.
