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

  using FollowJointTrajectory =
    control_msgs::action::FollowJointTrajectory;

  using JointTrajectoryPoint =
    trajectory_msgs::msg::JointTrajectoryPoint;

  using GoalHandleFollowJointTrajectory =
    rclcpp_action::ClientGoalHandle<FollowJointTrajectory>;


  explicit HomePosition(const rclcpp::NodeOptions & options)
  : Node("home_position", options)
  {
    head_client_ptr_ =
        rclcpp_action::create_client<FollowJointTrajectory>(
            this,
            "/joint_trajectory_controller_head/follow_joint_trajectory");

    left_arm_client_ptr_ =
        rclcpp_action::create_client<FollowJointTrajectory>(
            this,
            "/joint_trajectory_controller_left_arm/follow_joint_trajectory");

    right_arm_client_ptr_ =
        rclcpp_action::create_client<FollowJointTrajectory>(
            this,
            "/joint_trajectory_controller_right_arm/follow_joint_trajectory");

    left_leg_client_ptr_ =
        rclcpp_action::create_client<FollowJointTrajectory>(
            this,
            "/joint_trajectory_controller_left_leg/follow_joint_trajectory");

    right_leg_client_ptr_ =
        rclcpp_action::create_client<FollowJointTrajectory>(
            this,
            "/joint_trajectory_controller_right_leg/follow_joint_trajectory");
  }


  void send_goal()
  {
    using namespace std::placeholders;

    if (!this->client_ptr_->wait_for_action_server()) {
      RCLCPP_ERROR(this->get_logger(), "Action server not available after waiting");
      rclcpp::shutdown();
    }

    auto goal_msg = Fibonacci::Goal();
    goal_msg.order = 10;

    RCLCPP_INFO(this->get_logger(), "Sending goal");

    auto send_goal_options = rclcpp_action::Client<Fibonacci>::SendGoalOptions();
    send_goal_options.goal_response_callback = [this](const GoalHandleFibonacci::SharedPtr & goal_handle)
    {
      if (!goal_handle) {
        RCLCPP_ERROR(this->get_logger(), "Goal was rejected by server");
      } else {
        RCLCPP_INFO(this->get_logger(), "Goal accepted by server, waiting for result");
      }
    };

    send_goal_options.feedback_callback = [this](
      GoalHandleFibonacci::SharedPtr,
      const std::shared_ptr<const Fibonacci::Feedback> feedback)
    {
      std::stringstream ss;
      ss << "Next number in sequence received: ";
      for (auto number : feedback->partial_sequence) {
        ss << number << " ";
      }
      RCLCPP_INFO(this->get_logger(), ss.str().c_str());
    };

    send_goal_options.result_callback = [this](const GoalHandleFibonacci::WrappedResult & result)
    {
      switch (result.code) {
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
      std::stringstream ss;
      ss << "Result received: ";
      for (auto number : result.result->sequence) {
        ss << number << " ";
      }
      RCLCPP_INFO(this->get_logger(), ss.str().c_str());
      rclcpp::shutdown();
    };
    this->client_ptr_->async_send_goal(goal_msg, send_goal_options);
  }


private:

  rclcpp_action::Client<FollowJointTrajectory>::SharedPtr head_client_ptr_;
  rclcpp_action::Client<FollowJointTrajectory>::SharedPtr left_arm_client_ptr_;
  rclcpp_action::Client<FollowJointTrajectory>::SharedPtr right_arm_client_ptr_;
  rclcpp_action::Client<FollowJointTrajectory>::SharedPtr left_leg_client_ptr_;
  rclcpp_action::Client<FollowJointTrajectory>::SharedPtr right_leg_client_ptr_;

}; // class HomePosition

} // namespace darwin_control

RCLCPP_COMPONENTS_REGISTER_NODE(cpp_srvcli_actions::FibonacciActionClient)