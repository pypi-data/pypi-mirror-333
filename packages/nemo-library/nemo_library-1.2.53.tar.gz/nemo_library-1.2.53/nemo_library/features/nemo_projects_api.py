import re
import pandas as pd
import requests
import json
from typing import TypeVar

from nemo_library.model.dependency_tree import DependencyTree
from nemo_library.utils.config import Config
from nemo_library.utils.utils import (
    log_error,
)


def getProjectList(
    config: Config,
) -> pd.DataFrame:
    """
    Fetches the list of projects from the NEMO API and returns it as a pandas DataFrame.
    Logs an error message if the API request fails.

    Args:
        config (Config): Configuration object containing methods for generating headers
                         and the NEMO API URL.

    Returns:
        pandas.DataFrame: A DataFrame containing the normalized project data.

    Logs:
        Error: If the API request fails (e.g., non-200 status code).
    """

    headers = config.connection_get_headers()

    response = requests.get(
        config.get_config_nemo_url() + "/api/nemo-projects/projects", headers=headers
    )
    if response.status_code != 200:
        log_error(
            f"request failed. Status: {response.status_code}, error: {response.text}"
        )
    resultjs = json.loads(response.text)
    df = pd.json_normalize(resultjs)
    return df


def getProjectID(
    config: Config,
    projectname: str,
) -> str:
    """
    Retrieves the unique project ID for a given project name.

    Args:
        config (Config): Configuration object containing connection details.
        projectname (str): The name of the project for which to retrieve the ID.

    Returns:
        str: The unique identifier (ID) of the specified project.

    Raises:
        ValueError: If the project name cannot be uniquely identified in the project list.

    Notes:
        - This function relies on the `getProjectList` function to fetch the full project list.
        - If multiple or no entries match the given project name, an error is logged, and the first matching ID is returned.
    """
    df = getProjectList(config)
    crmproject = df[df["displayName"] == projectname]
    if len(crmproject) != 1:
        return None
    project_id = crmproject["id"].to_list()[0]
    return project_id


def getProjectProperty(
    config: Config,
    projectname: str,
    propertyname: str,
) -> str:
    """
    Retrieves a specific property value of a given project from the server.

    Args:
        config (Config): Configuration object containing connection details and headers.
        projectname (str): The name of the project for which the property is requested.
        propertyname (str): The name of the property to retrieve.

    Returns:
        str: The value of the specified property, with leading and trailing quotation marks removed.

    Raises:
        RuntimeError: If the request to fetch the project property fails (non-200 status code).

    Notes:
        - This function first fetches the project ID using the `getProjectID` function.
        - Constructs an endpoint URL using the project ID and property name.
        - Sends an HTTP GET request to fetch the property value.
        - Logs an error if the request fails and raises an exception.
    """
    project_id = getProjectID(config, projectname)

    headers = config.connection_get_headers()

    ENDPOINT_URL = (
        config.get_config_nemo_url()
        + "/api/nemo-persistence/ProjectProperty/project/{projectId}/{request}".format(
            projectId=project_id, request=propertyname
        )
    )

    response = requests.get(ENDPOINT_URL, headers=headers)

    if response.status_code != 200:
        log_error(
            f"request failed. Status: {response.status_code}, error: {response.text}"
        )

    return response.text[1:-1]  # cut off leading and trailing "


def createProject(
    config: Config,
    projectname: str,
    description: str,
) -> None:
    """
    Creates a new project with the specified name and description in the NEMO system.

    Args:
        config (Config): Configuration object containing connection details and headers.
        projectname (str): The display name for the new project.
        description (str): A brief description of the project.

    Returns:
        None

    Raises:
        RuntimeError: If the HTTP POST request to create the project fails (non-201 status code).

    Notes:
        - Generates a table name for the project by converting the project name to uppercase,
          replacing invalid characters with underscores, and ensuring it starts with "PROJECT_".
        - Sends a POST request to the project creation endpoint with the required metadata.
        - Logs an error if the request fails and raises an exception.
    """

    headers = config.connection_get_headers()
    ENDPOINT_URL = (
        config.get_config_nemo_url() + "/api/nemo-persistence/metadata/Project"
    )
    table_name = re.sub(r"[^A-Z0-9_]", "_", projectname.upper()).strip()
    if not table_name.startswith("PROJECT_"):
        table_name = "PROJECT_" + table_name

    data = {
        "autoDataRefresh": True,
        "displayName": projectname,
        "description": description,
        "type": "IndividualData",
        "status": "Active",
        "tableName": table_name,
        "importErrorType": "NoError",
        "id": "",
        "s3DataSourcePath": "",
        "showInitialConfiguration": False,
        "tenant": config.get_tenant(),
        "type": "0",
    }

    response = requests.post(ENDPOINT_URL, headers=headers, json=data)

    if response.status_code != 201:
        log_error(
            f"Request failed. Status: {response.status_code}, error: {response.text}"
        )


