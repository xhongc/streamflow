from applications.flow.constants import PIPELINE_STATE_TO_FLOW_STATE
from pipeline.core.flow import ExecutableEndEvent


class MyExecutableEndEvent(ExecutableEndEvent):
    def execute(self, in_subprocess, root_pipeline_id, current_pipeline_id):
        from applications.flow.models import ProcessRun

        ProcessRun.objects.filter(root_id=root_pipeline_id).update(state="success")
        return True
