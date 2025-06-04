import React from 'react';
import './ArcReactor.css';

interface ArcReactorProps {
  isThinking: boolean;
}

const ArcReactor: React.FC<ArcReactorProps> = ({ isThinking }) => {
  const reactorClass = `arc-reactor-wrapper ${isThinking ? 'thinking' : ''}`;
  
  return (
    <div className={reactorClass}>
      <div className="reactor">
        {/* <div className="triangle"></div> */ } {/* It covers the rest*/}
        <div className="circle-1">
          <span></span><span></span><span></span><span></span>
        </div>
        <div className="circle-2">
          <span></span><span></span><span></span><span></span>
          <span></span><span></span><span></span><span></span>
        </div>
        <div className="circle-3"></div>
        <div className="circle-4"><span></span><span></span><span></span></div>
        <div className="circle-5"><span></span><span></span><span></span></div>
        <div className="circle-6"></div>
        <div className="circle-7"></div>
        <div className="circle-8"><span></span><span></span><span></span></div>
      </div>
    </div>
  );
};

export default ArcReactor;
