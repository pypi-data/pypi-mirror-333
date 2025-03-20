import yaml
from pathlib import Path

# wise - Config url_resources via os.environ to resources on company sharepoint for local employees use.


class Config:
    """Handles configuration file loading and resource path management."""

    def __init__(self, url_resources=None):
        self.path = self._Path(url_resources)
        self.config = self._Config(self.path)

    class _Path:
        """Handles directory paths for resources and configurations."""

        def __init__(self, url_resources):
            self.base_dir = Path.cwd().resolve()
            self.resources = Path(url_resources).resolve() if url_resources else self.base_dir / 'simera_resources'
            self.config = Path(__file__).resolve().parent

            # For running and resting with interactive interpreter __file__ is <input>:
            if __file__.startswith('<'):
                self.config = Path.cwd() / 'simera/config'

    class _Config:
        """Loads and manages configuration settings from YAML files."""

        def __init__(self, path):
            self.path = path

            self.country = self._read_yaml(self.path.config / 'country.yaml')

            self._currency_builtin = self._read_yaml(self.path.config / 'currency.yaml')  # Future API integration
            self._currency_resources = self._read_yaml(self.path.resources / 'config' / 'currency.yaml')
            self.currency = self.setup_currency()  # todo integrate builtin and resources

            self._units_of_measure_builtin = self._read_yaml(self.path.config / 'units_of_measure.yaml')
            self._units_of_measure_resources = self._read_yaml(self.path.resources / 'config' / 'units_of_measure.yaml')
            self.units_of_measure = self._units_of_measure_builtin  # todo integrate

        @staticmethod
        def _read_yaml(file_path):
            """Reads a YAML configuration file and returns its contents."""
            try:
                with file_path.open('r', encoding='utf-8') as file:
                    return yaml.safe_load(file) or {}
            except FileNotFoundError:
                print(f"Warning: {file_path.name} not found at {file_path}. Returning an empty dictionary.")
                return {}
            except yaml.YAMLError as e:
                print(f"Error parsing {file_path}: {e}")
                return {}

        def setup_currency(self):

            # Default currency
            currency_default = {'default': self._currency_builtin.get('default', 'EUR')}
            if (currency_default_resources := self._currency_resources.get('default')) is not None:
                currency_default.update({'default': currency_default_resources})

            # Exchange rates
            currency_rates_builtin = self._currency_builtin.get('rates', {'EUR': {'EUR': 1}})
            currency_rates_resources = self._currency_resources.get('rates')
            # Clean resources for empty values
            currency_rates_resources = {k: v for k, v in currency_rates_resources.items() if v is not None}

            if currency_rates_resources:
                # Loop over all currencies in 'resources' and update (or add) 'builtins'. It's a dict in dict structure.
                for k, v in currency_rates_resources.items():
                    if currency_rates_builtin.get(k) is not None:
                        currency_rates_builtin.get(k).update(currency_rates_resources.get(k))
                    else:
                        currency_rates_builtin[k] = currency_rates_resources.get(k)

            currency_rates = {'rates': currency_rates_builtin}

            currency = {}
            currency.update(currency_default)
            currency.update(currency_rates)
            return currency


if __name__ == '__main__':
    sc = Config()
