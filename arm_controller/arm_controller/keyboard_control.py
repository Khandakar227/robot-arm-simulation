import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
from pynput import keyboard  # Importing keyboard from pynput


class KeyboardControl(Node):
    def __init__(self):
        super().__init__('keyboard_control')
        self.publisher_ = self.create_publisher(JointState, '/joint_states', 10)

        # Parameters
        self.declare_parameter('joint_names', ['joint_1', 'joint_2', 'joint_3', 'joint_4', 'joint_5', 'joint_6'])  # Replace with your joint names
        self.joint_names = self.get_parameter('joint_names').value
        self.joint_positions = [0.0] * len(self.joint_names)  # Initialize joint positions
        self.increment = 0.01  # Increment value for joint position adjustments

        # Timer to publish joint states
        self.timer = self.create_timer(0.1, self.publish_joint_state)

        # Start keyboard listener
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()
        self.get_logger().info('Keyboard Control Node Started')

    def publish_joint_state(self):
        msg = JointState()
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.joint_names
        msg.position = self.joint_positions

        self.publisher_.publish(msg)
        self.get_logger().info(f'Published joint states: {self.joint_positions}')

    def on_key_press(self, key):
        try:
            # Update joint positions based on key presses
            if key.char == 'w':  # Increase joint1
                self.joint_positions[1] += self.increment
                self.joint_positions[2] += self.increment
                self.joint_positions[4] += self.increment
            elif key.char == 's':  # Decrease joint1
                self.joint_positions[1] -= self.increment
                self.joint_positions[2] -= self.increment
                self.joint_positions[4] -= self.increment
            elif key.char == 'a':  # Increase joint2
                self.joint_positions[0] += self.increment
            elif key.char == 'd':  # Decrease joint2
                self.joint_positions[0] -= self.increment
        except AttributeError:
            # Handle special keys (not used in this example)
            pass

    def destroy_node(self):
        super().destroy_node()
        self.listener.stop()


def main(args=None):
    rclpy.init(args=args)
    node = KeyboardControl()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down Keyboard Control Node...')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
 