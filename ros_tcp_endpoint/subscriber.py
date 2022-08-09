#  Copyright 2020 Unity Technologies
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import rclpy
import socket

from rclpy.qos import QoSDurabilityPolicy, QoSHistoryPolicy, QoSReliabilityPolicy
from rclpy.qos import QoSProfile

from .communication import RosReceiver


class RosSubscriber(RosReceiver):
    """
    Class to send messages outside of ROS network
    """

    def __init__(self, topic, message_class, tcp_server, queue_size=10):
        """

        Args:
            topic:         Topic name to publish messages to
            message_class: The message class in catkin workspace
            queue_size:    Max number of entries to maintain in an outgoing queue
        """
        RosReceiver.__init__(self)
        self.topic = topic
        self.msg = message_class
        self.tcp_server = tcp_server
        self.queue_size = queue_size

        qos_profile = QoSProfile(depth=queue_size)

        # Start Subscriber listener function
        self.subscription = self.tcp_server.create_subscription(
            self.msg, self.topic, self.send, qos_profile  # queue_size
        )

    def send(self, data):
        """
        Connect to TCP endpoint on client and pass along message
        Args:
            data: message data to send outside of ROS network

        Returns:
            self.msg: The deserialize message

        """
        self.tcp_server.send_unity_message(self.topic, data)
        return self.msg

    def unregister(self):
        """

        Returns:

        """
        self.tcp_server.destroy_subscription(self.subscription)
