from tee.model.WorkflowRequestBase import WorkflowRequestBase


class PreAlnQcRequest(WorkflowRequestBase):
    def __init__(self, workflow_url, config=None, resume=False):
        super().__init__(workflow_url, config, resume)

    def buildWorkflowParams(self, run_config, song_score_config, resume=False):
        study_id = run_config["study_id"]
        analysis_id = run_config["analysis_id"]
        cpus = run_config["cpus"]
        mem = run_config["mem"]

        params = {
            "study_id": study_id,
            "analysis_id": analysis_id,
            "song_url": song_score_config["SONG_URL"],
            "score_url": song_score_config["SCORE_URL"],
            "cpus": 2,
            "mem": 4,
            "download": {
              "song_cpus": 2,
              "song_mem": 2,
              "score_cpus": 4,
              "score_mem": 10
            },
            "seqDataToLane": {
              "cpus": cpus,
              "mem": mem
            },
            "fastqc": {
              "cpus": cpus,
              "mem": mem
            },
            "cutadapt": {
              "cpus": 2,
              "mem": 2
            },
            "multiqc": {
              "cpus": 2,
              "mem": 2
            },
            "payloadGen": {
              "cpus": 2,
              "mem": 2
            },
            "uploadQc": {
              "song_cpus": 2,
              "song_mem": 2,
              "score_cpus": 4,
              "score_mem": 10
            },
            "tempdir": "/icgc-argo-scratch",
            "cleanup": True,
            "max_retries": 5,
            "first_retry_wait_time": 60
        }

        if song_score_config.get("DOWNLOAD_SONG_URL"):
            params["download"]["song_url"] = song_score_config["DOWNLOAD_SONG_URL"]

        if song_score_config.get("DOWNLOAD_SCORE_URL"):
            params["download"]["score_url"] = song_score_config["DOWNLOAD_SCORE_URL"]

        if song_score_config.get("DOWNLOAD_SCORE_TOKEN"):
            params["download"]["score_api_token"] = song_score_config["DOWNLOAD_SCORE_TOKEN"]

        return params

    def __str__(self):
        """
        Represent and request against analysis_id
        """
        return self.wp_config["analysis_id"]
