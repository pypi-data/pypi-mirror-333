from autosubmit_api.logger import logger
from autosubmit_api.builders.configuration_facade_builder import (
    ConfigurationFacadeDirector,
    AutosubmitConfigurationFacadeBuilder,
)
from autosubmit_api.config.basicConfig import APIBasicConfig
from collections import namedtuple
from typing import List

from autosubmit_api.repositories.experiment import create_experiment_repository
from autosubmit_api.repositories.experiment_details import (
    create_experiment_details_repository,
)


ExperimentDetails = namedtuple(
    "ExperimentDetails", ["owner", "created", "model", "branch", "hpc"]
)
Experiment = namedtuple("Experiment", ["id", "name"])


class DetailsProcessor:
    def __init__(self, basic_config: APIBasicConfig):
        self.basic_config = basic_config
        # self.main_db_engine = create_autosubmit_db_engine()
        self.experiment_db = create_experiment_repository()
        self.details_db = create_experiment_details_repository()

    def process(self):
        new_details = self._get_all_details()
        self._clean_table()
        return self._insert_many_into_details_table(new_details)

    def _get_experiments(self) -> List[Experiment]:
        experiments = []
        query_result = self.experiment_db.get_all()

        for exp in query_result:
            experiments.append(Experiment(exp.id, exp.name))

        return experiments

    def _get_details_data_from_experiment(self, expid: str) -> ExperimentDetails:
        autosubmit_config = ConfigurationFacadeDirector(
            AutosubmitConfigurationFacadeBuilder(expid)
        ).build_autosubmit_configuration_facade(self.basic_config)
        return ExperimentDetails(
            autosubmit_config.get_owner_name(),
            autosubmit_config.get_experiment_created_time_as_datetime(),
            autosubmit_config.get_model(),
            autosubmit_config.get_branch(),
            autosubmit_config.get_main_platform(),
        )

    def _get_all_details(self) -> List[dict]:
        experiments = self._get_experiments()
        result = []
        exp_ids = set()
        for experiment in experiments:
            try:
                detail = self._get_details_data_from_experiment(experiment.name)
                if experiment.id not in exp_ids:
                    result.append(
                        {
                            "exp_id": experiment.id,
                            "user": detail.owner,
                            "created": detail.created,
                            "model": detail.model,
                            "branch": detail.branch,
                            "hpc": detail.hpc,
                        }
                    )
                    exp_ids.add(experiment.id)
            except Exception as exc:
                logger.warning(
                    ("Error on experiment {}: {}".format(experiment.name, str(exc)))
                )
        return result

    def _insert_many_into_details_table(self, values: List[dict]) -> int:
        rowcount = self.details_db.insert_many(values)
        return rowcount

    def _clean_table(self) -> int:
        rowcount = self.details_db.delete_all()
        return rowcount
