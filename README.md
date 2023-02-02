# streaming-04-multiple-consumers

> Use RabbitMQ to distribute tasks to multiple workers

One process will create task messages. Multiple worker processes will share the work. 

## Before You Begin

1. Fork this starter repo into your GitHub.
1. Clone your repo down to your machine.
1. View / Command Palette - then Python: Select Interpreter
1. Select your conda environment. 

## Read

1. Read the [RabbitMQ Tutorial - Work Queues](https://www.rabbitmq.com/tutorials/tutorial-two-python.html)
1. Read the code and comments in this repo.

## RabbitMQ Admin 

RabbitMQ comes with an admin panel. When you run the task emitter, reply y to open it. 
- Note: The default login/password for this is guest/guest

(Python makes it easy to open a web page - see the code to learn how.)

## Execute the Producer

1. Run emitter_of_tasks.py (say y to monitor RabbitMQ queues)

v1 emitter:
![v1 emitting terminal script](https://github.com/ddwalk77/streaming-04-multiple-consumers/blob/main/v1_emitter.png "v1 Emitting terminal script")

Explore the RabbitMQ website.

## Execute a Consumer / Worker

1. Run listening_worker.py

Will it terminate on its own? How do you know? 
'''diff
# - listening_worker.py doesn't terminate on it's own. The code doesn't have a connection termination without a KeyboardInterrupt that forces the exit.
'''

v1 listeners:
![v1 listener terminal script](https://github.com/ddwalk77/streaming-04-multiple-consumers/blob/main/v1listener.png "v1 Listening terminal script")
![v1 listener terminal2 script](https://github.com/ddwalk77/streaming-04-multiple-consumers/blob/main/v1listener2.png "v1 Listening terminal2 script")

## Ready for Work

1. Use your emitter_of_tasks to produce more task messages.

v2 emitter:
![v2 emitting terminal script](https://github.com/ddwalk77/streaming-04-multiple-consumers/blob/main/v2_emitter.png "v2 Emitting terminal script")

## Start Another Listening Worker 

1. Use your listening_worker.py script to launch a second worker. 

Follow the tutorial. 
Add multiple tasks (e.g. First message, Second message, etc.)
How are tasks distributed?
'''diff
# - The tasks are rotated between the two consumers that are open.
'''
Monitor the windows with at least two workers. 
Which worker gets which tasks?
'''diff
# - One worker gets the odd number messages and one gets the evens.
'''

Version 2 running:

v1 listeners:
![v2 listener terminal script](https://github.com/ddwalk77/streaming-04-multiple-consumers/blob/main/v2listener.png "v2 Listening terminal script")
![v2 listener terminal2 script](https://github.com/ddwalk77/streaming-04-multiple-consumers/blob/main/v2listener2.png "v2 Listening terminal2 script")

## Reference

- [RabbitMQ Tutorial - Work Queues](https://www.rabbitmq.com/tutorials/tutorial-two-python.html)
''' diff
#   - Durable queues and messages: 
#        - In order to make sure that messages aren't lost if RabbitMQ quts or crashes, we must mark both the queue and messages as durable. This needs to be done in the code for the emitter and listener.
#        - The messages are marked as persistent byt supplying a delivery_mode property with the value of pika.spec.PERSISTENT_DELIVERY_MODE
#            - Ex for queue: channel.queue_declare(queue='task_queue', durable=True)
#            - Ex for messages: channel.basic_publish(exchange='',
#                                                     routing_key="task_queue",
#                                                     body=message,
#                                                     properties=pika.BasicProperties(
#                                                        delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE
#                                                     ))
#    - Consumer acknowledgements confirm the work was done and the message can be deleted.
#        - Ex: ch.basic_ack(delivery_tag = method.delivery_tag)
'''

## Project - Version 3 - Automating the Tasks
- Build a verison 3 much like version 2, except read from tasks.csv. Multiple workers will retrieve the messages as they do in version 2
'''diff
# - v3_emitter_of_tasks.py automatically runs the RabbitMQ admin panel to monitor messages, but this can be turned off through the variable show_offer. The file name can be updated if a different file is needed instead of tasks.csv. This script produces messages to the console from the csv file.
# - v3_listening_worker.py consumes the messages from the emitter/csv file and displays them on the console with confirmations of receipt.
'''

## Screenshot

See a running example with at least 3 concurrent process windows here:
