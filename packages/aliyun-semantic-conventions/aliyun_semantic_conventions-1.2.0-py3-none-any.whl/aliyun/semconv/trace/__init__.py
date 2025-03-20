from enum import Enum

class VSpanAttributes:
    # Attribute names copied from here to avoid version conflicts:
    # https://github.com/open-telemetry/semantic-conventions/blob/main/docs/gen-ai/gen-ai-spans.md
    GEN_AI_USAGE_COMPLETION_TOKENS = "gen_ai.usage.completion_tokens"
    GEN_AI_USAGE_PROMPT_TOKENS = "gen_ai.usage.prompt_tokens"
    GEN_AI_REQUEST_MAX_TOKENS = "gen_ai.request.max_tokens"
    GEN_AI_REQUEST_TOP_P = "gen_ai.request.top_p"
    GEN_AI_REQUEST_TEMPERATURE = "gen_ai.request.temperature"
    GEN_AI_RESPONSE_MODEL = "gen_ai.response.model"
    # Attribute names added until they are added to the semantic conventions:
    GEN_AI_REQUEST_ID = "gen_ai.request.id"
    GEN_AI_REQUEST_N = "gen_ai.request.n"
    GEN_AI_USAGE_NUM_SEQUENCES = "gen_ai.usage.num_sequences"
    GEN_AI_LATENCY_TIME_IN_QUEUE = "gen_ai.latency.time_in_queue"
    GEN_AI_LATENCY_TIME_TO_FIRST_TOKEN = "gen_ai.latency.time_to_first_token"
    GEN_AI_LATENCY_E2E = "gen_ai.latency.e2e"
    GEN_AI_LATENCY_TIME_IN_SCHEDULER = "gen_ai.latency.time_in_scheduler"
    # Time taken in the forward pass for this across all workers
    GEN_AI_LATENCY_TIME_IN_MODEL_FORWARD = (
        "gen_ai.latency.time_in_model_forward")
    # Time taken in the model execute function. This will include model
    # forward, block/sync across workers, cpu-gpu sync time and sampling time.
    GEN_AI_LATENCY_TIME_IN_MODEL_EXECUTE = (
        "gen_ai.latency.time_in_model_execute")


