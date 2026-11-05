#include <stdexcept>
#include <string>
#include <string_view>
#include <type_traits>

#include <gtest/gtest.h>

#include "asr_interface/ros_msg.hpp"

namespace {

    constexpr std::string_view kRobotNodeFqn = "/robot_a/asr";

    TEST(RosMsgHelpers, ProvidesPrivateEndpointOwnerNames) {
        EXPECT_EQ(asr_interface::kPrivateTopicEvent, "~/event");
        EXPECT_EQ(asr_interface::kPrivateTopicState, "~/state");
    }

    TEST(RosMsgHelpers, BuildsDefaultAbsoluteEndpointNames) {
        EXPECT_EQ(asr_interface::topic_event(), "/asr/event");
        EXPECT_EQ(asr_interface::topic_state(), "/asr/state");
    }

    TEST(RosMsgHelpers, BuildsNamesForCustomNodeFqn) {
        EXPECT_EQ(asr_interface::topic_event(kRobotNodeFqn), "/robot_a/asr/event");
        EXPECT_EQ(asr_interface::topic_state(kRobotNodeFqn), "/robot_a/asr/state");
        EXPECT_EQ(asr_interface::topic_event(std::string{kRobotNodeFqn} + "///"), "/robot_a/asr/event");
    }

    TEST(RosMsgHelpers, RejectsInvalidNodeFqn) {
        EXPECT_THROW(static_cast<void>(asr_interface::topic_event("")), std::invalid_argument);
        EXPECT_THROW(static_cast<void>(asr_interface::topic_event("asr")), std::invalid_argument);
        EXPECT_THROW(static_cast<void>(asr_interface::topic_event("/")), std::invalid_argument);
        EXPECT_THROW(static_cast<void>(asr_interface::topic_event("/asr//node")), std::invalid_argument);
        EXPECT_THROW(static_cast<void>(asr_interface::topic_event("/asr\t")), std::invalid_argument);
    }

    TEST(RosMsgHelpers, ExposesGeneratedTypeAliases) {
        static_assert(std::is_same_v<asr_interface::MsgAsrEvent, asr_interface::msg::AsrEvent>);
        static_assert(std::is_same_v<asr_interface::MsgAsrState, asr_interface::msg::AsrState>);
    }

} // namespace
