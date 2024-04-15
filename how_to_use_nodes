# **Node Usage Instructions**

## Large Model Nodes
1. Large model nodes allow customization of model name, temperature, API_KEY, and base_url. Currently, they only support OpenAI-type API calls.
2. You can directly input system prompts and user prompts on the node, or convert these two small components into inputs for the node, accepting string-type input.
3. Large model nodes can also accept output from tool nodes and receive string-formatted input from the file_content interface. These inputs are treated as the model's knowledge base, using word vector similarity to search for relevant content to input into the model.
4. The `is_memory` parameter of large model nodes determines whether the model has memory. You can set `is_memory` to "disable," and then run the node. In this case, the model will clear the previous conversation history. Switching back to "enable" will allow the model to retain your conversation history in subsequent runs.
5. You can use `assistant_response` to view the model's reply in the current round of conversation, or use `history` to review the history of multi-turn dialogues.
6. Even if external parameters remain unchanged, large model nodes always run because they provide different answers to the same question.

## start_dialog and end_dialog Nodes
1. These two nodes have a `dialog_id`. Connecting dialog IDs creates an archive point for the conversation. When you need to loop two large models, although it cannot be directly implemented in ComfyUI, you can save the output of the second model locally and pass it to the first model in the next run. You can use the ComfyUI API in other frontends to call ComfyUI, creating an infinite self-dialogue loop between the two models.
2. The `start_dialog` node has a `start_dialog` interface, which can serve as a user-provided prompt at the beginning of a conversation, guiding the large model to discuss topics based on the user's input.

## google_tool Node
1. You can input your Google API key and CSE ID to use this node.
2. The node returns the top 10 URLs and summary snippets from Google search results. You can request the model to paginate and view more search results.

## check_web_tool Node
1. You can input the desired website URL into this node as the default search URL for the model.
2. Due to limitations of the `request` module, some websites may not allow crawling. This project does not provide malicious web scraping code.

## time_tool and weather_tool Nodes
1. Used for querying time and weather. The `time_tool` node can change the default time zone for queries, and the `weather_tool` node will eventually add options to change the default location.
2. More practical nodes like these will be added to this project in the future.

## load_file from comfyui_LLM_party/file Node
1. The file path for reading files is in `comfyui_LLM_party/file`. You can place the file you want to read in this directory and fill in the filename in this node.
2. The output is a string containing all the text information from the file.

## file_conbine and tool_conbine Nodes
1. Used to combine multiple file nodes or multiple tool nodes into one input for the large model.
2. These combine nodes can be nested, but `tool_conbine` and `file_conbine` cannot be mixed. The output of tool nodes is a specific JSON format.
