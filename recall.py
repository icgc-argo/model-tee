import os
from tee.AlignWorkflow import AlignWorkflow
from tee.SangerWGSWorkflow import SangerWGSWorkflow
from tee.SangerWXSWorkflow import SangerWXSWorkflow
from tee.Mutect2Workflow import Mutect2Workflow
from tee.OpenAccessFiltering import OpenAccessFiltering
from tee.RnaAlignWorkflow import RnaAlignWorkflow
from tee.PreAlnQcWorkflow import PreAlnQcWorkflow
from dotenv import load_dotenv

# load env from file if present
load_dotenv()

# # Build workflow objects
align_wgs_workflow = AlignWorkflow({
    "sheet_id": os.getenv("ALIGN_WGS_SHEET_ID"),
    "sheet_range": os.getenv("ALIGN_WGS_SHEET_RANGE"),
    "wf_url": os.getenv("ALIGN_WGS_WF_URL"),
    "wf_version": os.getenv("ALIGN_WGS_WF_VERSION"),
    "max_runs": -1,
    "max_runs_per_dir": -1,
    "cpus": os.getenv("ALIGN_WGS_CPUS"),
    "mem": os.getenv("ALIGN_WGS_MEM")
})


# sanger_wgs_workflow = SangerWGSWorkflow({
#     "sheet_id": os.getenv("SANGER_WGS_SHEET_ID"),
#     "sheet_range": os.getenv("SANGER_WGS_SHEET_RANGE"),
#     "wf_url": os.getenv("SANGER_WGS_WF_URL"),
#     "wf_version": os.getenv("SANGER_WGS_WF_VERSION"),
#     "max_runs": -1,
#     "max_runs_per_dir": -1,
#     "cpus": os.getenv("SANGER_WGS_CPUS"),
#     "pindel_cpus": os.getenv("SANGER_WGS_PINDEL_CPUS"),
#     "mem": os.getenv("SANGER_WGS_MEM")
# })


# Resume Script (to be run locally only!)
recall_list = [
]
# Rerun Script (to be run locally only!)
rerun_list = [
]

align_wgs_workflow.update()
# align_wgs_workflow.recall(recall_list)
# align_wgs_workflow.rerun(rerun_list)

# sanger_wgs_workflow.update()
# sanger_wgs_workflow.recall(recall_list)
