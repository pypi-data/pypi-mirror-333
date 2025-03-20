import pytest

from px_pipeline import StraightPipeline, unwrap_context


def test_context_unwrapping():
    def step_one(context):
        context['step_one'] = True

    @unwrap_context
    def step_two(*, step_one: bool, **kw):
        return {'step_two': not step_one}

    pipeline = StraightPipeline([step_one, step_two])
    result = pipeline({'step_one': False})

    assert 'step_one' in result
    assert result['step_one']

    assert 'step_two' in result
    assert not result['step_two']
