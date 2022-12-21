import os
from abc import ABC, abstractmethod


class WorkflowRequestBase(ABC):
    def __init__(self, workflow_url, run_config=None, resume=False):
        self.song_score_config = {
            "SONG_URL": os.getenv("SONG_URL"),
            "SCORE_URL": os.getenv("SCORE_URL"),
            "DOWNLOAD_SONG_URL": os.getenv("DOWNLOAD_SONG_URL"),
            "DOWNLOAD_SCORE_URL": os.getenv("DOWNLOAD_SCORE_URL"),
            "DOWNLOAD_SCORE_TOKEN": os.getenv("DOWNLOAD_SCORE_TOKEN")
        }

        self.workflow_url = workflow_url
        #self.resume = resume
        self.wp_config = self.buildWorkflowParams(run_config, self.song_score_config, resume)
        self.wep_config = WorkflowRequestBase.buildEngineParams(run_config,
                                                                os.path.basename(self.workflow_url).split(".")[0], resume)

    def data(self):
        """
        Returns WorkflowRequest in WES format as Dict
        """
        data = {
            "workflow_url": self.workflow_url
        }

        WorkflowRequestBase.addValueIfValue(data, "workflow_params", self.wp_config)
        WorkflowRequestBase.addValueIfValue(data, "workflow_engine_params", self.wep_config)

        return data

    # def getExistingWorkDirForResumedJobs(self, run_config):
    #     if self.resume:
    #         scheduled_dir = '/' + run_config["work_dir"].split('/')[1]
    #     else:
    #         scheduled_dir = "<SCHEDULED_DIR>"
    #
    #     return scheduled_dir;

    @abstractmethod
    def buildWorkflowParams(self, run_config, song_score_config, resume=False):
        pass

    @classmethod
    def buildEngineParams(cls, run_config, workflow_name, resume=False):
        # return None of not specified
        if run_config == None:
            return None

        #scheduled_dir = WorkflowRequestBase.getExistingWorkDirForResumedJobs(run_config)
        if resume:
            scheduled_dir = '/' + run_config["work_dir"].split('/')[1]
        else:
            scheduled_dir = "<SCHEDULED_DIR>"

        engine_params = {}

        WorkflowRequestBase.addFormattedStringValueIfValue(engine_params, "launch_dir", "%s/launch", scheduled_dir)
        WorkflowRequestBase.addFormattedStringValueIfValue(engine_params, "project_dir", "%s/projects/%s/%s/",
                                                           scheduled_dir, workflow_name,
                                                           run_config.get("revision", "master"))
        WorkflowRequestBase.addFormattedStringValueIfValue(engine_params, "work_dir", "%s/work", scheduled_dir)

        WorkflowRequestBase.addValueIfValue(engine_params, "revision", run_config.get("revision", "master"))
        WorkflowRequestBase.addValueIfValue(engine_params, "resume", run_config.get("resume", None))

        return engine_params

    @classmethod
    def addValueIfValue(cls, dict, key, val):
        if not val:
            return

        dict[key] = val

    @classmethod
    def addFormattedStringValueIfValue(cls, dict, key, formatted, *val):
        if None in val:
            return

        dict[key] = formatted % tuple(val)
