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
    def bar_chart(parameters: list = None) -> Token:
        import matplotlib.pyplot
        plot_data = parameters[0].value
        matplotlib.pyplot.rcdefaults()
        import numpy as np
        data = {}
        for row in plot_data:
            data[DeveloperKit.value_of(row[0])] = int(DeveloperKit.value_of(row[1]))
        titles = list(data.keys())
        values = list(data.values())
        y_pos = np.arange(len(titles))
        matplotlib.pyplot.barh(y_pos, values, align="center", alpha=0.5)
        matplotlib.pyplot.yticks(y_pos, titles)
        matplotlib.pyplot.show()
        return parameters[0]


class ExternalParser(ExternalModule):
    functions = {
        "bar_chart": [1, Functions.bar_chart]
    }
