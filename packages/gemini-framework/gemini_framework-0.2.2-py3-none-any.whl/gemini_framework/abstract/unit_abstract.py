from abc import ABC


class UnitAbstract(ABC):
    """Abstract class for Unit."""

    def __init__(self, unit_id, unit_name, plant):
        """Basic constructor for unit objects.

        :param str unit_id: The unique identifier of the unit.
        :param str unit_name: The name of the unit.
        :param object plant: The plant.
        """

        self.id = unit_id
        self.name = unit_name
        self.plant = plant
        self.parameters = {'timestamps': [], 'property': []}
        self.tags = {'measured': {}, 'filtered': {}, 'calculated': {}}
        self.modules = {'preprocessor': [], 'model': [], 'postprocessor': []}
        self.from_units = []
        self.to_units = []

    def link(self):
        for phases in list(self.modules.keys()):
            module_list = self.modules[phases]

            for ii in range(0, len(module_list)):
                module_list[ii].link()

    def set_parameters(self, timestamps, property):
        """function to set unit parameters.

        :param list timestamps: list of parameters timestamps.
        :param list property: list of parameters property.
        """
        self.parameters['timestamps'] = timestamps
        self.parameters['property'] = property

    def set_tagnames(self, category, param):
        """function to set unit parameters.

        :param str category: tagnames category (measured, filtered, calculated).
        :param dict param: tagnames that need to be updated.
        """
        for key, value in param.items():
            self.tags[category][key] = value

    def update_model_parameter(self, timestamps):
        pass
