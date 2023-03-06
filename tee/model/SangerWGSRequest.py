from tee.model.WorkflowRequestBase import WorkflowRequestBase


class SangerWGSRequest(WorkflowRequestBase):
    def __init__(self, workflow_url, config=None, resume=False):
        super().__init__(workflow_url, config, resume)

    def buildWorkflowParams(self, run_config, song_score_config, resume=False):
        study_id = run_config["study_id"]
        normal_aln_analysis_id = run_config["normal_aln_analysis_id"]
        tumour_aln_analysis_id = run_config["tumour_aln_analysis_id"]
        cpus = run_config["cpus"]
        pindel_cpus = run_config["pindel_cpus"]
        mem = run_config["mem"]

        if resume:
            scheduled_dir = '/' + run_config["work_dir"].split('/')[1]
        else:
            scheduled_dir = "<SCHEDULED_DIR>"

        params = {
            "study_id": study_id,
            "normal_aln_analysis_id": normal_aln_analysis_id,
            "tumour_aln_analysis_id": tumour_aln_analysis_id,
            "song_url": song_score_config["SONG_URL"],
            "score_url": song_score_config["SCORE_URL"],
            "cpus": 2,
            "mem": 6,
            "download": {
                "song_cpus": 2,
                "song_mem": 2,
                "score_cpus": 4,
                "score_mem": 10
            },
            "sangerWgsVariantCaller": {
                "cpus": cpus,
                "mem": mem,
                "pindelcpu": pindel_cpus,
                "ref_genome_tar": scheduled_dir+"/reference/ref_hg19/Sanger_GRCh37d5_ref/core_ref_GRCh37d5.tar.gz",
                "vagrent_annot": scheduled_dir+"/reference/ref_hg19/Sanger_GRCh37d5_ref/VAGrENT_ref_GRCh37d5_ensembl_75.tar.gz",
                "ref_snv_indel_tar": scheduled_dir+"/reference/ref_hg19/Sanger_GRCh37d5_ref/SNV_INDEL_ref_GRCh37d5-fragment.tar.gz",
                "ref_cnv_sv_tar": scheduled_dir+"/reference/ref_hg19/Sanger_GRCh37d5_ref/CNV_SV_ref_GRCh37d5_brass6+.tar.gz",
                "qcset_tar": scheduled_dir+"/reference/ref_hg19/Sanger_GRCh37d5_ref/qcGenotype_GRCh37d5.tar.gz"
            },
            "generateBas": {
                "cpus": 6,
                "mem": 32,
                "ref_genome_fa": scheduled_dir+"/reference/ref_hg19/GRCh37d5_ref/genome.fa"
            },
            "repackSangerResults": {
                "cpus": 2,
                "mem": 4
            },
            "prepSangerSupplement": {
                "cpus": 2,
                "mem": 8
            },
            "cavemanVcfFix": {
                "cpus": 2,
                "mem": 16
            },
            "extractSangerCall": {
                "cpus": 2,
                "mem": 4
            },
            "payloadGenVariantCall": {
                "cpus": 2,
                "mem": 8
            },
            "prepSangerQc": {
                "cpus": 2,
                "mem": 8
            },
            "upload": {
                "song_cpus": 2,
                "song_mem": 2,
                "score_cpus": 4,
                "score_mem": 10
            },
            "cleanup": True,
            "max_retries": 0,
            "first_retry_wait_time": 60
        }

        if song_score_config.get("API_TOKEN"):
            params["api_token"] = song_score_config["API_TOKEN"]
        
        return params

    def __str__(self):
        """
        Represent and request against combo of normal_aln_analysis_id and tumour_aln_analysis_id
        """
        return "normal: {} - tumor: {}".format(self.wp_config["normal_aln_analysis_id"], self.wp_config["tumour_aln_analysis_id"])
