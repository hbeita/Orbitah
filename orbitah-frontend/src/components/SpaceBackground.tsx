import React, { useEffect, useState } from "react";

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

const BoomerangNebula: React.FC<{
  x: number;
  y: number;
  delay: number;
}> = ({ x, y, delay }) => (
  <div
    className="absolute animate-boomerang-nebula"
    style={{
      left: `${x}%`,
      top: `${y}%`,
      animationDelay: `${delay}s`,
    }}
  >
    {/* Main boomerang nebula structure */}
    <div className="relative">
      {/* Central hourglass shape */}
      <div className="absolute w-24 h-32 bg-gradient-to-b from-cyan-400/40 via-blue-500/30 to-transparent rounded-full blur-md" />

      {/* Left lobe - characteristic of boomerang nebula */}
      <div className="absolute left-0 top-1/2 w-20 h-16 bg-gradient-to-r from-cyan-400/50 via-blue-400/30 to-transparent rounded-full blur-lg transform -translate-y-1/2 -translate-x-2" />

      {/* Right lobe - characteristic of boomerang nebula */}
      <div className="absolute right-0 top-1/2 w-20 h-16 bg-gradient-to-l from-cyan-400/50 via-blue-400/30 to-transparent rounded-full blur-lg transform -translate-y-1/2 translate-x-2" />

      {/* Central star/white dwarf remnant */}
      <div className="absolute top-1/2 left-1/2 w-4 h-4 bg-white rounded-full blur-sm transform -translate-x-1/2 -translate-y-1/2 shadow-lg shadow-cyan-400/50" />

      {/* Additional nebula wisps */}
      <div className="absolute top-0 left-1/2 w-2 h-8 bg-gradient-to-b from-cyan-300/30 to-transparent rounded-full blur-sm transform -translate-x-1/2" />
      <div className="absolute bottom-0 left-1/2 w-2 h-8 bg-gradient-to-t from-cyan-300/30 to-transparent rounded-full blur-sm transform -translate-x-1/2" />

      {/* Outer glow */}
      <div className="absolute inset-0 w-40 h-48 bg-gradient-to-b from-cyan-400/10 via-blue-500/5 to-transparent rounded-full blur-xl transform -translate-x-1/2 -translate-y-1/2" />
    </div>
  </div>
);

const SpaceBackground: React.FC = () => {
  const [boomerangVisible, setBoomerangVisible] = useState(false);
  const [boomerangPosition, setBoomerangPosition] = useState({ x: 50, y: 50 });

  useEffect(() => {
    const showBoomerang = () => {
      // Random position
      const x = Math.random() * 80 + 10; // 10% to 90%
      const y = Math.random() * 80 + 10; // 10% to 90%
      setBoomerangPosition({ x, y });
      setBoomerangVisible(true);

      // Hide after 8 seconds
      setTimeout(() => {
        setBoomerangVisible(false);
      }, 8000);
    };

    // Show boomerang every 30 seconds
    const interval = setInterval(showBoomerang, 30000);

    // Show first boomerang after a random delay (5-15 seconds)
    const initialDelay = Math.random() * 10000 + 5000;
    const initialTimer = setTimeout(showBoomerang, initialDelay);

    return () => {
      clearInterval(interval);
      clearTimeout(initialTimer);
    };
  }, []);

  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
      {/* Darker cosmic background */}
      <div className="absolute inset-0 bg-gradient-to-br from-slate-950 via-slate-900 to-black" />

      {/* Additional dark nebula layers for depth */}
      <div className="absolute inset-0 bg-gradient-to-br from-indigo-950/30 via-purple-950/20 to-slate-950/40" />

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

      {/* Boomerang Nebula - appears randomly */}
      {boomerangVisible && (
        <BoomerangNebula
          x={boomerangPosition.x}
          y={boomerangPosition.y}
          delay={0}
        />
      )}
    </div>
  );
};

export default SpaceBackground;
