"""Address object models and utilities for SCM CLI."""

import json
import logging
from typing import Any, Dict, List, Optional, TypeVar

from pydantic import BaseModel
from scm.client import ScmClient
from scm.exceptions import NotFoundError
from scm.models.objects import (
    AddressCreateModel,
    AddressUpdateModel,
    AddressResponseModel,
)

from scm_cli.utils.decorators import timeit, retry

# Type for Pydantic models
T = TypeVar('T')

# Use child logger from the root logger
logger = logging.getLogger("scm_cli.cli.object.address_object.models")

# Common type mappings
CLI_TO_SDK_TYPE = {"ip-netmask": "ip", "ip-range": "range", "fqdn": "fqdn"}
SDK_TO_CLI_TYPE = {"ip": "ip-netmask", "range": "ip-range", "fqdn": "fqdn"}


# CLI-specific models based on Pydantic
class AddressObjectCLI(BaseModel):
    """CLI representation of an address object."""

    name: str
    type: str
    value: str
    description: Optional[str] = None
    tag: Optional[List[str]] = None
    folder: str
    id: Optional[str] = None


# Exception classes
class ValidationError(Exception):
    """Exception raised for address object validation errors."""

    pass


class APIError(Exception):
    """Exception raised for API-related errors."""

    pass


class ResourceNotFoundError(Exception):
    """Exception raised when a resource is not found."""

    pass


def get_attribute_safely(obj: Any, attr_name: str, default=None) -> Any:
    """Safely get an attribute from an object.

    Args:
        obj: Object to get attribute from
        attr_name: Name of the attribute
        default: Default value if attribute doesn't exist

    Returns:
        Attribute value or default
    """
    if hasattr(obj, attr_name):
        value = getattr(obj, attr_name)
        # Handle enum values
        if hasattr(value, "value"):
            return value.value
        return value
    return default


def serialize_model(model: Any) -> Dict[str, Any]:
    """Serialize a Pydantic model for caching.
    
    Args:
        model: Pydantic model to serialize
        
    Returns:
        Dictionary representation suitable for JSON serialization
    """
    if hasattr(model, "model_dump_json"):
        # Pydantic v2
        json_str = model.model_dump_json(exclude_unset=True, exclude_none=True)
        return {
            "__pydantic_serialized__": True,
            "model_name": model.__class__.__name__,
            "data": json.loads(json_str)
        }
    else:
        # Not a Pydantic model, try to convert to dict directly
        logger.warning(f"Object {model} isn't a standard Pydantic model, trying fallback serialization")
        if hasattr(model, "__dict__"):
            return {
                "__pydantic_serialized__": False,
                "data": model.__dict__
            }
        # Last resort
        return {"__pydantic_serialized__": False, "data": str(model)}


def deserialize_model(serialized_data: Dict[str, Any]) -> Any:
    """Deserialize cached data back to model or dictionary.
    
    Args:
        serialized_data: Data previously serialized with serialize_model
        
    Returns:
        Reconstructed model or dictionary
    """
    if not isinstance(serialized_data, dict) or "__pydantic_serialized__" not in serialized_data:
        # Not our serialized format, return as is
        return serialized_data
    
    is_pydantic = serialized_data.get("__pydantic_serialized__", False)
    data = serialized_data.get("data", {})
    model_name = serialized_data.get("model_name", "")
    
    if not is_pydantic or not model_name:
        # Not a Pydantic model, return the data directly
        return data
    
    # Try to reconstruct the model
    # First try imported models
    if model_name == "AddressResponseModel":
        try:
            return AddressResponseModel.model_validate(data)
        except Exception as e:
            logger.warning(f"Failed to deserialize {model_name}: {e}")
    
    # Return data as dictionary if model reconstruction fails
    return data


