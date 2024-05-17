from deepeval.benchmarks.mmlu.task import MMLUTask


class MMLUTemplate:

    # Most of this template was taken from MMLU Github Repo
    # The output confinement is a novel addition, since the original code
    # outputted log_probabilties for each answer choice

    @staticmethod
    def generate_output(
        input: str, train_set: object, task: MMLUTask, n_shots: int, template: str
    ):
        if template == "default":
            prompt = "Answer last multiple choice question (with answers) about {}. " \
                 "Output 'A', 'B', 'C', or 'D'. Full answer not needed. These are some examples to help you answer: \n\n"
        else:
            prompt = template
        if "{}" in prompt:
            prompt = prompt.format(MMLUTemplate.format_subject(task.value))
        for i in range(n_shots):
            prompt += MMLUTemplate.format_question(train_set[i])
        prompt += input

        # define ouptut confinement
        # prompt += "Output 'A', 'B', 'C', or 'D'. Full answer not needed."
        return prompt

    @staticmethod
    def format_question(data: dict, include_answer: bool = True):
        prompt = data["input"]
        choices = ["A", "B", "C", "D"]
        for j in range(len(choices)):
            choice = choices[j]
            prompt += "\n{}. {}".format(choice, data[choice])
        prompt += "\nAnswer:"
        if include_answer:
            prompt += " {}\n\n".format(data["target"])
        return prompt

    def format_subject(subject: str):
        l = subject.split("_")
        s = ""
        for entry in l:
            s += " " + entry
        return s
