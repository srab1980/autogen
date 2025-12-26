# api/routes/teams.py
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException

from ...datamodel import Team
from ...gallery.builder import create_default_gallery
from ..deps import get_db
from ...database.sync_service import ComponentSyncService


router = APIRouter()


@router.get("/")
async def list_teams(user_id: str, db=Depends(get_db)) -> Dict:
    """List all teams for a user"""
    response = db.get(Team, filters={"user_id": user_id})

    if not response.data or len(response.data) == 0:
        default_gallery = create_default_gallery()
        default_team = Team(user_id=user_id, component=default_gallery.components.teams[0].model_dump())

        db.upsert(default_team)
        response = db.get(Team, filters={"user_id": user_id})

    return {"status": True, "data": response.data}


@router.get("/{team_id}")
async def get_team(team_id: int, user_id: str, db=Depends(get_db)) -> Dict:
    """Get a specific team"""
    response = db.get(Team, filters={"id": team_id, "user_id": user_id})
    if not response.status or not response.data:
        raise HTTPException(status_code=404, detail="Team not found")
    return {"status": True, "data": response.data[0]}


@router.post("/")
async def create_team(team: Team, db=Depends(get_db)) -> Dict:
    """Create a new team"""
    response = db.upsert(team)
    if not response.status:
        raise HTTPException(status_code=400, detail=response.message)
    
    # Sync updates back to gallery if applicable
    if response.status and response.data:
        # Re-fetch the saved team to ensure we have the latest state (though 'team' obj might be enough)
        # response.data is dict, we need the model object for the service or pass the dict
        # The service expects a Team object. Let's construct it or modify service. 
        # Actually the service inputs 'Team' object. 'team' variable here is a Team object.
        ComponentSyncService.sync_team_updates_to_gallery(team, db)

    return {"status": True, "data": response.data}


@router.delete("/{team_id}")
async def delete_team(team_id: int, user_id: str, db=Depends(get_db)) -> Dict:
    """Delete a team"""
    db.delete(filters={"id": team_id, "user_id": user_id}, model_class=Team)
    return {"status": True, "message": "Team deleted successfully"}
