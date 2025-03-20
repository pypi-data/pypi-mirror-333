from pygeai.core.common.exceptions import WrongArgumentError


def get_agent_data_prompt_inputs(input_list: list):
    """
    Processes a list of input strings.

    :param input_list: list - A list of strings representing input names.
    :return: list - A list of input strings.
    :raises WrongArgumentError: If the input list contains non-string elements.
    """
    if not all(isinstance(item, str) for item in input_list):
        raise WrongArgumentError(
            "Inputs must be a list of strings: '[\"input_name\", \"another_input\"]'. "
            "Each element in the list must be a string representing an input name."
        )
    return input_list


def get_agent_data_prompt_outputs(output_list: list):
    """
    Processes a list of output dictionaries and extracts the "key" and "description" fields.

    :param output_list: list - A list of dictionaries, where each dictionary must contain the keys "key" and "description".
    :return: list - A list of dictionaries, each containing the "key" and "description" fields.
    :raises WrongArgumentError: If a dictionary in the list is not in the expected format or missing required keys.
    """
    outputs = []
    if any(output_list):
        try:
            for output_dict in output_list:
                outputs.append({
                    "key": output_dict["key"],
                    "description": output_dict["description"]
                })
        except (KeyError, TypeError):
            raise WrongArgumentError(
                "Each output must be in JSON format: '{\"key\": \"output_key\", \"description\": \"description of the output\"}' "
                "It must be a dictionary or a list of dictionaries. Each dictionary must contain 'key' and 'description'."
            )
    return outputs


def get_agent_data_prompt_examples(example_list: list):
    """
    Processes a list of example dictionaries and extracts the "inputData" and "output" fields.

    :param example_list: list - A list of dictionaries, where each dictionary must contain the keys "inputData" and "output".
    :return: list - A list of dictionaries, each containing the "inputData" and "output" fields.
    :raises WrongArgumentError: If a dictionary in the list is not in the expected format or missing required keys.
    """
    examples = []
    if any(example_list):
        try:
            for example_dict in example_list:
                examples.append({
                    "inputData": example_dict["inputData"],
                    "output": example_dict["output"]
                })
        except (KeyError, TypeError):
            raise WrongArgumentError(
                "Each example must be in JSON format: '{\"inputData\": \"example input\", \"output\": \"expected output in JSON string format\"}' "
                "Each dictionary must contain 'inputData' and 'output'."
            )
    return examples
