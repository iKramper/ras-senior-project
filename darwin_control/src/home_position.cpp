#include <functional>
#include <future>
#include <memory>
#include <string>
#include <sstream>

#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "rclcpp_components/register_node_macro.hpp"

#include "control_msgs/action/follow_joint_trajectory.hpp"
#include "trajectory_msgs/msg/joint_trajectory_point.hpp"

namespace darwin_control
{
class HomePosition : public rclcpp::Node
{
public:

  using FollowJointTrajectory = control_msgs::action::FollowJointTrajectory;
  using JointTrajectoryPoint = trajectory_msgs::msg::JointTrajectoryPoint;
  using GoalHandleFollowJointTrajectory = rclcpp_action::ClientGoalHandle<FollowJointTrajectory>;

  explicit HomePosition(const rclcpp::NodeOptions & options)
  : Node("home_position", options)
  {
    this->home_client_ptr_ = rclcpp_action::create_client<FollowJointTrajectory>(
        this,
        "/joint_trajectory_controller_general/follow_joint_trajectory");

    auto timer_callback_lambda = [this](){ return this->send_goal(); };
    this->timer_ = this->create_wall_timer(
      std::chrono::milliseconds(500),
      timer_callback_lambda);
  }

  void send_goal()
  {
    this->timer_->cancel();

    if (!this->home_client_ptr_->wait_for_action_server()) {
      RCLCPP_ERROR(this->get_logger(), "Action server not available after waiting");
      rclcpp::shutdown();
    }

    auto goal_msg = FollowJointTrajectory::Goal();
    goal_msg.trajectory.joint_names =
    {
      "neck_joint",
      "r_hip_joint",
      "r_thigh_joint",
      "r_knee_joint",
      "r_ankle_joint",
      "r_foot_joint",
      "r_shoulder_joint",
      "r_biceps_joint",
      "r_elbow_joint",
      "l_hip_joint",
      "l_thigh_joint",
      "l_knee_joint",
      "l_ankle_joint",
      "l_foot_joint",
      "l_shoulder_joint",
      "l_biceps_joint",
      "l_elbow_joint"
    };

    JointTrajectoryPoint home_point;
    home_point.positions =
    {
      2.66,  // neck_joint
      5.23,  // r_hip_joint
      0.00,  // r_thigh_joint
      1.78,  // r_knee_joint
      0.00,  // r_ankle_joint
      0.00,  // r_foot_joint
      2.27,  // r_shoulder_joint
      1.54,  // r_biceps_joint
      3.31,  // r_elbow_joint
      0.00,  // l_hip_joint
      0.00,  // l_thigh_joint
      1.84,  // l_knee_joint
      0.00,  // l_ankle_joint
      5.23,  // l_foot_joint
      2.60,  // l_shoulder_joint
      3.76,  // l_biceps_joint
      1.75   // l_elbow_joint
    };

    home_point.time_from_start.sec = 10;
    goal_msg.trajectory.points.push_back(home_point);

    RCLCPP_INFO(this->get_logger(), "Sending goal");

    auto send_goal_options = rclcpp_action::Client<FollowJointTrajectory>::SendGoalOptions();
    send_goal_options.goal_response_callback = [this](const GoalHandleFollowJointTrajectory::SharedPtr & goal_handle)
    {
      if (!goal_handle) {
        RCLCPP_ERROR(this->get_logger(), "Goal was rejected by server");
      } else {
        RCLCPP_INFO(this->get_logger(), "Goal accepted by server, waiting for result");
      }
    };

    send_goal_options.feedback_callback =
      [this](
        GoalHandleFollowJointTrajectory::SharedPtr,
        const std::shared_ptr<const FollowJointTrajectory::Feedback> feedback)
    {
      std::stringstream ss;
      ss << "Desired and current positions:\n";
      for (size_t i = 0; i < feedback->joint_names.size(); ++i)
      {
        ss << feedback->joint_names[i]
           << ": Desired: "
           << feedback->desired.positions[i]
           << " Current: "
           << feedback->actual.positions[i]
           << "\n";
      }
      RCLCPP_INFO(this->get_logger(), ss.str().c_str());
    };

    send_goal_options.result_callback =
      [this](const GoalHandleFollowJointTrajectory::WrappedResult & result)
    {
      switch (result.code)
      {
        case rclcpp_action::ResultCode::SUCCEEDED:
          break;
        case rclcpp_action::ResultCode::ABORTED:
          RCLCPP_ERROR(this->get_logger(), "Goal was aborted");
          return;
        case rclcpp_action::ResultCode::CANCELED:
          RCLCPP_ERROR(this->get_logger(), "Goal was canceled");
          return;
        default:
          RCLCPP_ERROR(this->get_logger(), "Unknown result code");
          return;
      }

      if (result.result->error_code != FollowJointTrajectory::Result::SUCCESSFUL){
        RCLCPP_ERROR(this->get_logger(),
          "Trajectory failed.\n"
          "Error code: %d\n"
          "Description: %s",
          result.result->error_code,
          result.result->error_string.c_str());
        return;
      }
      RCLCPP_INFO(this->get_logger(),"Robot is now in HOME position");
      rclcpp::shutdown();
    };
    this->home_client_ptr_->async_send_goal(goal_msg, send_goal_options);
  }

private:
  rclcpp_action::Client<FollowJointTrajectory>::SharedPtr home_client_ptr_;
  rclcpp::TimerBase::SharedPtr timer_;

}; // class HomePosition

} // namespace darwin_control

RCLCPP_COMPONENTS_REGISTER_NODE(darwin_control::HomePosition)