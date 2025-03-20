import pytest
from collections import OrderedDict

from px_pipeline import Filter


def step_one(context):
    context['step_one'] = True

def step_two(context):
    return {'step_two': True}

def step_n_three(context):
    pass

def step_n_four(context):
    pass

def step_n_five(context):
    pass


def test_simple_run():
    filter = Filter()
    filter.add(step_one)
    filter.add(step_two)

    assert filter.is_fresh() is False

    context = filter(OrderedDict())

    assert filter.is_fresh() is True
    assert context['step_one']
    assert context['step_two']
    # Execution order preserved
    assert tuple(context.keys()) == ('step_one', 'step_two')


def test_initial():
    filter = Filter([step_one, step_two])
    filter.add(step_n_three)
    filter.resolve_pipeline()

    assert tuple(filter.pipeline.pipeline) == (step_one, step_two, step_n_three)


def test_initial_no_add_or_empty():
    filter = Filter([step_one, step_two])

    assert not filter.is_fresh()
    filter.resolve_pipeline()

    assert tuple(filter.pipeline.pipeline) == (step_one, step_two)

    empty = Filter()
    context = {}
    assert not empty.is_fresh()
    assert empty(context) is context
    assert empty.is_fresh()


def test_registry_errors():
    filter = Filter()
    filter.add(step_one)
    filter.add(step_two)

    with pytest.raises(ValueError):
        filter.add(step_one)

    filter.remove(step_one)

    with pytest.raises(ValueError):
        filter.remove(step_one)

    filter.add(step_one)


def test_refresh(monkeypatch):
    filter = Filter()
    filter.add(step_one)
    filter.add(step_two)

    assert filter.is_fresh() is False

    filter(OrderedDict())

    assert filter.is_fresh() is True
    saved = filter.pipeline

    def patched(*a):
        raise NotImplementedError()

    monkeypatch.setattr(filter, 'pipeline_class', patched)

    assert filter.is_fresh() is True

    filter(OrderedDict())

    assert filter.is_fresh() is True
    assert filter.pipeline == saved


def test_registry_ordering():
    # After removing and then adding item to a pipeline it should change
    # it's ordering because filters will maintain their definition ordering
    # in terms of one priority index.
    filter = Filter()
    filter.add(step_one)
    filter.add(step_two)
    filter.add(step_n_three)
    filter.resolve_pipeline()

    assert tuple(filter.pipeline.pipeline) == (step_one, step_two, step_n_three)

    filter.remove(step_one)
    filter.add(step_one)
    filter.resolve_pipeline()

    assert tuple(filter.pipeline.pipeline) == (step_two, step_n_three, step_one)

    # Now we have one function with largest priority of all provided(10 is
    # default value).
    # So it should remain it's ordering no matter how many handlers will be
    # added with 10 priority value afterwords.
    filter = Filter()
    filter.add(step_one)
    filter.add(step_two, 11)
    filter.add(step_n_three)
    filter.resolve_pipeline()

    assert tuple(filter.pipeline.pipeline) == (step_one, step_n_three, step_two)

    filter.remove(step_one)
    filter.add(step_one)
    filter.resolve_pipeline()

    assert tuple(filter.pipeline.pipeline) == (step_n_three, step_one, step_two)

    # Other thing here. Handler with lower priority always runs first.
    filter = Filter()
    filter.add(step_one)
    filter.add(step_two, 9)
    filter.add(step_n_three)
    filter.resolve_pipeline()

    assert tuple(filter.pipeline.pipeline) == (step_two, step_one, step_n_three)

    filter.remove(step_two)
    filter.add(step_two, 9)
    filter.resolve_pipeline()

    assert tuple(filter.pipeline.pipeline) == (step_two, step_one, step_n_three)

    # Layering check.
    # All the priorities are working inside layers. No priority change
    # can overcome layer.
    filter = Filter()
    filter.add(step_one, layer=filter.Layer.PRECEDE)
    filter.add(step_two)
    filter.add(step_n_three)
    filter.add(step_n_four)
    filter.add(step_n_five, layer=filter.Layer.FINAL)
    filter.resolve_pipeline()

    ordering = (
        step_one, step_two, step_n_three, step_n_four, step_n_five
    )
    assert tuple(filter.pipeline.pipeline) == ordering

    filter.remove(step_n_three)
    filter.add(step_n_three)
    filter.remove(step_n_four)
    filter.add(step_n_four, float('inf'))
    filter.remove(step_two)
    filter.add(step_two, float('-inf'))
    filter.resolve_pipeline()

    assert tuple(filter.pipeline.pipeline) == ordering