class SpanAttributes:
    OUTPUT_VALUE = "output.value"
    OUTPUT_MIME_TYPE = "output.mime_type"
    """
    The type of output.value. If unspecified, the type is plain text by default.
    If type is JSON, the value is a string representing a JSON object.
    """
    INPUT_VALUE = "input.value"
    INPUT_MIME_TYPE = "input.mime_type"
    """
    The type of input.value. If unspecified, the type is plain text by default.
    If type is JSON, the value is a string representing a JSON object.
    """

    EMBEDDING_EMBEDDINGS = "embedding.embeddings"
    """
    A list of objects containing embedding data, including the vector and represented piece of text.
    """
    EMBEDDING_MODEL_NAME = "embedding.model_name"
    """
    The name of the embedding model.
    """

    # LLM_FUNCTION_CALL = "llm.function_call"
    """
    For models and APIs that support function calling. Records attributes such as the function
    name and arguments to the called function.
    """
    # LLM_INVOCATION_PARAMETERS = "llm.invocation_parameters"
    """
    Invocation parameters passed to the LLM or API, such as the model name, temperature, etc.
    """
    GEN_AI_PROMPT = "gen_ai.prompts"
    """
    Messages provided to a chat API.
    """
    GEN_AI_COMPLETION = "gen_ai.completions"
    """
    Messages received from a chat API.
    """
    # LLM_MODEL_NAME = "llm.model_name"

    # LLM_VENDOR_NAME = "llm.vendor.name"
    """
    The name of the model being used.
    """
    # LLM_PROMPTS = "llm.prompts"
    """
    Prompts provided to a completions API.
    """
    GEN_AI_PROMPT_TEMPLATE = "gen_ai.prompt_template.template"
    """
    The prompt template as a Python f-string.
    """
    GEN_AI_PROMPT_VARIABLES = "gen_ai.prompt_template.variables"
    """
    A list of input variables to the prompt template.
    """
    GEN_AI_PROMPT_VERSION = "gen_ai.prompt_template.version"

    GEN_AI_SYSTEM = "gen_ai.system"

    # LLM_PROMPT_TEMPLATE_VERSION = "llm.prompt_template.version"
    """
    The version of the prompt template being used.
    """
    # LLM_TOKEN_COUNT_PROMPT = "llm.token_count.prompt"
    """
    Number of tokens in the prompt.
    """
    # LLM_TOKEN_COUNT_COMPLETION = "llm.token_count.completion"
    """
    Number of tokens in the completion.
    """
    # LLM_TOKEN_COUNT_TOTAL = "llm.token_count.total"
    """
    Total number of tokens, including both prompt and completion.
    """

    TOOL_NAME = "tool.name"
    """
    Name of the tool being used.
    """
    TOOL_DESCRIPTION = "tool.description"
    """
    Description of the tool's purpose, typically used to select the tool.
    """
    TOOL_PARAMETERS = "tool.parameters"
    """
    Parameters of the tool represented a dictionary JSON string, e.g.
    see https://platform.openai.com/docs/guides/gpt/function-calling
    """

    RETRIEVAL_DOCUMENTS = "retrieval.documents"

    METADATA = "metadata"
    """
    Metadata attributes are used to store user-defined key-value pairs.
    For example, LangChain uses metadata to store user-defined attributes for a chain.
    """

    TAG_TAGS = "tag.tags"
    """
    Custom categorical tags for the span.
    """

    GEN_AI_SPAN_KIND = "gen_ai.span.kind"

    GEN_AI_SPAN_SUB_KIND = "gen_ai.span.sub_kind"

    # LLM_MODEL_PROVIDER = "llm.model_provider"

    SESSION_ID = "session.id"
    GEN_AI_SESSION_ID = "gen_ai.session.id"
    """
    The id of the session
    """
    USER_ID = "user.id"
    GEN_AI_USER_ID = "gen_ai.user.id"
    """
    The id of the user
    """
    GEN_AI_USER_NAME = "gen_ai.user.name"

    GEN_AI_FRAMEWORK = "gen_ai.framework"

    GEN_AI_USAGE_PROMPT_TOKENS = "gen_ai.usage.input_tokens"

    GEN_AI_USAGE_COMPLETION_TOKENS = "gen_ai.usage.output_tokens"

    GEN_AI_USAGE_TOTAL_TOKENS = "gen_ai.usage.total_tokens"

    SERVICE_NAME = "service.name"

    SERVICE_VERSION = "service.version"

    SERVICE_APP_NAME = "service.app.name"

    SERVICE_OWNER_ID = "service.owner.id"

    SERVICE_USER_ID = "service.user_id"

    SERVICE_USER_NAME = "service.user_name"

    SERVICE_OWNER_SUB_ID = "service.owner.sub_id"

    SERVICE_APP_OWNER_ID = "service.app.owner_id"

    GEN_AI_REQUEST_TOP_P = "gen_ai.request.top_p"

    GEN_AI_REQUEST_IS_STREAM = "gen_ai.request.is_stream"

    GEN_AI_REQUEST_MODEL_NAME = "gen_ai.request.model_name"

    GEN_AI_REQUEST_MAX_TOKENS = "gen_ai.request.max_tokens"

    GEN_AI_REQUEST_TEMPERATURE = "gen_ai.request.temperature"

    GEN_AI_REQUEST_STOP_SEQUENCES = "gen_ai.request.stop_sequences"

    GEN_AI_REQUEST_TOOL_CALLS = "gen_ai.request.tool_calls"

    GEN_AI_REQUEST_PARAMETERS = "gen_ai.request.parameters"

    GEN_AI_RESPONSE_MODEL_NAME = "gen_ai.response.model_name"

    GEN_AI_RESPONSE_FINISH_REASON = "gen_ai.response.finish_reason"

    GEN_AI_USER_TIME_TO_FIRST_TOKEN = "gen_ai.user.time_to_first_token"

    GEN_AI_MODEL_NAME = "gen_ai.model_name"

    ALI_TRACE_FLAG = "ali.trace.flag"

    CONTENT = "content"


