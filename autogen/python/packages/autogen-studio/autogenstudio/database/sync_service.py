
from typing import Any, Dict, List, Optional
from loguru import logger
from ..datamodel import Team, Gallery
from .db_manager import DatabaseManager

class ComponentSyncService:
    """
    Service to handle bi-directional synchronization between Gallery components and Team components.
    Uses '_origin' metadata to link components.
    """

    @staticmethod
    def _find_component_in_gallery(gallery_config: Dict, component_type: str, component_id: str) -> Optional[Dict]:
        """Helper to find a component within a gallery config."""
        if not gallery_config or "components" not in gallery_config:
            return None
        
        components = gallery_config["components"]
        # Map component types to the list keys in GalleryComponents
        key_map = {
            "agent": "agents",
            "model": "models",
            "tool": "tools", 
            "termination": "terminations",
            "workbench": "workbenches"
        }
        
        list_key = key_map.get(component_type)
        if not list_key or list_key not in components:
            return None
            
        for comp in components[list_key]:
            # comp is likely a dict or object. accessing as dict
            # ensure we handle if it's pydantic model or dict
            c_id = comp.get("client_id") or comp.get("id") # client_id is often used
            if not c_id and hasattr(comp, "id"):
                 c_id = comp.id
                 
            # If still not found, check if it matches component_id directly (fallback)
            if c_id == component_id:
                return comp
                
        return None

    @staticmethod
    def _update_component_in_gallery(gallery_config: Dict, component_type: str, component_id: str, new_config: Dict) -> bool:
        """Helper to update a component within a gallery config. Modifies in-place."""
        if not gallery_config or "components" not in gallery_config:
            return False
            
        components = gallery_config["components"]
        key_map = {
            "agent": "agents",
            "model": "models",
            "tool": "tools",
            "termination": "terminations",
            "workbench": "workbenches"
        }
        list_key = key_map.get(component_type)
        if not list_key or list_key not in components:
            return False
            
        target_list = components[list_key]
        for i, comp in enumerate(target_list):
             # Handle dict vs object access if needed, but assuming dict for JSON blobs
             c_id = comp.get("id") or comp.get("client_id")
             if c_id == component_id:
                 # Update!
                 # We probably want to keep the ID and Metadata, but update the config fields.
                 # Or just Replace?
                 # Let's replace but preserve ID if missing in new_config (unlikely)
                 target_list[i] = new_config
                 return True
        return False

    @staticmethod
    def sync_team_updates_to_gallery(team: Team, db: DatabaseManager):
        """
        Called when a Team is updated.
        Scans team components for '_origin' metadata and updates corresponding Gallery items.
        """
        try:
            # Team component is a structure that contains agents (participants)
            # We need to traverse the team structure to find agents.
            team_config = team.component
            if not isinstance(team_config, dict):
                team_config = team_config.model_dump()

            if "participants" not in team_config:
                return 

            updated_galleries = set()

            for agent in team_config["participants"]:
                metadata = agent.get("metadata", {})
                origin = metadata.get("_origin")
                
                # Handle stringified JSON (required for strict metadata typing)
                if isinstance(origin, str):
                    try:
                        import json
                        origin = json.loads(origin)
                    except Exception:
                        pass # Treat as invalid or raw string if parse fails

                if origin and isinstance(origin, dict):
                    gallery_id = origin.get("gallery_id")
                    component_id = origin.get("component_id")
                    component_type = origin.get("component_type", "agent") # Default to agent
                    
                    if gallery_id and component_id:
                        # Fetch Gallery
                        response = db.get(Gallery, filters={"id": gallery_id})
                        if response.status and response.data:
                            gallery_item = response.data[0]
                            gallery_config = gallery_item.config
                            if not isinstance(gallery_config, dict):
                                gallery_config = gallery_config.model_dump()
                            
                            # Update the component in the gallery config
                            # Important: "agent" here is the *updated* configuration from the team
                            # We might need to sanitize it or ensure it matches Gallery expectations
                            # e.g. remove _origin from the gallery version? keeping it is harmless.
                            
                            if ComponentSyncService._update_component_in_gallery(gallery_config, component_type, component_id, agent):
                                gallery_item.config = gallery_config
                                db.upsert(gallery_item)
                                updated_galleries.add(gallery_id)
                                logger.info(f"Synced changes from Team {team.id} to Gallery {gallery_id} for component {component_id}")

        except Exception as e:
            logger.error(f"Error syncing team to gallery: {e}")

    @staticmethod
    def sync_gallery_updates_to_teams(gallery: Gallery, db: DatabaseManager):
        """
        Called when a Gallery Item is updated.
        Finds all Teams that use components from this Gallery and updates them.
        """
        try:
            gallery_id = gallery.id
            gallery_config = gallery.config
            if not isinstance(gallery_config, dict):
                gallery_config = gallery_config.model_dump()
            
            # We need to iterate over ALL components in this gallery to see if they are used
            # But efficiently: maybe just iterate over all teams and check their origins?
            # Iterating teams is safer.
            
            # Fetch all teams for this user (or all teams? Probably just user's due to permissions, 
            # but technically a gallery could be public? For now scope to user_id if present)
            filters = {}
            if gallery.user_id:
                filters["user_id"] = gallery.user_id
            
            response = db.get(Team, filters=filters)
            if not response.status or not response.data:
                return

            teams = response.data 
            
            for team in teams:
                team_updated = False
                team_config = team.component
                if not isinstance(team_config, dict):
                    team_config = team_config.model_dump()
                
                if "participants" not in team_config:
                    continue

                for i, agent in enumerate(team_config["participants"]):
                    metadata = agent.get("metadata", {})
                    origin = metadata.get("_origin")
                    
                     # Handle stringified JSON
                    origin_dict = origin
                    if isinstance(origin, str):
                        try:
                            import json
                            origin_dict = json.loads(origin)
                        except Exception:
                            pass

                    if origin_dict and isinstance(origin_dict, dict) and str(origin_dict.get("gallery_id")) == str(gallery_id):
                        component_id = origin_dict.get("component_id")
                        component_type = origin_dict.get("component_type", "agent")
                        
                        # Find the *new* version in the gallery
                        new_component_config = ComponentSyncService._find_component_in_gallery(gallery_config, component_type, component_id)
                        
                        if new_component_config:
                            # Update the agent in the team
                            # Preserve the _origin metadata!
                            if "metadata" not in new_component_config:
                                new_component_config["metadata"] = {}
                            new_component_config["metadata"]["_origin"] = origin
                            
                            team_config["participants"][i] = new_component_config
                            team_updated = True
                
                if team_updated:
                    team.component = team_config
                    db.upsert(team)
                    logger.info(f"Synced changes from Gallery {gallery_id} to Team {team.id}")

        except Exception as e:
            logger.error(f"Error syncing gallery to teams: {e}")
