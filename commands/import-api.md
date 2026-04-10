Load an external project's API reference and use it to inform a specific task
in the current project.

## Step 1: Load the reference file

Ask the user for the path to the exported API reference file if not provided.
Read the file at that path.

## Step 2: Load the task description

Ask the user to describe what they want to build or implement using the
external project. Example: "I want to build the format conversion from
this library into my orchestrator."

If a task was already provided alongside the command, use that directly.

## Step 3: Confirm understanding before proceeding

State clearly:
1. What the external project provides that is relevant to this task
2. Which entry points, classes, or contracts you will use
3. What the current project (consumer) must provide: paths, configs,
   managers, etc.
4. What you are about to implement and where it will live in the
   current codebase
5. Any constraints or gotchas from the reference file that affect
   the implementation

Wait for explicit confirmation before writing any code.

## Step 4: Implement

Write the implementation informed by the reference. Follow the calling
conventions exactly as documented in the reference file -- do not infer
or invent interfaces that are not present there.

If the reference file is ambiguous on any point, flag it and ask before
proceeding rather than assuming.

## Constraints

- Treat the reference file as the source of truth for the external API
- Do not browse the external project's source directly unless the user
  explicitly asks
- If something the task requires is not present in the reference file,
  say so explicitly rather than hallucinating an interface
- Follow the current project's CLAUDE.md conventions for code style
  and architecture