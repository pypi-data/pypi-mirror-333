from oarepo_model_builder.datatypes import DataTypeComponent
from oarepo_model_builder.datatypes.components.model import ServiceModelComponent
from oarepo_model_builder.datatypes.model import ModelDataType
from oarepo_model_builder_files.datatypes.components import ParentRecordComponent

PLAIN_RECORD_SERVICE = (
    "invenio_records_resources.services.RecordService{InvenioRecordService}"
)
DRAFT_RECORD_SERVICE = (
    "invenio_drafts_resources.services.RecordService{InvenioRecordService}"
)
RDM_RECORD_SERVICE = "invenio_rdm_records.services.services.RDMRecordService"

PLAIN_SERVICE_CONFIG = (
    "invenio_records_resources.services.RecordServiceConfig{InvenioRecordServiceConfig}"
)
DRAFT_SERVICE_CONFIG = "invenio_drafts_resources.services.RecordServiceConfig{InvenioRecordDraftsServiceConfig}"
RDM_SERVICE_CONFIG = "invenio_rdm_records.services.config.RDMRecordServiceConfig"


class RDMServiceComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [ServiceModelComponent, ParentRecordComponent]

    def before_model_prepare(self, datatype, *, context, **kwargs):

        if datatype.profile not in ["record", "draft"]:
            return
        components_to_remove = [
            "{{oarepo_runtime.services.files.FilesComponent}}",
            "{{invenio_drafts_resources.services.records.components.DraftFilesComponent}}",
            "{{oarepo_runtime.services.components.OwnersComponent}}",
        ]
        datatype.service_config["components"] = [
            component
            for component in datatype.service_config["components"]
            if component not in components_to_remove
        ]
        service_base_classes = datatype.definition["service"].setdefault(
            "base-classes", []
        )
        if service_base_classes:
            if PLAIN_RECORD_SERVICE in service_base_classes:
                idx = service_base_classes.index(PLAIN_RECORD_SERVICE)
                service_base_classes[idx] = RDM_RECORD_SERVICE
            if DRAFT_RECORD_SERVICE in service_base_classes:
                idx = service_base_classes.index(DRAFT_RECORD_SERVICE)
                service_base_classes[idx] = RDM_RECORD_SERVICE
        else:
            service_base_classes.append(RDM_RECORD_SERVICE)

        config_base_classes = datatype.definition["service-config"].setdefault(
            "base-classes", []
        )
        if config_base_classes:
            if PLAIN_SERVICE_CONFIG in config_base_classes:
                idx = config_base_classes.index(PLAIN_SERVICE_CONFIG)
                config_base_classes[idx] = RDM_SERVICE_CONFIG
            if DRAFT_SERVICE_CONFIG in config_base_classes:
                idx = config_base_classes.index(DRAFT_SERVICE_CONFIG)
                config_base_classes[idx] = RDM_SERVICE_CONFIG
        else:
            config_base_classes.append(RDM_SERVICE_CONFIG)