def setProjectMetaData(
    config: Config,
    projectname: str,
    processid_column: str = None,
    processdate_column: str = None,
    corpcurr_value: str = None,
) -> None:
    """
    Updates metadata for a specific project, including process ID, process date, and corporate currency value.

    Args:
        config (Config): Configuration object containing connection details and headers.
        projectname (str): The name of the project to update metadata for.
        processid_column (str, optional): The column name representing the process ID.
        processdate_column (str, optional): The column name representing the process date.
        corpcurr_value (str, optional): The corporate currency value to set.

    Returns:
        None

    Raises:
        RuntimeError: If the HTTP PUT request to update the metadata fails (non-200 status code).

    Notes:
        - Fetches the project ID using `getProjectID`.
        - Constructs a metadata payload based on the provided parameters.
        - Sends an HTTP PUT request to update the project's business process metadata.
        - Logs an error if the request fails and raises an exception.
    """

    headers = config.connection_get_headers()
    projectID = getProjectID(config, projectname)

    data = {}
    if corpcurr_value:
        data["corporateCurrencyValue"] = corpcurr_value
    if processdate_column:
        data["processDateColumnName"] = processdate_column
    if processid_column:
        data["processIdColumnName"] = processid_column

    ENDPOINT_URL = config.get_config_nemo_url() + "/api/nemo-persistence/ProjectProperty/project/{projectId}/BusinessProcessMetadata".format(
        projectId=projectID
    )

    response = requests.put(ENDPOINT_URL, headers=headers, json=data)
    if response.status_code != 200:
        log_error(
            f"Request failed. Status: {response.status_code}, error: {response.text}"
        )


def deleteProject(config: Config, projectname: str) -> None:
    """
    Deletes a specified project from the NEMO system.

    Args:
        config (Config): Configuration object containing connection details and headers.
        projectname (str): The name of the project to delete.

    Returns:
        None

    Raises:
        RuntimeError: If the HTTP DELETE request to delete the project fails (non-204 status code).

    Notes:
        - Fetches the project ID using `getProjectID`.
        - Sends an HTTP DELETE request to the endpoint associated with the project's metadata.
        - Logs an error if the request fails and raises an exception.
    """

    headers = config.connection_get_headers()
    projectID = getProjectID(config, projectname)
    if projectID:
        response = requests.delete(
            (
                config.get_config_nemo_url()
                + "/api/nemo-persistence/metadata/Project/{id}".format(id=projectID)
            ),
            headers=headers,
        )

        if response.status_code != 204:
            log_error(
                f"Request failed. Status: {response.status_code}, error: {response.text}"
            )


def getDependencyTree(config: Config, id: str) -> DependencyTree:
    # Initialize request
    headers = config.connection_get_headers()
    data = {"id": id}

    response = requests.get(
        f"{config.get_config_nemo_url()}/api/nemo-persistence/metadata/Metrics/DependencyTree",
        headers=headers,
        params=data,
    )

    if response.status_code != 200:
        log_error(
            f"{config.get_config_nemo_url()}/api/nemo-persistence/metadata/Metrics/DependencyTree",
        )
        return None

    data = json.loads(response.text)
    return DependencyTree.from_dict(data)


def createImportedColumns(config: Config, projectname: str, columns: dict) -> None:

    # add generic data
    project_id = getProjectID(config, projectname)
    tenant = config.get_tenant()
    for col in columns:
        col["tenant"] = tenant
        col["projectId"] = project_id
        col["unit"] = col["unit"] if "unit" in col.keys() else ""

    # initialize reqeust
    headers = config.connection_get_headers()

    response = requests.post(
        config.get_config_nemo_url()
        + "/api/nemo-persistence/metadata/Columns/project/{projectId}/Columns".format(
            projectId=project_id
        ),
        headers=headers,
        json=columns,
    )
    if response.status_code != 200:
        raise Exception(
            f"request failed. Status: {response.status_code}, error: {response.text}"
        )


