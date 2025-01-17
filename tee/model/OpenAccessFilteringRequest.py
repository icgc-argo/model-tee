from tee.model.WorkflowRequestBase import WorkflowRequestBase


class OpenAccessFilteringRequest(WorkflowRequestBase):
    def __init__(self, workflow_url, config=None, resume=False):
        super().__init__(workflow_url, config, resume)

    def buildWorkflowParams(self, run_config, song_score_config, resume=False):
        study_id = run_config["study_id"]
        analysis_id = run_config["analysis_id"]
        cpus = run_config["cpus"]
        mem = run_config["mem"]

        if resume:
            scheduled_dir = '/' + run_config["work_dir"].split('/')[1]
        else:
            scheduled_dir = "<SCHEDULED_DIR>"

        params = {
            "study_id": study_id,
            "analysis_id": analysis_id,
            "song_url": song_score_config["SONG_URL"],
            "score_url": song_score_config["SCORE_URL"],
            "regions_file": scheduled_dir+"/reference/open-access-filter/open_access.gencode_v38.20210915.bed.gz",
            #"regions_file": "<scheduled_dir>/reference/open-access-variant-filtering/open_access.20210318.bed.gz",  #QA
            "download": {},
            "cpus": cpus,
            "mem": mem,
            "cleanup": True,
            "max_retries": 3,
            "first_retry_wait_time": 5
        }

        if song_score_config.get("DOWNLOAD_SONG_URL"):
            params["download"]["song_url"] = song_score_config["DOWNLOAD_SONG_URL"]

        if song_score_config.get("DOWNLOAD_SCORE_URL"):
            params["download"]["score_url"] = song_score_config["DOWNLOAD_SCORE_URL"]

        if song_score_config.get("DOWNLOAD_SCORE_TOKEN"):
            params["download"]["api_token"] = song_score_config["DOWNLOAD_SCORE_TOKEN"]

        return params

    def __str__(self):
        """
        Represent and request against analysis_id
        """
        return self.wp_config["analysis_id"]
