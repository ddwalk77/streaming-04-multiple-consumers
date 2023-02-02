"""
    This program sends a message to a queue on the RabbitMQ server.
    Make tasks harder/longer-running by adding dots at the end of the message.

    Author: Denise Case
    Date: January 15, 2023

    Student/Editor: DeeDee Walker
    Date: 1/29/23

"""
import pika
import sys
import webbrowser
import csv
import time

def offer_rabbitmq_admin_site(show_offer):
    """Pass true or false to offer the RabbitMQ Admin website to open automatically or prompt"""
    if show_offer == True :
        ans = input("Would you like to monitor RabbitMQ queues? y or n ")
        print()
        if ans.lower() == "y":
            webbrowser.open_new("http://localhost:15672/#/queues")
            print()
    else:
        webbrowser.open_new("http://localhost:15672/#/queues")
        
def send_message(host: str, queue_name: str, file_name):
    """
    Reads csv file as a message to the queue each execution.
    This process runs and finishes.

    Parameters:
        host (str): the host name or IP address of the RabbitMQ server
        queue_name (str): the name of the queue

    """
    # read from a file to get the messages (aka data) to be sent - declaring variable input_file
    with open(file_name, 'r') as file:
        # Create a csv reader for a comma delimited file
        reader = csv.reader(file, delimiter= '\n')
    
        for row in reader:
            # use an fstring to create a message from our data
            string = f"{row}"
            # prepare a binary (1s and 0s) message to stream
            message = string.encode()

            try:
                # create a blocking connection to the RabbitMQ server
                conn = pika.BlockingConnection(pika.ConnectionParameters(host))
                # use the connection to create a communication channel
                ch = conn.channel()
                # use the channel to declare a durable queue
                # a durable queue will survive a RabbitMQ server restart
                # and help ensure messages are processed in order
                # messages will not be deleted until the consumer acknowledges
                ch.queue_declare(queue=queue_name, durable=True)
                # use the channel to publish a message to the queue
                # every message passes through an exchange
                ch.basic_publish(exchange="", routing_key=queue_name, body=message)
                # print a message to the console for the user
                print(f" [x] Sent {message}")
            except pika.exceptions.AMQPConnectionError as e:
                print(f"Error: Connection to RabbitMQ server failed: {e}")
                sys.exit(1)
            finally:
                # close the connection to the server
                conn.close()
            
            #sleep for a couple of seconds
            time.sleep(2)

# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":  
    # ask the user if they'd like to open the RabbitMQ Admin site or just open it by passing True or False
    offer_rabbitmq_admin_site(False)

    # send the message to the queue
    send_message('localhost','task_queue3','tasks.csv')