from ..digitaltwin import bp
from flask import render_template, request
from ..library import asyncTasks
from celery.result import AsyncResult

@bp.route("/live_data")
def livedata():
    return render_template("live_data.html")

@bp.get("/live_data/result/<id>")
def result(id: str) -> dict[str, object]:
    result = AsyncResult(id)
    ready = result.ready()
    return {
        "ready": ready,
        "successful": result.successful() if ready else None,
        "value": result.get() if ready else result.result,
    }


@bp.post("/live_data/add")
def add() -> dict[str, object]:
    a = request.form.get("a", type=int)
    b = request.form.get("b", type=int)
    result = asyncTasks.add.delay(a, b)
    return {"result_id": result.id}

@bp.post("/live_data/block")
def block() -> dict[str, object]:
    result = asyncTasks.block.delay()
    return {"result_id": result.id}


@bp.post("/live_data/process")
def process() -> dict[str, object]:
    result = asyncTasks.process.delay(total=request.form.get("total", type=int))
    return {"result_id": result.id}