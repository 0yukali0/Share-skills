import flyte

# The `hello_env` TaskEnvironment is assigned to the variable `env`.
# It is then used in the `@env.task` decorator to define tasks.
# The environment groups configuration for all tasks defined within it.
env = flyte.TaskEnvironment(name="hello_env")

# We use the `@env.task` decorator to define a task called `fn`.
@env.task
def hello(name: str): # Type annotations are required
    print(f"hello {name}")