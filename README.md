# Find an item

Finds a lost item from what the robot remembers, then searches room by room, after asking what it looks like. A Robonix skill package (`robonix.skill.find_item`).

The skill is a procedure: its `CAPABILITY.md` tells Pilot what to ask the user before starting, to confirm the plan, which calls to make in which order, how to report progress, and the format of the final report. The calls themselves are typed MCP contracts (`robonix/skill/find_item/{look_at, look_in}`).

Every move goes through `robonix/service/navigation/navigate`; the skill never drives the chassis itself.

## Requirements

- A mobile base with navigation (`robonix/service/navigation/navigate` and its `status`).
- Scene with a saved map and named regions (`robonix/system/scene/goal_region`, `goal_near`, `list_regions`, `find`).
- An RGB camera (`robonix/primitive/camera/snapshot`).
- A Pilot model that can read images.

Tested in the Robonix Webots example (TIAGo in the office world).

## Use

```yaml
skill:
  - name: find_item
    url: https://github.com/syswonder/skill-find-item-rbnx
    config:
      nav_timeout_s: 180
      save_dir: ""        # optional: also write every photo here
```
