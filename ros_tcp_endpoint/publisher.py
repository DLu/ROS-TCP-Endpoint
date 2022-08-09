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

from rclpy.qos import QoSProfile, QoSDurabilityPolicy

from rclpy.serialization import deserialize_message

from .communication import RosSender


class RosPublisher(RosSender):
    """
    Class to publish messages to a ROS topic
    """

    def __init__(self, topic, message_class, tcp_server, queue_size=10, latch=False):
        """

        Args:
            topic:         Topic name to publish messages to
            message_class: The message class in catkin workspace
            queue_size:    Max number of entries to maintain in an outgoing queue
        """
        RosSender.__init__(self)
        self.tcp_server = tcp_server
        self.msg = message_class()

        qos_profile = QoSProfile(depth=queue_size)
        if latch:
            qos_profile.durability = QoSDurabilityPolicy.RMW_QOS_POLICY_DURABILITY_TRANSIENT_LOCAL

        self.pub = self.tcp_server.create_publisher(message_class, topic, qos_profile)

    def send(self, data):
        """
        Takes in serialized message data from source outside of the ROS network,
        deserializes it into it's message class, and publishes the message to ROS topic.

        Args:
            data: The already serialized message_class data coming from outside of ROS

        Returns:
            None: Explicitly return None so behaviour can be
        """
        # message_type = type(self.msg)
        # message = deserialize_message(data, message_type)

        self.pub.publish(data)

        return None

    def unregister(self):
        """

        Returns:

        """
        self.tcp_server.destroy_publisher(self.pub)
