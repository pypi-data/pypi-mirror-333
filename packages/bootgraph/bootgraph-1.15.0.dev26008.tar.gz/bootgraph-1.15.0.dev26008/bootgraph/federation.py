"""
Module providing helper functions for adding GraphQL Federation support to Graphemy models.
"""
import strawberry
from typing import Union, List, Type, Optional, Callable, Any

def add_federation_key(
    model_class: Type,
    key_fields: Union[str, List[str]],
) -> None:
    """
    Adds federation key configuration to a Graphemy model after it's been defined.
    
    Args:
        model_class: The Graphemy model class to add federation to
        key_fields: Field or list of fields to use as federation key
    
    Example:
        ```python
        class Product(Graphemy, table=True):
            __tablename__ = "product"
            db_id: int = Field(primary_key=True, exclude=True)
            name: str = Field(nullable=False)
            
        # Add federation key after model definition
        add_federation_key(Product, "id")
        
        # Add id resolver separately  
        @strawberry.field(name="id")
        def resolve_product_id(root: Product) -> strawberry.ID:
            return strawberry.ID(str(root.db_id))
            
        # Add resolver to model
        Product.__custom_resolvers__ = [resolve_product_id]
        ```
    """
    model_class.__federation_key__ = key_fields


def id_resolver(
    model_class: Type,
    id_field_name: str = "id",
    db_id_field_name: str = "db_id",
) -> Callable:
    """
    Creates an ID field resolver for a federated entity that maps a database ID to a GraphQL ID.
    
    Args:
        model_class: The model class the resolver is for
        id_field_name: The name of the GraphQL ID field (default: "id")
        db_id_field_name: The name of the database ID field (default: "db_id")
    
    Returns:
        A strawberry field resolver function for the ID field
        
    Example:
        ```python
        class Product(Graphemy, table=True):
            __tablename__ = "product"
            db_id: int = Field(primary_key=True, exclude=True)
            name: str = Field(nullable=False)
            
        # Add federation key
        add_federation_key(Product, "id")
        
        # Create and add id resolver  
        Product.__custom_resolvers__ = [id_resolver(Product)]
        ```
    """
    @strawberry.field(name=id_field_name)
    def resolve_id(root: Any) -> strawberry.ID:
        """Resolves the database ID to a GraphQL ID field."""
        return strawberry.ID(str(getattr(root, db_id_field_name)))
    
    return resolve_id


def setup_federation(
    model_class: Type,
    key_fields: Union[str, List[str]] = "id",
    create_id_resolver: bool = True,
    id_field_name: str = "id",
    db_id_field_name: str = "db_id",
) -> None:
    """
    Comprehensive helper that adds full federation support to a Graphemy model.
    
    This function:
    1. Sets the federation key on the model
    2. Creates an ID field resolver if requested and adds it to custom resolvers
    
    Args:
        model_class: The Graphemy model class to add federation to
        key_fields: Field or list of fields to use as federation key (default: "id")
        create_id_resolver: Whether to create an ID resolver that maps db_id to id (default: True)
        id_field_name: The name of the GraphQL ID field (default: "id")
        db_id_field_name: The name of the database ID field (default: "db_id")
    
    Example:
        ```python
        class Product(Graphemy, table=True):
            __tablename__ = "product"
            db_id: int = Field(primary_key=True, exclude=True)
            name: str = Field(nullable=False)
            
        # Set up federation with one function call
        setup_federation(Product)
        ```
    """
    # Add federation key to model
    add_federation_key(model_class, key_fields)
    
    # Create and add ID resolver if requested
    if create_id_resolver:
        # Only create resolver if id field is among key fields
        key_list = key_fields if isinstance(key_fields, list) else [key_fields]
        if id_field_name in key_list and hasattr(model_class, db_id_field_name):
            resolver = id_resolver(model_class, id_field_name, db_id_field_name)
            
            # Add to custom resolvers or create list if needed
            if not hasattr(model_class, "__custom_resolvers__") or model_class.__custom_resolvers__ is None:
                model_class.__custom_resolvers__ = []
            model_class.__custom_resolvers__.append(resolver) 