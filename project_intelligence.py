import os
import psycopg
from dotenv import load_dotenv

load_dotenv()


def get_project_context():

    connection = psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
    )

    cursor = connection.cursor()

    print("Connected to ShopSphere database!")

    # --------------------------------
    # Get open blockers for Sprint 1
    # --------------------------------

    cursor.execute("""
        SELECT
            b.blocker_id,
            b.description,
            t.task_id,
            t.task_name,
            t.status AS task_status,
            s.sprint_name,
            s.end_date
        FROM blockers b
        JOIN tasks t
            ON b.task_id = t.task_id
        JOIN sprints s
            ON t.sprint_id = s.sprint_id
        WHERE b.status = 'Open'
          AND s.sprint_id = 'S1'
        ORDER BY b.reported_date;
    """)

    blockers = cursor.fetchall()

    # --------------------------------
    # Get client change requests
    # --------------------------------

    cursor.execute("""
        SELECT
            change_id,
            requested_date,
            requested_by,
            description,
            impact,
            status
        FROM change_requests
        WHERE project_id = 'P001'
        ORDER BY requested_date;
    """)

    changes = cursor.fetchall()

    # --------------------------------
    # Get project updates
    # --------------------------------

    cursor.execute("""
        SELECT
            update_date,
            submitted_by,
            update_type,
            content
        FROM updates
        WHERE project_id = 'P001'
        ORDER BY update_date, update_id;
    """)

    updates = cursor.fetchall()

    # --------------------------------
    # Build Project Context
    # --------------------------------

    project_context = {
        "project_id": "P001",
        "project_name": "ShopSphere",
        "sprint": {
            "name": "Authentication & Catalog",
            "deadline": "2026-10-10"
        },
        "blockers": [],
        "change_requests": [],
        "updates": [],
        "tasks": [],
        "sprints": []
    }

    # --------------------------------
    # Add blockers
    # --------------------------------

    for blocker in blockers:
        project_context["blockers"].append({
            "blocker_id": blocker[0],
            "description": blocker[1],
            "task_id": blocker[2],
            "task_name": blocker[3],
            "task_status": blocker[4],
            "sprint": blocker[5],
            "deadline": str(blocker[6])
        })

    # --------------------------------
    # Add change requests
    # --------------------------------

    for change in changes:
        project_context["change_requests"].append({
            "change_id": change[0],
            "date": str(change[1]),
            "requested_by": change[2],
            "description": change[3],
            "impact": change[4],
            "status": change[5]
        })

    # --------------------------------
    # Add project updates
    # --------------------------------

    for update in updates:
        project_context["updates"].append({
            "date": str(update[0]),
            "submitted_by": update[1],
            "type": update[2],
            "details": update[3].split("Update:", 1)[-1].strip()
        })

    # --------------------------------
    # Get project tasks
    # --------------------------------

    cursor.execute("""
        SELECT
            task_id,
            task_name,
            assignee,
            status,
            priority,
            sprint_id
        FROM tasks
        WHERE project_id = 'P001'
        ORDER BY task_id;
    """)

    tasks = cursor.fetchall()

    for task in tasks:
        project_context["tasks"].append({
            "task_id": task[0],
            "task_name": task[1],
            "assignee": task[2],
            "status": task[3],
            "priority": task[4],
            "sprint_id": task[5]
        })

    # --------------------------------
    # Get sprint information
    # --------------------------------

    cursor.execute("""
        SELECT
            sprint_id,
            sprint_name,
            start_date,
            end_date,
            status
        FROM sprints
        WHERE project_id = 'P001'
        ORDER BY start_date;
    """)

    sprints = cursor.fetchall()

    for sprint in sprints:
        project_context["sprints"].append({
            "sprint_id": sprint[0],
            "sprint_name": sprint[1],
            "start_date": str(sprint[2]),
            "end_date": str(sprint[3]),
            "status": sprint[4]
        })

    cursor.close()
    connection.close()

    return project_context


# --------------------------------
# Test the function
# --------------------------------

if __name__ == "__main__":

    project_context = get_project_context()

    print("\n--- Project Context ---")
    print(project_context)