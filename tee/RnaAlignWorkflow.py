from tee.SingleInputWorkflowBase import SingleInputWorkflowBase
from tee.model.RnaAlignRequest import RnaAlignRequest


class RnaAlignWorkflow(SingleInputWorkflowBase):

    def __init__(self, config):
        super().__init__(config)

 
    def buildRunRequests(self, run, resume=False):
        config = {
            "study_id": run["study_id"],
            "analysis_id": run["analysis_id"],
            "work_dir": run["work_dir"],
            "revision": self.wf_version,
            "cpus": int(self.cpus),
            "mem": int(self.mem)
        }

        if resume:
            config["resume"] = run["session_id"]

        return RnaAlignRequest(self.wf_url, config, resume)
