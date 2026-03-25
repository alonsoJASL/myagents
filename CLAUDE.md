# Jose Alonso's Developer Manifest

## Core Architecture

**Separate orchestration from logic.** The orchestrator handles file I/O, 
environment variables, logging, and path construction. The library handles 
stateless data transformation. Libraries never assume a file system structure 
or persistence layer -- they accept data, they do not go looking for it.

**Use explicit data contracts.** Communication between layers uses Dataclasses 
or TypedDicts. No magic strings, no positional argument soup. If a function 
needs five parameters, it likely needs one structured contract.

**Logic components must be stateless.** Behavior is determined entirely by 
initialization (dependencies) and input (contracts). Same input always produces 
same output.

## Dependencies and Environment

**No singletons. No globals.** Objects receive their collaborators at 
instantiation. Dependency injection is the default, not the exception.

**Explicit environment injection always.** External processes never rely on 
ambient environment. All environment variables, paths, and configurations are 
explicitly injected. This ensures portability across dev, CI, and production.

## Abstraction Discipline

**Wait for the Rule of Three.** Do not abstract logic into a generic component 
until there are three distinct use cases. Code duplication is cheaper than the 
wrong abstraction.

## General directives

+ Favor readable and traceable over clever and terse.
+ Before implementing anything, write a plan and wait for explicit approval
+ When context window usage exceeds 80%, warn me before taking any compaction action and suggest running /context_migration first.

## Tools

`packer` — concatenates project files into a single labeled text file.
Usage: `packer -o output.txt -r /path/to/project --no-interactive`
Use this when asked to generate or refresh context files for a project.