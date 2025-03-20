import json
import sys

from pygeai.cli.commands import Command, Option, ArgumentsEnum
from pygeai.cli.commands.builders import build_help_text
from pygeai.cli.commands.studio.common import get_agent_data_prompt_inputs, get_agent_data_prompt_outputs, \
    get_agent_data_prompt_examples
from pygeai.cli.texts.help import AI_STUDIO_HELP_TEXT
from pygeai.core.common.exceptions import MissingRequirementException, WrongArgumentError
from pygeai.studio.clients import AIStudioClient


def show_assistant_help():
    """
    Displays help text in stdout
    """
    help_text = build_help_text(ai_studio_commands, AI_STUDIO_HELP_TEXT)
    sys.stdout.write(help_text)


def create_agent(option_list: list):
    name = None
    access_scope = None
    public_name = None
    job_description = None
    avatar_image = None
    description = None
    agent_data_prompt_instructions = None
    agent_data_prompt_inputs = list()
    agent_data_prompt_outputs = list()
    agent_data_prompt_examples = list()
    agent_data_llm_max_tokens = None
    agent_data_llm_timeout = None
    agent_data_llm_temperature = None
    agent_data_llm_top_k = None
    agent_data_llm_top_p = None
    agent_data_model_name = None

    for option_flag, option_arg in option_list:
        if option_flag.name == "name":
            name = option_arg
        if option_flag.name == "access_scope":
            access_scope = option_arg
        if option_flag.name == "public_name":
            public_name = option_arg
        if option_flag.name == "job_description":
            job_description = option_arg
        if option_flag.name == "avatar_image":
            avatar_image = option_arg
        if option_flag.name == "description":
            description = option_arg

        if option_flag.name == "agent_data_prompt_instructions":
            agent_data_prompt_instructions = option_arg
        if option_flag.name == "agent_data_prompt_input":

            if "[" not in option_arg:
                agent_data_prompt_inputs.append(option_arg)
            else:
                try:
                    input_json = json.loads(option_arg)
                    if not isinstance(input_json, list):
                        raise ValueError

                    agent_data_prompt_inputs = input_json
                except Exception as e:
                    raise WrongArgumentError(
                        "Inputs must be a list of strings: '[\"input_name\", \"another_input\"]'. "
                        "Each element in the list must be a string representing an input name."
                    )
        if option_flag.name == "agent_data_prompt_output":
            try:
                output_json = json.loads(option_arg)
                if isinstance(output_json, list):
                    agent_data_prompt_outputs = output_json
                elif isinstance(output_json, dict):
                    agent_data_prompt_outputs.append(output_json)
            except Exception as e:
                raise WrongArgumentError(
                    "Each output must be in JSON format: '{\"key\": \"output_key\", \"description\": \"description of the output\"}' "
                    "It must be a dictionary or a list of dictionaries. Each dictionary must contain 'key' and 'description'."
                )

        if option_flag.name == "agent_data_prompt_example":
            try:
                examples_json = json.loads(option_arg)
                if isinstance(examples_json, list):
                    agent_data_prompt_examples = examples_json
                elif isinstance(examples_json, dict):
                    agent_data_prompt_examples.append(examples_json)
            except Exception as e:
                raise WrongArgumentError(
                    "Each example must be in JSON format: '{\"inputData\": \"example input\", \"output\": \"expected output in JSON string format\"}' "
                    "It must be a dictionary or a list of dictionaries. Each dictionary must contain 'inputData' and 'output'."
                )

        if option_flag.name == "agent_data_llm_max_tokens":
            agent_data_llm_max_tokens = option_arg
        if option_flag.name == "agent_data_llm_timeout":
            agent_data_llm_timeout = option_arg
        if option_flag.name == "agent_data_llm_temperature":
            agent_data_llm_temperature = option_arg
        if option_flag.name == "agent_data_llm_top_k":
            agent_data_llm_top_k = option_arg
        if option_flag.name == "agent_data_llm_top_p":
            agent_data_llm_top_p = option_arg

        if option_flag.name == "agent_data_model_name":
            agent_data_model_name = option_arg

    if not (name and access_scope and public_name):
        raise MissingRequirementException("Cannot create assistant without specifying name, access scope and public name")

    prompt_inputs = get_agent_data_prompt_inputs(agent_data_prompt_inputs)
    prompt_outputs = get_agent_data_prompt_outputs(agent_data_prompt_outputs)
    prompt_examples = get_agent_data_prompt_examples(agent_data_prompt_examples)

    agent_data_prompt = {
        "instructions": agent_data_prompt_instructions,
        "inputs": prompt_inputs,
        "outputs": prompt_outputs,
        "examples": prompt_examples
    }
    agent_data_llm_config = {
        "maxTokens": agent_data_llm_max_tokens,
        "timeout": agent_data_llm_timeout,
        "sampling": {
            "temperature": agent_data_llm_temperature,
            "topK": agent_data_llm_top_k,
            "topP": agent_data_llm_top_p,
        }
    }
    agent_data_models = [
        {"name": agent_data_model_name}
    ]

    client = AIStudioClient()
    result = client.create_agent(
        name=name,
        access_scope=access_scope,
        public_name=public_name,
        job_description=job_description,
        avatar_image=avatar_image,
        description=description,
        agent_data_prompt=agent_data_prompt,
        agent_data_llm_config=agent_data_llm_config,
        agent_data_models=agent_data_models
    )
    sys.stdout.write(f"New agent detail: \n{result}\n")


