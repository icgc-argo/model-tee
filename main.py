import os
from multiprocessing import Process
from service.Kafka import Kafka
from service.CircuitBreaker import CircuitBreaker
from tee.AlignWorkflow import AlignWorkflow
from tee.SangerWGSWorkflow import SangerWGSWorkflow
from tee.SangerWXSWorkflow import SangerWXSWorkflow
from tee.Mutect2Workflow import Mutect2Workflow
from tee.OpenAccessFiltering import OpenAccessFiltering
from tee.RnaAlignWorkflow import RnaAlignWorkflow
from tee.PreAlnQcWorkflow import PreAlnQcWorkflow
from tee.Utils import Utils
from dotenv import load_dotenv

# load env from file
load_dotenv()

# Build circuit breaker
circuit_breaker = CircuitBreaker(
    int(os.getenv("CB_LIMIT", 3)),
    int(os.getenv("CB_RANGE_DAYS", 2))
)

# Build workflow objects
align_wgs_workflow = AlignWorkflow({
    "sheet_id": os.getenv("ALIGN_WGS_SHEET_ID"),
    "sheet_range": os.getenv("ALIGN_WGS_SHEET_RANGE"),
    "wf_url": os.getenv("ALIGN_WGS_WF_URL"),
    "wf_version": os.getenv("ALIGN_WGS_WF_VERSION"),
    "max_runs": os.getenv("ALIGN_WGS_MAX_RUNS"),
    "max_runs_per_dir": os.getenv("ALIGN_WGS_MAX_RUNS_PER_DIR"),
    "cpus": os.getenv("ALIGN_WGS_CPUS"),
    "mem": os.getenv("ALIGN_WGS_MEM")
})


sanger_wgs_workflow = SangerWGSWorkflow({
    "sheet_id": os.getenv("SANGER_WGS_SHEET_ID"),
    "sheet_range": os.getenv("SANGER_WGS_SHEET_RANGE"),
    "wf_url": os.getenv("SANGER_WGS_WF_URL"),
    "wf_version": os.getenv("SANGER_WGS_WF_VERSION"),
    "max_runs": os.getenv("SANGER_WGS_MAX_RUNS"),
    "max_runs_per_dir": os.getenv("SANGER_WGS_MAX_RUNS_PER_DIR"),
    "cpus": os.getenv("SANGER_WGS_CPUS"),
    "pindel_cpus": os.getenv("SANGER_WGS_PINDEL_CPUS"),
    "mem": os.getenv("SANGER_WGS_MEM")
})



runOrUpdateAlignWGS = Utils.methodOrUpdateFactory(align_wgs_workflow, "run", circuit_breaker)


getMergeWorkDirsInUse = Utils.mergeWorkDirsInUseFuncGen(align_wgs_workflow, 
                                                        sanger_wgs_workflow)


def onWorkflowMessageFunc(message):
    print("Workflow event received ... applying filter ...")

    if message.value["event"] == "completed":
        print("Workflow event valid, starting configured processes ...")
        runOrUpdateAlignWGS(quick=False, global_work_dirs_in_use=getMergeWorkDirsInUse(align_wgs_workflow))

    else:
        print("Workflow event does not pass filter!")


# Processes
workflowConsumer = Process(target=Kafka.consumeTopicWith, args=(os.getenv("KAFKA_TOPIC", "workflow"), onWorkflowMessageFunc))

# Main
if __name__ == '__main__':
    # # run on start (if we are not in circuit breaker blown state)
    runOrUpdateAlignWGS(quick=True, global_work_dirs_in_use=getMergeWorkDirsInUse(align_wgs_workflow))


