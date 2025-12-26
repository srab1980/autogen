import os
import asyncio
from autogenstudio.web.config import settings
from autogenstudio.web.initialization import AppInitializer
from autogenstudio.database import DatabaseManager
from autogenstudio.datamodel import Gallery
from autogenstudio.gallery.builder import create_default_gallery

# Set up environment
os.environ["AUTOGENSTUDIO_DATABASE_URI"] = "sqlite:///autogen04202.db"
os.environ["OPENAI_DEFAULT_MODEL"] = "gpt-5.1"  # Ensure builder uses this

async def update_gallery():
    print(f"Using Database URI: {os.environ['AUTOGENSTUDIO_DATABASE_URI']}")
    
    # Initialize DB Manager
    # We need to find the app root. Assuming current dir is okay or set correctly.
    # Initialize DatabaseManager directly
    db_manager = DatabaseManager(engine_uri=os.environ["AUTOGENSTUDIO_DATABASE_URI"])
    
    user_id = settings.DEFAULT_USER_ID
    print(f"Targeting User ID: {user_id}")
    
    # Get existing gallery
    response = db_manager.get(Gallery, filters={"user_id": user_id})
    
    if not response.status or not response.data:
        print("No existing gallery found. Creating new one from default...")
        gallery_config = create_default_gallery()
        default_gallery = Gallery(user_id=user_id, config=gallery_config.model_dump())
        db_manager.upsert(default_gallery)
        print("Created default gallery.")
        return

    gallery = response.data[0]
    print(f"Found existing gallery ID: {gallery.id}")
    
    # Get new default gallery to extract GPT-5.1
    new_default = create_default_gallery()
    
    # Find GPT-5.1 model in new default
    gpt5_model = None
    # Verify structure of models list
    models_list = new_default.components.models if hasattr(new_default.components, 'models') else []
    
    for model in models_list:
        # Handle config being dict or object
        config = model.config
        model_name = None
        if isinstance(config, dict):
            model_name = config.get("model")
        else:
             model_name = getattr(config, "model", None)
             
        if model_name == "gpt-5.1" or model.label == "OpenAI GPT-5.1":
            gpt5_model = model
            break
            
    if not gpt5_model:
        print("Error: Could not find GPT-5.1 in create_default_gallery(). Check builder.py.")
        return

    print(f"Found new model template: {gpt5_model.label}")
    
    # Check if user already has it
    current_models = gallery.config["components"]["models"] # DB stores as dict in config
    
    exists = False
    for m in current_models:
        # Check label or model name
        m_config = m.get("config", {})
        m_model = m_config.get("model") if isinstance(m_config, dict) else getattr(m_config, "model", None)
        
        if m.get("label") == gpt5_model.label or m_model == "gpt-5.1":
            exists = True
            break
            
    if exists:
        print("Gallery already contains GPT-5.1.")
    else:
        print("Adding GPT-5.1 to gallery...")
        current_models.append(gpt5_model.model_dump())
        gallery.config["components"]["models"] = current_models
        
        # Save
        res = db_manager.upsert(gallery)
        if res.status:
            print("Successfully updated gallery.")
        else:
            print(f"Failed to update gallery: {res.message}")

if __name__ == "__main__":
    asyncio.run(update_gallery())
