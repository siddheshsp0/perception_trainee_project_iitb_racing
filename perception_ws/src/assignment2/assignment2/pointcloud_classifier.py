import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud
from visualization_msgs.msg import Marker, MarkerArray
import numpy as np
from sklearn.cluster import DBSCAN



class PointCloudClassifier(Node):
    def __init__(self):
        super().__init__('pointcloud_classifier')

        # # Markers and subscriptions, timers definition
        # self.create_timer(1, self.pub_markers)
        self.markers_publisher = self.create_publisher(MarkerArray, '/ ', 10)
        self.pointcloud_sub = self.create_subscription(PointCloud, '/carmaker/pointcloud', self.pointcloud_callback, 10)


        # Constants Definition
        self.z_threshhold = -0.15
        self.prev_pub_size=0
    


    def pointcloud_callback(self, msg):
        marker_array =MarkerArray()
        points = np.array([[pt.x, pt.y, pt.z] for pt in msg.points if pt.z > self.z_threshhold])  # threshholding z for ground points
        # print(points)
        # Applying DBSCAN
        dbscan = DBSCAN(eps=1, min_samples=2)
        # Check if points is empty
        if (points.shape[0]==0):
            return
        labels = dbscan.fit_predict(points)


# --------------------------------- OLD CODE FOR CONE CENTRES ----------------------- #
        # num_labels = np.max(labels) + 1
        # classified_points = [[[]]] * num_labels

        # # print(f'size of classified_points: {len(classified_points)}, max of labels: {np.max(labels)}')
        # # print()

        # for i in range(points.shape[0]):
        #     try:
        #         # classified_points[labels[i]] = np.append(classified_points[labels[i]], points[i])
        #         if(labels[i]==-1):
        #             continue
        #         classified_points[labels[i]].append([points[i][0], points[i][1], points[i][2]])
        #     except Exception as e:
        #         pass
        #         # self.get_logger().info(f'error is: {e}')

        # # Removing first element from each classes's points, coz for some reason first point is an empty list idk why
        # for k in range(len(classified_points)):
        #     classified_points[k].pop(0)
        # # classified_points_np = np.array(classified_points)
        # cone_coords = np.array([np.mean(np.array(class_), axis=0) for class_ in classified_points])

# --------------------------------- END ----------------------- #
        
# --------------------------------- NEW CODE FOR CONE CENTRES ----------------------- #

        unique_labels = set(labels) - {-1} # to get unique set of labels
        cone_coords = np.array([points[labels==label_].mean(axis=0) for label_ in unique_labels])

        


# --------------------------------- END ----------------------- #

        

        # Publishing calculated centres and resetting rviz display
        delete_marker = Marker()
        delete_marker.action = Marker.DELETEALL
        marker_array.markers.append(delete_marker)
        self.prev_pub_size = len(points)

        for i in range(cone_coords.shape[0]):
            marker = Marker()
            marker.header.frame_id = "map"
            marker.header.stamp = self.get_clock().now().to_msg()
            marker.ns = "cylinder"
            marker.id = i
            marker.type = Marker.CYLINDER
            marker.action = Marker.ADD
            marker.scale.x = 0.1
            marker.scale.y = 0.1
            marker.scale.z = 0.5
            marker.pose.position.x = cone_coords[i][0]
            marker.pose.position.y = cone_coords[i][1]
            marker.pose.position.z = marker.scale.z / 2
            marker.pose.orientation.x = 0.0
            marker.pose.orientation.y = 0.0
            marker.pose.orientation.z = 0.0
            marker.pose.orientation.w = 1.0
            marker.color.r = 0.0
            marker.color.g = 1.0
            marker.color.b = 0.0
            marker.color.a = 1.0
            marker_array.markers.append(marker)
        self.prev_pub_size=cone_coords.shape[0]

                # TO RESET RVIZ DISPLAY
        # for i in range(self.prev_pub_size):
        #     marker = Marker()
        #     marker.header.frame_id = "map"
        #     marker.id = i
        #     marker.action = Marker.DELETE
        #     delete_array.markers.append(marker)
        

        # self.markers_publisher.publish(delete_array)

        self.markers_publisher.publish(marker_array)


        # # Setting up marker array, publishing all points above threshold
        # for pt,i in zip(points, range(0, len(points))):
        #     marker = Marker()
        #     marker.header.frame_id = "map"
        #     marker.header.stamp = self.get_clock().now().to_msg()
        #     marker.ns = "marker_ns"
        #     marker.id = i
        #     marker.type = Marker.SPHERE
        #     marker.action = Marker.ADD
        #     marker.pose.position.x = pt[0]
        #     marker.pose.position.y = pt[1]
        #     marker.pose.position.z = pt[2]
        #     marker.scale.y = 0.05
        #     marker.scale.x = 0.05
        #     marker.scale.z = 0.05
        #     marker.color.a = 1.0
        #     marker.color.r = 1.0
        #     marker.color.g = 0.0
        #     marker.color.b = 0.0
        #     marker_array.markers.append(marker)
        
        # self.markers_publisher.publish(marker_array)

        # # TO RESET RVIZ DISPLAY
        # for i in range(self.prev_pub_size):
        #     marker = Marker()
        #     marker.header.frame_id = "map"
        #     marker.id = i  # Use same IDs as previous markers
        #     marker.action = Marker.DELETE  # Delete this marker
        #     delete_array.markers.append(marker)
        # self.prev_pub_size = len(points)
        # self.markers_publisher.publish(delete_array)





def main(args=None):
    rclpy.init(args=args)
    classifier = PointCloudClassifier()
    rclpy.spin(classifier)
    classifier.destroy_node()
    rclpy.shutdown()


if __name__=='__main__':
    main()