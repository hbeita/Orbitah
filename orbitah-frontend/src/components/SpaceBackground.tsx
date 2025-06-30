import React from "react";

const FloatingStar: React.FC<{
  delay: number;
  duration: number;
  size: number;
  x: number;
  y: number;
}> = ({ delay, duration, size, x, y }) => (
  <div
    className="absolute animate-star-twinkle"
    style={{
      left: `${x}%`,
      top: `${y}%`,
      width: `${size}px`,
      height: `${size}px`,
      animationDelay: `${delay}s`,
      animationDuration: `${duration}s`,
    }}
  >
    <div className="w-full h-full bg-white rounded-full shadow-lg shadow-blue-400/50" />
  </div>
);

const SpaceBackground: React.FC = () => (
  <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
    {/* Floating stars - more stars for better coverage */}
    <FloatingStar delay={0} duration={3} size={2} x={10} y={15} />
    <FloatingStar delay={1} duration={4} size={1} x={85} y={25} />
    <FloatingStar delay={2} duration={5} size={3} x={20} y={60} />
    <FloatingStar delay={0.5} duration={3.5} size={1.5} x={75} y={70} />
    <FloatingStar delay={1.5} duration={4.5} size={2} x={90} y={45} />
    <FloatingStar delay={3} duration={6} size={1} x={15} y={80} />
    <FloatingStar delay={0.8} duration={3.8} size={2.5} x={60} y={20} />
    <FloatingStar delay={2.2} duration={4.2} size={1.8} x={40} y={85} />
    <FloatingStar delay={1.2} duration={5.2} size={1.2} x={80} y={85} />
    <FloatingStar delay={0.3} duration={3.3} size={2.2} x={5} y={40} />
    <FloatingStar delay={2.8} duration={4.8} size={1.6} x={95} y={65} />
    <FloatingStar delay={1.8} duration={5.8} size={2.8} x={25} y={35} />
    <FloatingStar delay={0.7} duration={3.7} size={1.3} x={70} y={90} />
    <FloatingStar delay={3.2} duration={6.2} size={1.9} x={45} y={10} />
    <FloatingStar delay={1.6} duration={4.6} size={2.1} x={88} y={75} />
  </div>
);

export default SpaceBackground;
