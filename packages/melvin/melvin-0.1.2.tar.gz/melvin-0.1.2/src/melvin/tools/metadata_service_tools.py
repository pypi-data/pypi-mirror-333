from typing import List, Dict
from utils import _err, _log
from tecton._internals import metadata_service
from tecton import conf
from tecton_core.fco_container import FcoContainer
from tecton_proto.metadataservice.metadata_service__client_pb2 import (
    GetAllFeatureServicesRequest,
    ListWorkspacesRequest,
    QueryFeatureViewsRequest,
    GetAllTransformationsRequest,
    GetTransformationRequest,
    GetAllVirtualDataSourcesRequest,
    GetAllEntitiesRequest
)


def list_workspaces() -> List[str]:
    """
    List all workspaces in the currently connected Tecton cluster.

    Returns:
        List[str]: A list of workspace names in the connected Tecton cluster.
        Returns an empty list if the operation fails.
    """
    try:
        request = ListWorkspacesRequest()
        response = metadata_service.instance().ListWorkspaces(request)
        return [ws.name for ws in response.workspaces]
    except Exception as e:
        _err(f"Failed to list workspaces: {str(e)}")
        return []


def list_feature_views() -> List[Dict]:
    """
    List all feature views in the currently connected tecton cluster

    Returns:
        List[dict]: A list of dictionaries containing name, description, workspace, and tags for each feature view
    """
    try:
        feature_views = []
        workspaces = list_workspaces()

        for workspace in workspaces:
            request = QueryFeatureViewsRequest(workspace=workspace)
            response = metadata_service.instance().QueryFeatureViews(request)

            for fco in response.fco_container.fcos:
                if hasattr(fco, "feature_view") and fco.feature_view.fco_metadata.name:
                    feature_views.append(
                        {
                            "name": fco.feature_view.fco_metadata.name,
                            "description": fco.feature_view.fco_metadata.description,
                            "workspace": workspace,
                            "tags": dict(fco.feature_view.fco_metadata.tags),
                        }
                    )

        return sorted(feature_views, key=lambda x: x["name"])
    except Exception as e:
        _err(f"Failed to list feature views: {str(e)}")
        return []


def list_feature_services() -> List[Dict]:
    """
    List all feature services in the currently connected tecton cluster

    Returns:
        List[dict]: A list of dictionaries containing name, description, workspace, and tags for each feature service
    """
    try:
        feature_services = []
        workspaces = list_workspaces()

        for workspace in workspaces:
            request = GetAllFeatureServicesRequest(workspace=workspace)
            response = metadata_service.instance().GetAllFeatureServices(request)

            for feature_service in response.feature_services:
                if feature_service.fco_metadata.name:
                    feature_services.append(
                        {
                            "name": feature_service.fco_metadata.name,
                            "description": feature_service.fco_metadata.description,
                            "workspace": workspace,
                            "tags": dict(feature_service.fco_metadata.tags),
                        }
                    )

        _log("Inspecting FeatureServices")

        return sorted(feature_services, key=lambda x: x["name"])
    except Exception as e:
        _err(f"Failed to list feature services: {str(e)}")
        return []


def list_transformations() -> List[Dict]:
    """
    List all transformations in the currently connected tecton cluster

    Returns:
        List[dict]: A list of dictionaries containing name, description, workspace, and tags for each transformation
    """
    try:
        transformations = []
        workspaces = list_workspaces()

        for workspace in workspaces:
            request = GetAllTransformationsRequest(workspace=workspace)
            response = metadata_service.instance().GetAllTransformations(request)

            for transformation in response.transformations:
                if transformation.fco_metadata.name:
                    transformations.append(
                        {
                            "name": transformation.fco_metadata.name,
                            "description": transformation.fco_metadata.description,
                            "workspace": workspace,
                            "tags": dict(transformation.fco_metadata.tags),
                        }
                    )

        return sorted(transformations, key=lambda x: x["name"])
    except Exception as e:
        _err(f"Failed to list transformations: {str(e)}")
        return []

def get_feature_service_configuration(name: str, workspace: str) -> str:
    """
    Get the entire definition of a feature service from the Tecton cluster.

    Args:
        name: The name of the feature service to retrieve
        workspace: The workspace containing the feature service

    Returns:
        str: A serialized protobuf for a Tecton Feature Service. Also includes all objects this FS depends on, like their FeatureViews etc.

    Raises:
        Exception: If the feature service is not found or other errors occur
    """
    try:

        _log(f"Getting feature service configuration for {name} in workspace {workspace}")

        import tecton
        fs = tecton.get_feature_service(name=name, workspace=workspace)

        fs_spec = str(fs._feature_set_config)
        spec_str = f"""
        Feature Service Proto:

        {fs_spec}

        """

        return spec_str
    except Exception as e:
        _err(f"Failed to get feature view definition: {str(e)}")
        return ""