def createImportedColumn(
    config: Config,
    projectname: str,
    displayName: str,
    dataType: str,
    importName: str = None,
    internalName: str = None,
    description: str = None,
) -> None:
    """
    Creates a new imported column for a specified project in the NEMO system.

    Args:
        config (Config): Configuration object containing connection details and headers.
        projectname (str): The name of the project to which the column will be added.
        displayName (str): The display name of the column.
        dataType (str): The data type of the column (e.g., "String", "Integer").
        importName (str, optional): The name used for importing data into the column. Defaults to a sanitized version of `displayName`.
        internalName (str, optional): The internal system name of the column. Defaults to a sanitized version of `displayName`.
        description (str, optional): A description of the column. Defaults to an empty string.

    Returns:
        None

    Raises:
        RuntimeError: If the HTTP POST request to create the column fails (non-201 status code).

    Notes:
        - Generates `importName` and `internalName` from `displayName` if not explicitly provided.
        - Sends an HTTP POST request to the appropriate endpoint with metadata for the new column.
        - Logs and raises an exception if the request fails.
    """
    # initialize reqeust
    headers = config.connection_get_headers()
    project_id = getProjectID(config, projectname)

    if not importName:
        importName = re.sub(r"[^a-z0-9_]", "_", displayName.lower()).strip()
    if not internalName:
        internalName = re.sub(r"[^a-z0-9_]", "_", displayName.lower()).strip()
    if not description:
        description = ""

    data = {
        "categorialType": True,
        "columnType": "ExportedColumn",
        "containsSensitiveData": False,
        "dataType": dataType,
        "description": description,
        "displayName": displayName,
        "importName": importName,
        "internalName": internalName,
        "id": "",
        "unit": "",
        "tenant": config.get_tenant(),
        "projectId": project_id,
    }

    response = requests.post(
        config.get_config_nemo_url() + "/api/nemo-persistence/metadata/Columns",
        headers=headers,
        json=data,
    )
    if response.status_code != 201:
        raise Exception(
            f"request failed. Status: {response.status_code}, error: {response.text}"
        )


def createOrUpdateRule(
    config: Config,
    projectname: str,
    displayName: str,
    ruleSourceInternalName: str,
    internalName: str = None,
    ruleGroup: str = None,
    description: str = None,
) -> None:
    """
    Creates or updates a rule in the specified project within the NEMO system.

    Args:
        config (Config): Configuration object containing connection details and headers.
        projectname (str): The name of the project where the rule will be created or updated.
        displayName (str): The display name of the rule.
        ruleSourceInternalName (str): The internal name of the rule source that the rule depends on.
        internalName (str, optional): The internal system name of the rule. Defaults to a sanitized version of `displayName`.
        ruleGroup (str, optional): The group to which the rule belongs. Defaults to None.
        description (str, optional): A description of the rule. Defaults to an empty string.

    Returns:
        None

    Raises:
        RuntimeError: If any HTTP request fails (non-200/201 status code).

    Notes:
        - Fetches the project ID using `getProjectID`.
        - Retrieves the list of existing rules in the project to check if the rule already exists.
        - If the rule exists, updates it with the new data using a PUT request.
        - If the rule does not exist, creates a new rule using a POST request.
        - Logs errors and raises exceptions for failed requests.
    """
    headers = config.connection_get_headers()
    project_id = getProjectID(config, projectname)

    if not internalName:
        internalName = re.sub(r"[^a-z0-9_]", "_", displayName.lower()).strip()

    # load list of rules first
    response = requests.get(
        config.get_config_nemo_url()
        + "/api/nemo-persistence/metadata/Rule/project/{projectId}/rules".format(
            projectId=project_id
        ),
        headers=headers,
    )
    resultjs = json.loads(response.text)
    df = pd.json_normalize(resultjs)
    if df.empty:
        internalNames = []
    else:
        internalNames = df["internalName"].to_list()
    rule_exist = internalName in internalNames

    data = {
        "active": True,
        "projectId": project_id,
        "displayName": displayName,
        "internalName": internalName,
        "tenant": config.get_tenant(),
        "description": description if description else "",
        "ruleGroup": ruleGroup,
        "ruleSourceInternalName": ruleSourceInternalName,
    }

    if rule_exist:
        df_filtered = df[df["internalName"] == internalName].iloc[0]
        data["id"] = df_filtered["id"]
        response = requests.put(
            config.get_config_nemo_url()
            + "/api/nemo-persistence/metadata/Rule/{id}".format(id=df_filtered["id"]),
            headers=headers,
            json=data,
        )
        if response.status_code != 200:
            log_error(
                f"Request failed. Status: {response.status_code}, error: {response.text}"
            )
    else:
        response = requests.post(
            config.get_config_nemo_url() + "/api/nemo-persistence/metadata/Rule",
            headers=headers,
            json=data,
        )
        if response.status_code != 201:
            log_error(
                f"Request failed. Status: {response.status_code}, error: {response.text}"
            )
