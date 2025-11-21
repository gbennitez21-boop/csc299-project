# tasks2 — Selene Prototype (PKMS + Tasks + Cycle Tracking)

This is the second prototype for the CSC 299 project.  
It expands the simple JSON task manager into a more complete system called **Selene**, including:

- Task management (add, list, search, complete, delete)
- Notes (create, list, search, view)
- Cycle tracking (log symptoms, moods, phases)
- Simple planning assistant based on cycle patterns
- Local chat-style lookup for notes and tasks
- All data saved in a single JSON file: `selene_data.json`

## How to run

From inside the `tasks2` directory:

```bash
python selene.py task-add "Buy iron supplements" --due 2025-11-24 --tags health
python selene.py task-list
python selene.py note-add "Cramps journal" --body "Started at 10am" --tags cycle
python selene.py note-list
python selene.py cycle-log 2025-11-03 --phase start --symptoms cramps mood low
python selene.py cycle-predict
python selene.py plan
python selene.py chat cramps
