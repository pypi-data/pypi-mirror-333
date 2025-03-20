import os
import re
import subprocess
import tempfile
from argparse import Namespace
from typing import Optional, cast

from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import get_lexer_by_name
from pygments.lexers.special import TextLexer
from pygments.util import ClassNotFound
from pygments_tsx.tsx import patch_pygments, TypeScriptXLexer

from assistants.ai.anthropic import Claude
from assistants.ai.dummy_assistant import DummyAssistant
from assistants.ai.types import AssistantInterface
from assistants.ai.openai import Assistant, Completion
from assistants.config import Config
from assistants.lib.exceptions import ConfigError

fallback_lexers = {
    "tsx": TypeScriptXLexer,
    "plaintext": TextLexer,
}


def highlight_code_blocks(markdown_text):
    patch_pygments()
    code_block_pattern = re.compile(r"```(\w+)?\n(.*?)```", re.DOTALL)

    def replacer(match):
        lang = match.group(1)
        code = match.group(2)
        if lang:
            lexer_class = fallback_lexers.get(lang)
            if not lexer_class:
                try:
                    lexer = get_lexer_by_name(lang, stripall=True)
                except ClassNotFound:
                    lexer = TextLexer()
            else:
                lexer = lexer_class()
        else:
            lexer = get_lexer_by_name("text", stripall=True)
        return f"```{lang if lang else ''}\n{highlight(code, lexer, TerminalFormatter())}```"

    return code_block_pattern.sub(replacer, markdown_text)


def get_text_from_default_editor(initial_text=None):
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as temp_file:
        temp_file_path = temp_file.name

    if initial_text:
        with open(temp_file_path, "w") as text_file:
            text_file.write(initial_text)

    # Open the editor for the user to input text
    editor = os.environ.get("EDITOR", "nano")
    subprocess.run([editor, temp_file_path])

    # Read the contents of the file after the editor is closed
    with open(temp_file_path, "r") as file:
        text = file.read()

    # Remove the temporary file
    os.remove(temp_file_path)

    return text


MODEL_LOOKUP = {
    "code": {
        "o1": Completion,
        "o3": Completion,
        "claude-": Claude,
    },
    "default": {
        "claude-": Claude,
        "dummy-model": DummyAssistant,
        "gpt-4o": Assistant,
        "o1": Assistant,
        "o3": Assistant,
    },
}


async def create_assistant_and_thread(
    args: Namespace, environment: Config
) -> tuple[AssistantInterface, Optional[str]]:
    thread_id = None
    instructions = environment.ASSISTANT_INSTRUCTIONS

    if args.instructions:
        with open(args.instructions, "r") as file:
            instructions = file.read()

    def get_model_class(model_type: str, model_name: str):
        for key, assistant_type in MODEL_LOOKUP[model_type].items():
            if model_name.startswith(key):
                return assistant_type
        raise ConfigError(f"Invalid {model_type} model: {model_name}")

    if args.code:
        model_class = get_model_class("code", environment.CODE_MODEL)
        assistant = model_class(model=environment.CODE_MODEL)
        if isinstance(assistant, Claude):
            assistant.thinking = True
    else:
        model_class = get_model_class("default", args.model)

        if model_class == Assistant:
            assistant = model_class(
                name=environment.ASSISTANT_NAME,
                model=args.model,
                instructions=instructions,
                tools=[{"type": "code_interpreter"}],
                thinking=args.thinking,
            )
        elif model_class == Claude:
            assistant = model_class(
                model=args.model,
                instructions=(
                    instructions
                    if instructions != environment.ASSISTANT_INSTRUCTIONS
                    else None
                ),
                thinking=bool(args.thinking),
            )
        else:
            assistant = model_class(model=args.model)

    await assistant.start()

    if args.continue_thread:
        thread_id = await assistant.async_get_conversation_id()

    return assistant, thread_id