def get_feature_view_configuration(name: str, workspace: str) -> str:
    """
    Get the entire definition of a feature view from the Tecton cluster.

    Args:
        name: The name of the feature view to retrieve
        workspace: The workspace containing the feature view

    Returns:
        str: A serialized protobuf for a Tecton Feature View, defining metadata, schema, pipeline, and storage. Also includes all objects this FV depends on.

    Raises:
        Exception: If the feature view is not found or other errors occur
    """
    try:

        _log(f"Getting feature view configuration for {name} in workspace {workspace}")

        import tecton
        fv = tecton.get_feature_view(name=name, workspace=workspace)


        fv_spec = str(fv._feature_definition) # str(fv._spec)
        dependent_specs = '\n'.join(str(k) for k in fv._get_dependent_specs())
        spec_str = f"""
        Feature View Proto:

        {fv_spec}

        Proto of all objects this FV depends on (you will see references in the Feature View Proto above to these objects):

        {dependent_specs}

        """

        return spec_str
    except Exception as e:
        _err(f"Failed to get feature view definition: {str(e)}")
        return ""


def get_feature_view_code(name: str, workspace: str) -> str:
    """
    Get the code definition of a feature view from the Tecton cluster.
    This essentially gets the transformation using the feature view name and assumes its the same name as transformation name which works in most cases.

    Args:
        name: The name of the feature view to retrieve
        workspace: The workspace containing the feature view

    Returns:
        str: The Python code definition of the feature view

    Raises:
        Exception: If the feature view is not found or other errors occur
    """
    try:
        request = GetTransformationRequest(
            name=name,
            workspace=workspace,
            run_object_version_check=not conf.get_bool("SKIP_OBJECT_VERSION_CHECK"),
        )
        response = metadata_service.instance().GetTransformation(request)
        fco_container = FcoContainer.from_proto(response.fco_container)
        transformation_spec = fco_container.get_single_root()

        if transformation_spec is None:
            msg = f"Transformation '{name}' not found in workspace '{workspace}'. Try running `list_feature_views()` to view all registered feature views."
            raise ValueError(msg)

        # Validate that all required fields are present
        if not hasattr(transformation_spec, "validation_args"):
            raise ValueError("Missing validation_args in transformation_spec")
        if not hasattr(transformation_spec.validation_args, "transformation"):
            raise ValueError("Missing transformation in validation_args")
        if not hasattr(transformation_spec.validation_args.transformation, "args"):
            raise ValueError("Missing args in transformation")
        if not hasattr(
            transformation_spec.validation_args.transformation.args, "user_function"
        ):
            raise ValueError("Missing user_function in args")
        if not hasattr(
            transformation_spec.validation_args.transformation.args.user_function,
            "body",
        ):
            raise ValueError("Missing body in user_function")

        return (
            transformation_spec.validation_args.transformation.args.user_function.body
        )
    except Exception as e:
        _err(f"Failed to get feature view code: {str(e)}")
        return ""


def list_data_sources() -> List[Dict]:
    """
    List all data sources in the currently connected tecton cluster

    Returns:
        List[dict]: A list of dictionaries containing name, description, workspace, and tags for each data source
    """
    try:
        data_sources = []
        workspaces = list_workspaces()

        for workspace in workspaces:
            request = GetAllVirtualDataSourcesRequest(workspace=workspace)
            response = metadata_service.instance().GetAllVirtualDataSources(request)

            for data_source in response.virtual_data_sources:
                if data_source.fco_metadata.name:
                    data_sources.append(
                        {
                            "name": data_source.fco_metadata.name,
                            "description": data_source.fco_metadata.description,
                            "workspace": workspace,
                            "tags": dict(data_source.fco_metadata.tags),
                        }
                    )

        return sorted(data_sources, key=lambda x: x["name"])
    except Exception as e:
        _err(f"Failed to list data sources: {str(e)}")
        return []


def list_entities() -> List[Dict]:
    """
    List all entities in the currently connected tecton cluster

    Returns:
        List[dict]: A list of dictionaries containing name, description, workspace, and tags for each entity
    """
    try:
        entities = []
        workspaces = list_workspaces()

        for workspace in workspaces:
            request = GetAllEntitiesRequest(workspace=workspace)
            response = metadata_service.instance().GetAllEntities(request)

            for entity in response.entities:
                if entity.fco_metadata.name:
                    entities.append(
                        {
                            "name": entity.fco_metadata.name,
                            "description": entity.fco_metadata.description,
                            "workspace": workspace,
                            "tags": dict(entity.fco_metadata.tags),
                        }
                    )

        return sorted(entities, key=lambda x: x["name"])
    except Exception as e:
        _err(f"Failed to list entities: {str(e)}")
        return []
