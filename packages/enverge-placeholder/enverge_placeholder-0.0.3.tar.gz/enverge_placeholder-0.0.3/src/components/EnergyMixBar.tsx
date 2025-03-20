import * as React from 'react';
import { useState, useEffect } from 'react';

export const EnergyMixBar = () => {
  const [isDark, setIsDark] = useState(false);
  const [energyMix, setEnergyMix] = useState({
    solar: 40,
    wind: 30,
    battery: 25,
    grid: 5
  });

  useEffect(() => {
    // Theme management
    const themeManager = (window as any).jupyterlab?.themeManager;
    
    const updateTheme = () => {
      setIsDark(!themeManager?.isLight(themeManager?.theme));
    };

    if (themeManager) {
      updateTheme();
      themeManager.themeChanged.connect(updateTheme);
      return () => themeManager.themeChanged.disconnect(updateTheme);
    }
  }, []);

  useEffect(() => {
    // Energy mix animation
    const updateValues = () => {
      setEnergyMix(prev => {
        // Generate random fluctuations between -2.5% and +2.5%
        const fluctuate = () => (Math.random() - 0.5) * 5;
        
        // Calculate new values with fluctuations
        let newSolar = Math.max(35, Math.min(45, prev.solar + fluctuate()));
        let newWind = Math.max(25, Math.min(35, prev.wind + fluctuate()));
        let newBattery = Math.max(20, Math.min(30, prev.battery + fluctuate()));
        let newGrid = Math.max(2, Math.min(5, prev.grid + fluctuate()));
        
        // Normalize to ensure total is 100%
        const total = newSolar + newWind + newBattery + newGrid;
        const scale = 100 / total;
        
        return {
          solar: Math.round(newSolar * scale * 10) / 10,
          wind: Math.round(newWind * scale * 10) / 10,
          battery: Math.round(newBattery * scale * 10) / 10,
          grid: Math.round(newGrid * scale * 10) / 10
        };
      });
    };

    const interval = setInterval(updateValues, 2000);
    return () => clearInterval(interval);
  }, []);

  const colors = {
    solar: isDark ? '#FFD700' : '#FFB84D',
    wind: isDark ? '#87CEFA' : '#5B9FFF',
    battery: isDark ? '#DA70D6' : '#B57EDC',
    grid: isDark ? '#FF4444' : '#FF6B6B'
  };

  return (
    <div style={{ 
      display: 'flex', 
      alignItems: 'center',
      marginLeft: '20px',
    }}>
      <div style={{ 
        display: 'flex',
        alignItems: 'center',
        height: '20px',
        width: '200px',
        border: '1px solid var(--jp-border-color1)',
        borderRadius: '4px',
        overflow: 'hidden'
      }}>
        <div style={{ width: `${energyMix.solar}%`, height: '100%', backgroundColor: colors.solar }} title={`Solar: ${energyMix.solar}%`} />
        <div style={{ width: `${energyMix.wind}%`, height: '100%', backgroundColor: colors.wind }} title={`Wind: ${energyMix.wind}%`} />
        <div style={{ width: `${energyMix.battery}%`, height: '100%', backgroundColor: colors.battery }} title={`Battery: ${energyMix.battery}%`} />
        <div style={{ width: `${energyMix.grid}%`, height: '100%', backgroundColor: colors.grid }} title={`Grid: ${energyMix.grid}%`} />
      </div>
      <div style={{ 
        marginLeft: '10px', 
        fontSize: '12px',
        display: 'flex',
        gap: '8px'
      }}>
        <span style={{ color: 'var(--jp-ui-font-color1)' }}>
          <span style={{ color: colors.solar }}>■</span> Solar {energyMix.solar}%
        </span>
        <span style={{ color: 'var(--jp-ui-font-color1)' }}>
          <span style={{ color: colors.wind }}>■</span> Wind {energyMix.wind}%
        </span>
        <span style={{ color: 'var(--jp-ui-font-color1)' }}>
          <span style={{ color: colors.battery }}>■</span> Battery {energyMix.battery}%
        </span>
        <span style={{ color: 'var(--jp-ui-font-color1)' }}>
          <span style={{ color: colors.grid }}>■</span> Grid {energyMix.grid}%
        </span>
      </div>
    </div>
  );
}; 