import functools
import re
from collections import defaultdict

from dojson import Overdo
from dojson.errors import IgnoreKey, MissingRule, IgnoreItem
from dojson.utils import GroupableOrderedDict
from six import iteritems


class NuslMarkOverdo(Overdo):

    def do(self, blob, ignore_missing=True, exception_handlers=None):
        """See Overdo.do for details
        """
        handlers = {IgnoreKey: None}
        handlers.update(exception_handlers or {})

        def clean_missing(exc, output, key, value):
            order = output.get('__order__')
            if order:
                order.remove(key)

        if ignore_missing:
            handlers.setdefault(MissingRule, clean_missing)

        if self.index is None:
            self.build()

        if isinstance(blob, GroupableOrderedDict):
            items = blob.iteritems(repeated=True)
        else:
            items = iteritems(blob)

        original_data = defaultdict(list)
        for key, value in items:
            original_data[key].append(value)

        output = self._transform(original_data, handlers)

        return output

    def _transform(self, original_data, handlers):
        output = {}
        for key, values in original_data.items():
            try:
                result = self.index.query(key)
                if not result:
                    raise MissingRule(key)

                name, creator = result
                extra = self._get_extra_arguments(creator, key, original_data)
                data = creator(output, key, values, **extra)
                if getattr(creator, '__output_reduce__', False):
                    reduce_func = getattr(creator, '__output_reduce__', False)
                    reduce_func(output=output, name=name, key=key, data=data, original_value=values)
                else:
                    output[name] = data
            except Exception as exc:
                if exc.__class__ in handlers:
                    handler = handlers[exc.__class__]
                    if handler is not None:
                        handler(exc, output, key, values)
                else:
                    raise
        return output

    def _get_extra_arguments(self, creator, key, original_data):
        extra = {}
        if hasattr(creator, '__extra__'):
            for name, marc, single, defaultval in creator.__extra__:
                if marc.startswith('^'):
                    # regexp
                    data = []
                    for mk, mvals in original_data.items():
                        if re.match(marc, mk):
                            data.extend(mvals)
                    e = data
                else:
                    e = original_data.get(marc)
                if e is None and defaultval is not None:
                    e = [defaultval] if not isinstance(defaultval, list) else defaultval

                if e is None:
                    raise AttributeError('Extra field(%s, marc %s) for rule %s not found' % (
                        name, marc, key
                    ))

                if single:
                    if len(e) > 1:
                        raise AttributeError('Extra (%s, marc %s) for rule %s requires only one value, has %s' % (
                            name, marc, key, e
                        ))
                    e = e[0] if e else None
                extra[name] = e
        return extra


def result_setter(reduce_func):
    def outer(f):
        setattr(f, '__output_reduce__', reduce_func)

        @functools.wraps(f)
        def wrapper(self, key, values, **kwargs):
            return f(self, key, values, **kwargs)

        return wrapper

    return outer


def list_value(f):
    @functools.wraps(f)
    def wrapper(self, key, values, **kwargs):
        parsed_values = []

        for value in values:
            try:
                parsed_values.append(f(self, key, value, **kwargs))
            except IgnoreItem:
                continue

        return parsed_values

    return wrapper


def merge_results(f):
    def dict_setter(output, name, key, data, original_value, **kwargs):
        output.update(data)

    return result_setter(dict_setter)(f)


def append_results(f):
    def list_setter(output, name, key, data, original_value, **kwargs):
        if name not in output:
            output[name] = []
        output[name].extend(data)

    return result_setter(list_setter)(f)


def single_value(f):
    @functools.wraps(f)
    def wrapper(self, key, values, **kwargs):
        if len(values) > 1:
            raise AttributeError('Too many values for', key, values)
        return f(self, key, values[0], **kwargs)

    return wrapper


def extra_argument(name, marc, single=True, default=None):
    def outer(f):
        if not hasattr(f, '__extra__'):
            f.__extra__ = []
        f.__extra__.append((name, marc, single, default))

        @functools.wraps(f)
        def wrapper(self, key, values, **kwargs):
            return f(self, key, values, **kwargs)

        return wrapper

    return outer


def handled_values(*args):
    args = set(args)
    def outer(f):
        @functools.wraps(f)
        def wrapper(self, key, values, **kwargs):
            if isinstance(values, list):
                test_values = values
            else:
                test_values = [values]
            for value in test_values:
                extra_args = set(value.keys()) - args
                if extra_args:
                    raise AttributeError(f"Unhandled case { {k: value.get(k) for k in extra_args} } ")

            return f(self, key, values, **kwargs)

        return wrapper

    return outer