class AddressObjectAPI:
    """API for address object operations."""

    def __init__(self, client: ScmClient, cache_manager=None):
        """Initialize the address object API.

        Args:
            client: Initialized SCM client
            cache_manager: Optional API cache manager
        """
        self.client = client
        self.address = client.address
        self.cache_manager = cache_manager
        self.cache_ttl = 300  # Default TTL of 5 minutes

    @timeit
    def list_objects(
        self, folder: str, filter_criteria: Optional[Dict[str, str]] = None
    ) -> List[Any]:
        """List address objects in a folder.

        Args:
            folder: Folder to list objects from
            filter_criteria: Optional filter criteria

        Returns:
            List of address objects as Pydantic models

        Raises:
            APIError: If API request fails
        """
        try:
            # Try to get from cache first
            if not filter_criteria and self.cache_manager:
                cache_key = "address/list"
                cache_params = {"folder": folder}
                
                # Try to get from cache
                cached_result = self.cache_manager.get_cached_response(
                    cache_key, cache_params
                )
                
                if cached_result:
                    logger.debug(f"Using cached address list for folder '{folder}'")
                    # Deserialize each model in the list
                    deserialized_addresses = []
                    for addr_data in cached_result:
                        deserialized_addresses.append(deserialize_model(addr_data))
                    return deserialized_addresses
            
            # Get address objects from the API
            addresses = self.address.list(folder=folder)
            
            # Cache the result if we have a cache manager and no filters
            if not filter_criteria and self.cache_manager:
                # Serialize each model in the list for JSON compatibility
                serialized_addresses = [serialize_model(addr) for addr in addresses]
                
                logger.debug(f"Caching address list for folder '{folder}'")
                self.cache_manager.cache_response(
                    "address/list", 
                    {"folder": folder}, 
                    serialized_addresses,
                    self.cache_ttl
                )

            # Apply filters if provided
            if filter_criteria:
                filtered_result = []
                for addr in addresses:
                    match = True

                    # Apply filters - work directly with attributes
                    for key, value in filter_criteria.items():
                        if key == "name":
                            name_attr = get_attribute_safely(addr, "name", "")
                            if value.lower() not in name_attr.lower():
                                match = False
                                break
                        elif key == "type":
                            # Get type from model
                            addr_type = get_attribute_safely(addr, "type", None)
                            if addr_type:
                                # Convert for comparison
                                cli_type = SDK_TO_CLI_TYPE.get(addr_type, addr_type)
                                if value.lower() != cli_type.lower():
                                    match = False
                                    break
                            else:
                                match = False
                                break
                        elif key == "value":
                            # Check in all possible value fields
                            value_fields = ["ip_netmask", "ip_range", "fqdn"]
                            value_match = False
                            for field in value_fields:
                                field_value = get_attribute_safely(addr, field, None)
                                if (
                                    field_value
                                    and value.lower() in str(field_value).lower()
                                ):
                                    value_match = True
                                    break
                            if not value_match:
                                match = False
                                break
                        elif key == "tag":
                            tags = get_attribute_safely(addr, "tag", []) or []
                            if not any(value.lower() in tag.lower() for tag in tags):
                                match = False
                                break

                    if match:
                        filtered_result.append(addr)

                return filtered_result

            return addresses

        except Exception as e:
            raise APIError(f"Failed to list address objects: {str(e)}")

    @timeit
    def get_object(self, folder: str, name: str) -> Optional[Any]:
        """Get an address object by name.

        Args:
            folder: Folder containing the object
            name: Name of the object

        Returns:
            Address object (Pydantic model) or None if not found

        Raises:
            APIError: If API request fails
        """
        try:
            # Try to get from cache if we have a cache manager
            if self.cache_manager:
                cache_key = "address/fetch"
                cache_params = {"folder": folder, "name": name}
                
                # Try to get from cache
                cached_result = self.cache_manager.get_cached_response(
                    cache_key, cache_params
                )
                
                if cached_result:
                    logger.debug(f"Using cached address object '{name}' from folder '{folder}'")
                    # Deserialize the model
                    return deserialize_model(cached_result)
            
            # Use fetch if available
            if hasattr(self.address, "fetch") and callable(
                getattr(self.address, "fetch")
            ):
                try:
                    # Use the retry decorator for API operations that might fail intermittently
                    @retry(max_attempts=3, delay=0.5)
                    def fetch_with_retry():
                        return self.address.fetch(folder=folder, name=name)
                    
                    obj = fetch_with_retry()
                    
                    # Cache the result if we have a cache manager
                    if obj and self.cache_manager:
                        # Serialize the model for JSON compatibility
                        serialized_obj = serialize_model(obj)
                        
                        logger.debug(f"Caching address object '{name}' from folder '{folder}'")
                        self.cache_manager.cache_response(
                            "address/fetch", 
                            {"folder": folder, "name": name}, 
                            serialized_obj,
                            self.cache_ttl
                        )
                        
                    return obj
                except NotFoundError:
                    return None
                except Exception as e:
                    logger.debug(f"Fetch method failed: {str(e)}, trying alternatives")

            # Use list and filter if fetch not available
            addresses = self.address.list(folder=folder)
            for addr in addresses:
                if get_attribute_safely(addr, "name", None) == name:
                    # Cache the result if we have a cache manager
                    if self.cache_manager:
                        # Serialize the model for JSON compatibility
                        serialized_obj = serialize_model(addr)
                        
                        logger.debug(f"Caching address object '{name}' from folder '{folder}'")
                        self.cache_manager.cache_response(
                            "address/fetch", 
                            {"folder": folder, "name": name}, 
                            serialized_obj,
                            self.cache_ttl
                        )
                    
                    return addr

            return None

        except Exception as e:
            raise APIError(f"Failed to get address object: {str(e)}")

    @timeit
    def create_object(self, folder: str, data: Dict[str, Any]) -> Any:
        """Create a new address object.

        Args:
            folder: Folder to create object in
            data: Object data

        Returns:
            Created address object as Pydantic model

        Raises:
            ValidationError: If object data is invalid
            APIError: If API request fails
        """
        try:
            # Ensure folder is set
            data["folder"] = folder

            # Convert CLI type to SDK type if needed
            if "type" in data:
                type_value = data["type"]
                data["type"] = CLI_TO_SDK_TYPE.get(type_value, type_value)

            # Handle value field
            if "value" in data:
                value = data.pop("value")

                # If type is specified, use it
                if "type" in data:
                    addr_type = data.pop("type")
                # If not, try to infer from value
                else:
                    # Determine type from value format
                    if "/" in value:  # Looks like a CIDR notation
                        addr_type = "ip"
                    elif "-" in value:  # Looks like a range
                        addr_type = "range"
                    elif any(
                        c.isalpha() for c in value
                    ):  # Contains letters, likely FQDN
                        addr_type = "fqdn"
                    else:  # Default to IP if we can't determine
                        addr_type = "ip"
                    logger.debug(
                        f"Inferred type '{addr_type}' from value format: {value}"
                    )

                # Set the appropriate field based on type
                if addr_type == "ip":
                    data["ip_netmask"] = value
                elif addr_type == "range":
                    data["ip_range"] = value
                elif addr_type == "fqdn":
                    data["fqdn"] = value
                else:
                    raise ValidationError(f"Invalid address type: {addr_type}")

            # Create the object with Pydantic v2 model and model_dump
            try:
                # Define a retry-enabled creation function for API stability
                @retry(max_attempts=2, delay=1.0)
                def create_with_retry(data_dict):
                    # Create model and convert to dict using model_dump
                    model = AddressCreateModel(**data_dict)
                    model_dict = model.model_dump(exclude_unset=True, exclude_none=True)
                    return self.address.create(model_dict)
                
                # Call the retry-wrapped function
                obj = create_with_retry(data)
                
                # Invalidate cache entries after a create operation
                if self.cache_manager:
                    # Invalidate the list cache for this folder
                    self.cache_manager.invalidate_cache("address/list", {"folder": folder})
                    logger.debug(f"Invalidated address list cache for folder '{folder}'")
                
                return obj
            except Exception as e:
                # This will be reached if all retry attempts failed
                logger.error(f"All creation attempts failed: {str(e)}")
                raise

        except Exception as e:
            if "already exists" in str(e) or "not unique" in str(e):
                raise ValidationError(
                    f"Address object with name '{data.get('name')}' already exists"
                )
            raise APIError(f"Failed to create address object: {str(e)}")

    @timeit
    def update_object(self, folder: str, name: str, data: Dict[str, Any]) -> Any:
        """Update an existing address object.

        Args:
            folder: Folder containing the object
            name: Name of the object
            data: Updated object data

        Returns:
            Updated address object as Pydantic model

        Raises:
            ResourceNotFoundError: If object not found
            ValidationError: If object data is invalid
            APIError: If API request fails
        """
        try:
            # Get existing object (as Pydantic model)
            existing_obj = self.get_object(folder, name)
            if not existing_obj:
                raise ResourceNotFoundError(
                    f"Address object '{name}' not found in folder '{folder}'"
                )

            # Build update dictionary from existing object attributes
            update_data = {}
            # Extract key attributes from existing object
            for attr_name in [
                "name",
                "folder",
                "id",
                "type",
                "description",
                "tag",
                "ip_netmask",
                "ip_range",
                "fqdn",
            ]:
                value = get_attribute_safely(existing_obj, attr_name, None)
                if value is not None:
                    update_data[attr_name] = value

            # Update with new data
            update_data.update(data)

            # Ensure name and folder are set
            update_data["name"] = name
            update_data["folder"] = folder

            # Convert CLI type to SDK type if needed
            if "type" in update_data:
                type_value = update_data["type"]
                update_data["type"] = CLI_TO_SDK_TYPE.get(type_value, type_value)

            # Handle value field if present in new data
            if "value" in data:
                value = data["value"]

                # Try to determine address type
                # First try using the provided type
                if "type" in update_data:
                    addr_type = update_data.pop("type")
                    addr_type = CLI_TO_SDK_TYPE.get(addr_type, addr_type)
                # Next try getting type from existing object
                else:
                    # Try to infer from existing value fields
                    if get_attribute_safely(existing_obj, "ip_netmask", None):
                        addr_type = "ip"
                    elif get_attribute_safely(existing_obj, "ip_range", None):
                        addr_type = "range"
                    elif get_attribute_safely(existing_obj, "fqdn", None):
                        addr_type = "fqdn"
                    # Try to infer from value format as last resort
                    else:
                        # Determine type from value format
                        if "/" in value:  # Looks like a CIDR notation
                            addr_type = "ip"
                        elif "-" in value:  # Looks like a range
                            addr_type = "range"
                        elif any(
                            c.isalpha() for c in value
                        ):  # Contains letters, likely FQDN
                            addr_type = "fqdn"
                        else:  # Default to IP if we can't determine
                            addr_type = "ip"
                        logger.debug(
                            f"Inferred type '{addr_type}' from value format: {value}"
                        )

                # Set the appropriate field based on type
                if addr_type == "ip":
                    update_data["ip_netmask"] = value
                    update_data.pop("ip_range", None)
                    update_data.pop("fqdn", None)
                elif addr_type == "range":
                    update_data["ip_range"] = value
                    update_data.pop("ip_netmask", None)
                    update_data.pop("fqdn", None)
                elif addr_type == "fqdn":
                    update_data["fqdn"] = value
                    update_data.pop("ip_netmask", None)
                    update_data.pop("ip_range", None)
                else:
                    raise ValidationError(f"Invalid address type: {addr_type}")

                # Log what we determined
                logger.debug(f"Using address type '{addr_type}' for value '{value}'")

                # Remove the value field as we've processed it
                update_data.pop("value", None)

            # Log what we're about to update with
            logger.debug(f"Updating address object with data: {update_data}")

            # Update the object with Pydantic v2 model and model_dump
            # Define a retry-enabled update function for API stability
            @retry(max_attempts=2, delay=1.0)
            def update_with_retry(update_dict):
                # Create model and convert to dict using model_dump
                model = AddressUpdateModel(**update_dict)
                # model_dict = model.model_dump(exclude_unset=True, exclude_none=True)
                return self.address.update(model)
            
            # Call the retry-wrapped function
            obj = update_with_retry(update_data)
            
            # Invalidate cache entries after update
            if self.cache_manager:
                # Invalidate the list cache for this folder
                self.cache_manager.invalidate_cache("address/list", {"folder": folder})
                # Invalidate the specific object cache
                self.cache_manager.invalidate_cache("address/fetch", {"folder": folder, "name": name})
                logger.debug(f"Invalidated cache for address object '{name}' in folder '{folder}'")
            
            return obj

        except NotFoundError:
            raise ResourceNotFoundError(
                f"Address object '{name}' not found in folder '{folder}'"
            )
        except Exception as e:
            if "not found" in str(e).lower():
                raise ResourceNotFoundError(
                    f"Address object '{name}' not found in folder '{folder}'"
                )
            raise APIError(f"Failed to update address object: {str(e)}")

    @timeit
    def delete_object(self, folder: str, name: str) -> None:
        """Delete an address object.

        Args:
            folder: Folder containing the object
            name: Name of the object

        Raises:
            ResourceNotFoundError: If object not found
            APIError: If API request fails
        """
        try:
            # Get existing object to get its ID
            existing_obj = self.get_object(folder, name)
            if not existing_obj:
                raise ResourceNotFoundError(
                    f"Address object '{name}' not found in folder '{folder}'"
                )

            # Get the ID from the object
            obj_id = get_attribute_safely(existing_obj, "id", None)

            if not obj_id:
                raise APIError(f"Address object '{name}' has no ID")

            # Delete the object with retry
            @retry(max_attempts=2, delay=1.0)
            def delete_with_retry(id_to_delete):
                return self.address.delete(id_to_delete)
                
            delete_with_retry(obj_id)
            
            # Invalidate cache entries after delete
            if self.cache_manager:
                # Invalidate the list cache for this folder
                self.cache_manager.invalidate_cache("address/list", {"folder": folder})
                # Invalidate the specific object cache
                self.cache_manager.invalidate_cache("address/fetch", {"folder": folder, "name": name})
                logger.debug(f"Invalidated cache for address object '{name}' in folder '{folder}'")

        except NotFoundError:
            raise ResourceNotFoundError(
                f"Address object '{name}' not found in folder '{folder}'"
            )
        except Exception as e:
            if "not found" in str(e).lower():
                raise ResourceNotFoundError(
                    f"Address object '{name}' not found in folder '{folder}'"
                )
            raise APIError(f"Failed to delete address object: {str(e)}")
