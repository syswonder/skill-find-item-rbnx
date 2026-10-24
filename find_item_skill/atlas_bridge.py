"""Atlas registration and the MCP entrypoints of the find-item skill."""
from __future__ import annotations

import asyncio
import logging
import time

from robonix_api import ATLAS, Err, Ok, Skill

from find_item_mcp import (
    LookAtObject_Request,
    LookAtObject_Response,
    LookInRegion_Request,
    LookInRegion_Response,
)

from .goto_look import NEEDS, GoLook

logging.basicConfig(level=logging.INFO, format="[find-item] %(levelname)s %(message)s")
log = logging.getLogger("find_item")

skill = Skill(id="find_item", namespace="robonix/skill/find_item")
config: dict = {}
go: GoLook | None = None


def resolve(deadline_s: float = 45.0) -> dict[str, str]:
    """MCP endpoints of everything in NEEDS, found through Atlas."""
    found: dict[str, str] = {}
    deadline = time.monotonic() + deadline_s
    while time.monotonic() < deadline and len(found) < len(NEEDS):
        for tool, contract in NEEDS.items():
            if tool in found:
                continue
            try:
                view = ATLAS.find_unique_capability(contract_id=contract, transport="mcp")
                channel = skill.connect_capability(view, contract, "mcp")
                if channel.endpoint:
                    found[tool] = channel.endpoint
                channel.close()
            except Exception:  # noqa: BLE001
                continue
        time.sleep(1.0)
    missing = [NEEDS[t] for t in NEEDS if t not in found]
    if missing:
        raise RuntimeError(f"missing Atlas dependencies: {missing}")
    return found


@skill.mcp("robonix/skill/find_item/look_at")
async def look_at(req: LookAtObject_Request) -> LookAtObject_Response:
    """Drive next to a remembered object and photograph it."""
    arrived, image, detail = await _go("goal_near", "object_id", req.object_id, False)
    return LookAtObject_Response(arrived=arrived, image_base64=image, format="jpeg" if image else "", detail=detail)


@skill.mcp("robonix/skill/find_item/look_in")
async def look_in(req: LookInRegion_Request) -> LookInRegion_Response:
    """Drive to a region and photograph it."""
    arrived, image, detail = await _go("goal_region", "region_id", req.region, True)
    return LookInRegion_Response(arrived=arrived, image_base64=image, format="jpeg" if image else "", detail=detail)


async def _go(goal_tool: str, key: str, target: str, sweep: bool) -> tuple[bool, str, str]:
    if go is None:
        raise RuntimeError("find-item is not active")
    arrived, image, detail = await asyncio.to_thread(go.visit, goal_tool, key, target.strip(), sweep)
    log.info("%s %s: %s", goal_tool, target, detail)
    return arrived, image, detail


@skill.on_init
def init(cfg: dict):
    global config
    config = dict(cfg or {})
    if float(config.get("nav_timeout_s", 180)) <= 0:
        return Err("nav_timeout_s must be greater than zero")
    return Ok()


@skill.on_activate
def activate():
    global go
    if go is not None:
        return Ok()
    try:
        go = GoLook(resolve(), float(config.get("nav_timeout_s", 180)), str(config.get("save_dir", "")))
    except Exception as exc:  # noqa: BLE001
        return Err(str(exc))
    return Ok()


@skill.on_deactivate
def deactivate():
    global go
    go = None
    return Ok()


if __name__ == "__main__":
    skill.run()
