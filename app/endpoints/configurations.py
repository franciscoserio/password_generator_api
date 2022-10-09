from typing import List
from fastapi import Depends, APIRouter, Request, status

from app.schemas import Configuration, ConfigurationCreate, ConfigurationUpdate
from app.utils.data_handlers import ConfigurationDataHandler
from app.utils import get_logged_user_instance
from app.utils.exceptions import NotFoundException

router = APIRouter(
    dependencies=[Depends(get_logged_user_instance)],
)

# create
@router.post(
    "/api/admin/configurations/",
    status_code=status.HTTP_201_CREATED,
    response_model=Configuration,
)
def create_configurations(request: Request, configuration: ConfigurationCreate):
    config_data_handler = ConfigurationDataHandler(request.state.db, request.state.user)
    return config_data_handler.create_configuration(configuration=configuration)


# list
@router.get(
    "/api/admin/configurations/",
    status_code=status.HTTP_200_OK,
    response_model=List[Configuration],
)
def list_configurations(request: Request):
    config_data_handler = ConfigurationDataHandler(request.state.db, request.state.user)
    return config_data_handler.get_all_configs


# update
@router.patch(
    "/api/admin/configurations/{id}/",
    status_code=status.HTTP_201_CREATED,
    response_model=Configuration,
)
def update_configuration(request: Request, id: int, configuration: ConfigurationUpdate):
    config_data_handler = ConfigurationDataHandler(request.state.db, request.state.user)
    configuration_update = configuration.dict(exclude_unset=True)
    if updated_config := config_data_handler.update_configuration_by_id(
        id, configuration_update
    ):
        return updated_config
    raise NotFoundException("configuration not found")


# retrieve
@router.get(
    "/api/admin/configurations/{id}/",
    status_code=status.HTTP_200_OK,
    response_model=Configuration,
)
def retrieve_configuration(request: Request, id: int):
    config_data_handler = ConfigurationDataHandler(request.state.db, request.state.user)
    if config := config_data_handler.get_config_by_id(id):
        return config
    raise NotFoundException("configuration not found")


# delete
@router.delete(
    "/api/admin/configurations/{id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_configuration(request: Request, id: int):
    config_data_handler = ConfigurationDataHandler(request.state.db, request.state.user)
    if config_data_handler.delete_configuration_by_id(id):
        return
    raise NotFoundException("configuration not found")
