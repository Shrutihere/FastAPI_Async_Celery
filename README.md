<h1 align='center'>
  FastAPI Asynchronous Task
<span>
  <img src="https://styles.redditmedia.com/t5_22y58b/styles/communityIcon_r5ax236rfw961.png" width='30px'>
  </span>
</h1> 
  <h2 align='center'>
  Celery 
   <span>
  <img src='https://docs.celeryproject.org/en/stable/_static/celery_512.png' width='60px' align='center'>
  </span>
  + 
  RabbitMQ
   <span>
  <img src='https://assets.zabbix.com/img/brands/rabbitmq.svg' width='30px' align='center'>
  </span> 
  + 
  Flower
</h2>
Implementation of celery background task using FastAPI and monitor the tasks using Flower. The RabbitMQ service will used as the message broker.


# task-scheduler
This repository contains the endpoints to schedule a task at a specific time or repeating in a pattern based on the RRules.

## Local Setup - Development
Install rabbitmq : `sudo apt-get install rabbitmq-server` <br />
Install celery : `pip install celery` <br />
Run the celery worker server : `celery -A tasks worker --loglevel=INFO` <br />
For specific queue : `celery -A app.worker.celery_app worker --loglevel=info -Q test-queue` <br />
Run celery beat : `celery -A app.worker.celery_app beat --loglevel=INFO -s celery_file` <br />
<br />
Run celery server using Flower : `celery -A app.worker.celery_app flower --port=5555` <br />
Url to Flower : `http://localhost:5555/dashboard` <br />
<br />
Run main.py for endpoints<br />
 
## Dockersizing - Production
Build docker image : `docker-compose build` <br />
Run image : `docker-compose up` -d <br />
See logs : `docker-compose logs` -f<br />
List of running containers : `docker container ls` <br />
Stop a server : `docker stop <.container_id.>` <br />

## Celery Concepts
### Introduction
Celery is generally used as a task queue to run the tasks asynchronously, we use it for scheduling (repeating) jobs that are to be run at a (list of) date(s) in future. <i> Celery Architecture </i> <br />
Web (Fastapi): Provide APIs to receive requests.<br />
Broker (RabbitMQ) : A queue for scheduled jobs.<br />
Worker : Servers which pick up tasks to be executed.<br />
Results Backend : To store the task results.<br />
<br /> 
<i> RabbitMQ is an open source message broker - an intermediary for messaging. Celery is a Task Queue software which uses RabbitMQ as a broker to know the status of the tasks in progress </i> <br /> 

### Integration with FastAPI Server
The fastapi app receives the request and uses TaskScheduker to schedule a task.<br /> 
### Scheduling and Executing jobs
1. Request to schedule a `task` is sent through API
2. `Taskscheduler` is used to schedule the task

`TaskScheduler.schedule(func, description, args=None, kwargs=None, rrule_string=None, trigger_at=None, until=None)` <br /> 


## Flow
### User Flow
`notification_metadata` : <br /> 
| Variable | Type |
| --- | --- |
| `auth_header` | `str` |
| `title` | `str` |
| `body` | `str` |
| `item_id` | `str` |
| `created_at` | `int` |
| `created_by` | `str` |
| `classroom_id` | `str` |
| `kind` | `int` |



`Task` : <br /> 
| Variable | Type |
| --- | --- |
| `rrule` | `RRule` |
| `start_datetime` | `int` |
| `notification_metadata` | `notification_metadata` |

`/remind_me` : Request endpoint, takes `Task` as input<br /> 

### Data Flow
`apply_async` - a celery function to schedule a task to the celery worker; `eta` can be defined as a parameter.<br />
`TaskScheduler` uses generated `eta` from the rrule and uses `apply_sync` to send the task to the queue.<br />

- https://github.com/okteto/python-fastapi-celery
- https://github.com/bstiel/celery-docker/blob/master/docker-compose.yml
- https://github.com/kubernetes-for-developers/kfd-celery