create_agent_options = [
    Option(
        "name",
        ["--name", "-n"],
        "name",
        True
    ),
    Option(
        "access_scope",
        ["--access-scope", "--as"],
        "accessScope",
        True
    ),
    Option(
        "public_name",
        ["--public-name", "--pn"],
        "publicName",
        True
    ),
    Option(
        "job_description",
        ["--job-description", "--jd"],
        "jobDescription",
        True
    ),
    Option(
        "avatar_image",
        ["--avatar-image", "--aimg"],
        "avatarImage",
        True
    ),
    Option(
        "description",
        ["--description", "-d"],
        "description",
        True
    ),
    Option(
        "agent_data_prompt_instructions",
        ["--agent-data-prompt-instructions", "--adp-inst"],
        "Agent Data prompt instructions",
        True
    ),
    Option(
        "agent_data_prompt_input",
        ["--agent-data-prompt-input", "--adp-input"],
        "Agent Data prompt input: "
        "Inputs must be a list of strings '[\"input_name\", \"another_input\"]' or each string can be passed as a "
        "single item with multiple instances of --adp-input"
        "Each element in the list must be a string representing an input name.",
        True
    ),
    Option(
        "agent_data_prompt_output",
        ["--agent-data-prompt-output", "--adp-out"],
        "Agent Data prompt output: "
        "Each output must be in JSON format: '{\"key\": \"output_key\", \"description\": \"description of the output\"}' "
        "It must be a dictionary or a list of dictionaries. Each dictionary must contain 'key' and 'description'.",
        True
    ),
    Option(
        "agent_data_prompt_example",
        ["--agent-data-prompt-example", "--adp-ex"],
        "Agent Data prompt example"
        "Each example must be in JSON format: '{\"inputData\": \"example input\", \"output\": \"expected output in JSON string format\"}' "
        "It must be a dictionary or a list of dictionaries. Each dictionary must contain 'inputData' and 'output'.",
        True
    ),
    Option(
        "agent_data_llm_max_tokens",
        ["--agent-data-llm-max-tokens", "--adl-max-tokens"],
        "Agent Data LLM config max tokens",
        True
    ),
    Option(
        "agent_data_llm_timeout",
        ["--agent-data-llm-timeout", "--adl-timeout"],
        "Agent Data LLM config timeout",
        True
    ),
    Option(
        "agent_data_llm_temperature",
        ["--agent-data-llm-temperature", "--adl-temperature"],
        "Agent Data LLM config temperature",
        True
    ),
    Option(
        "agent_data_llm_top_k",
        ["--agent-data-llm-top-k", "--adl-top-k"],
        "Agent Data LLM config topK",
        True
    ),
    Option(
        "agent_data_llm_top_p",
        ["--agent-data-llm-top-p", "--adl-top-p"],
        "Agent Data LLM config topP",
        True
    ),
    Option(
        "agent_data_model_name",
        ["--agent-data-model-name", "--adm-name"],
        "Agent Data LLM model name",
        True
    ),

]


ai_studio_commands = [
    Command(
        "help",
        ["help", "h"],
        "Display help text",
        show_assistant_help,
        ArgumentsEnum.NOT_AVAILABLE,
        [],
        []
    ),
    Command(
        "create_agent",
        ["create-agent", "ca"],
        "Create agent",
        create_agent,
        ArgumentsEnum.REQUIRED,
        [],
        create_agent_options
    ),
]
