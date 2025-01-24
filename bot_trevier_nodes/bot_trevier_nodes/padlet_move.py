import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint


class FollowJointTrajectoryClient(Node):
    def __init__(self):
        super().__init__('follow_joint_trajectory_client')

        # Cliente de acción para <controller_name>/follow_joint_trajectory
        self.action_client = ActionClient(self, FollowJointTrajectory, '/padlet_cont/follow_joint_trajectory')

        # Configuración inicial
        self.joint_name = 'padlet_joint'
        self.positions = [0.7, 0.0]  # Secuencia de posiciones
        self.durations = [2.0, 3.0]  # Duración de cada movimiento

    def send_trajectory(self):
        # Esperar que el servidor de acción esté disponible
        self.get_logger().info('Esperando al servidor de acción...')
        if not self.action_client.wait_for_server(timeout_sec=10.0):
            self.get_logger().error('Servidor de acción no disponible.')
            return

        # Crear la meta (Goal)
        goal_msg = FollowJointTrajectory.Goal()
        goal_msg.trajectory.joint_names = [self.joint_name]

        # Crear puntos de trayectoria
        current_time = 0.0
        for position, duration in zip(self.positions, self.durations):
            point = JointTrajectoryPoint()
            point.positions = [position]
            point.time_from_start.sec = int(current_time + duration)
            point.time_from_start.nanosec = int((current_time + duration - int(current_time + duration)) * 1e9)
            goal_msg.trajectory.points.append(point)
            current_time += duration

        # Enviar la meta al servidor de acción
        self.get_logger().info('Enviando trayectoria al controlador...')
        self.action_client.send_goal_async(goal_msg, self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('La meta fue rechazada.')
            return

        self.get_logger().info('Meta aceptada. Monitoreando resultado...')
        goal_handle.get_result_async().add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Trayectoria completada con éxito. Estado: {result.error_code}')


def main(args=None):
    rclpy.init(args=args)

    # Crear nodo y ejecutar cliente
    node = FollowJointTrajectoryClient()
    node.send_trajectory()

    # Mantener el nodo vivo hasta completar el resultado
    rclpy.spin(node)

    # Finalizar nodo
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
