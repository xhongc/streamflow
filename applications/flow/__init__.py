from applications.flow.end_event_expand import MyExecutableEndEvent
from pipeline.core.flow import FlowNodeClsFactory

FlowNodeClsFactory.register_node("ExecutableEndEvent", MyExecutableEndEvent)
