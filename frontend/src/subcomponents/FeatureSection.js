import React from "react";
import FeatureBox from "../ui/FeatureBox";
import { ReactComponent as Logo } from "../assets/logo.svg";
import { FaRegLightbulb } from "react-icons/fa";
import { MdOutlineRememberMe } from "react-icons/md";
import { AiOutlineExclamationCircle } from "react-icons/ai";

function FeatureSection() {
  return (
    <>
      <Logo className="logo-large" />
      <p>How can I help you today?</p>
      <div className="features-container">
        <FeatureBox
          icon={<FaRegLightbulb />}
          title="Examples"
          description="Can interpret the P&ID from Highline Industries?"
        />
        {/* <FeatureBox
            icon={<MdOutlineRememberMe />}
            title="Capabilities"
            description="Remembers what user said earlier in the conversation."
          /> */}
        <FeatureBox
          icon={<AiOutlineExclamationCircle />}
          title="Limitations"
          description="May occasionally generate incorrect information."
        />
      </div>
    </>
  );
}

export default FeatureSection;
