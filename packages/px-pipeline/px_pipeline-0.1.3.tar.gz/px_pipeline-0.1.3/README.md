# Pipeline runner

## Installation

```sh
pip install px-pipeline
```

## Usage

Simple usage:

```python
from px_pipeline import StraightPipeline, StopFlow


def second_pipeline_handler(context: dict) -> Optional[dict]:
  if 'nothing' in context:
    # You could return empty result so nothing would happen with context.
    return

  # You could mutate context with new data
  context['update'] = True

  # Or return a chunk of data, that will update context object.
  return {'update': False}


def flow_stopper(context):
  if context.get('update', False):
    return {'stopped': False}

  # Or you could raise an error that will stop pipeline from further execution.
  raise StopFlow({'stopped': True})


pipeline = StraightPipeline((
  # Callables can be used in form of import strings.
  'some.path.to.your.execution_function',
  second_pipeline_handler,
  flow_stopper,
))

result = pipeline({})
print(result['stopped']) # > True
print(result['update']) # > False


pipeline = StraightPipeline((
  flow_stopper,
  lambda context: {'called': True},
))

result = pipeline({'update': True})
print(result['stopped']) # > False
print(result['update']) # > True
print(result['called']) # > True

# Here flow stopped and lambda function were not executed.
result = pipeline({'update': False})
print(result['stopped']) # > True
print(result['update']) # > False
print('called' in result) # > False
```

Context typing is a bit awkward and requires some additional boilerplate code
to be used.

So if you want to type you pipeline steps, you could use context unwrapping decorator `unwrap_context`. And the steps from example above could be rewritten as:

```python
from px_pipeline import StraightPipeline, unwrap_context


@unwrap_context
def second_pipeline_handler(
  *,
  nothing: Optional[bool] = None,
  **kw,
) -> Optional[dict]:
  if nothing is not None:
    # You could return empty result so nothing would happen with context.
    return

  # You can not mutate context inside "unwrapped" step:
  kw['update'] = True

  # And partial context return is the only option now.
  return {'update': False}


@unwrap_context
def flow_stopper(*, update: bool = False, **kw):
  if update:
    return {'stopped': False}

  raise StopFlow({'stopped': True})


pipeline = StraightPipeline((
  'some.path.to.your.execution_function',
  second_pipeline_handler,
  flow_stopper,
))
```

### Filter

It's a wrapper around `Pipeline` class, by default it uses a `StraightPipeline` runner. It works similarly to Django's `Signal` API and gives the ability to add and remove handlers from pipeline runners.

It might be useful when you have an breakpoints in your app/library that might be extended from outside. It not just an event that fires, and only informs about something, but you can also change incoming the data in some way that fits your logic.

So based on previous code it could look like that:

```python
from px_pipeline import Filter, StraightPipeline


table_data_for_report_generated = Filter(
  # Initial pipeline that your app provides for this breakpoint.
  initial=(
    'some.path.to.your.execution_function',
    second_pipeline_handler,
  ),
  # Class that will handle pipeline running. Optional.
  pipeline_class=StraightPipeline,
  # Default priority which your handlers will have by default.
  default_priority=10,
)

# ...

# Elsewhere outside your app you may add handlers to pipeline runner.
# Handlers by default will be run in the order they was registered.
table_data_for_report_generated.add(
  # Handle function.
  flow_stopper,
  # This function's priority. Optional.
  priority=10,
  # By default there are 3 layers of execution:
  #   1. PRECEDE - Those handlers that must be executed at first.
  #   2. AVERAGE - Default layer where all handlers executes.
  #   3. FINAL - Those handlers that must be executed at the end.
  # Layers are just another type priority separation.
  # Optional.
  layer=table_data_for_report_generated.Layer.PRECEDE,
)

# ...

# Somewhere in your code you run this filter.
# Runs `pipeline_class` that you were provided previously(or default one).
result = table_data_for_report_generated({})
print(result['stopped']) # > True
print(result['update']) # > False
```
