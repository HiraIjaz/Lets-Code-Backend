import epicbox


def check_code(code, function_name, parameters, input_values, output):
    epicbox.configure(profiles=[epicbox.Profile("python", "python:3.11-alpine")])

    input_params_list = input_values.replace(' ', ',')
    code_with_input = f"""
{code}

print({function_name}({input_params_list}))
"""

    files = [{"name": "main.py", "content": code_with_input.encode()}]
    limits = {"cputime": 1, "memory": 64}
    result = epicbox.run("python", "python3 main.py", files=files, limits=limits)
    # print(
    #     function_name,
    #     " testcase: ",
    #     input_values,
    #     " result: ",
    #     result["stdout"].decode("utf-8"),
    #     result["stderr"].decode("utf-8"),
    #     "\n",
    #     'expected output: ', output
    # )
    if result["stderr"].decode("utf-8") == "":
        return 1 if result["stdout"].decode("utf-8") == output + '\n' else 0
    return 0
