
# LobeChat

Hosted version: similar to ChatLLM with fewer features.
Local version: container very easy to use:
```
singularity pull docker://lobehub/lobe-chat
singularity run ./lobe-chat_latest.sif
```

A full deployment requires a database server (pgvector) for RAG.

Plugins and integration with audio and image generation.
Knowledge base for RAG similar to OpenWebUI

[Server side deployment](https://lobehub.com/docs/self-hosting/server-database/docker)

After starting the database instance specify the database url in
the DATABASE_URL variable.


# AnythingLLM

Similar to OpenWebUI, container does not work with Singularity beacuse require
non-readonly filesystem.

# OpenWebUI

Knowledge base for RAG.
Audio input.
Web search integration.
Embedded database.
By far the easiest to install, container or 'pip install open-webui'.
