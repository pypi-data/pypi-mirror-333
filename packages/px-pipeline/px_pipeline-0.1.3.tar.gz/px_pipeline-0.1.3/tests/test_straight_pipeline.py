from collections import OrderedDict
import pytest

from px_pipeline import StraightPipeline


def test_simple_run():
    def step_one(context):
        context['step_one'] = True

    def step_two(context):

        return {'step_two': True}

    pipeline = StraightPipeline([step_one, step_two])
    context = pipeline(OrderedDict())

    assert context['step_one']
    assert context['step_two']
    # Execution order preserved
    assert tuple(context.keys()) == ('step_one', 'step_two')


def test_context_passing():
    def step_one(context):
        context['step_one'] = True

    def step_two(context):
        assert not context['step_one']

    pipeline = StraightPipeline([step_one, step_two])

    with pytest.raises(AssertionError):
        pipeline(OrderedDict())


def test_importable_pipeline():
    def step_one(context):
        context['step_one'] = True

    pipeline = StraightPipeline([
        step_one,
        'tests.fixtures.importable_executor.execute',
    ])
    context = pipeline(OrderedDict())

    assert context['step_one']
    assert context['importable']
    # Execution order preserved
    assert tuple(context.keys()) == ('step_one', 'importable')
