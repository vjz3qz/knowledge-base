import React from 'react';
import '../styles/Home.css';
import FeatureBox from '../components/FeatureBox';
import ExampleBox from '../components/ExampleBox';
import logo from '../logo.svg'

// Import icons from react-icons
import { FaRegLightbulb } from 'react-icons/fa'; // Example icon for "Examples"
import { MdOutlineRememberMe } from 'react-icons/md'; // Example icon for "Capabilities"
import { AiOutlineExclamationCircle } from 'react-icons/ai'; // Example icon for "Limitations"

const Home = () => {
  return (
    <div className="app-container">
      <div className="top-bar">
        <div className="slogo-box">
          <img src={logo} alt="Logo" className="square-logo" />
        </div>
      </div>
      <main className="main-content">
        <h1>Hi, I'm Tracy</h1>
        <p>How can I help you today?</p>
        <div className="features-container">
          <div className="feature-wrapper">
            <FeatureBox
              icon={<FaRegLightbulb />} // Corrected prop to the actual icon component
              title="Examples"
              description="Can interpret the P&ID from Highline Industries."
            />
            <ExampleBox text="Secondary example content 1" />
          </div>
          <div className="feature-wrapper">
            <FeatureBox
              icon={<MdOutlineRememberMe />} // Corrected prop to the actual icon component
              title="Capabilities"
              description="Remembers what user said earlier in the conversation."
            />
            <ExampleBox text="Secondary example content 2" />
          </div>
          <div className="feature-wrapper">
            <FeatureBox
              icon={<AiOutlineExclamationCircle />} // Corrected prop to the actual icon component
              title="Limitations"
              description="May occasionally generate incorrect information."
            />
            <ExampleBox text="Secondary example content 3" />
          </div>
        </div>
      </main>
      
      <div className="bottom-container">
        <div className="action-buttons">
          {/* Replace divs with button elements or icon components */}
          <button className="action-button">Upload</button>
          <button className="action-button">Answer Question</button>
          <button className="action-button">Extract Data</button>
          <button className="action-button">Incident Capture</button>
        </div>
        <div className="chat-bar">
          <input type="text" className="chat-input" placeholder="Send a message..." />
          <button className="chat-send-button">Send</button>
        </div>
      </div>
    </div>
  );
};

export default Home;