class MessageAttributes:
    """
    Attributes for a message generated by a LLM
    """

    MESSAGE_ROLE = "message.role"
    """
    The role of the message, such as "user", "agent", "function".
    """
    MESSAGE_CONTENT = "message.content"
    """
    The content of the message to the llm
    """
    MESSAGE_NAME = "message.name"
    """
    The name of the message, often used to identify the function
    that was used to generate the message.
    """
    MESSAGE_TOOL_CALLS = "message.tool_calls"
    """
    The tool calls generated by the model, such as function calls.
    """
    MESSAGE_FUNCTION_CALL_NAME = "message.function_call_name"
    """
    The function name that is a part of the message list.
    This is populated for role 'function' or 'agent' as a mechanism to identify
    the function that was called during the execution of a tool
    """
    MESSAGE_FUNCTION_CALL_ARGUMENTS_JSON = "message.function_call_arguments_json"
    """
    The JSON string representing the arguments passed to the function
    during a function call
    """


class DocumentAttributes:
    """
    Attributes for a document
    """

    DOCUMENT_ID = "document.id"
    """
    The id of the document
    """
    DOCUMENT_SCORE = "document.score"
    """
    The score of the document
    """
    DOCUMENT_CONTENT = "document.content"
    """
    The content of the document
    """
    DOCUMENT_METADATA = "document.metadata"
    """
    The metadata of the document represented as a dictionary
    JSON string, e.g. `"{ 'title': 'foo' }"`
    """


class RerankerAttributes:
    """
    Attributes for a reranker
    """

    RERANKER_INPUT_DOCUMENTS = "reranker.input_documents"
    """
    List of documents as input to the reranker
    """
    RERANKER_OUTPUT_DOCUMENTS = "reranker.output_documents"
    """
    List of documents as output from the reranker
    """
    RERANKER_QUERY = "reranker.query"
    """
    Query string for the reranker
    """
    RERANKER_MODEL_NAME = "reranker.model_name"
    """
    Model name of the reranker
    """
    RERANKER_TOP_K = "reranker.top_k"
    """
    Top K parameter of the reranker
    """


class EmbeddingAttributes:
    """
    Attributes for an embedding
    """

    EMBEDDING_TEXT = "embedding.text"
    """
    The text represented by the embedding.
    """
    EMBEDDING_VECTOR = "embedding.vector"
    """
    The embedding vector.
    """
    EMBEDDING_VECTOR_SIZE = "embedding.vector_size"
    """
    The embedding vector size.
    """


class ToolCallAttributes:
    """
    Attributes for a tool call
    """

    TOOL_CALL_FUNCTION_NAME = "tool_call.function.name"
    """
    The name of function that is being called during a tool call.
    """
    TOOL_CALL_FUNCTION_ARGUMENTS_JSON = "tool_call.function.arguments"
    """
    The JSON string representing the arguments passed to the function
    during a tool call.
    """
    TOOL_CALL_FUNCTION_DESCRIPTION = "tool_call.function.description"

    TOOL_CALL_FUNCTION_THOUGHTS = "tool_call.function.thoughts"


class AliyunSpanKindValues(Enum):
    TOOL = "TOOL"
    CHAIN = "CHAIN"
    LLM = "LLM"
    RETRIEVER = "RETRIEVER"
    EMBEDDING = "EMBEDDING"
    AGENT = "AGENT"
    RERANKER = "RERANKER"
    UNKNOWN = "UNKNOWN"

    XTRACE = "xtrace"
    ARMS = "arms"
    LLAMA_INDEX = "llama_index"


class AliyunMemoryTypeValues(Enum):
    BUFFER = "buffer"
    VECTOR = "vector"
    KVDB = "kv-db"
    SQLDB = "sql-db"


class AliyunSpanSubKindValues(Enum):
    CHAT = "chat"
    COMPLETION = "completion"
    WORKFLOW = "workflow"
    TASK = "task"


class AliyunMimeTypeValues(Enum):
    TEXT = "text/plain"
    JSON = "application/json"
