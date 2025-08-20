import uuid
import pytest


def create_task(client, title="Test Task", description="desc", status="pending"):
    payload = {"title": title, "description": description, "status": status}
    res = client.post("/tasks/", json=payload)
    assert res.status_code == 201
    return res.json()


def list_tasks(client, **params):
    res = client.get("/tasks/", params=params)
    assert res.status_code == 200
    return res.json()


def patch_task(client, task_id, **fields):
    res = client.patch(f"/tasks/{task_id}", json=fields)
    return res


def delete_task(client, task_id):
    res = client.delete(f"/tasks/{task_id}")
    return res


def extract_id(created):
    if isinstance(created, dict) and "id" in created:
        task_id = created["id"]
        if isinstance(task_id, str):
            try:
                uuid.UUID(task_id)
            except ValueError:
                print(f"Invalid UUID format: {task_id}")
        return task_id
    return created


def test_create_and_list(client):
    created = create_task(client, title="Alpha", description="A", status="pending")
    task_id = extract_id(created)
    tasks = list_tasks(client)
    assert any(t.get("title") == "Alpha" for t in tasks)


def test_update_task(client):
    created = create_task(client, title="Bravo", description="B", status="pending")
    task_id = extract_id(created)
    res = patch_task(client, task_id, title="Bravo+", status="in_progress")
    assert res.status_code == 200
    updated = res.json()
    assert updated.get("title") == "Bravo+"
    assert str(updated.get("status")).lower().replace(" ", "_") == "in_progress"


def test_filter_by_status(client):
    a = create_task(client, title="C1", status="done")
    b = create_task(client, title="C2", status="pending")
    done = list_tasks(client, status="done")
    assert len(done) >= 1
    assert all(
        str(item.get("status")).lower().replace(" ", "_") == "done" for item in done
    )


def test_delete_task(client):
    created = create_task(client, title="Delta", description=None, status="pending")
    task_id = extract_id(created)
    res = delete_task(client, task_id)
    assert res.status_code == 200
    tasks = list_tasks(client)
    assert not any(str(t.get("id")) == str(task_id) for t in tasks)


def test_update_nonexistent_returns_404(client):
    bogus_id = uuid.uuid4()
    res = patch_task(client, bogus_id, title="X")
    assert res.status_code == 404


def test_delete_nonexistent_returns_404(client):
    bogus_id = uuid.uuid4()
    res = delete_task(client, bogus_id)
    assert res.status_code == 404
