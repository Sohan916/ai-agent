from openai.types.chat import ChatCompletionToolUnionParam

from functions.get_files_info import schema_get_files_info

available_functions: list[ChatCompletionToolUnionParam] = [
    schema_get_files_info,
]
