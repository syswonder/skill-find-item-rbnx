---
description: Find a lost item (a procedure; read this before any call). Asks what it looks like, confirms, checks where Scene last saw it (Scene labels are English nouns), then searches room by room.
---

# Find an item

Use this skill when the user asks where something is or asks the robot to
find it, for example "where is my cup" or "find my keys".

This skill is a procedure. Follow the sections below in order. Do not skip
the questions, and do not move the robot before the user has confirmed.

## Information needed

Ask everything that is missing in one reply, numbered, at most three
questions. Ask only what the user has not already said.

1. What the item is and how to recognise it (colour, size, anything on it).
2. Where it might be, if the user has an idea. Offer the room names returned
   by `robonix/system/scene/list_regions`; "no idea" is a valid answer.
3. What to do when it is found: only say where it is, or stay next to it.
   Default: only say where it is.

Keep the questions short enough to be read aloud. When the user answers only
some of them, ask again for the rest only.

## Confirm before starting

Always confirm, even when the user answered everything at once. Say in one
sentence where the robot will look first and in what order, and wait for the
user to agree.

## Steps

1. Look in memory: call `robonix/system/scene/find` with the item's label
   as a short English noun (`lamp`, `cup`, `backpack`), whatever language
   the user spoke; Scene labels are English. Scene is a record of where
   things were seen, not proof they are still there.
2. For each remembered match, nearest first: call
   `robonix/skill/find_item/look_at` with its object ID and check the photo
   against the user's description. Stop at the first photo that shows it.
3. If nothing in memory matched or no photo showed it: call
   `robonix/skill/find_item/look_in` for each room, the rooms the user
   suggested first, then the rest, and check each photo. Stop when found.
4. When found and the user asked the robot to stay, it is already there:
   say so and wait.

When `arrived` is false, note the place as "not reached" with the reason
from `detail` and continue.

## Progress

Visit one place per plan, so there is a turn between places to report in.
After each place, say one short line, for example "Not in the kitchen,
going to the bedroom next."

## Stopping early

If the user says stop, or says the item was found, stop after the current
place and report what was searched so far.

## Report

Two parts, in the user's language.

Spoken: one sentence. Found: where it is, in words a person can use ("on
the living-room table, next to the laptop"). Not found: that it was not
found and how many places were searched.

Written, below it:

- Found: the room and position, the photo, and whether it was seen just now
  or only remembered.
- Searched: every place in visiting order with its result: seen, not here,
  not reached, not searched.

Never say an item is somewhere because Scene remembers it there unless a
photo from this search shows it.
