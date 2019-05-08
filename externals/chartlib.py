"""
Chartlib for OpenE
"""

from lib.opene.lexer import Token
from lib.opene.devkit import ExternalModule
from lib.opene.devkit import DeveloperKit


class Functions:
    # noinspection SpellCheckingInspection
    @staticmethod
    @DeveloperKit.require_python_module("matplotlib")
    @DeveloperKit.require_python_module("numpy")
    def bar_chart(parameters: list = None) -> Token:
        import matplotlib.pyplot
        import numpy
        plot_data = parameters[0].value
        matplotlib.pyplot.rcdefaults()
        data = {}
        for row in plot_data:
            try:
                data[DeveloperKit.value_of(row[0])] = float(DeveloperKit.value_of(row[1]))
            except ValueError:
                print("The value '{}' is being ignored as it is not a number".format(DeveloperKit.value_of(row[1])))
        titles = list(data.keys())
        values = list(data.values())
        y_pos = numpy.arange(len(titles))
        matplotlib.pyplot.barh(y_pos, values, align="center", alpha=0.5)
        matplotlib.pyplot.yticks(y_pos, titles)
        matplotlib.pyplot.show()
        return parameters[0]


class ExternalParser(ExternalModule):
    functions = {
        "bar_chart": [1, Functions.bar_chart]
    }
