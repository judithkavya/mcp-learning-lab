"""
Phase 10 — Google Calendar MCP Server
Tools: list_events, create_event, delete_event
Auth: OAuth 2.0 via credentials.json / token.json
"""

import os
import json
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv

from mcp.server.fastmcp import FastMCP
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# ── Config ──────────────────────────────────────────────────────────────────

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "./credentials.json")
TOKEN_PATH = os.getenv("GOOGLE_TOKEN_PATH", "./token.json")

mcp = FastMCP("google-calendar")


# ── Auth helper ──────────────────────────────────────────────────────────────

def get_calendar_service():
    """
    Returns an authenticated Google Calendar API service.
    - First run: opens browser for OAuth consent → saves token.json
    - Subsequent runs: loads token.json, refreshes if expired
    """
    creds = None

    if Path(TOKEN_PATH).exists():
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    # Refresh or re-authenticate if needed
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save token for next run
        with open(TOKEN_PATH, "w") as f:
            f.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)


# ── Tools ────────────────────────────────────────────────────────────────────

@mcp.tool()
def list_events(start_date: str, end_date: str, max_results: int = 10) -> str:
    """
    List calendar events between two dates.

    Args:
        start_date: Start date in YYYY-MM-DD format (e.g. '2025-07-01')
        end_date:   End date in YYYY-MM-DD format (e.g. '2025-07-31')
        max_results: Max number of events to return (default 10)

    Returns:
        JSON string of events with id, summary, start, end, description
    """
    service = get_calendar_service()

    # Convert dates to RFC3339 format required by Google Calendar API
    time_min = f"{start_date}T00:00:00Z"
    time_max = f"{end_date}T23:59:59Z"

    result = service.events().list(
        calendarId="primary",
        timeMin=time_min,
        timeMax=time_max,
        maxResults=max_results,
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    events = result.get("items", [])

    if not events:
        return json.dumps({"message": "No events found in this date range.", "events": []})

    formatted = []
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        end = event["end"].get("dateTime", event["end"].get("date"))
        formatted.append({
            "id": event["id"],
            "summary": event.get("summary", "(No title)"),
            "start": start,
            "end": end,
            "description": event.get("description", ""),
            "location": event.get("location", ""),
        })

    return json.dumps({"events": formatted, "count": len(formatted)}, indent=2)


@mcp.tool()
def create_event(
    title: str,
    start_datetime: str,
    end_datetime: str,
    description: str = "",
    location: str = "",
    attendee_emails: str = "",
) -> str:
    """
    Create a new calendar event.

    Args:
        title:            Event title / summary
        start_datetime:   Start in ISO format e.g. '2025-07-15T10:00:00'
        end_datetime:     End in ISO format e.g. '2025-07-15T11:00:00'
        description:      Optional event description
        location:         Optional location string
        attendee_emails:  Optional comma-separated list of attendee emails
                          e.g. 'alice@example.com,bob@example.com'

    Returns:
        JSON with created event id, link, and summary
    """
    service = get_calendar_service()

    event_body = {
        "summary": title,
        "description": description,
        "location": location,
        "start": {
            "dateTime": start_datetime,
            "timeZone": "Asia/Kolkata",
        },
        "end": {
            "dateTime": end_datetime,
            "timeZone": "Asia/Kolkata",
        },
    }

    # Add attendees if provided
    if attendee_emails.strip():
        emails = [e.strip() for e in attendee_emails.split(",") if e.strip()]
        event_body["attendees"] = [{"email": e} for e in emails]

    created = service.events().insert(
        calendarId="primary",
        body=event_body,
        sendUpdates="all" if attendee_emails.strip() else "none",
    ).execute()

    return json.dumps({
        "status": "created",
        "event_id": created["id"],
        "summary": created.get("summary"),
        "start": created["start"].get("dateTime"),
        "end": created["end"].get("dateTime"),
        "link": created.get("htmlLink"),
    }, indent=2)


@mcp.tool()
def delete_event(event_id: str) -> str:
    """
    Delete a calendar event by its ID.

    Use list_events first to find the event_id you want to delete.

    Args:
        event_id: The Google Calendar event ID (from list_events output)

    Returns:
        JSON confirming deletion or describing the error
    """
    service = get_calendar_service()

    try:
        service.events().delete(
            calendarId="primary",
            eventId=event_id,
        ).execute()

        return json.dumps({
            "status": "deleted",
            "event_id": event_id,
            "message": "Event successfully deleted.",
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "status": "error",
            "event_id": event_id,
            "message": str(e),
        }, indent=2)


@mcp.tool()
def update_event(
    event_id: str,
    title: str = "",
    start_datetime: str = "",
    end_datetime: str = "",
    description: str = "",
    location: str = "",
) -> str:
    """
    Update an existing calendar event. Only provided fields are changed.

    Args:
        event_id:        The Google Calendar event ID (from list_events output)
        title:           New title (leave empty to keep existing)
        start_datetime:  New start in ISO format (leave empty to keep existing)
        end_datetime:    New end in ISO format (leave empty to keep existing)
        description:     New description (leave empty to keep existing)
        location:        New location (leave empty to keep existing)

    Returns:
        JSON with updated event details
    """
    service = get_calendar_service()

    # Fetch existing event first
    event = service.events().get(calendarId="primary", eventId=event_id).execute()

    # Only patch fields that were provided
    if title:
        event["summary"] = title
    if description:
        event["description"] = description
    if location:
        event["location"] = location
    if start_datetime:
        event["start"]["dateTime"] = start_datetime
    if end_datetime:
        event["end"]["dateTime"] = end_datetime

    updated = service.events().update(
        calendarId="primary",
        eventId=event_id,
        body=event,
    ).execute()

    return json.dumps({
        "status": "updated",
        "event_id": updated["id"],
        "summary": updated.get("summary"),
        "start": updated["start"].get("dateTime"),
        "end": updated["end"].get("dateTime"),
        "link": updated.get("htmlLink"),
    }, indent=2)


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Starting Google Calendar MCP server (stdio)...")
    mcp.run(transport="stdio")