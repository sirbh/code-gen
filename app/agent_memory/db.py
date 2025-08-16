import os
from langgraph.store.postgres.aio import AsyncPostgresStore
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver


DB_URI = "postgresql://spec_gen_test:password@localhost:5430/thread_details"

async def init_memory():
    store_ctx = AsyncPostgresStore.from_conn_string(DB_URI)
    checkpointer_ctx = AsyncPostgresSaver.from_conn_string(DB_URI)

    store = await store_ctx.__aenter__()
    checkpointer = await checkpointer_ctx.__aenter__()

    return store, checkpointer, store_ctx, checkpointer_ctx
