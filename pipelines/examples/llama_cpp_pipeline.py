from typing import List, Union, Generator, Iterator
from open_webui.pipelines.schemas import OpenAIChatMessage


class Pipeline:
    def __init__(self):
        # Optionally, you can set the id and name of the pipeline.
        self.id = "llama_cpp_pipeline"
        self.name = "Llama C++ Pipeline"
        self.llm = None
        pass

    async def on_startup(self):
        # This function is called when the server is started.
        print(f"on_startup:{__name__}")
        from llama_cpp import Llama

        self.llm = Llama(
            model_path="./models/llama3.gguf",
            # n_gpu_layers=-1, # Uncomment to use GPU acceleration
            # seed=1337, # Uncomment to set a specific seed
            # n_ctx=2048, # Uncomment to increase the context window
        )

        pass

    async def on_shutdown(self):
        # This function is called when the server is stopped.
        print(f"on_shutdown:{__name__}")
        pass

    def get_response(
        self, user_message: str, messages: List[OpenAIChatMessage], body: dict
    ) -> Union[str, Generator, Iterator]:
        # This is where you can add your custom pipelines like RAG.'
        print(f"get_response:{__name__}")

        print(messages)
        print(user_message)
        print(body)

        response = self.llm.create_chat_completion_openai_v1(
            messages=[message.model_dump() for message in messages],
            stream=body["stream"],
        )

        return response
