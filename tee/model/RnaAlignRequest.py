from tee.model.WorkflowRequestBase import WorkflowRequestBase


class RnaAlignRequest(WorkflowRequestBase):
    def __init__(self, workflow_url, config=None):
        super().__init__(workflow_url, config)

    def buildWorkflowParams(self, run_config, song_score_config):
        study_id = run_config["study_id"]
        analysis_id = run_config["analysis_id"]
        cpus = run_config["cpus"]
        mem = max((cpus * 3) + 2, run_config["mem"])

        params = {
            "study_id": study_id,
            "analysis_id": analysis_id,
            "song_url": song_score_config["SONG_URL"],
            "score_url": song_score_config["SCORE_URL"],
            "genome_annotation": "GENCODE v40",
            "genome_build": "GRCh38_Verily_v1",
            "ref_genome_index_star": "<SCHEDULED_DIR>/reference/rna-seq-references/GRCh38_Verily_v1.STARindex.sjdbOverhang_75",
            "ref_genome_index_hisat2": "<SCHEDULED_DIR>/reference/rna-seq-references/GRCh38_Verily_v1.HISAT2index/GRCh38_Verily_v1",
            "ref_genome_gtf": "<SCHEDULED_DIR>/reference/rna-seq-references/GRCh38_Verily_v1.annotation/gencode.v40.chr_patch_hapl_scaff.annotation.gtf",
            "ref_genome_fa": "<SCHEDULED_DIR>/reference/rna-seq-references/GRCh38_Verily_v1.genome/GRCh38_Verily_v1.genome.fa",
            "ref_flat": "<SCHEDULED_DIR>/reference/rna-seq-references/GRCh38_Verily_v1.Picard_CollectRnaSeqMetrics/GRCh38_Verily_v1.refFlat.txt.gz",
            "ribosomal_interval_list": "<SCHEDULED_DIR>/reference/rna-seq-references/GRCh38_Verily_v1.Picard_CollectRnaSeqMetrics/GRCh38_Verily_v1.rRNA.interval_list",
            "sjdboverhang": 75,
            "star": True,
            "hisat2": True,
            "lane_qc": False,
            "aln_qc": True,
            "cpus": 2,
            "mem": 4,
            "download": {
                "song_cpus": 2,
                "song_mem": 2,
                "score_cpus": 4,
                "score_mem": 10
            },
            "seqDataToLaneBam": {
                "cpus": 4,
                "mem": 18
            },
            "starAligner": {
              "mem": mem,
              "cpus": cpus    
            },
            "hisat2Aligner": {
              "mem": mem,
              "cpus": cpus    
            },
            "bamMergeSortMarkdup": {
                "cpus": 4,
                "mem": 18
            },
            "readGroupUBamQC": {
                "cpus": 3,
                "mem": 8
            },
            "alignedSeqQC": {
              "mem": 16,
              "cpus": 4
            },
            "payloadGen": {
              "mem": 8,
              "cpus": 2
            },
            "upload": {
              "score_mem": 10,
              "song_mem": 2,
              "score_cpus": 4,
              "song_cpus": 2
            },
            "tempdir": "/icgc-argo-scratch",
            "cleanup": True,
            "max_retries": 2,
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
