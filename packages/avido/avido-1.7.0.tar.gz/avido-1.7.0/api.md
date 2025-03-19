# ValidateWebhook

Types:

```python
from avido.types import ValidateWebhookValidateResponse
```

Methods:

- <code title="post /v0/validate-webhook">client.validate_webhook.<a href="./src/avido/resources/validate_webhook.py">validate</a>(\*\*<a href="src/avido/types/validate_webhook_validate_params.py">params</a>) -> <a href="./src/avido/types/validate_webhook_validate_response.py">ValidateWebhookValidateResponse</a></code>

# Applications

Types:

```python
from avido.types import Application, ApplicationResponse
```

Methods:

- <code title="post /v0/applications">client.applications.<a href="./src/avido/resources/applications.py">create</a>(\*\*<a href="src/avido/types/application_create_params.py">params</a>) -> <a href="./src/avido/types/application_response.py">ApplicationResponse</a></code>
- <code title="get /v0/applications/{id}">client.applications.<a href="./src/avido/resources/applications.py">retrieve</a>(id) -> <a href="./src/avido/types/application_response.py">ApplicationResponse</a></code>
- <code title="get /v0/applications">client.applications.<a href="./src/avido/resources/applications.py">list</a>(\*\*<a href="src/avido/types/application_list_params.py">params</a>) -> <a href="./src/avido/types/application.py">SyncOffsetPagination[Application]</a></code>

# Traces

Types:

```python
from avido.types import (
    LlmStep,
    LogStep,
    RetrieverStep,
    ToolStep,
    Trace,
    TraceRetrieveResponse,
    TraceListResponse,
)
```

Methods:

- <code title="get /v0/traces/{id}">client.traces.<a href="./src/avido/resources/traces.py">retrieve</a>(id) -> <a href="./src/avido/types/trace_retrieve_response.py">TraceRetrieveResponse</a></code>
- <code title="get /v0/traces">client.traces.<a href="./src/avido/resources/traces.py">list</a>(\*\*<a href="src/avido/types/trace_list_params.py">params</a>) -> <a href="./src/avido/types/trace_list_response.py">TraceListResponse</a></code>

# Ingest

Types:

```python
from avido.types import IngestCreateResponse
```

Methods:

- <code title="post /v0/ingest">client.ingest.<a href="./src/avido/resources/ingest.py">create</a>(\*\*<a href="src/avido/types/ingest_create_params.py">params</a>) -> <a href="./src/avido/types/ingest_create_response.py">IngestCreateResponse</a></code>

# Tasks

Types:

```python
from avido.types import Task, TaskResponse, TaskTriggerResponse
```

Methods:

- <code title="post /v0/tasks">client.tasks.<a href="./src/avido/resources/tasks.py">create</a>(\*\*<a href="src/avido/types/task_create_params.py">params</a>) -> <a href="./src/avido/types/task_response.py">TaskResponse</a></code>
- <code title="get /v0/tasks/{id}">client.tasks.<a href="./src/avido/resources/tasks.py">retrieve</a>(id) -> <a href="./src/avido/types/task_response.py">TaskResponse</a></code>
- <code title="get /v0/tasks">client.tasks.<a href="./src/avido/resources/tasks.py">list</a>(\*\*<a href="src/avido/types/task_list_params.py">params</a>) -> <a href="./src/avido/types/task.py">SyncOffsetPagination[Task]</a></code>
- <code title="post /v0/tasks/trigger">client.tasks.<a href="./src/avido/resources/tasks.py">trigger</a>(\*\*<a href="src/avido/types/task_trigger_params.py">params</a>) -> <a href="./src/avido/types/task_trigger_response.py">TaskTriggerResponse</a></code>

# Evals

Types:

```python
from avido.types import Eval, EvalRetrieveResponse
```

Methods:

- <code title="get /v0/evals/{id}">client.evals.<a href="./src/avido/resources/evals.py">retrieve</a>(id) -> <a href="./src/avido/types/eval_retrieve_response.py">EvalRetrieveResponse</a></code>
- <code title="get /v0/evals">client.evals.<a href="./src/avido/resources/evals.py">list</a>(\*\*<a href="src/avido/types/eval_list_params.py">params</a>) -> <a href="./src/avido/types/eval.py">SyncOffsetPagination[Eval]</a></code>

# Runs

Types:

```python
from avido.types import Run, RunRetrieveResponse
```

Methods:

- <code title="get /v0/runs/{id}">client.runs.<a href="./src/avido/resources/runs.py">retrieve</a>(id) -> <a href="./src/avido/types/run_retrieve_response.py">RunRetrieveResponse</a></code>
- <code title="get /v0/runs">client.runs.<a href="./src/avido/resources/runs.py">list</a>(\*\*<a href="src/avido/types/run_list_params.py">params</a>) -> <a href="./src/avido/types/run.py">SyncOffsetPagination[Run]</a></code>

# Tests

Types:

```python
from avido.types import Test, TestRetrieveResponse
```

Methods:

- <code title="get /v0/tests/{id}">client.tests.<a href="./src/avido/resources/tests.py">retrieve</a>(id) -> <a href="./src/avido/types/test_retrieve_response.py">TestRetrieveResponse</a></code>
- <code title="get /v0/tests">client.tests.<a href="./src/avido/resources/tests.py">list</a>(\*\*<a href="src/avido/types/test_list_params.py">params</a>) -> <a href="./src/avido/types/test.py">SyncOffsetPagination[Test]</a></code>

# Topics

Types:

```python
from avido.types import Topic, TopicResponse
```

Methods:

- <code title="post /v0/topics">client.topics.<a href="./src/avido/resources/topics.py">create</a>(\*\*<a href="src/avido/types/topic_create_params.py">params</a>) -> <a href="./src/avido/types/topic_response.py">TopicResponse</a></code>
- <code title="get /v0/topics/{id}">client.topics.<a href="./src/avido/resources/topics.py">retrieve</a>(id) -> <a href="./src/avido/types/topic_response.py">TopicResponse</a></code>
- <code title="get /v0/topics">client.topics.<a href="./src/avido/resources/topics.py">list</a>(\*\*<a href="src/avido/types/topic_list_params.py">params</a>) -> <a href="./src/avido/types/topic.py">SyncOffsetPagination[Topic]</a></code>
